from typing import Optional, TypedDict, List

from sai_rl.api.requestor import APIRequestor


class ActionFunctionType(TypedDict):
    id: str
    name: str
    compatible_types: List[str]
    download_url: str


class ActionFunctionListType(TypedDict):
    id: str
    name: str
    compatible_types: List[str]


class ActionFunctionSubmitResponseType(TypedDict):
    action_function: ActionFunctionType
    upload_url: str


class ActionFunctionAPI:
    def __init__(self, api: APIRequestor):
        self._api = api

    def get(self, action_function_id: str) -> Optional[ActionFunctionType]:
        response = self._api.get(f"/v1/action-functions/{action_function_id}")

        if not response:
            return None

        raw_action_function = response.json()
        if not raw_action_function:
            return None

        action_function: ActionFunctionType = {
            "id": raw_action_function.get("id"),
            "name": raw_action_function.get("name"),
            "compatible_types": raw_action_function.get("compatibleTypes"),
            "download_url": raw_action_function.get("downloadUrl"),
        }

        return action_function

    def list(self) -> Optional[List[ActionFunctionListType]]:
        response = self._api.get("/v1/action-functions")

        if not response:
            return None

        raw_action_functions = response.json()
        if not raw_action_functions:
            return None

        action_functions: List[ActionFunctionListType] = []

        for raw_action_function in raw_action_functions:
            action_function: ActionFunctionListType = {
                "id": raw_action_function.get("id"),
                "name": raw_action_function.get("name"),
                "compatible_types": raw_action_function.get("compatibleTypes"),
            }

            action_functions.append(action_function)

        return action_functions

    def submit(
        self, name: str, compatible_types: List[str]
    ) -> Optional[ActionFunctionSubmitResponseType]:
        response = self._api.post(
            "/v1/action-functions",
            json={
                "name": name,
                "compatibleTypes": compatible_types,
            },
            params={"getDownloadUrl": "true"},
        )

        if not response:
            return None

        data = response.json()
        if not data:
            return None

        result: ActionFunctionSubmitResponseType = {
            "action_function": {
                "id": data.get("id"),
                "name": data.get("name"),
                "compatible_types": data.get("compatibleTypes"),
                "download_url": data.get("downloadUrl"),
            },
            "upload_url": data.get("uploadUrl"),
        }

        return result
