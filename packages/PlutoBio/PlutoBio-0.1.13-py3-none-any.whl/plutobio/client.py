import requests
from typing import Union
import os
import uuid

from .plots import Plot, Plots, Displays, Display
from .assay_data import AssayData
from .sample_data import SampleData
from .analyses import Analysis
from .attachments import Attachment
from .pipelines import Pipelines
from .projects import Project
from .results import Results
from .experiments import Experiment, Experiments
from .download_upload import DownloadUploadHandler
from .settings import DEFAULT_TMP_PATH
import pandas as pd
from . import utils


class PlutoClient:
    """Base class for Pluto API access"""

    def __init__(self, token: str, test_client=None) -> None:
        self._experiment = Experiment(client=self)
        self._plots = Plot(client=self)
        self._assay_data = AssayData(client=self)
        self._sample_data = SampleData(client=self)
        self._attachment = Attachment(client=self)
        self._analysis = Analysis(client=self)
        self._pipelines = Pipelines(client=self)
        self._project = Project(client=self)
        self._results = Results(client=self)
        self._download_upload = DownloadUploadHandler(client=self)
        self._plot_displays = Display(client=self)
        self._token = token
        self._base_url = os.environ.get("PLUTO_API_URL", "https://api.pluto.bio")
        self._test_client = test_client

    def _handle_response_errors(self, response) -> None:
        """Handle HTTP errors based on the response status code.

        :param response: The HTTP response.
        :type response: requests.Response
        :raises HTTPError: With a specific message based on the status code.
        """
        response_content = response.json()

        error_message = f"Response: {response.status_code}"
        if hasattr(response, "status_text"):
            error_message += f" - {response.status_text}"
        if "message" in response_content:
            error_message += f" | Message: {response_content['message']}"
        if "code" in response_content:
            error_message += f" | Code ID: {response_content['code']}"
        if "details" in response_content:
            error_message += f" | Additional details: {response_content['details']}"

        if response.status_code == 400:
            raise requests.HTTPError(error_message)
        elif response.status_code == 401:
            raise requests.HTTPError(error_message)
        elif response.status_code == 403:
            raise requests.HTTPError(error_message)
        elif response.status_code == 404:
            raise requests.HTTPError(error_message)
        elif response.status_code == 500:
            raise requests.HTTPError(error_message)
        else:
            raise requests.HTTPError(error_message)

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: dict = None,
        data: dict = None,
        headers: dict = None,
    ) -> dict:
        """
        Make a generic HTTP request to the API.

        :param method: HTTP method (e.g., GET, POST, PUT, DELETE).
        :type method: str
        :param endpoint: Specific endpoint for the API request.
        :type endpoint: str
        :param params: Query parameters to be included in the request, defaults to None.
        :type params: dict, optional
        :param data: JSON data to be sent in the request body, defaults to None.
        :type data: dict, optional
        :return: The parsed JSON response from the server.
        :rtype: dict
        :raises HTTPError: If the request to the API is not successful.
        """
        url = f"{self._base_url}/{endpoint}/"

        # For django testing we need to use the django client
        if self._test_client:
            request_headers = {
                "HTTP_AUTHORIZATION": f"Token {self._token}",
            }

            if headers is not None:
                request_headers.update(headers)

            if method == "GET":
                response = self._test_client.get(
                    url, data=data, content_type="application/json", **request_headers
                )
            elif method == "POST":
                response = self._test_client.post(
                    url, data=data, content_type="application/json", **request_headers
                )
            elif method == "DELETE":
                response = self._test_client.delete(
                    url, data=data, content_type="application/json", **request_headers
                )
            elif method == "PUT":
                response = self._test_client.put(
                    url, data=data, content_type="application/json", **request_headers
                )
            elif method == "PATCH":
                response = self._test_client.patch(
                    url, data=data, content_type="application/json", **request_headers
                )

        else:
            request_headers = {
                "AUTHORIZATION": f"Token {self._token}",
            }

            response = requests.request(
                method, url, params=params, json=data, headers=request_headers
            )

        # Raise an exception if the status code is not 200 or 201
        if response.status_code != 200 and response.status_code != 201:
            self._handle_response_errors(response)

        return response.json()

    def get(self, endpoint: str, data: dict = None, params: dict = None) -> dict:
        """
        Make a GET request to the specified API endpoint.

        :param endpoint: Specific endpoint for the API request.
        :type endpoint: str
        :param params: Query parameters to be included in the GET request, defaults to None.
        :type params: dict, optional
        :return: The parsed JSON response from the server.
        :rtype: dict
        :raises HTTPError: If the GET request to the API is not successful.
        """
        return self._make_request("GET", endpoint, params=params, data=data)

    def post(self, endpoint: str, data: dict = None) -> dict:
        """
        Make a POST request to the specified API endpoint.

        :param endpoint: Specific endpoint for the API request.
        :type endpoint: str
        :param data: Data payload to be sent in the POST request, defaults to None.
        :type data: dict, optional
        :return: The parsed JSON response from the server.
        :rtype: dict
        :raises HTTPError: If the POST request to the API is not successful.
        """
        return self._make_request("POST", endpoint, data=data)

    def delete(self, endpoint: str, data: dict = None) -> dict:
        """
        Make a DELETE request to the specified API endpoint.

        :param endpoint: Specific endpoint for the API request.
        :type endpoint: str
        :param data: Data payload to be sent in the DELETE request, defaults to None.
        :type data: dict, optional
        :return: The parsed JSON response from the server.
        :rtype: dict
        :raises HTTPError: If the DELETE request to the API is not successful.
        """
        return self._make_request("DELETE", endpoint, data=data)

    def put(self, endpoint: str, data: dict = None, headers: dict = None) -> dict:
        """
        Make a PUT request to the specified API endpoint.

        :param endpoint: Specific endpoint for the API request.
        :type endpoint: str
        :param data: Data payload to be sent in the PUT request, defaults to None.
        :type data: dict, optional
        :return: The parsed JSON response from the server.
        :rtype: dict
        :raises HTTPError: If the PUT request to the API is not successful.
        """
        return self._make_request("PUT", endpoint, data=data, headers=headers)

    def patch(self, endpoint: str, data: dict = None) -> dict:
        """
        Make a PATCH request to the specified API endpoint.

        :param endpoint: Specific endpoint for the API request.
        :type endpoint: str
        :param data: Data payload to be sent in the PATCH request, defaults to None.
        :type data: dict, optional
        :return: The parsed JSON response from the server.
        :rtype: dict
        :raises HTTPError: If the PATCH request to the API is not successful.
        """
        return self._make_request("PATCH", endpoint, data=data)

    def list_projects(self):
        return self._project.list()

    def get_project(self, project_id: Union[str, uuid.UUID]):
        """Retrieves details for a specific project based on its uuid or pluto ID.

        Args:
            project_id (str or uuid): The pluto id or object uuid of the project to retrieve.

        Returns:
            Project Object: Project object.
        """
        return self._project.get(project_id=project_id)

    def list_experiments(self) -> Experiments:
        """Lists all projects.

        Returns:
            list: List of projects.
        """
        return self._experiment.list()

    def get_experiment(self, experiment_id: Union[str, uuid.UUID]) -> Experiment:
        """Retrieves details for a specific project based on its uuid or pluto ID.

        Args:
            experiment_id (str or uuid): The pluto id or object uuid of the experiment to retrieve.

        Returns:
            dict: Experiment details.
        """
        return self._experiment.get(experiment_id)

    def list_plots(self, experiment_id: Union[str, uuid.UUID]) -> Plots:
        """Retriveves a list for all plots inside an experiment

        Args:
            experiment_id (Union[str, uuid.UUID]): Pluto ID or Experiment UUID

        Returns:
            Plots: Returns a list of Plots
        """
        return self._plots.list(experiment_id)

    def get_plot(
        self, experiment_id: Union[str, uuid.UUID], plot_id: Union[str, uuid.UUID]
    ) -> Plot:
        """Retrieves a plot from an experiment

        Args:
            experiment_id (Union[str, uuid.UUID]): Experiment ID or UUID
            plot_id (Union[str, uuid.UUID]): Plot UUID

        Returns:
            Plot: Returns a plot object
        """
        return self._plots.get(experiment_id=experiment_id, plot_id=plot_id)

    def get_plot_data(
        self,
        experiment_id: Union[str, uuid.UUID],
        plot_id: Union[str, uuid.UUID],
        folder_path: str = DEFAULT_TMP_PATH,
    ) -> pd.DataFrame:
        """Get the data from a specific plot. It returns the data that was used to generate that plot

        Args:
            experiment_id (Union[str, uuid.UUID]): Experiment ID or UUID
            plot_id (Union[str, uuid.UUID]): Plot UUID

        Returns:
            pd.DataFrame: Plot data as a dataframe
        """

        return self._plots.data(
            experiment_id=experiment_id, plot_id=plot_id, folder_path=folder_path
        )

    def get_assay_data(
        self, experiment_id: Union[str, uuid.UUID], folder_path: str = DEFAULT_TMP_PATH
    ) -> pd.DataFrame:
        """Get the assay data from an experiment

        Args:
            experiment_id (Union[str, uuid.UUID]): Experiment ID or UUID
            folder_path (str, optional): Folder path to save the data. Defaults to /tmp.

        Returns:
            pd.DataFrame: Returns assay data as a pandas dataframe
        """
        return self._assay_data.get(experiment_id, folder_path=folder_path)

    def get_sample_data(
        self, experiment_id: Union[str, uuid.UUID], folder_path: str = DEFAULT_TMP_PATH
    ) -> pd.DataFrame:
        """Get the sample data from an experiment

        Args:
            experiment_id (Union[str, uuid.UUID]): Experiment ID or UUID
            folder_path (str, optional): Folder path to save the data. Defaults to /tmp.

        Returns:
            pd.DataFrame: Returns sample data as a pandas dataframe
        """
        return self._sample_data.get(experiment_id, folder_path=folder_path)

    def download_bam_files(
        self,
        experiment_id: Union[str, uuid.UUID],
        file_id: Union[str, uuid.UUID],
        folder_path: str = DEFAULT_TMP_PATH,
    ):
        """Download bam files from an experiment

        Args:
            experiment_id (Union[str, uuid.UUID]): Experiment ID or UUID
            file_id (Union[str, uuid.UUID]): BAM file UUID
            folder_path (str, optional): _description_. Defaults to DEFAULT_TMP_PATH.

        Returns:
            _type_: _description_
        """
        return self._pipelines.download_bam_files(
            experiment_id, file_id=file_id, folder_path=folder_path
        )

    def download_qc_report(
        self, experiment_id: Union[str, uuid.UUID], folder_path: str = DEFAULT_TMP_PATH
    ):
        return self._pipelines.download_qc_report(experiment_id, folder_path)

    def list_attachments(self, experiment_id: Union[str, uuid.UUID]):
        return self._attachment.list(experiment_id)

    def download_attachments(
        self,
        experiment_id: Union[str, uuid.UUID],
        file_id: Union[str, uuid.UUID],
        folder_path: str = DEFAULT_TMP_PATH,
    ):
        return self._attachment.download(
            experiment_id, file_id, folder_path=folder_path
        )

    def create_or_update_plot(
        self,
        experiment_id: Union[str, uuid.UUID],
        plot_uuid: Union[str, uuid.UUID] = None,
        methods_str_or_path: str = "",
        name: str = None,
        origin: str = "python",
        display_file_path: str = None,
        results_file_path: str = None,
        script_file_path: str = None,
    ):

        # We support the user to add methods as a string or as a file
        methods = utils.get_content(methods_str_or_path)

        # Prepare the request body
        request_data = {
            "analysis_type": "external",
            "display_type": "html",
            "status": "published",
            "origin": origin,
            "methods": methods,
        }

        # Add optional name if provided
        if name:
            request_data["name"] = name

        # Upload optional files and add their UUIDs to the request
        if display_file_path:
            display_file = self._download_upload.upload_file(
                experiment_id=experiment_id,
                file_path=display_file_path,
                data={
                    "analysis_type": "external",
                    "origin": origin,
                    "filename": os.path.basename(display_file_path),
                    "data_type": "external",
                    "file_type": os.path.splitext(display_file_path)[1],
                    "file_size": os.path.getsize(display_file_path),
                },
            )
            request_data["display_file_id"] = display_file["experiment_file"]["uuid"]

        if results_file_path:
            results_file = self._download_upload.upload_file(
                experiment_id=experiment_id,
                file_path=results_file_path,
                data={
                    "analysis_type": "external",
                    "origin": origin,
                    "filename": os.path.basename(results_file_path),
                    "data_type": "external",
                    "file_type": os.path.splitext(results_file_path)[1],
                    "file_size": os.path.getsize(results_file_path),
                },
            )
            request_data["results_file_id"] = results_file["experiment_file"]["uuid"]

        if script_file_path:
            script_file = self._download_upload.upload_file(
                experiment_id=experiment_id,
                file_path=script_file_path,
                data={
                    "analysis_type": "external",
                    "origin": origin,
                    "filename": os.path.basename(script_file_path),
                    "data_type": "external",
                    "file_type": os.path.splitext(script_file_path)[1],
                    "file_size": os.path.getsize(script_file_path),
                },
            )
            request_data["script_file_id"] = script_file["experiment_file"]["uuid"]

        # Handle plot creation or update
        if plot_uuid:
            # Update existing plot
            response = self._plots.update(
                experiment_id=experiment_id,
                plot_uuid=plot_uuid,
                data=request_data,
            )
        else:
            # Create a new plot
            response = self._plots.create(
                experiment_id=experiment_id,
                data=request_data,
            )

        return response

    def download_file(
        self, experiment_id: Union[str, uuid.UUID], file_id: Union[str, uuid.UUID]
    ):
        return self._download_upload.download_file(experiment_id, file_id)
