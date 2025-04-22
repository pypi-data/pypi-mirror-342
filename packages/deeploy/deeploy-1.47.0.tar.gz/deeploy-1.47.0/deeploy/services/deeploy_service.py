from typing import Dict, List, Optional

import requests
from pydantic import TypeAdapter

from deeploy.enums import AuthType
from deeploy.enums.artifact import Artifact
from deeploy.models import (
    ActualResponse,
    CreateActuals,
    CreateAzureMLDeployment,
    CreateCustomMetric,
    CreateCustomMetricDataPoint,
    CreateDeployment,
    CreateEnvironmentVariable,
    CreateEvaluation,
    CreateExternalDeployment,
    CreateRegistrationDeployment,
    CreateSageMakerDeployment,
    CustomMetric,
    CustomMetricDataPoint,
    CustomMetricGraphData,
    Deployment,
    EnvironmentVariable,
    Evaluation,
    GetPredictionLogsOptions,
    PredictionLog,
    RawEnvironmentVariable,
    Repository,
    UpdateAzureMLDeployment,
    UpdateCustomMetric,
    UpdateDeployment,
    UpdateDeploymentDescription,
    UpdateExternalDeployment,
    UpdateRegistrationDeployment,
    UpdateSageMakerDeployment,
    Workspace,
)
from deeploy.models.create_job_schedule import CreateJobSchedule
from deeploy.models.get_request_logs_options import GetRequestLogsOptions
from deeploy.models.job_schedule import JobSchedule
from deeploy.models.prediction_log import RequestLog
from deeploy.models.test_job_schedule import TestJobSchedule
from deeploy.models.update_job_schedule import UpdateJobSchedule


