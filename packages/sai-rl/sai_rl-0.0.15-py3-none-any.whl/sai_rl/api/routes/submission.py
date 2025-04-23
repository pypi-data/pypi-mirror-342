from typing import Optional, TypedDict, List

from sai_rl.utils import config
from sai_rl.api.requestor import APIRequestor


class SubmissionListType(TypedDict):
    id: str
    name: str
    model_type: str
    status: str
    last_score: str
    competition_name: str
    environment_name: str
    link: str


class SubmissionCreateType(TypedDict):
    submission: SubmissionListType
    upload_url: str


class SubmissionRunType(TypedDict):
    id: str
    status: str


class SubmissionAPI:
    def __init__(self, api: APIRequestor):
        self._api = api

    def list(self) -> Optional[List[SubmissionListType]]:
        response = self._api.get("/v1/submissions")

        if not response:
            return None

        raw_submissions = response.json()
        if not raw_submissions:
            return None

        submissions: List[SubmissionListType] = []

        for raw_submission in raw_submissions:
            submission: SubmissionListType = {
                "id": raw_submission.get("id"),
                "name": raw_submission.get("name"),
                "model_type": raw_submission.get("type"),
                "environment_name": raw_submission.get("environmentName"),
                "competition_name": raw_submission.get("competitionName"),
                "status": raw_submission.get("status"),
                "last_score": (
                    f"{raw_submission.get('lastScore'):.4f}"
                    if raw_submission.get("lastScore") is not None
                    else ""
                ),
                "link": (
                    f"{config.platform_url}/submissions/{raw_submission.get('id')}"
                    if raw_submission.get("status") == "completed"
                    else ""
                ),
            }

            submissions.append(submission)

        return submissions

    def create(self, data: dict) -> Optional[SubmissionCreateType]:
        response = self._api.post("/v1/submissions", json=data)

        if not response:
            return None

        raw_submission = response.json()

        submission: SubmissionCreateType = {
            "submission": raw_submission.get("submission"),
            "upload_url": raw_submission.get("uploadUrl"),
        }

        return submission

    def run(self, submission_id: str) -> Optional[SubmissionRunType]:
        response = self._api.get(f"/v1/submissions/{submission_id}/run")

        if not response:
            return None

        raw_submission = response.json()

        submission: SubmissionRunType = {
            "id": raw_submission.get("id"),
            "status": raw_submission.get("status"),
        }

        return submission
