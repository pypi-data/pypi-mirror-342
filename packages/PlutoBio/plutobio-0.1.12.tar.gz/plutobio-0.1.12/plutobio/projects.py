from typing import TYPE_CHECKING
from . import utils
from . import api_endpoints

if TYPE_CHECKING:
    from . import PlutoClient


class Projects(dict):
    def __init__(self, client: "PlutoClient") -> None:
        super().__init__()  # Initialize the dictionary
        self._client = client


class Project:
    def __init__(self, client: "PlutoClient") -> None:
        self._client = client
        self.pluto_id = ""
        self.name = ""

    def list(self):
        response = self._client.get(f"{api_endpoints.PROJECTS}")

        projects = Projects(self._client)
        for project in response["items"]:
            project_as_object = utils.to_class(Project(self._client), project)
            projects[project_as_object.pluto_id] = project_as_object

        return projects

    def get(self, project_id: str):
        response = self._client.get(f"{api_endpoints.PROJECTS}/{project_id}")
        return utils.to_class(Project(self._client), response)

    def __repr__(self) -> str:
        return f"{self.name}"
