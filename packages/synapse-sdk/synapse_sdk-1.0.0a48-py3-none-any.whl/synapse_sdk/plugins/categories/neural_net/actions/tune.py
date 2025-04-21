import copy
import tempfile
from pathlib import Path
from typing import Annotated, Optional

from pydantic import AfterValidator, BaseModel, field_validator
from pydantic_core import PydanticCustomError

from synapse_sdk.clients.exceptions import ClientError
from synapse_sdk.plugins.categories.decorators import register_action
from synapse_sdk.plugins.categories.neural_net.actions.train import TrainAction, TrainRun
from synapse_sdk.plugins.enums import PluginCategory, RunMethod
from synapse_sdk.utils.file import archive
from synapse_sdk.utils.module_loading import import_string
from synapse_sdk.utils.pydantic.validators import non_blank


class TuneRun(TrainRun):
    is_tune = True
    completed_samples = 0
    num_samples = 0
    checkpoint_output = None


class TuneConfig(BaseModel):
    mode: Optional[str] = None
    metric: Optional[str] = None
    num_samples: int = 1
    max_concurrent_trials: Optional[int] = None


class TuneParams(BaseModel):
    name: Annotated[str, AfterValidator(non_blank)]
    description: str
    checkpoint: int | None
    dataset: int
    tune_config: TuneConfig

    @field_validator('name')
    @staticmethod
    def unique_name(value, info):
        action = info.context['action']
        client = action.client
        try:
            job_exists = client.exists(
                'list_jobs',
                params={
                    'ids_ex': action.job_id,
                    'category': 'neural_net',
                    'job__action': 'tune',
                    'is_active': True,
                    'params': f'name:{value}',
                },
            )
            assert not job_exists, '존재하는 튜닝 작업 이름입니다.'
        except ClientError:
            raise PydanticCustomError('client_error', '')
        return value


