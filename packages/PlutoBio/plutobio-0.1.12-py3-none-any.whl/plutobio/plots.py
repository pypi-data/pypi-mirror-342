import pandas as pd
from typing import TYPE_CHECKING, Union
from . import utils
from .settings import DEFAULT_TMP_PATH
from . import api_endpoints
import os

if TYPE_CHECKING:
    from . import PlutoClient


class Plots(list):
    def __init__(self, client: "PlutoClient") -> None:
        super().__init__()  # Initialize the list
        self._client = client


class Plot:
    def __init__(self, client: "PlutoClient") -> None:
        self._client = client

    def list(self, experiment_id: str):
        response = self._client.get(
            f"{api_endpoints.EXPERIMENTS}/{experiment_id}/plots"
        )

        plots = Plots(self._client)
        for plot in response["items"]:
            plot_as_object = utils.to_class(Plot(self._client), plot)
            plots.append(plot_as_object)

        return plots

    def get(self, experiment_id: str, plot_id: str):
        response = self._client.get(
            f"{api_endpoints.EXPERIMENTS}/{experiment_id}/plots/{plot_id}"
        )
        return utils.to_class(Plot(self._client), response)

    def data(
        self, experiment_id: str, plot_id: str, folder_path: str = DEFAULT_TMP_PATH
    ):
        file_path = os.path.join(folder_path, f"{plot_id}_plot_data.csv")

        response = self._client.get(
            f"{api_endpoints.EXPERIMENTS}/{experiment_id}/plots/{plot_id}/download",
            params={"filename": f"{plot_id}_plot_data.csv"},
        )

        if response["url"] is None:
            raise Exception("Plot does not have any data associated with it")

        self._client._download_upload.download_file(
            experiment_id=experiment_id,
            file_path=file_path,
            session_url=response["url"],
        )
        df = pd.read_csv(file_path)

        return df

    def update(self, experiment_id: str, plot_uuid: str, data):
        response = self._client.put(
            f"{api_endpoints.EXPERIMENTS}/{experiment_id}/external/plots/{plot_uuid}",
            data=data,
        )
        return response

    def create(self, experiment_id, data):
        response = self._client.post(
            f"{api_endpoints.EXPERIMENTS}/{experiment_id}/external/plots",
            data=data,
        )
        return utils.to_class(Plot(self._client), response)

    def add(
        self,
        experiment_id: str,
        plot_id: str = None,
        file_path: str = DEFAULT_TMP_PATH,
        plot_data: Union[pd.DataFrame, str] = None,
        methods: str = "",
    ):
        plot_uuid = ""
        analysis_uuid = ""
        if plot_id is not None:
            analysis_response = self.get(experiment_id, plot_id, raw=True)
            analysis_uuid = analysis_response["analysis"]["uuid"]
            plot_uuid = plot_id
        else:
            create_figure = self.create(
                experiment_id=experiment_id,
                data={
                    "analysis_type": "external",
                    "display_type": "html",
                    "status": "published",
                },
            )

            plot_uuid = create_figure.uuid

            analysis_data = {
                "analysis_type": "external",
                "name": f"{os.path.basename(file_path)}",
                "methods": methods,
            }

            if plot_data is not None:
                analysis_data["results"] = "plot_data.csv"

            create_analysis = self._client._analysis.create(
                experiment_id=experiment_id, data=analysis_data
            )

            analysis_uuid = create_analysis.uuid

        upload_response = self._client._download_upload.upload_file(
            experiment_id=experiment_id,
            file_path=file_path,
            data={
                "analysis_type": "external",
                "origin": "python",
                "filename": f"{analysis_uuid}/{os.path.basename(file_path)}",
                "data_type": "external",
                "file_type": os.path.splitext(os.path.basename(file_path))[1],
                "file_size": os.path.getsize(file_path),
            },
        )

        if plot_data is not None:
            if isinstance(plot_data, pd.DataFrame):
                temp_file_path = os.path.join(DEFAULT_TMP_PATH, "plot_data.csv")
                plot_data.to_csv(temp_file_path, index=False)

                upload_post_data_response = self._client._download_upload.upload_file(
                    experiment_id=experiment_id,
                    data={
                        "analysis_type": "external",
                        "origin": "python",
                        "filename": f"{analysis_uuid}/{os.path.basename(temp_file_path)}",
                        "data_type": "external",
                        "file_type": os.path.splitext(os.path.basename(temp_file_path))[
                            1
                        ],
                        "file_size": os.path.getsize(file_path),
                    },
                    file_path=temp_file_path,
                )

                os.remove(temp_file_path)
            else:
                upload_post_data_response = self._client._download_upload.upload_file(
                    experiment_id,
                    data={
                        "analysis_type": "external",
                        "origin": "python",
                        "filename": f"{analysis_uuid}/{os.path.basename(plot_data)}",
                        "data_type": "external",
                        "file_type": os.path.splitext(os.path.basename(plot_data))[1],
                        "file_size": os.path.getsize(file_path),
                    },
                    file_path=plot_data,
                )

        # TODO: We need to add a safe for the upload response. In case it fails, we need to be able to
        # remove the analysis that we created

        # TODO: We need to have a post validation after files are uploaded

        self.update(
            experiment_id=experiment_id,
            plot_uuid=plot_uuid,
            data={"analysis_id": analysis_uuid},
        )

        response = self._client._analysis.update(
            experiment_id=experiment_id,
            analysis_uuid=analysis_uuid,
            data={"methods": methods},
        )

        return response

    def get_signed_url(self, experiment_id, plot_id):
        response = self._client.get(
            f"{api_endpoints.EXPERIMENTS}/{experiment_id}/plots/{plot_id}/data",
        )
        return response["url"]

    def link_analysis(self, experiment_id, plot_id, analysis_id, display_id):
        response = self._client.post(
            f"{api_endpoints.EXPERIMENTS}/{experiment_id}/plots/{plot_id}/link-analysis",
            data={
                "analysis_id": analysis_id,
                "display_id": display_id,
            },
        )
        return response


class Displays(list):
    def __init__(self, client: "PlutoClient") -> None:
        super().__init__()  # Initialize the list
        self._client = client


class Display:
    def __init__(self, client: "PlutoClient") -> None:
        self._client = client

    def list(self, experiment_id: str, plot_uuid: str):
        response = self._client.get(
            f"{api_endpoints.EXPERIMENTS}/{experiment_id}/plots/{plot_uuid}/displays"
        )

        displays = Displays(self._client)
        for display in response["items"]:
            display_as_object = utils.to_class(Plot(self._client), display)
            displays.append(display_as_object)

        return displays

    def get(self, experiment_id: str, plot_uuid: str):
        response = self._client.get(
            f"{api_endpoints.EXPERIMENTS}/{experiment_id}/plots/{plot_uuid}/displays"
        )
        return utils.to_class(Plot(self._client), response)

    def create(self, experiment_id, data):
        response = self._client.post(
            f"{api_endpoints.EXPERIMENTS}/{experiment_id}/plots", data=data
        )
        return utils.to_class(Plot(self._client), response)

    def update(self, experiment_id, plot_uuid, display_uuid, data):
        response = self._client.put(
            f"{api_endpoints.EXPERIMENTS}/{experiment_id}/plots/{plot_uuid}/displays/{display_uuid}",
            data=data,
        )
        return utils.to_class(Plot(self._client), response)
