from typing import Optional, TypedDict, List

from sai_rl.utils import config
from sai_rl.api.requestor import APIRequestor


class EnvironmentType(TypedDict):
    id: str
    name: str
    env_name: str
    env_library: str
    link: str


class EnvironmentListType(TypedDict):
    id: str
    name: str
    description: str
    env_name: str
    env_library: str
    link: str


class EnvironmentAPI:
    def __init__(self, api: APIRequestor):
        self._api = api

    def get(self, environment_id: str) -> Optional[EnvironmentType]:
        response = self._api.get(f"/v1/environments/{environment_id}")

        if not response:
            return None

        raw_environment = response.json()
        if not raw_environment:
            return None

        environment: EnvironmentType = {
            "id": raw_environment.get("id"),
            "name": raw_environment.get("name"),
            "env_name": raw_environment.get("gymnasiumEnv"),
            "env_library": raw_environment.get("package").get("name"),
            "link": f"{config.platform_url}/environments/{raw_environment.get('slug')}",
        }

        return environment

    def list(self) -> Optional[List[EnvironmentListType]]:
        response = self._api.get("/v1/environments")

        if not response:
            return None

        raw_environments = response.json()
        if not raw_environments:
            return None

        environments: List[EnvironmentListType] = []

        for raw_environment in raw_environments:
            environment: EnvironmentListType = {
                "id": raw_environment.get("id"),
                "name": raw_environment.get("name"),
                "description": raw_environment.get("description"),
                "env_name": raw_environment.get("gymnasiumEnv"),
                "env_library": raw_environment.get("package").get("name"),
                "link": f"{config.platform_url}/environments/{raw_environment.get('slug')}",
            }

            environments.append(environment)

        return environments
