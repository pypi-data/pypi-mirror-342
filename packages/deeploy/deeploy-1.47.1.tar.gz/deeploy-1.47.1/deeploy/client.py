import warnings
from typing import Dict, List, Optional

from deeploy.enums.artifact import Artifact
from deeploy.models import (
    ActualResponse,
    ClientConfig,
    CreateActuals,
    CreateAzureMLDeployment,
    CreateDeployment,
    CreateEvaluation,
    CreateExplainerReference,
    CreateExternalDeployment,
    CreateModelReference,
    CreateRegistrationDeployment,
    CreateSageMakerDeployment,
    CreateTransformerReference,
    Deployment,
    Evaluation,
    GetPredictionLogsOptions,
    PredictionLog,
    UpdateAzureMLDeployment,
    UpdateDeployment,
    UpdateDeploymentDescription,
    UpdateExternalDeployment,
    UpdateRegistrationDeployment,
    UpdateSageMakerDeployment,
    V1Prediction,
    V2Prediction,
)
from deeploy.models.create_environment_variable import CreateEnvironmentVariable
from deeploy.models.create_job_schedule import CreateJobSchedule
from deeploy.models.custom_metric import (
    CreateCustomMetric,
    CreateCustomMetricDataPoint,
    CustomMetric,
    CustomMetricDataPoint,
    CustomMetricGraphData,
    UpdateCustomMetric,
)
from deeploy.models.environment_variable import EnvironmentVariable
from deeploy.models.get_request_logs_options import GetRequestLogsOptions
from deeploy.models.job_schedule import JobSchedule
from deeploy.models.prediction_log import RequestLog
from deeploy.models.reference_json import (
    ExplainerReferenceJson,
    ModelReferenceJson,
    TransformerReferenceJson,
)
from deeploy.models.test_job_schedule import TestJobSchedule
from deeploy.models.update_job_schedule import UpdateJobSchedule
from deeploy.services import (
    DeeployService,
    FileService,
    GitService,
)


