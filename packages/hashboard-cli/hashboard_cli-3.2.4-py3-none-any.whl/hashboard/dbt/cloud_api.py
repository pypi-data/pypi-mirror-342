from os import environ

from click import ClickException
import requests
import time
from typing import List, Dict

from hashboard.utils.display import verbose_cli_print

HB_DBT_CLOUD_AUTH_KEY = environ.get("HB_DBT_CLOUD_AUTH_KEY")


class DbtCloudAPIClient:
    def __init__(self, account_id):
        if not HB_DBT_CLOUD_AUTH_KEY:
            raise ClickException(
                "HB_DBT_CLOUD_AUTH_KEY environment variable is not set."
            )
        self.metadata_base_url = "https://cloud.getdbt.com/api"
        self.discovery_base_url = "https://metadata.cloud.getdbt.com/graphql"
        self.headers = {
            "Authorization": f"Bearer {HB_DBT_CLOUD_AUTH_KEY}",
            "Content-Type": "application/json",
        }
        self.account_id = account_id

    def _wait_for_run_completion(self, run_id: str, poll_interval: int = 5) -> Dict:
        """
        Polls the job status until it completes or fails.

        Args:
            run_id: dbt Cloud run ID
            poll_interval: Seconds to wait between status checks (default: 5)

        Returns:
            Dict containing the final job status

        Raises:
            requests.exceptions.HTTPError: If the API request fails
            ValueError: If an unknown status code is received
        """
        endpoint = (
            f"{self.metadata_base_url}/v2/accounts/{self.account_id}/runs/{run_id}"
        )

        # Status code mapping
        STATUS_COMPLETED = "10"
        STATUS_ERROR = "20"
        STATUS_CANCELLED = "30"
        STATUS_QUEUED = "1"
        STATUS_STARTING = "2"
        STATUS_RUNNING = "3"

        while True:
            response = requests.get(endpoint, headers=self.headers)

            if response.status_code != 200:
                verbose_cli_print(
                    f"Error: Received HTTP status code {response.status_code} when checking job status"
                )
                verbose_cli_print(f"Response body: {response.text}")
                response.raise_for_status()

            data = response.json()["data"]
            status = str(data["status"])
            artifacts_saved = data.get("artifacts_saved", False)

            if status == STATUS_COMPLETED and artifacts_saved:
                verbose_cli_print("Job completed successfully and artifacts are saved")
                return data
            elif status == STATUS_COMPLETED:
                verbose_cli_print(
                    "Job completed successfully, waiting for artifacts to be saved..."
                )
            elif status == STATUS_ERROR:
                raise ValueError("Error: dbt run failed")
            elif status == STATUS_CANCELLED:
                raise ValueError("Error: dbt run was cancelled")
            elif status == STATUS_QUEUED or status == STATUS_STARTING or status == STATUS_RUNNING:
                verbose_cli_print("Job still running, waiting 5 seconds...")
            else:
                raise ValueError(f"Unknown dbt run status code {status}")

            time.sleep(poll_interval)

    def get_manifest(self, run_id: str) -> Dict:
        """
        Downloads the manifest.json artifact for a completed job.

        Args:
            run_id: dbt Cloud run ID

        Returns:
            Dict containing the manifest.json contents
        """
        self._wait_for_run_completion(run_id)
        endpoint = f"{self.metadata_base_url}/v2/accounts/{self.account_id}/runs/{run_id}/artifacts/manifest.json"
        response = requests.get(endpoint, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_models_executed_in_run(self, run_id: str) -> List[str]:
        """
        Gets the list of models that were executed in the job using the Discovery GraphQL API.

        Args:
            run_id: dbt Cloud run ID

        Returns:
            List of model names that were executed
        """
        endpoint = (
            f"{self.metadata_base_url}/v2/accounts/{self.account_id}/runs/{run_id}/"
        )
        response = requests.get(endpoint, headers=self.headers)
        job_id = response.json()["data"]["job_id"]

        query = """
        query WhichNodesWereRunInCI($runId: BigInt, $jobId: BigInt!) {
            job(runId: $runId, id: $jobId) {
                id
                models {
                    database
                    schema
                    alias
                    uniqueId
                    status
                    meta
                }
            }
        }
        """
        variables = {"runId": int(run_id), "jobId": int(job_id)}

        response = requests.post(
            self.discovery_base_url,
            headers=self.headers,
            json={"query": query, "variables": variables},
        )
        response.raise_for_status()

        data = response.json()
        models = []

        if data.get("data", {}).get("job", {}).get("models"):
            for model in data["data"]["job"]["models"]:
                models.append(model)

        return models

    def _get_prod_environment(self, project_id: str) -> str:
        """
        Gets the id of the production environment of a given project

        Args:
            project_id: dbt Cloud project id

        Returns:
            project id string

        """
        endpoint = f"{self.metadata_base_url}/v3/accounts/{self.account_id}/projects/{project_id}/environments/"

        response = requests.get(endpoint, headers=self.headers)
        response.raise_for_status()
        envs: List[dict] = response.json()["data"]
        prod_env_id = ""
        for env in envs:
            if env.get("deployment_type") == "production":
                prod_env_id = env.get("id")
                break

        if not prod_env_id:
            raise ValueError("Error: Could not identify production model state")
        return prod_env_id

    def get_prod_location_for_models(
        self,
        project_id: str,
        model_unique_ids: List[str],
    ) -> List[Dict]:
        """
        Gets the database and schema information for a list of model unique IDs.

        Args:
            project_id: dbt Cloud project id
            model_unique_ids: List of model unique IDs to look up

        Returns:
            List of dictionaries containing database, schema, and uniqueId for each model
        """
        env_id = self._get_prod_environment(project_id)

        query = """
        query NodeProductionLocation($environmentId: BigInt!, $filter: ModelAppliedFilter, $after: String) {
            environment(id: $environmentId) {
                applied {
                    models(first: 500, filter: $filter, after: $after) {
                        edges {
                            node {
                                database
                                schema
                                alias
                                uniqueId
                                meta
                            }
                        }
                        pageInfo {
                            hasNextPage
                            endCursor
                        }
                    }
                }
            }
        }
        """
        model_locations = []
        has_next_page = True
        end_cursor = None

        while has_next_page:
            variables = {
                "environmentId": int(env_id),
                "filter": {"uniqueIds": model_unique_ids},
            }

            if end_cursor:
                variables["after"] = end_cursor

            response = requests.post(
                self.discovery_base_url,
                headers=self.headers,
                json={"query": query, "variables": variables},
            )
            response.raise_for_status()

            data = response.json()
            if data.get("errors"):
                raise ValueError(
                    f"Error getting prod model locations: {data['errors']}"
                )
            models_data = (
                data.get("data", {})
                .get("environment", {})
                .get("applied", {})
                .get("models", {})
            )

            if models_data.get("edges"):
                for edge in models_data["edges"]:
                    node = edge["node"]
                    model_locations.append(
                        {
                            "uniqueId": node["uniqueId"],
                            "database": node["database"],
                            "schema": node["schema"],
                            "alias": node["alias"],
                        }
                    )

            page_info = models_data.get("pageInfo", {})
            has_next_page = page_info.get("hasNextPage", False)
            end_cursor = page_info.get("endCursor")

        return model_locations
