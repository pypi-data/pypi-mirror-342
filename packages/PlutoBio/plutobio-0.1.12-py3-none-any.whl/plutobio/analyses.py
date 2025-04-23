from . import api_endpoints

from . import utils


class Analysis:
    def __init__(self, client) -> None:
        self._client = client

    def list(self, experiment_id):
        return self.client.get(f"{api_endpoints.EXPERIMENTS}/{experiment_id}/plots")

    def get(self, experiment_id, analysis_uuid):
        response = self._client.get(
            f"{api_endpoints.EXPERIMENTS}/{experiment_id}/analyses/{analysis_uuid}"
        )
        return utils.to_class(Analysis(self._client), response)

    def create(self, experiment_id, data):
        response = self._client.post(
            f"{api_endpoints.EXPERIMENTS}/{experiment_id}/analyses",
            data=data,
        )

        return utils.to_class(Analysis(self._client), response)

    def update(self, experiment_id, analysis_uuid, data):
        response = self._client.put(
            f"{api_endpoints.EXPERIMENTS}/{experiment_id}/analyses/{analysis_uuid}",
            data=data,
        )
        return response

    def delete(self):
        pass
