from .settings import (
    DATA_ANALYSIS_OPTIONS_ENUM,
    DATA_ANALYSIS_OPTIONS,
    DEFAULT_TMP_PATH,
)
import pandas as pd
from typing import TYPE_CHECKING
import math
import os
from .log_handler import download_upload_logger
import time
from . import api_endpoints
import queue
import threading

if TYPE_CHECKING:
    from . import PlutoClient


class SampleData:
    def __init__(self, client: "PlutoClient") -> None:
        self._client = client

    def get(self, experiment_id, folder_path=DEFAULT_TMP_PATH, is_cache=True):
        response = self._client.get(
            f"{api_endpoints.EXPERIMENTS}/{experiment_id}/sample-data"
        )

        if (
            os.path.exists(
                os.path.join(folder_path, f"{experiment_id}_sample_data.csv")
            )
            and is_cache
        ):
            df = pd.read_csv(
                os.path.join(folder_path, f"{experiment_id}_sample_data.csv")
            )
            return df

        count = response["count"]
        step = 0

        response = self._client.get(
            f"{api_endpoints.EXPERIMENTS}/{experiment_id}/sample-data/download"
        )

        self._client._download_upload.download_file(
            experiment_id,
            os.path.join(folder_path, f"{experiment_id}_sample_data.csv"),
            response["url"],
        )

        df = pd.read_csv(os.path.join(folder_path, f"{experiment_id}_sample_data.csv"))

        return df