class DeeployService(object):
    """
    A class for interacting with the Deeploy API
    """

    request_timeout = 300

    def __init__(
        self,
        host: str,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        token: Optional[str] = None,
        team_id: Optional[str] = None,
    ) -> None:
        if not (access_key and secret_key) and not token:
            raise Exception(
                "No authentication method provided. Please provide a token or personal key pair"
            )

        self.__access_key = access_key
        self.__secret_key = secret_key
        self.__token = token
        self.__host = f"https://api.{host}"
        self.__request_session = requests.Session()

        if team_id:
            self.__request_session.headers.update({'team-id': team_id})
        if access_key and secret_key:
            self.__request_session.auth = (access_key, secret_key)


    def get_repositories(self, workspace_id: str) -> List[Repository]:
        url = "%s/workspaces/%s/repositories" % (self.__host, workspace_id)
        self.__set_auth(AuthType.BASIC)
        repositories_response = self.__request_session.get(
            url,
            timeout=self.request_timeout,
        )

        repositories = TypeAdapter(List[Repository]).validate_python(repositories_response.json())

        return repositories

    def get_repository(self, workspace_id: str, repository_id: str) -> Repository:
        url = "%s/workspaces/%s/repositories/%s" % (
            self.__host,
            workspace_id,
            repository_id,
        )
        self.__set_auth(AuthType.BASIC)
        repository_response = self.__request_session.get(
            url,
            timeout=self.request_timeout,
        )
        if not self.__request_is_successful(repository_response):
            raise Exception("Repository does not exist in the workspace.")

        repository = TypeAdapter(Repository).validate_python(repository_response.json())

        return repository

    def create_environment_variable(
        self, workspace_id: str, environment_variable: CreateEnvironmentVariable
    ) -> EnvironmentVariable:
        url = "%s/workspaces/%s/environmentVariables" % (self.__host, workspace_id)
        data = environment_variable.to_request_body()
        self.__set_auth(AuthType.BASIC)
        environment_variable_response = self.__request_session.post(
            url,
            json=data,
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(environment_variable_response):
            raise Exception(
                "Failed to create environment variable: %s"
                % str(environment_variable_response.json())
            )

        environment_variable = TypeAdapter(EnvironmentVariable).validate_python(
            environment_variable_response.json()["data"]
        )

        return environment_variable

    def get_all_environment_variables(self, workspace_id: str) -> List[EnvironmentVariable]:
        url = "%s/workspaces/%s/environmentVariables" % (self.__host, workspace_id)
        self.__set_auth(AuthType.BASIC)
        environment_variables_response = self.__request_session.get(
            url,
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(environment_variables_response):
            raise Exception("Failed to get environment variables.")

        environment_variables = TypeAdapter(List[EnvironmentVariable]).validate_python(
            environment_variables_response.json()
        )

        return environment_variables

    def get_environment_variable_ids_for_deployment_artifact(
        self, workspace_id: str, deployment_id: str, artifact: Artifact
    ) -> List[str]:
        url = "%s/workspaces/%s/environmentVariables/raw" % (self.__host, workspace_id)
        params = {
            "deploymentId": "eq:%s" % deployment_id,
            "artifact": "eq:%s" % artifact,
        }
        self.__set_auth(AuthType.BASIC)
        environment_variables_response = self.__request_session.get(
            url,
            params=params,
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(environment_variables_response):
            raise Exception("Failed to get environment variables.")

        raw_environment_variables = TypeAdapter(List[RawEnvironmentVariable]).validate_python(
            environment_variables_response.json()["data"]
        )
        environment_variable_ids = list(map(lambda env: env.id, raw_environment_variables))

        return environment_variable_ids

    def get_deployment(
        self, workspace_id: str, deployment_id: str, withExamples: bool = False
    ) -> Deployment:
        url = "%s/workspaces/%s/deployments/%s" % (
            self.__host,
            workspace_id,
            deployment_id,
        )
        params = {
            "withExamples": withExamples,
        }
        self.__set_auth(AuthType.BASIC)
        deployment_response = self.__request_session.get(
            url,
            params=params,
            timeout=self.request_timeout,
        )
        if not self.__request_is_successful(deployment_response):
            raise Exception(
                "Failed to retrieve the deployment: %s" % str(deployment_response.json())
            )

        deployment = TypeAdapter(Deployment).validate_python(deployment_response.json())

        return deployment

    def create_deployment(self, workspace_id: str, deployment: CreateDeployment) -> Deployment:
        url = "%s/workspaces/%s/deployments" % (self.__host, workspace_id)
        data = deployment.to_request_body()
        self.__set_auth(AuthType.BASIC)
        deployment_response = self.__request_session.post(
            url,
            json=data,
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(deployment_response):
            raise Exception("Failed to create the Deployment: %s" % str(deployment_response.json()))

        deployment = TypeAdapter(Deployment).validate_python(deployment_response.json())

        return deployment

    def create_sagemaker_deployment(
        self, workspace_id: str, deployment: CreateSageMakerDeployment
    ) -> Deployment:
        url = "%s/workspaces/%s/deployments" % (self.__host, workspace_id)
        data = deployment.to_request_body()
        self.__set_auth(AuthType.BASIC)
        deployment_response = self.__request_session.post(
            url,
            json=data,
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(deployment_response):
            raise Exception("Failed to create the Deployment: %s" % str(deployment_response.json()))

        deployment = TypeAdapter(Deployment).validate_python(deployment_response.json())

        return deployment

    def create_azure_ml_deployment(
        self, workspace_id: str, deployment: CreateAzureMLDeployment
    ) -> Deployment:
        url = "%s/workspaces/%s/deployments" % (self.__host, workspace_id)
        data = deployment.to_request_body()
        self.__set_auth(AuthType.BASIC)
        deployment_response = self.__request_session.post(
            url,
            json=data,
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(deployment_response):
            raise Exception("Failed to create the Deployment: %s" % str(deployment_response.json()))

        deployment = TypeAdapter(Deployment).validate_python(deployment_response.json())

        return deployment

    def create_external_deployment(
        self, workspace_id: str, deployment: CreateExternalDeployment
    ) -> Deployment:
        url = "%s/workspaces/%s/deployments" % (self.__host, workspace_id)
        data = deployment.to_request_body()
        self.__set_auth(AuthType.BASIC)
        deployment_response = self.__request_session.post(
            url,
            json=data,
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(deployment_response):
            raise Exception("Failed to create the Deployment: %s" % str(deployment_response.json()))

        deployment = TypeAdapter(Deployment).validate_python(deployment_response.json())

        return deployment

    def create_registration_deployment(
        self, workspace_id: str, deployment: CreateRegistrationDeployment
    ) -> Deployment:
        url = "%s/workspaces/%s/deployments" % (self.__host, workspace_id)
        data = deployment.to_request_body()
        self.__set_auth(AuthType.BASIC)
        deployment_response = self.__request_session.post(
            url,
            json=data,
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(deployment_response):
            raise Exception("Failed to create the Deployment: %s" % str(deployment_response.json()))

        deployment = TypeAdapter(Deployment).validate_python(deployment_response.json())

        return deployment

    def update_deployment(
        self, workspace_id: str, deployment_id: str, update: UpdateDeployment
    ) -> Deployment:
        url = "%s/workspaces/%s/deployments/%s" % (
            self.__host,
            workspace_id,
            deployment_id,
        )
        data = update.to_request_body()
        self.__set_auth(AuthType.BASIC)
        deployment_response = self.__request_session.patch(
            url,
            json=data,
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(deployment_response):
            raise Exception("Failed to update the Deployment: %s" % str(deployment_response.json()))

        deployment = TypeAdapter(Deployment).validate_python(deployment_response.json())

        return deployment

    def update_sagemaker_deployment(
        self, workspace_id: str, deployment_id: str, update: UpdateSageMakerDeployment
    ) -> Deployment:
        url = "%s/workspaces/%s/deployments/%s" % (
            self.__host,
            workspace_id,
            deployment_id,
        )
        data = update.to_request_body()
        self.__set_auth(AuthType.BASIC)
        deployment_response = self.__request_session.patch(
            url,
            json=data,
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(deployment_response):
            raise Exception("Failed to update the Deployment: %s" % str(deployment_response.json()))

        deployment = TypeAdapter(Deployment).validate_python(deployment_response.json())

        return deployment

    def update_azure_ml_deployment(
        self, workspace_id: str, deployment_id: str, update: UpdateAzureMLDeployment
    ) -> Deployment:
        url = "%s/workspaces/%s/deployments/%s" % (
            self.__host,
            workspace_id,
            deployment_id,
        )
        data = update.to_request_body()
        self.__set_auth(AuthType.BASIC)
        deployment_response = self.__request_session.patch(
            url,
            json=data,
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(deployment_response):
            raise Exception("Failed to update the Deployment: %s" % str(deployment_response.json()))

        deployment = TypeAdapter(Deployment).validate_python(deployment_response.json())

        return deployment

    def update_external_deployment(
        self, workspace_id: str, deployment_id: str, update: UpdateExternalDeployment
    ) -> Deployment:
        url = "%s/workspaces/%s/deployments/%s" % (
            self.__host,
            workspace_id,
            deployment_id,
        )
        data = update.to_request_body()
        self.__set_auth(AuthType.BASIC)
        deployment_response = self.__request_session.patch(
            url,
            json=data,
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(deployment_response):
            raise Exception("Failed to update the Deployment: %s" % str(deployment_response.json()))

        deployment = TypeAdapter(Deployment).validate_python(deployment_response.json())

        return deployment

    def update_registration_deployment(
        self, workspace_id: str, deployment_id: str, update: UpdateRegistrationDeployment
    ) -> Deployment:
        url = "%s/workspaces/%s/deployments/%s" % (
            self.__host,
            workspace_id,
            deployment_id,
        )
        data = update.to_request_body()
        self.__set_auth(AuthType.BASIC)
        deployment_response = self.__request_session.patch(
            url,
            json=data,
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(deployment_response):
            raise Exception("Failed to update the Deployment: %s" % str(deployment_response.json()))

        deployment = TypeAdapter(Deployment).validate_python(deployment_response.json())

        return deployment

    def update_deployment_description(
        self, workspace_id: str, deployment_id: str, update: UpdateDeploymentDescription
    ) -> Deployment:
        url = "%s/workspaces/%s/deployments/%s/description" % (
            self.__host,
            workspace_id,
            deployment_id,
        )
        data = update.to_request_body()
        self.__set_auth(AuthType.BASIC)
        deployment_response = self.__request_session.patch(
            url,
            json=data,
            timeout=self.request_timeout,
        )
        if not self.__request_is_successful(deployment_response):
            raise Exception("Failed to update the deployment: %s" % str(deployment_response.json()))

        deployment = TypeAdapter(Deployment).validate_python(deployment_response.json()["data"])

        return deployment

    def create_job_schedule(self, workspace_id: str, options: CreateJobSchedule) -> JobSchedule:
        url = "%s/workspaces/%s/jobSchedules" % (
            self.__host,
            workspace_id,
        )
        data = options.to_request_body()
        self.__set_auth(AuthType.BASIC)
        job_schedule_response = self.__request_session.post(
            url,
            json=data,
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(job_schedule_response):
            raise Exception("Failed to create job schedule: %s" % str(job_schedule_response.json()))

        job_schedule = TypeAdapter(JobSchedule).validate_python(
            job_schedule_response.json()["data"]
        )

        return job_schedule

    def test_job_schedule(self, workspace_id: str, options: TestJobSchedule) -> List[Dict]:
        url = "%s/workspaces/%s/jobSchedules/test" % (
            self.__host,
            workspace_id,
        )
        data = options.to_request_body()
        self.__set_auth(AuthType.BASIC)
        data_response = self.__request_session.post(
            url,
            json=data,
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(data_response):
            raise Exception("Job schedule test failed: %s" % str(data_response.json()))

        return data_response.json()

    def update_job_schedule(
        self, workspace_id: str, job_schedule_id: str, options: UpdateJobSchedule
    ) -> JobSchedule:
        url = "%s/workspaces/%s/jobSchedules/%s" % (
            self.__host,
            workspace_id,
            job_schedule_id,
        )
        data = options.to_request_body()
        self.__set_auth(AuthType.BASIC)
        job_schedule_response = self.__request_session.patch(
            url,
            json=data,
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(job_schedule_response):
            raise Exception("Failed to update job schedule: %s" % str(job_schedule_response.json()))

        job_schedule = TypeAdapter(JobSchedule).validate_python(
            job_schedule_response.json()["data"]
        )

        return job_schedule

    def deactivate_job_schedule(self, workspace_id: str, job_schedule_id: str) -> JobSchedule:
        url = "%s/workspaces/%s/jobSchedules/%s/deactivate" % (
            self.__host,
            workspace_id,
            job_schedule_id,
        )
        self.__set_auth(AuthType.BASIC)
        job_schedule_response = self.__request_session.patch(
            url,
            json={},
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(job_schedule_response):
            raise Exception(
                "Failed to deactivate job schedule: %s" % str(job_schedule_response.json())
            )

        job_schedule = TypeAdapter(JobSchedule).validate_python(
            job_schedule_response.json()["data"]
        )

        return job_schedule

    def activate_job_schedule(self, workspace_id: str, job_schedule_id: str) -> JobSchedule:
        url = "%s/workspaces/%s/jobSchedules/%s/activate" % (
            self.__host,
            workspace_id,
            job_schedule_id,
        )
        self.__set_auth(AuthType.BASIC)
        job_schedule_response = self.__request_session.patch(
            url,
            json={},
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(job_schedule_response):
            raise Exception(
                "Failed to activate job schedule: %s" % str(job_schedule_response.json())
            )

        job_schedule = TypeAdapter(JobSchedule).validate_python(
            job_schedule_response.json()["data"]
        )

        return job_schedule

    def get_workspace(self, workspace_id: str) -> Workspace:
        url = "%s/workspaces/%s" % (self.__host, workspace_id)

        self.__set_auth(AuthType.BASIC)
        workspace_response = self.__request_session.get(
            url,
            timeout=self.request_timeout,
        )
        if not self.__request_is_successful(workspace_response):
            raise Exception("Workspace does not exist.")

        workspace = TypeAdapter(Workspace).validate_python(workspace_response.json())

        return workspace

    def predict(self, workspace_id: str, deployment_id: str, request_body: dict) -> object:
        url = "%s/workspaces/%s/deployments/%s/predict" % (
            self.__host,
            workspace_id,
            deployment_id,
        )
        self.__set_auth(AuthType.ALL)
        prediction_response = self.__request_session.post(
            url,
            json=request_body,
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(prediction_response):
            raise Exception(f"Failed to call predictive model: {prediction_response.json()}")

        prediction = prediction_response.json()
        return prediction

    def explain(
        self,
        workspace_id: str,
        deployment_id: str,
        request_body: dict,
        image: bool = False,
    ) -> object:
        url = "%s/workspaces/%s/deployments/%s/explain" % (
            self.__host,
            workspace_id,
            deployment_id,
        )
        params = {
            "image": str(image).lower(),
        }

        self.__set_auth(AuthType.ALL)
        explanation_response = self.__request_session.post(
            url,
            json=request_body,
            params=params,
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(explanation_response):
            raise Exception(f"Failed to call explainer model: {explanation_response.json()}")

        explanation = explanation_response.json()
        return explanation

    def get_one_prediction_log(
        self,
        workspace_id: str,
        deployment_id: str,
        request_log_id: str,
        prediction_log_id: str,
    ) -> PredictionLog:
        url = "%s/workspaces/%s/deployments/%s/requestLogs/%s/predictionLogs/%s" % (
            self.__host,
            workspace_id,
            deployment_id,
            request_log_id,
            prediction_log_id,
        )
        self.__set_auth(AuthType.ALL)

        log_response = self.__request_session.get(
            url,
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(log_response):
            raise Exception("Failed to get log %s." % prediction_log_id)

        log = TypeAdapter(PredictionLog).validate_python(log_response.json())
        return log

    def get_prediction_logs(
        self, workspace_id: str, deployment_id: str, params: GetPredictionLogsOptions
    ) -> List[PredictionLog]:
        url = "%s/workspaces/%s/deployments/%s/predictionLogs" % (
            self.__host,
            workspace_id,
            deployment_id,
        )
        self.__set_auth(AuthType.ALL)
        
        logs_response = self.__request_session.get(
            url,
            params=params.to_params(),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(logs_response):
            raise Exception("Failed to get logs.")

        logs = TypeAdapter(List[PredictionLog]).validate_python(logs_response.json())
        return logs

    def get_request_logs(
        self, workspace_id: str, deployment_id: str, params: GetRequestLogsOptions
    ) -> List[RequestLog]:
        url = "%s/workspaces/%s/deployments/%s/requestLogs" % (
            self.__host,
            workspace_id,
            deployment_id,
        )

        self.__set_auth(AuthType.ALL)
        logs_response = self.__request_session.get(
            url,
            params=params.to_params(),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(logs_response):
            raise Exception("Failed to get logs.")

        logs = TypeAdapter(List[RequestLog]).validate_python(logs_response.json())
        return logs

    def evaluate(
        self,
        workspace_id: str,
        deployment_id: str,
        prediction_log_id: str,
        evaluation_input: CreateEvaluation,
    ) -> Evaluation:
        url = "%s/workspaces/%s/deployments/%s/predictionLogs/%s/evaluatePrediction" % (
            self.__host,
            workspace_id,
            deployment_id,
            prediction_log_id,
        )

        if evaluation_input.agree is True and ("desired_output" in evaluation_input):
            raise Exception(
                "A desired_output can not be provided when agreeing with the inference."
            )

        data = evaluation_input.to_request_body()
        self.__set_auth(AuthType.TOKEN)
        evaluation_response = self.__request_session.post(
            url,
            json=data,
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(evaluation_response):
            if evaluation_response.status_code == 409:
                raise Exception("Log has already been evaluated.")
            elif evaluation_response.status_code in (401, 403):
                raise Exception("No permission to perform this action.")
            else:
                raise Exception(
                    "Failed to request evaluation. Response code: %s"
                    % evaluation_response.status_code
                )

        evaluation = TypeAdapter(Evaluation).validate_python(evaluation_response.json())
        return evaluation

    def actuals(
        self, workspace_id: str, deployment_id: str, actuals_input: CreateActuals
    ) -> List[ActualResponse]:
        url = "%s/workspaces/%s/deployments/%s/actuals" % (
            self.__host,
            workspace_id,
            deployment_id,
        )

        data = actuals_input.to_request_body()
        self.__set_auth(AuthType.TOKEN)
        actuals_response = self.__request_session.put(
            url,
            json=data,
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(actuals_response):
            if actuals_response.status_code == 401:
                raise Exception("No permission to perform this action.")
            else:
                raise Exception("Failed to submit actuals.")

        actuals = TypeAdapter(List[ActualResponse]).validate_python(actuals_response.json())
        return actuals

    def set_token(self, deployment_token) -> None:
        self.__token = deployment_token

    def __request_is_successful(self, request: requests.Response) -> bool:
        if str(request.status_code)[0] == "2":
            return True
        return False
    
    def __set_auth(self, supported_auth: AuthType):
        if (self.__access_key and self.__secret_key) and (
            supported_auth == AuthType.BASIC or supported_auth == AuthType.ALL
        ):
            self.__request_session.auth = (self.__access_key, self.__secret_key)
        elif (self.__token) and (
            supported_auth == AuthType.TOKEN or supported_auth == AuthType.ALL
        ):
            self.__request_session.auth = None
            self.__request_session.headers.update({"Authorization": "Bearer " + self.__token})

        elif (self.__access_key and self.__secret_key) and not (
                    supported_auth == AuthType.BASIC or supported_auth == AuthType.ALL
                ):
            raise ValueError("This function currently does not support authenticating with personal access key, please use a deployment token instead.")
        else:
            raise ValueError("This function currently does not support authenticating with deployment token, please use a personal access key instead.")
        
    def get_custom_metrics_with_chart_data(
        self, workspace_id: str, deployment_id: str
    ) -> List[CustomMetricGraphData]:
        url = "%s/workspaces/%s/deployments/%s/customMetricsChartData" % (
            self.__host,
            workspace_id,
            deployment_id,
        )
        self.__set_auth(AuthType.ALL)
        
        logs_response = self.__request_session.get(
            url,
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(logs_response):
            raise Exception("Failed to get logs.")

        logs = TypeAdapter(List[CustomMetricGraphData]).validate_python(logs_response.json())
        return logs
    
    def get_custom_metrics(
        self, workspace_id: str, deployment_id: str
    ) -> List[CustomMetric]:
        url = "%s/workspaces/%s/deployments/%s/customMetrics" % (
            self.__host,
            workspace_id,
            deployment_id,
        )
        self.__set_auth(AuthType.ALL)
        
        logs_response = self.__request_session.get(
            url,
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(logs_response):
            raise Exception("Failed to get logs.")

        logs = TypeAdapter(List[CustomMetric]).validate_python(logs_response.json())
        return logs

    def create_custom_metric(
        self, workspace_id: str, deployment_id: str, create_custom_metric: CreateCustomMetric
    ) -> CustomMetric:
        url = "%s/workspaces/%s/deployments/%s/customMetric" % (
            self.__host,
            workspace_id,
            deployment_id,
        )
        data = create_custom_metric.to_request_body()
        self.__set_auth(AuthType.BASIC)
        custom_metric_response = self.__request_session.post(
            url,
            json=data,
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(custom_metric_response):
            raise Exception(
                "Failed to create custom metric: %s"
                % str(custom_metric_response.json())
            )

        custom_metric = TypeAdapter(CustomMetric).validate_python(
            custom_metric_response.json()
        )

        return custom_metric 
    
    def update_custom_metric(
        self, workspace_id: str, deployment_id: str, custom_metric_id: str, update_custom_metric: UpdateCustomMetric
    ) -> CustomMetric:
        url = "%s/workspaces/%s/deployments/%s/customMetric/%s" % (
            self.__host,
            workspace_id,
            deployment_id,
            custom_metric_id
        )
        data = update_custom_metric.to_request_body()
        self.__set_auth(AuthType.BASIC)
        custom_metric_response = self.__request_session.patch(
            url,
            json=data,
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(custom_metric_response):
            raise Exception(
                "Failed to update custom metric: %s"
                % str(custom_metric_response.json())
            )

        custom_metric = TypeAdapter(CustomMetric).validate_python(
            custom_metric_response.json()
        )

        return custom_metric
    
    def delete_custom_metric(
        self, workspace_id: str, deployment_id: str, custom_metric_id: str
    ):
        url = "%s/workspaces/%s/deployments/%s/customMetric/%s" % (
            self.__host,
            workspace_id,
            deployment_id,
            custom_metric_id
        )
        self.__set_auth(AuthType.BASIC)
        custom_metric_response = self.__request_session.delete(
            url,
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(custom_metric_response):
            raise Exception(
                "Failed to delete custom metric: %s"
                % str(custom_metric_response.json())
            )

        return
    
    def create_custom_metric_data_points(
        self, workspace_id: str, deployment_id: str, custom_metric_id: str, create_custom_metric_data_points: List[CreateCustomMetricDataPoint]
    ) -> List[CustomMetricDataPoint]:
        url = "%s/workspaces/%s/deployments/%s/customMetric/%s/dataPoints" % (
            self.__host,
            workspace_id,
            deployment_id,
            custom_metric_id
        )
        data = [create_custom_metric_data_point.to_request_body() for create_custom_metric_data_point in create_custom_metric_data_points]
        self.__set_auth(AuthType.ALL)
        custom_metric_data_points_response = self.__request_session.post(
            url,
            json=data,
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(custom_metric_data_points_response):
            raise Exception(
                "Failed to create custom metric: %s"
                % str(custom_metric_data_points_response.json())
            )

        custom_metric_data_points = TypeAdapter(List[CustomMetricDataPoint]).validate_python(
            custom_metric_data_points_response.json()
        )

        return custom_metric_data_points 
    
    def clear_custom_metric_data_points(
        self, workspace_id: str, deployment_id: str, custom_metric_id: str
    ):
        url = "%s/workspaces/%s/deployments/%s/customMetric/%s/dataPoints" % (
            self.__host,
            workspace_id,
            deployment_id,
            custom_metric_id
        )
        self.__set_auth(AuthType.ALL)
        custom_metric_data_points_response = self.__request_session.delete(
            url,
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(custom_metric_data_points_response):
            raise Exception(
                "Failed to delete data points of custom metric: %s"
                % str(custom_metric_data_points_response.json())
            )

        return
    