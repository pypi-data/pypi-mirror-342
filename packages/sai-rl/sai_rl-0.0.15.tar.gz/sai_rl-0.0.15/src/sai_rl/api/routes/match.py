from typing import Optional, TypedDict

from sai_rl.types import ModelLibraryType
from sai_rl.api.requestor import APIRequestor


class MatchType(TypedDict):
    id: str
    competition_id: str
    model_type: ModelLibraryType
    model_url: str
    action_function_url: str


class MatchAPI:
    def __init__(self, api: APIRequestor):
        self._api = api

    def get(self, match_id: str) -> Optional[MatchType]:
        response = self._api.get(f"/v1/submissions/{match_id}/benchmark")

        if not response:
            return None

        raw_match = response.json()
        if not raw_match:
            return None

        match: MatchType = {
            "id": raw_match.get("id"),
            "competition_id": raw_match.get("competitionId"),
            "model_type": raw_match.get("modelType"),
            "model_url": raw_match.get("modelUrl"),
            "action_function_url": raw_match.get("actionFunctionUrl"),
        }

        return match

    def submit_results(self, match_id: str, results: dict):
        response = self._api.post(f"/v1/submissions/{match_id}/benchmark", json=results)
        if not response:
            return None

        return response.json()
