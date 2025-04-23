from typing import TYPE_CHECKING
from .settings import DEFAULT_TMP_PATH
import os
import requests
from .log_handler import download_upload_logger
from . import api_endpoints
from typing import Union
import uuid
from . import utils
import time
import queue
import threading

if TYPE_CHECKING:
    from . import PlutoClient


class DownloadUploadHandler:
    """
    Manager class to handle upload and downloading data from pluto api.
    The manager does not interact directly with the cloud storage, rather it interacts with the pluto api to get a signed url.
    With the signed url it will then upload and download the data to that url
    """

    def __init__(self, client: "PlutoClient") -> None:
        self._client = client

    def _get_data_from_big_query(self, experiment_id, step, limit, result_queue):
        data = {"offset": step, "limit": limit}
        response = self._client.get(
            f"{api_endpoints.EXPERIMENTS}/{experiment_id}/assay-data", params=data
        )
        result_queue.put(response)

    def _download_from_gcs(
        self, download_url, dest_path, chunk_size=8 * 1024 * 1024, update_interval=5
    ):
        response = requests.get(download_url, stream=True)
        total_size = int(response.headers.get("Content-Length", 0))
        downloaded_size = 0
        is_user_updated = False

        # Ensure the directory exists
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

        with open(dest_path, "wb") as file:
            start_time = time.time()
            # chunk_size is 8 MiB (8*1024*1024) as recommended by gcs: https://cloud.google.com/storage/docs/performing-resumable-uploads
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                downloaded_size += len(data)
                current_time = time.time()

                if current_time - start_time >= update_interval:
                    is_user_updated = True
                    download_upload_logger.info(
                        f"Downloading file {round((downloaded_size / total_size) * 100)}%"
                    )
                    start_time = current_time

        if is_user_updated:
            download_upload_logger.info("Done 100%")

    def _download_from_big_query(self, experiment_id, file_path, count, step=0):
        data = {"filename": file_path}
        response = self._client.get(
            f"{api_endpoints.EXPERIMENTS}/{experiment_id}/assay-data/download",
            params=data,
        )
        count = response["count"]

        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Assuming this is the typical BigQuery download logic
        result_queue = queue.Queue()
        thread = threading.Thread(
            target=self._get_data_from_big_query,
            args=(
                experiment_id,
                step,
                count,
                result_queue,
            ),
        )
        thread.start()

        update_interval = 5  # Update progress every 5 seconds
        while thread.is_alive():
            download_upload_logger.info(
                "Our Zebrafish are going through the datalake to fetch your data. Please wait..."
            )
            time.sleep(update_interval)

        response = result_queue.get()
        download_upload_logger.info("Done")

        # You can further handle the response and process the data
        return response

    def upload_file(
        self,
        experiment_id: Union[str, uuid.UUID],
        data,
        file_path=DEFAULT_TMP_PATH,
    ):
        # TODO: Uncomment this out and test in prod to see if this actuall works.
        # md5_hash = utils.calculate_md5_base64(file_path)

        # response = self._client.get(
        #     f"lab/external/google-cloud/storage/blob/pluto-staging-user-content/{experiment_id}/analyses/external/{analysis_id}/{os.path.basename(file_path)}",
        # )

        # if md5_hash == response["md5_hash"]:
        #     download_upload_logger.debug(
        #         f"Identical file detected in the cloud. Skipping upload for {file_path}."
        #     )
        #     return {"message": "success"}

        response = self._client.post(
            f"{api_endpoints.EXPERIMENTS}/{experiment_id}/upload-sessions",
            data=data,
        )

        session_uri = response["session_url"]
        session_uuid = response["uuid"]
        experiment_file = response["file"]

        # Unfortunantely the GCS emulated does not support
        # querying the upload status. Which we achieve by setting the headers as:
        # headers = {"Content-Length": "0", "Content-Range": "bytes */*"}
        # For that reason we wrap this around so that we don't query initially and just
        # directly upload
        if not self._client._test_client:
            uploaded_range = ""
            headers = {"Content-Length": "0", "Content-Range": "bytes */*"}
            response = requests.put(session_uri, headers=headers)

            if 308 == response.status_code:
                if "Range" in response.headers:
                    # Range will be in the format "bytes=0-x"
                    uploaded_range = [
                        int(x)
                        for x in response.headers["Range"].split("=")[1].split("-")
                    ]
                else:
                    uploaded_range = [0, -1]

            if not uploaded_range:
                download_upload_logger.info("Could not determine uploaded range.")
                return

        else:
            uploaded_range = [0, -1]

        start_byte = uploaded_range[1] + 1
        with open(file_path, "rb") as f:
            f.seek(start_byte)
            file_data = f.read()

        total_size = os.path.getsize(file_path)
        headers = {
            "Content-Length": str(len(file_data)),
            "Content-Range": f"bytes {start_byte}-{total_size-1}/{total_size}",
        }

        response = requests.put(session_uri, headers=headers, data=file_data)

        # If successful, response should be 201 or 200
        if response.status_code in [200, 201]:
            download_upload_logger.info("Upload successful!")
            response = self._client.post(
                f"{api_endpoints.EXPERIMENTS}/{experiment_id}/upload-sessions/{session_uuid}/complete",
                data=data,
            )

        else:
            download_upload_logger.info(
                f"Upload failed with status code: {response.status_code}. Response: {response.text}"
            )

        response["experiment_file"] = experiment_file
        response["session_uuid"] = session_uuid
        return response

    def download_file(self, experiment_id, file_path, session_url=None):
        if session_url:
            return self._download_from_gcs(session_url, file_path)
        else:  # Assuming default is GCS
            return self._download_from_big_query(experiment_id, file_path)

    def get_signed_url(self, experiment_id, file_id):
        response = self._client.get(
            f"{api_endpoints.EXPERIMENTS}/{experiment_id}/files/{file_id}/download",
            params={"filename": {file_id}},
        )
        return response