class Client(object):
    """
    A class for interacting with Deeploy
    """

    def __init__(
        self,
        host: str,
        workspace_id: str,
        access_key: str = None,
        secret_key: str = None,
        deployment_token: str = None,
        team_id: str = None
    ) -> None:
        """Initialise the Deeploy client
        Parameters:
            host (str): The host at which Deeploy is located, i.e. deeploy.example.com
            workspace_id (str): The ID of the workspace in which your repository
                is located
            access_key (str, optional): Personal Access Key generated from the Deeploy UI
            secret_key (str, optional): Secret Access Key generated from the Deeploy UI
            deployment_token (str, optional): Can be a Deployment token generated from the Deeploy UI or JWT
                when using OpenID Connect 
            team_id (str, optional): Provide your team ID only when authenticating to Deeploy cloud
                using OpenID Connect
        """

        self.__config = ClientConfig(
            **{
                "host": host,
                "workspace_id": workspace_id,
                "access_key": access_key,
                "secret_key": secret_key,
                "token": deployment_token,
                "team_id": team_id,
            }
        )

        self.__deeploy_service = DeeployService(host, access_key, secret_key, deployment_token, team_id)

        self.__file_service = FileService()

    def create_environment_variable(
        self, options: CreateEnvironmentVariable
    ) -> EnvironmentVariable:
        """Create an environment variable in a Workspace"
        Parameters:
            options (CreateEnvironmentVariable): An instance of the CreateEnvironmentVariable class
                containing the environment variable configuration options
        """

        return self.__deeploy_service.create_environment_variable(
            self.__config.workspace_id, CreateEnvironmentVariable(**options)
        )

    
    def get_all_environment_variables(self) -> List[EnvironmentVariable]:
        """Get all environment variables from your Workspace"""

        return self.__deeploy_service.get_all_environment_variables(self.__config.workspace_id)

    
    def get_environment_variable_ids_for_deployment_artifact(
        self, deployment_id: str, artifact: Artifact
    ) -> List[str]:
        """Get the current environment variable IDs for an artifact of your Deployment
        This method can be used to help update your Deployment
        Parameters:
            deployment_id (str): The uuid of the Deployment of which to retrieve the environment variable IDs
            artifact (str): The artifact of which to retrieve the environment variable IDs from
        """

        return self.__deeploy_service.get_environment_variable_ids_for_deployment_artifact(
            self.__config.workspace_id, deployment_id, artifact
        )

    
    def create_deployment(
        self,
        options: CreateDeployment,
        local_repository_path: Optional[str] = None,
    ) -> Deployment:
        """Create a Deployment on Deeploy
        Parameters:
            options (CreateDeployment): An instance of the CreateDeployment class
                containing the deployment configuration options
            local_repository_path (str, optional): Absolute path to the local git repository
                which is connected to Deeploy used to check if your Repository is present in the Workspace
        """

        options = self.__check_local_git_config(local_repository_path, options)

        return self.__deeploy_service.create_deployment(
            self.__config.workspace_id, CreateDeployment(**options)
        )

    
    def create_sagemaker_deployment(
        self,
        options: CreateSageMakerDeployment,
        local_repository_path: Optional[str] = None,
    ) -> Deployment:
        """Create a SageMaker Deployment on Deeploy
        Parameters:
            options (CreateSageMakerDeployment): An instance of the CreateSageMakerDeployment class
                containing the deployment configuration options
            local_repository_path (str, optional): Absolute path to the local git repository
                which is connected to Deeploy used to check if your Repository is present in the Workspace
        """

        options = self.__check_local_git_config(local_repository_path, options)

        return self.__deeploy_service.create_sagemaker_deployment(
            self.__config.workspace_id, CreateSageMakerDeployment(**options)
        )

    
    def create_azure_ml_deployment(
        self,
        options: CreateAzureMLDeployment,
        local_repository_path: Optional[str] = None,
    ) -> Deployment:
        """Create an Azure Machine Learning Deployment on Deeploy
        Parameters:
            options (CreateAzureMLDeployment): An instance of the CreateAzureMLDeployment class
                containing the deployment configuration options
            local_repository_path (str, optional): Absolute path to the local git repository
                which is connected to Deeploy used to check if your Repository is present in the Workspace
        """

        options = self.__check_local_git_config(local_repository_path, options)

        return self.__deeploy_service.create_azure_ml_deployment(
            self.__config.workspace_id, CreateAzureMLDeployment(**options)
        )

    
    def create_external_deployment(
        self,
        options: CreateExternalDeployment,
        local_repository_path: Optional[str] = None,
    ) -> Deployment:
        """Create a Deployment on Deeploy
        Parameters:
            options (CreateExternalDeployment): An instance of the CreateExternalDeployment class
                containing the deployment configuration options
            local_repository_path (str, optional): Absolute path to the local git repository
                which is connected to Deeploy used to check if your Repository is present in the Workspace
        """

        if self.__has_new_git_values(options):
            options = self.__check_local_git_config(local_repository_path, options)
        elif self.__has_no_git_values(options):
            pass
        else:
            raise Exception(
                "Both repository_id and branch_name are not provided. Either set both to None or provide both."
            )

        return self.__deeploy_service.create_external_deployment(
            self.__config.workspace_id, CreateExternalDeployment(**options)
        )

    
    def create_registration_deployment(
        self,
        options: CreateRegistrationDeployment,
        local_repository_path: Optional[str] = None,
    ) -> Deployment:
        """Create a Deployment on Deeploy
        Parameters:
            options (CreateRegistrationDeployment): An instance of the CreateRegistrationDeployment class
                containing the deployment configuration options
            local_repository_path (str, optional): Absolute path to the local git repository
                which is connected to Deeploy used to check if your Repository is present in the Workspace
        """

        if self.__has_new_git_values(options):
            options = self.__check_local_git_config(local_repository_path, options)
        elif self.__has_no_git_values(options):
            pass
        else:
            raise Exception(
                "Both repository_id and branch_name are not provided. Either set both to None or provide both."
            )

        return self.__deeploy_service.create_registration_deployment(
            self.__config.workspace_id, CreateRegistrationDeployment(**options)
        )

    
    def update_deployment(
        self,
        deployment_id: str,
        options: UpdateDeployment,
        local_repository_path: Optional[str] = None,
    ) -> Deployment:
        """Update a Deployment on Deeploy
        Parameters:
            deployment_id (str): The uuid of the Deployment to update
            options (UpdateDeployment): An instance of the UpdateDeployment class
                containing the deployment configuration options
            local_repository_path (str, optional): Absolute path to the local git repository
                which is connected to Deeploy used to check if your Repository is present in the Workspace
        """

        current_deployment = self.__deeploy_service.get_deployment(
            self.__config.workspace_id, deployment_id
        )

        if not (current_deployment):
            raise Exception(
                "Deployment was not found in the Deeploy Workspace. \
                 Make sure the deployment_id is correct."
            )

        if self.__has_new_git_values(options):
            options = self.__check_local_git_config(local_repository_path, options)
        elif self.__has_no_git_values(options):
            pass
        else:
            raise Exception(
                "Both repository_id and branch_name are not provided. Either set both to None or provide both."
            )

        return self.__deeploy_service.update_deployment(
            self.__config.workspace_id, deployment_id, UpdateDeployment(**options)
        )

    
    def update_sagemaker_deployment(
        self,
        deployment_id: str,
        options: UpdateSageMakerDeployment,
        local_repository_path: Optional[str] = None,
    ) -> Deployment:
        """Update a SageMaker Deployment on Deeploy
        Parameters:
            deployment_id (str): The uuid of the Deployment to update
            options (UpdateSageMakerDeployment): An instance of the UpdateSageMakerDeployment class
                containing the deployment configuration options
            local_repository_path (str, optional): Absolute path to the local git repository
                which is connected to Deeploy used to check if your Repository is present in the Workspace
        """

        current_deployment = self.__deeploy_service.get_deployment(
            self.__config.workspace_id, deployment_id
        )

        if not (current_deployment):
            raise Exception(
                "Deployment was not found in the Deeploy Workspace. \
                 Make sure the deployment_id is correct."
            )

        if self.__has_new_git_values(options):
            options = self.__check_local_git_config(local_repository_path, options)
        elif self.__has_no_git_values(options):
            pass
        else:
            raise Exception(
                "Both repository_id and branch_name are not provided. Either set both to None or provide both."
            )

        return self.__deeploy_service.update_sagemaker_deployment(
            self.__config.workspace_id, deployment_id, UpdateSageMakerDeployment(**options)
        )

    
    def update_azure_ml_deployment(
        self,
        deployment_id: str,
        options: UpdateAzureMLDeployment,
        local_repository_path: Optional[str] = None,
    ) -> Deployment:
        """Update an Azure Machine Learning Deployment on Deeploy
        Parameters:
            deployment_id (str): The uuid of the Deployment to update
            options (UpdateAzureMLDeployment): An instance of the UpdateAzureMLDeployment class
                containing the deployment configuration options
            local_repository_path (str, optional): Absolute path to the local git repository
                which is connected to Deeploy used to check if your Repository is present in the Workspace
        """

        current_deployment = self.__deeploy_service.get_deployment(
            self.__config.workspace_id, deployment_id
        )

        if not (current_deployment):
            raise Exception(
                "Deployment was not found in the Deeploy Workspace. \
                 Make sure the deployment_id is correct."
            )

        if self.__has_new_git_values(options):
            options = self.__check_local_git_config(local_repository_path, options)
        elif self.__has_no_git_values(options):
            pass
        else:
            raise Exception(
                "Both repository_id and branch_name are not provided. Either set both to None or provide both."
            )

        return self.__deeploy_service.update_azure_ml_deployment(
            self.__config.workspace_id, deployment_id, UpdateAzureMLDeployment(**options)
        )

    
    def update_external_deployment(
        self,
        deployment_id: str,
        options: UpdateExternalDeployment,
        local_repository_path: Optional[str] = None,
    ) -> Deployment:
        """Update a Deployment on Deeploy
        Parameters:
            deployment_id (str): The uuid of the Deployment to update
            options (UpdateExternalDeployment): An instance of the UpdateExternalDeployment class
                containing the deployment configuration options
            local_repository_path (str, optional): Absolute path to the local git repository
                which is connected to Deeploy used to check if your Repository is present in the Workspace
        """

        current_deployment = self.__deeploy_service.get_deployment(
            self.__config.workspace_id, deployment_id
        )

        if not (current_deployment):
            raise Exception(
                "Deployment was not found in the Deeploy Workspace. \
                 Make sure the deployment_id is correct."
            )

        if self.__has_new_git_values(options):
            options = self.__check_local_git_config(local_repository_path, options)
        elif self.__has_no_git_values(options):
            pass
        else:
            raise Exception(
                "Both repository_id and branch_name are not provided. Either set both to None or provide both."
            )

        return self.__deeploy_service.update_external_deployment(
            self.__config.workspace_id, deployment_id, UpdateExternalDeployment(**options)
        )

    
    def update_registration_deployment(
        self,
        deployment_id: str,
        options: UpdateRegistrationDeployment,
        local_repository_path: Optional[str] = None,
    ) -> Deployment:
        """Update a Deployment on Deeploy
        Parameters:
            deployment_id (str): The uuid of the Deployment to update
            options (UpdateRegistrationDeployment): An instance of the UpdateRegistrationDeployment class
                containing the deployment configuration options
            local_repository_path (str, optional): Absolute path to the local git repository
                which is connected to Deeploy used to check if your Repository is present in the Workspace
        """

        current_deployment = self.__deeploy_service.get_deployment(
            self.__config.workspace_id, deployment_id
        )

        if not (current_deployment):
            raise Exception(
                "Deployment was not found in the Deeploy Workspace. \
                 Make sure the deployment_id is correct."
            )

        if self.__has_new_git_values(options):
            options = self.__check_local_git_config(local_repository_path, options)
        elif self.__has_no_git_values(options):
            pass
        else:
            raise Exception(
                "Both repository_id and branch_name are not provided. Either set both to None or provide both."
            )

        return self.__deeploy_service.update_registration_deployment(
            self.__config.workspace_id, deployment_id, UpdateRegistrationDeployment(**options)
        )

    
    def update_deployment_description(
        self, deployment_id: str, options: UpdateDeploymentDescription
    ) -> Deployment:
        """Update the description of a Deployment on Deeploy
        Parameters:
            deployment_id (str): The uuid of the Deployment to update
            options (UpdateDeploymentDescription): An instance of the UpdateDeploymentDescription class
                containing the deployment description options
        """

        current_deployment = self.__deeploy_service.get_deployment(
            self.__config.workspace_id, deployment_id
        )

        if not (current_deployment):
            raise Exception(
                "Deployment was not found in the Deeploy Workspace. \
                 Make sure the deployment_id is correct."
            )

        return self.__deeploy_service.update_deployment_description(
            self.__config.workspace_id, deployment_id, UpdateDeploymentDescription(**options)
        )

    
    def create_job_schedule(self, options: CreateJobSchedule) -> List[Dict]:
        """Create a job schedule in a Workspace"
        Parameters:
            options (CreateJobSchedule): An instance of the CreateJobSchedule class
                containing the job schedule configuration options
        """

        return self.__deeploy_service.create_job_schedule(
            self.__config.workspace_id, CreateJobSchedule(**options)
        )

    
    def test_job_schedule(self, options: TestJobSchedule) -> JobSchedule:
        """Test a job schedule in a Workspace"
        Parameters:
            options (TestJobSchedule): An instance of the TestJobSchedule class
                containing the test job schedule configuration options
        """

        return self.__deeploy_service.test_job_schedule(
            self.__config.workspace_id, TestJobSchedule(**options)
        )

    
    def update_job_schedule(self, job_schedule_id: str, options: UpdateJobSchedule) -> JobSchedule:
        """Update a job schedule in a Workspace"
        Parameters:
            job_schedule_id (str): The uuid of the job schedule to update
            options (UpdateJobSchedule): An instance of the UpdateJobSchedule class
                containing the job schedule configuration options
        """

        return self.__deeploy_service.update_job_schedule(
            self.__config.workspace_id, job_schedule_id, UpdateJobSchedule(**options)
        )

    
    def deactivate_job_schedule(self, job_schedule_id: str) -> JobSchedule:
        """Deactivate a job schedule in a Workspace"
        Parameters:
            job_schedule_id (str): The uuid of the job schedule to deactivate
        """

        return self.__deeploy_service.deactivate_job_schedule(
            self.__config.workspace_id, job_schedule_id
        )

    
    def activate_job_schedule(self, job_schedule_id: str) -> JobSchedule:
        """Activate a job schedule in a Workspace"
        Parameters:
            job_schedule_id (str): The uuid of the job schedule to activate
        """

        return self.__deeploy_service.activate_job_schedule(
            self.__config.workspace_id, job_schedule_id
        )
    
    def get_custom_metrics(self, deployment_id: str) -> List[CustomMetric]:
        """Get all custom metrics in a Deployment"
        Parameters:
            deployment_id (str): The uuid of the deployment
        """

        return self.__deeploy_service.get_custom_metrics(
            self.__config.workspace_id, deployment_id
        )
    
    def get_custom_metrics_with_chart_data(self, deployment_id: str) -> List[CustomMetricGraphData]:
        """Get all custom metrics with graph data in a Deployment"
        Parameters:
            deployment_id (str): The uuid of the deployment
        """

        return self.__deeploy_service.get_custom_metrics_with_chart_data(
            self.__config.workspace_id, deployment_id
        )
    
    def create_custom_metric(self, deployment_id: str, options: CreateCustomMetric) -> CustomMetric:
        """Create a custom metric in a Deployment"
        Parameters:
            deployment_id (str): The uuid of the deployment
            options (CreateCustomMetric): An instance of the CreateCustomMetric class
                containing the custom metric configuration options
        """

        return self.__deeploy_service.create_custom_metric(
            self.__config.workspace_id, deployment_id, CreateCustomMetric(**options)
        )
    
    def update_custom_metric(self, deployment_id: str, custom_metric_id: str, options: UpdateCustomMetric) -> CustomMetric:
        """Update a custom metric in a Deployment"
        Parameters:
            deployment_id (str): The uuid of the deployment
            custom_metric_id (str): The uuid of the custom metric to update
            options (UpdateCustomMetric): An instance of the UpdateCustomMetric class
                containing the custom metric configuration options
        """

        return self.__deeploy_service.update_custom_metric(
            self.__config.workspace_id, deployment_id, custom_metric_id, UpdateCustomMetric(**options)
        )
    
    def delete_custom_metric(self, deployment_id: str, custom_metric_id: str) -> List[Dict]:
        """Delete a custom metric in a Deployment"
        Parameters:
            deployment_id (str): The uuid of the deployment
            custom_metric_id (str): The uuid of the custom metric to delete
        """

        return self.__deeploy_service.delete_custom_metric(
            self.__config.workspace_id, deployment_id, custom_metric_id
        )
    
    def create_custom_metric_data_points(self, deployment_id: str, custom_metric_id: str, options_list: List[CreateCustomMetricDataPoint]) -> List[CustomMetricDataPoint]:
        """Add custom metric datapoints to a custom metric in a Deployment"
        Parameters:
            deployment_id (str): The uuid of the deployment
            custom_metric_id (str): The uuid of the custom metric to add data points to.
            options (List[CreateCustomMetric]): An instance list of create custom metric data points configuration options
        """

        metric_to_add = [CreateCustomMetricDataPoint(**options) for options in options_list]

        return self.__deeploy_service.create_custom_metric_data_points(
            self.__config.workspace_id, deployment_id, custom_metric_id, metric_to_add
        )
    
    def clear_custom_metric_data_points(self, deployment_id: str, custom_metric_id: str) -> List[Dict]:
        """Clear custom metric datapoints of a custom metric in a Deployment"
        Parameters:
            deployment_id (str): The uuid of the deployment
            custom_metric_id (str): The uuid of the custom metric to clear
        """

        return self.__deeploy_service.clear_custom_metric_data_points(
            self.__config.workspace_id, deployment_id, custom_metric_id
        )

    def predict(self, deployment_id: str, request_body: dict) -> V1Prediction or V2Prediction:
        """Make a predict call
        Parameters:
            deployment_id (str): ID of the Deeploy deployment
            request_body (dict): Request body with input data for the model
        """

        return self.__deeploy_service.predict(
            self.__config.workspace_id, deployment_id, request_body
        )

    def explain(self, deployment_id: str, request_body: dict, image: bool = False) -> object:
        """Make an explain call
        Parameters:
            deployment_id (str): ID of the Deeploy deployment
            request_body (dict): Request body with input data for the model
            image (bool): Return image or not
        """

        return self.__deeploy_service.explain(
            self.__config.workspace_id, deployment_id, request_body, image
        )

    def get_request_logs(
        self, deployment_id: str, params: GetRequestLogsOptions
    ) -> List[RequestLog]:
        """Retrieve request logs
        Parameters:
            deployment_id (str): ID of the Deeploy deployment
            params (GetRequestLogsOptions): An instance of the GetRequestLogsOptions class
                containing the params used for the retrieval of request logs
        """

        return self.__deeploy_service.get_request_logs(
            self.__config.workspace_id, deployment_id, GetRequestLogsOptions(**params)
        )

    def get_prediction_logs(
        self, deployment_id: str, params: GetPredictionLogsOptions
    ) -> List[PredictionLog]:
        """Retrieve prediction logs
        Parameters:
            deployment_id (str): ID of the Deeploy deployment
            params (GetPredictionLogsOptions): An instance of the GetPredictionLogsOptions class
                containing the params used for the retrieval of prediction logs
        """

        return self.__deeploy_service.get_prediction_logs(
            self.__config.workspace_id, deployment_id, GetPredictionLogsOptions(**params)
        )

    def get_one_prediction_log(
        self, deployment_id: str, request_log_id: str, prediction_log_id: str
    ) -> PredictionLog:
        """*** Deprecated in favor of get_prediction_logs ***

        Retrieve one prediction log
        Parameters:
            deployment_id (str): ID of the Deeploy deployment
            request_log_id (str): ID of the request_log containing the prediction
            prediction_log_id (str): ID of the prediction_log to be retrieved
        """

        return self.__deeploy_service.get_one_prediction_log(
            self.__config.workspace_id, deployment_id, request_log_id, prediction_log_id
        )

    def evaluate(
        self,
        deployment_id: str,
        prediction_log_id: str,
        evaluation_input: CreateEvaluation,
    ) -> Evaluation:
        """Evaluate a prediction log
        Parameters:
            deployment_id (str): ID of the Deeploy deployment
            log_id (int): ID of the log to be evaluated
            evaluation_input (CreateEvaluation): An instance of the CreateEvaluation class
                containing the evaluation input
        """

        return self.__deeploy_service.evaluate(
            self.__config.workspace_id,
            deployment_id,
            prediction_log_id,
            CreateEvaluation(**evaluation_input),
        )

    def upload_actuals(
        self, deployment_id: str, actuals_input: CreateActuals
    ) -> List[ActualResponse]:
        """Upload actuals for prediction logs
        Parameters:
            deployment_id (str): ID of the Deeploy deployment
            actuals_input (CreateActuals): An instance of the CreateActuals class
                containing the prediction log id's and corresponding actuals
        """

        return self.__deeploy_service.actuals(
            self.__config.workspace_id, deployment_id, CreateActuals(**actuals_input)
        )


    def generate_metadata_json(self,
        target_path: str, metadata_input: dict
    ) -> str:
        """Generate a metadata.json file
        Parameters:
            target_path (str): Absolute path to the directory in which the
                metadata.json should be saved.
            metadata_input (dict, Metadata): The keys and values you would like to include
                in your metadata.json 
        """
        # validate against metadata class
        return self.__file_service.generate_metadata_json(
            target_path, metadata_input
        )

    def generate_model_reference_json(
        self, target_path: str, reference_input: CreateModelReference
    ) -> ModelReferenceJson:
        """Generate a reference.json file for your model
        Parameters:
            target_path (str): Absolute path to the directory in which the
                model directory with reference.json file should be saved.
            reference_input (CreateModelReference): An instance of the CreateModelReference
                class containing the configuration options of your model
        """

        return self.__file_service.generate_reference_json(
            target_path, CreateModelReference(**reference_input)
        )

    def generate_explainer_reference_json(
        self, target_path: str, reference_input: CreateExplainerReference
    ) -> ExplainerReferenceJson:
        """Generate a reference.json file for your explainer
        Parameters:
            target_path (str): Absolute path to the directory in which the
                explainer directory with reference.json file should be saved.
            reference_input (CreateExplainerReference): An instance of the CreateExplainerReference
                class containing the configuration options of your explainer
        """

        return self.__file_service.generate_reference_json(
            target_path, CreateExplainerReference(**reference_input)
        )

    def generate_transformer_reference_json(
        self, target_path: str, reference_input: CreateTransformerReference
    ) -> TransformerReferenceJson:
        """Generate a reference.json file for your transformer
        Parameters:
            target_path (str): Absolute path to the directory in which the
                transformer directory with reference.json file should be saved.
            reference_input (CreateTransformerReference): An instance of the CreateTransformerReference
                class containing the configuration options of your transformer
        """

        return self.__file_service.generate_reference_json(
            target_path, CreateTransformerReference(**reference_input)
        )
    
    def set_deployment_token(self, deployment_token) -> None:
        """Sets a new deployment token for future requests, usefull when using short lived JWTs
        Parameters:
            deployment_token (str): token used for authenticating with Deployments
        """
        self.__deeploy_service.set_token(deployment_token)

    def __has_new_git_values(self, options: dict) -> bool:
        """Check if the options contain new git values (repository_id or branch_name)
        Parameters:
            options (CreateDeployment, CreateSagemakerDeployment, CreateAzureMLDeployment, CreateExternalDeployment, CreateRegistrationDeployment
                     UpdateDeployment,  UpdateSagemakerDeployment, UpdateAzureMLDeployment, UpdateExternalDeployment, UpdateRegistrationDeployment):
                An instance of the CreateDeployment classcontaining the deployment configuration options
        """

        if ("repository_id" in options and options["repository_id"] is not None) or (
            "branch_name" in options and options["branch_name"] is not None
        ):
            return True
        else:
            return False

    def __has_no_git_values(self, options: dict) -> bool:
        """Check if the options contain no git values (repository_id or branch_name)
        Parameters:
            options (CreateDeployment, CreateSagemakerDeployment, CreateAzureMLDeployment, CreateExternalDeployment, CreateRegistrationDeployment
                     UpdateDeployment,  UpdateSagemakerDeployment, UpdateAzureMLDeployment, UpdateExternalDeployment, UpdateRegistrationDeployment):
                An instance of the CreateDeployment classcontaining the deployment configuration options
        """

        if (
            "repository_id" not in options
            or ("repository_id" in options and options["repository_id"] is None)
        ) and (
            "branch_name" not in options
            or ("branch_name" in options and options["branch_name"] is None)
        ):
            return True
        else:
            return False

    def __check_local_git_config(self, local_repository_path: str, options: dict) -> dict:
        """Check local Git config in repository
        Parameters:
            options (CreateDeployment, CreateSagemakerDeployment, CreateAzureMLDeployment, CreateExternalDeployment, CreateRegistrationDeployment
                     UpdateDeployment,  UpdateSagemakerDeployment, UpdateAzureMLDeployment, UpdateExternalDeployment, UpdateRegistrationDeployment):
                An instance of the CreateDeployment classcontaining the deployment configuration options
            local_repository_path (str, optional): Absolute path to the local git repository
                which is connected to Deeploy used to check if your Repository is present in the Workspace
        """
        if local_repository_path:
            git_service = GitService(local_repository_path)
            if "repository_id" in options:
                warnings.warn(
                    """The repository_id that you defined in the create_options will
                                be overwritten by the git configuration in your local_repository_path""",
                    stacklevel=2,
                )
            options["repository_id"] = self.__get_repository_id(git_service)
            if "branch_name" in options:
                warnings.warn(
                    """The branch_name that you defined in the create_options will
                                be overwritten by the git configuration in your local_repository_path""",
                    stacklevel=2,
                )
            options["branch_name"] = git_service.get_branch_name()
            if "commit" in options:
                warnings.warn(
                    """The commit that you defined in the create_options will
                                be overwritten by the git configuration in your local_repository_path""",
                    stacklevel=2,
                )
            options["commit"] = git_service.get_commit()
        else:
            if "repository_id" not in options:
                raise Exception("Missing repository_id in your create options.")
            if "branch_name" not in options:
                raise Exception("Missing branch_name in your create options.")
        return options

    def __get_repository_id(self, git_service: GitService) -> str:
        remote_url = git_service.get_remote_url()
        workspace_id = self.__config.workspace_id

        repositories = self.__deeploy_service.get_repositories(workspace_id)

        correct_repositories = list(
            filter(
                lambda x: x.remote_path == self.__parse_url_ssh_to_https(remote_url)
                or x.remote_path == remote_url,
                repositories,
            )
        )

        if len(correct_repositories) == 1:
            repository_id = correct_repositories[0].id
        else:
            raise Exception(
                "Repository ID was not found in Deeploy Workspace. \
                             Make sure you have connected it before deploying."
            )

        return repository_id

    def __parse_url_ssh_to_https(self, remote_path: str) -> str or None:
        if remote_path[:4] != "git@":
            # https to ssh
            path_tokens = remote_path.split("/")
            provider = path_tokens[2]
            user = path_tokens[3]
            path = path_tokens[4:]
            link = "git@" + provider + ":" + user
            for sub_directory in path:
                link += "/" + sub_directory
        else:
            # ssh to https
            path_tokens = remote_path.split("@")
            link = "https://" + path_tokens[1].replace(":", "/")
        return link