@register_action
class TuneAction(TrainAction):
    """
    **Must read** Important notes before using Tune:

    1. Path to the model output (which is the return value of your train function)
       should be set to the checkpoint_output attribute of the run object **before**
       starting the training.
    2. Before exiting the training function, report the results to Tune.
    3. When using own tune.py, take note of the difference in the order of parameters.
       tune() function starts with hyperparameter, run, dataset, checkpoint, **kwargs
       whereas the train() function starts with run, dataset, hyperparameter, checkpoint, **kwargs.
    ----
    1)
    Set the output path for the checkpoint to export best model

    output_path = Path('path/to/your/weights')
    run.checkpoint_output = str(output_path)

    2)
    Before exiting the training function, report the results to Tune.
    The results_dict should contain the metrics you want to report.

    Example: (In train function)
    results_dict = {
        "accuracy": accuracy,
        "loss": loss,
        # Add other metrics as needed
    }
    if hasattr(self.dm_run, 'is_tune') and self.dm_run.is_tune:
        tune.report(results_dict, checkpoint=tune.Checkpoint.from_directory(self.dm_run.checkpoint_output))


    3)
    tune() function takes hyperparameter, run, dataset, checkpoint, **kwargs in that order
    whereas train() function takes run, dataset, hyperparameter, checkpoint, **kwargs in that order.

    --------------------------------------------------------------------------------------------------------

    **중요** Tune 사용 전 반드시 읽어야 할 사항들

    1. 본 플러그인의 train 함수에서, 학습을 진행하기 코드 전에
       결과 모델 파일의 경로(train함수의 리턴 값)을 checkpoint_output 속성에 설정해야 합니다.
    2. 학습이 종료되기 전에, 결과를 Tune에 보고해야 합니다.
    3. 플러그인에서 tune.py를 직접 생성해서 사용할 시, 매개변수의 순서가 다릅니다.

    ----
    1)
    체크포인트를 설정할 경로를 지정합니다.
    output_path = Path('path/to/your/weights')
    run.checkpoint_output = str(output_path)

    2)
    학습이 종료되기 전에, 결과를 Tune에 보고합니다.
    results_dict = {
        "accuracy": accuracy,
        "loss": loss,
        # 필요한 다른 메트릭 추가
    }
    if hasattr(self.dm_run, 'is_tune') and self.dm_run.is_tune:
        tune.report(results_dict, checkpoint=tune.Checkpoint.from_directory(self.dm_run.checkpoint_output))

    3)
    tune() 함수는 hyperparameter, run, dataset, checkpoint, **kwargs 순서이고
    train() 함수는 run, dataset, hyperparameter, checkpoint, **kwargs 순서입니다.
    """

    name = 'tune'
    category = PluginCategory.NEURAL_NET
    method = RunMethod.JOB
    run_class = TuneRun
    params_model = TuneParams
    progress_categories = {
        'dataset': {
            'proportion': 5,
        },
        'trials': {
            'proportion': 90,
        },
        'model_upload': {
            'proportion': 5,
        },
    }

    def start(self):
        from ray import tune

        # download dataset
        self.run.log_message('Preparing dataset for hyperparameter tuning.')
        input_dataset = self.get_dataset()

        # retrieve checkpoint
        checkpoint = None
        if self.params['checkpoint']:
            self.run.log_message('Retrieving checkpoint.')
            checkpoint = self.get_model(self.params['checkpoint'])

        # train dataset
        self.run.log_message('Starting training for hyperparameter tuning.')

        # Save num_samples to TuneRun for logging
        self.run.num_samples = self.params['tune_config']['num_samples']

        entrypoint = self.entrypoint
        if not self._tune_override_exists():
            # entrypoint must be train entrypoint
            def _tune(param_space, run, dataset, checkpoint=None, **kwargs):
                return entrypoint(run, dataset, param_space, checkpoint, **kwargs)

            entrypoint = _tune

        trainable = tune.with_parameters(entrypoint, run=self.run, dataset=input_dataset, checkpoint=checkpoint)
        tune_config = self.params['tune_config']

        hyperparameter = self.params['hyperparameter']
        param_space = self.convert_tune_params(hyperparameter)
        temp_path = tempfile.TemporaryDirectory()

        tuner = tune.Tuner(
            tune.with_resources(trainable, resources=self.tune_resources),
            tune_config=tune.TuneConfig(**tune_config),
            run_config=tune.RunConfig(
                name=f'synapse_tune_hpo_{self.job_id}',
                log_to_file=('stdout.log', 'stderr.log'),
                storage_path=temp_path.name,
            ),
            param_space=param_space,
        )
        result = tuner.fit()

        best_result = result.get_best_result()

        # upload model_data
        self.run.log_message('Registering best model data.')
        self.run.set_progress(0, 1, category='model_upload')
        self.create_model_from_result(best_result)
        self.run.set_progress(1, 1, category='model_upload')

        self.run.end_log()

        return {'best_result': best_result.config}

    @property
    def tune_resources(self):
        resources = {}
        for option in ['num_cpus', 'num_gpus']:
            option_value = self.params.get(option)
            if option_value:
                # Remove the 'num_' prefix and trailing s from the option name
                resources[(lambda s: s[4:-1])(option)] = option_value
        return resources

    def create_model_from_result(self, result):
        params = copy.deepcopy(self.params)
        configuration_fields = ['hyperparameter']
        configuration = {field: params.pop(field) for field in configuration_fields}

        with tempfile.TemporaryDirectory() as temp_path:
            archive_path = Path(temp_path, 'archive.zip')

            # Archive tune results
            # https://docs.ray.io/en/latest/tune/tutorials/tune_get_data_in_and_out.html#getting-data-out-of-tune-using-checkpoints-other-artifacts
            archive(result.path, archive_path)

            return self.client.create_model({
                'plugin': self.plugin_release.plugin,
                'version': self.plugin_release.version,
                'file': str(archive_path),
                'configuration': configuration,
                **params,
            })

    @staticmethod
    def convert_tune_params(param_list):
        """
        Convert YAML hyperparameter configuration to Ray Tune parameter dictionary.

        Args:
            param_list (list): List of hyperparameter configurations.

        Returns:
            dict: Ray Tune parameter dictionary
        """
        from ray import tune

        param_space = {}

        for param in param_list:
            name = param['name']
            param_type = param['type']

            if param_type == 'loguniform':
                param_space[name] = tune.loguniform(param['min'], param['max'])
            elif param_type == 'choice':
                param_space[name] = tune.choice(param['options'])
            elif param_type == 'randint':
                param_space[name] = tune.randint(param['min'], param['max'])
            # Add more type handlers as needed

        return param_space

    @staticmethod
    def _tune_override_exists(module_path='plugin.tune') -> bool:
        try:
            import_string(module_path)
            return True
        except ImportError:
            return False
