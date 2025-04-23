from .settings import (
    DEFAULT_TMP_PATH,
)
import pandas as pd
from typing import TYPE_CHECKING
import os
from . import api_endpoints

if TYPE_CHECKING:  # pragma: no cover
    from . import PlutoClient


class AssayData:
    def __init__(self, client: "PlutoClient") -> None:
        self._client = client

    def get(self, experiment_id, is_cache=True, folder_path=DEFAULT_TMP_PATH):
        # TODO: Allow Caching
        # TODO: Implement Download Assay_Data
        # TODO: Load Assay_Data

        response = self._client.get(
            f"{api_endpoints.EXPERIMENTS}/{experiment_id}/assay-data"
        )

        if (
            os.path.exists(os.path.join(folder_path, f"{experiment_id}_assay_data.csv"))
            and is_cache
        ):
            df = pd.read_csv(
                os.path.join(folder_path, f"{experiment_id}_assay_data.csv")
            )
            return df

        count = response["count"]
        step = 0

        response = self._client.get(
            f"{api_endpoints.EXPERIMENTS}/{experiment_id}/assay-data/download"
        )

        self._client._download_upload.download_file(
            experiment_id,
            os.path.join(folder_path, f"{experiment_id}_assay_data.csv"),
            response["url"],
        )

        df = pd.read_csv(os.path.join(folder_path, f"{experiment_id}_assay_data.csv"))

        return df
