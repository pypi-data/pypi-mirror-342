from .settings import DEFAULT_TMP_PATH
from typing import TYPE_CHECKING
from . import utils
import time
import os
from .log_handler import download_upload_logger
import requests
from . import api_endpoints

# TODO: Need to add results and methods to the API

if TYPE_CHECKING:
    from . import PlutoClient


class Attachments(list):
    def __init__(self, client: "PlutoClient") -> None:
        super().__init__()  # Initialize the list
        self._client = client


class Attachment:
    def __init__(self, client: "PlutoClient") -> None:
        self._client = client
        self.data_type = "attachment"
        self.uuid = ""
        self.filename = ""
        self.display_name = ""

    def list(self, experiment_id: str):
        data = {"data_type": self.data_type}
        response = self._client.get(
            f"{api_endpoints.EXPERIMENTS}/{experiment_id}/files",
            data=data,
        )
        attachments = Attachments(self._client)
        for attachment in response["attachments"]["items"]:
            attachment_as_object = utils.to_class(Attachment(self._client), attachment)
            attachments.append(attachment_as_object)

        return attachments

    def get(self, experiment_id: str, file_id: str):
        response = self.list(experiment_id)
        for attachment in response:
            if attachment.uuid == file_id:
                return attachment
            else:
                raise Exception("Attachment not found")

    def download(
        self,
        experiment_id: str,
        file_id: str,
        folder_path=DEFAULT_TMP_PATH,
        is_cache=True,
    ):
        attachment = self.get(experiment_id, file_id)
        name = (
            attachment.display_name if attachment.display_name else attachment.filename
        )
        data = {"filename": name}
        attachment_download = self._client.get(
            f"{api_endpoints.EXPERIMENTS}/{experiment_id}/files/{file_id}/download",
            params=data,
        )

        self._client._download_upload.download_file(
            experiment_id,
            os.path.join(folder_path, name),
            attachment_download["url"],
        )
