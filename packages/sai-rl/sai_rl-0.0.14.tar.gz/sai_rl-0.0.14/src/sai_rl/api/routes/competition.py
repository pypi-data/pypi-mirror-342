from typing import Any, Mapping, Optional, TypedDict, List

from sai_rl.utils import config
from sai_rl.api.requestor import APIRequestor


class CompetitionType(TypedDict):
    id: str
    slug: str
    name: str
    env_name: str
    env_lib: str
    env_vars: Mapping[str, Any]
    link: str


class CompetitionListType(TypedDict):
    id: str
    slug: str
    name: str
    description: str
    environment_name: str
    link: str


class CompetitionAPI:
    def __init__(self, api: APIRequestor):
        self._api = api

    def get(self, competition_id: str) -> Optional[CompetitionType]:
        response = self._api.get(f"/v1/competitions/{competition_id}/benchmark")

        if not response:
            return None

        raw_competition = response.json()
        if not raw_competition:
            return None

        competition: CompetitionType = {
            "id": raw_competition.get("id"),
            "slug": raw_competition.get("slug"),
            "name": raw_competition.get("name"),
            "env_name": raw_competition.get("envName"),
            "env_lib": raw_competition.get("envLib"),
            "env_vars": raw_competition.get("envVars"),
            "link": f"{config.platform_url}/competitions/{raw_competition.get('slug')}",
        }

        return competition

    def list(self) -> Optional[List[CompetitionListType]]:
        response = self._api.get("/v1/competitions")

        if not response:
            return None

        raw_competitions = response.json()
        if not raw_competitions:
            return None

        competitions: List[CompetitionListType] = []

        for raw_competition in raw_competitions:
            competition: CompetitionListType = {
                "id": raw_competition.get("id"),
                "slug": raw_competition.get("slug"),
                "name": raw_competition.get("name"),
                "description": raw_competition.get("description"),
                "environment_name": raw_competition.get("environmentName"),
                "link": f"{config.platform_url}/competitions/{raw_competition.get('id')}",
            }

            competitions.append(competition)

        return competitions
