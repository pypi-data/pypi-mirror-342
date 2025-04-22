"""DBT Cloud mixin for dapi_validator"""

# pylint: disable=too-few-public-methods, too-many-locals

from __future__ import annotations

import json
import os
import threading
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Set
from urllib.parse import urljoin

import requests

from opendapi.cli.common import print_cli_output
from opendapi.defs import CommitType
from opendapi.logging import logger
from opendapi.utils import (
    HTTPMethod,
    create_session_with_retries,
    make_api_w_query_and_body,
)

DBT_CLOUD_RUN_STATUSES = {
    "queued": 1,
    "starting": 2,
    "running": 3,
    "success": 10,  # means the job has completed
    "error": 20,
    "cancelled": 30,
}
OPENDAPI_DBT_CLOUD_JOB_NAME = "opendapi_ci_fast_generate_docs"

_thread_local = threading.local()


def _get_session() -> requests.Session:  # pragma: no cover
    if not hasattr(_thread_local, "session"):
        _thread_local.session = create_session_with_retries(
            total_retries=2,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["POST", "GET"],
        )
    return _thread_local.session


@dataclass
class DBTCloudProject:
    """DBT Cloud project"""

    project_id: int
    account_id: int
    repo_name: str
    ci_job_id: int
    opendapi_project_info: "DBTProjectInfo"
    subdirectory: str
    prod_docs_job_id: Optional[int] = None
    processed = False

    @staticmethod
    def build_run_html_url(run: Dict) -> str:
        """Build the HTML URL for a run"""
        return urljoin(
            os.environ["DAPI_DBT_CLOUD_URL"],
            f"/deploy/{run['account_id']}"
            f"/projects/{run['project_id']}/runs/{run['id']}",
        )

    def get_custom_schema(
        self, github_pr_number: Optional[int], commit_type: CommitType
    ) -> str:
        """Get the custom schema"""
        if github_pr_number:
            # not including commit_sha in hopes that it will be reused
            # NOTE: for PRs any schema that has prefix `dbt_cloud_pr_JOB_ID_PR_NUMBER`
            #       will be cleaned up by dbt cloud once the PR is closed.
            return (
                f"dbt_cloud_pr_{self.ci_job_id}_{github_pr_number}_{commit_type.value}"
            )

        # update this when we are able to run for main branch
        raise RuntimeError("PR number not supplied for CI job")  # pragma: no cover

    @staticmethod
    def dbt_cloud_request(
        uri_path: str,
        http_method: HTTPMethod = HTTPMethod.GET,
        body: Optional[Dict] = None,
        params: Optional[Dict] = None,
        content_type: str = "application/json",
    ) -> requests.Response:
        """Make a request to the DBT Cloud API"""
        headers = {
            "Content-Type": content_type,
            "Authorization": f"Token {os.environ['DAPI_DBT_CLOUD_API_TOKEN']}",
        }

        response, _ = make_api_w_query_and_body(
            url=urljoin(os.environ["DAPI_DBT_CLOUD_URL"], uri_path),
            headers=headers,
            body_json=body,
            query_params=params,
            method=http_method,
            timeout=10,
            req_session=_get_session(),
        )

        response.raise_for_status()
        return response

    @staticmethod
    def _validate_json_response(response: requests.Response) -> None:
        response = response.json()
        if response["status"]["code"] != 200 or not response["status"]["is_success"]:
            logger.error("DBT Cloud API request failed: %s", response)
            raise RuntimeError("DBT Cloud API request failed")

    @classmethod
    def dbt_cloud_api_request(
        cls,
        uri_path: str,
        http_method: HTTPMethod = HTTPMethod.GET,
        body: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> Dict:
        """Make a request to the DBT Cloud API"""
        response = cls.dbt_cloud_request(uri_path, http_method, body, params)
        cls._validate_json_response(response)
        return response.json()["data"]

    @classmethod
    def get_opendapi_job_id(
        cls,
        account_id: int,
        project_id: int,
    ) -> int:
        """Get the opendapi job id for a given dbt cloud project and commit sha"""
        base_url = f"/api/v2/accounts/{account_id}/jobs"
        params = {
            "project_id": project_id,
            "state": 1,
            "name__icontains": OPENDAPI_DBT_CLOUD_JOB_NAME,
            # allow for a few that have the job name as a substring, even though
            # that is really an anti-pattern
            "limit": 5,
        }
        response = cls.dbt_cloud_api_request(base_url, params=params)
        try:
            return next(
                (
                    job["id"]
                    for job in response
                    if job["name"] == OPENDAPI_DBT_CLOUD_JOB_NAME
                ),
            )
        except StopIteration as e:
            raise RuntimeError(
                f"No opendapi job found for the given project {project_id}"
            ) from e

    def get_latest_run(
        self,
        statuses: Set[int] = frozenset({DBT_CLOUD_RUN_STATUSES["success"]}),
        match_git_sha: Optional[str] = None,
        job_id: Optional[int] = None,
        ci_only: bool = True,
        allowed_runs_without_has_docs_generated: Set[int] = frozenset(),
    ) -> Optional[Dict]:
        """Get latest run of dbt Cloud for a given project, optionally matching git sha or job ID"""
        base_url = f"/api/v2/accounts/{self.account_id}/runs"
        params = {
            "project_id": self.project_id,
            "status__in": str(list(statuses)),
            # to be used later to filter by PR number
            "include_related": str(["trigger", "job"]),
            "order_by": "-created_at",
            "limit": 100,
            "offset": 0,
        }
        if job_id:
            params["job_definition_id"] = job_id

        match_run = None
        for idx in range(os.environ.get("DAPI_DBT_CLOUD_MAX_ITERATIONS", 20)):
            params["offset"] = idx * params["limit"]
            runs = self.dbt_cloud_api_request(base_url, params=params)
            match_run = next(
                (
                    r
                    for r in runs
                    if (
                        # NOTE: there are diff artifacts depending on how it was triggered,
                        #       and rn we can only handle CI, so skip others, unless
                        #       intended by knowing job_id
                        (not ci_only or r["job"]["job_type"] == "ci")
                        and (
                            r.get("has_docs_generated")
                            or r["id"] in allowed_runs_without_has_docs_generated
                        )
                        and ((r["git_sha"] == match_git_sha) or not match_git_sha)
                    )
                ),
                None,
            )
            if match_run or not runs:
                # End early if no more runs found
                break
        return match_run

    @staticmethod
    def _write_artifact(artifact_path: str, content: str) -> None:
        """Write the artifact to the file system"""
        os.makedirs(os.path.dirname(artifact_path), exist_ok=True)
        with open(artifact_path, "w", encoding="utf-8") as fp:
            fp.write(content)

    def download_artifact(
        self, artifact_name: str, run_id: int, download_path: str
    ) -> str:
        """Download the artifact from dbt cloud"""
        base_url = f"/api/v2/accounts/{self.account_id}/runs"
        artifacts_url = f"{base_url}/{run_id}/artifacts/"
        artifact_url = f"{artifacts_url}{artifact_name}"
        content = self.dbt_cloud_request(
            artifact_url, content_type="application/text"
        ).text

        if os.path.exists(download_path):
            print_cli_output(
                f"Artifact exists. Overwriting: {download_path}", color="yellow"
            )

        print_cli_output(f"Downloading artifact {artifact_name} to {download_path}")
        self._write_artifact(download_path, content)

        return download_path

    def merge_catalogs(self) -> str:
        """Merge the catalogs"""
        with open(
            self.opendapi_project_info.production_catalog_path, "r", encoding="utf-8"
        ) as fp:
            base_catalog = json.load(fp)

        with open(self.opendapi_project_info.catalog_path, "r", encoding="utf-8") as fp:
            merging_catalog = json.load(fp)

        merged_catalog = base_catalog.copy()

        # Overwrite models that exist in both catalogs - merging catalog takes precedence
        for model in merged_catalog["nodes"]:
            if model in merging_catalog["nodes"]:
                merged_catalog["nodes"][model] = merging_catalog["nodes"][model]

        # Add models that exist in merging catalog but not in base catalog
        for model in merging_catalog["nodes"]:
            if model not in merged_catalog["nodes"]:
                merged_catalog["nodes"][model] = merging_catalog["nodes"][model]

        os.makedirs(
            os.path.dirname(self.opendapi_project_info.catalog_path), exist_ok=True
        )
        with open(self.opendapi_project_info.catalog_path, "w", encoding="utf-8") as fp:
            json.dump(merged_catalog, fp)
        return self.opendapi_project_info.catalog_path

    def _trigger_opendapi_job(
        self,
        github_pr_number: Optional[int],
        branch_name: Optional[str],
        commit_type: CommitType,
    ) -> Dict:
        """Trigger the opendapi job"""
        base_url = f"/api/v2/accounts/{self.account_id}/jobs/{self.ci_job_id}/run"

        # for now we only do this for PRs
        if github_pr_number is None or branch_name is None:
            raise RuntimeError("PR number or branch name not supplied for CI job")

        body = {
            "cause": "opendapi_ci_initiated",
            # We will explicitly generate docs in a command for modified models
            "generate_docs_override": False,
            # Modified/New models and their downstream models
            "steps_override": [
                # NOTE: We are excluding tests, snapshot, unit_tests, analysis, saved_query
                # but they still come through in the manifest
                # one build command is better than multiple to avoid parsing/compiling costs
                "dbt build --select state:modified+ --empty "
                "--exclude-resource-type test snapshot unit_test analysis",
                # We will generate only for modified
                # because we will merge with production catalog
                "dbt docs generate --select state:modified+",
            ],
            # NOTE: We do NOT want this to set a commit status.
            #       But, if we pass in the PR number and the commit sha the
            #       commit status gets set. Instead, if only pass in the git sha,
            #       no commit status is set, but then we want to ensure that
            #       the schema is still associated with the PR, and so we do this by
            #       setting the `schema_override` to the pattern that dbt cloud
            #       checks for when cleaning up PR presence.
            "git_branch": branch_name,
            "github_pull_request_id": github_pr_number,
            "schema_override": self.get_custom_schema(github_pr_number, commit_type),
        }
        triggered_run = self.dbt_cloud_api_request(
            base_url, http_method=HTTPMethod.POST, body=body
        )
        print_cli_output(f"Triggered run at: {self.build_run_html_url(triggered_run)}")
        return triggered_run

    def ensure_opendapi_job_initiated(
        self,
        github_pr_number: Optional[int],
        branch_name: Optional[str],
        commit_sha: str,
        commit_type: CommitType,
    ) -> Dict:
        """Ensure the opendapi job is initiated"""
        print_cli_output(
            f"Checking if there is an ongoing run for job {self.ci_job_id} for project "
            f"{self.project_id} and commit sha {commit_sha}."
        )
        run = self.get_latest_run(
            statuses={
                DBT_CLOUD_RUN_STATUSES["queued"],
                DBT_CLOUD_RUN_STATUSES["starting"],
                DBT_CLOUD_RUN_STATUSES["running"],
                DBT_CLOUD_RUN_STATUSES["success"],
            },
            job_id=self.ci_job_id,
            match_git_sha=commit_sha,
        )
        if run:
            print_cli_output(
                f"Found an ongoing run for job {self.ci_job_id} for project "
                f"{self.project_id} and commit sha {commit_sha}. We will wait for it "
                "to complete."
            )
            print_cli_output(f"Run URL: {self.build_run_html_url(run)}")
            return run

        print_cli_output(
            f"No ongoing run found. We will trigger a new run for job {self.ci_job_id} "
            f"for project {self.project_id} and commit sha {commit_sha}."
        )
        print_cli_output("Triggering opendapi job")
        return self._trigger_opendapi_job(github_pr_number, branch_name, commit_type)

    @classmethod
    def get_dbt_cloud_projects(
        cls,
        opendapi_project_infos: List["DBTProjectInfo"],
    ) -> List[DBTCloudProject]:
        """Get the dbt cloud projects"""
        dbt_cloud_projects = []
        accounts = cls.dbt_cloud_api_request("/api/v2/accounts/")
        current_repo_name = os.environ["GITHUB_REPOSITORY"]

        for account in accounts:
            projects = cls.dbt_cloud_api_request(
                f"/api/v2/accounts/{account['id']}/projects/"
            )

            for project in projects:
                repo_name = project["repository"]["full_name"]
                repo_subdirectory = project.get("dbt_project_subdirectory") or ""
                prod_docs_job_id = project.get("docs_job_id")

                if repo_name != current_repo_name:
                    continue

                opendapi_project_infos = [
                    opendapi_project_info
                    for opendapi_project_info in opendapi_project_infos
                    if opendapi_project_info.full_path.endswith(repo_subdirectory)
                ]

                if not opendapi_project_infos:
                    raise RuntimeError(
                        f"No opendapi project infos found for project {project['id']}"
                    )

                if len(opendapi_project_infos) > 1:  # pragma: no cover
                    raise RuntimeError(
                        f"Multiple opendapi project infos found for project {project['id']}"
                    )

                dbt_cloud_projects.append(
                    DBTCloudProject(
                        project_id=project["id"],
                        account_id=account["id"],
                        repo_name=repo_name,
                        ci_job_id=cls.get_opendapi_job_id(account["id"], project["id"]),
                        opendapi_project_info=opendapi_project_infos[0],
                        subdirectory=repo_subdirectory,
                        prod_docs_job_id=prod_docs_job_id,
                    )
                )

        return dbt_cloud_projects


class DBTCloudMixin:
    """
    A mixin plugin used for adding dbt_cloud support to DBT DAPI validator.
    This plugin helps with downloading the dbt models from dbt cloud.
    """

    _dbt_commit_sha: Optional[str]
    _github_pr_number: Optional[int]
    _branch_name: Optional[str]

    @staticmethod
    def _sync_dbt_cloud_artifacts(
        dbt_cloud_projects: List[DBTCloudProject],
        commit_sha: str,
        triggered_runs_by_project: Dict[int, Dict],
    ) -> bool:
        """Sync the dbt projects from dbt cloud"""

        for dbt_cp in dbt_cloud_projects:
            # if there is nothing to do, skip
            if dbt_cp.processed:  # pragma: no cover
                continue

            triggered_run_id = (
                triggered_runs_by_project.get(dbt_cp.project_id, {})
            ).get("id")
            match_run = dbt_cp.get_latest_run(
                match_git_sha=commit_sha,
                # We might have triggered runs that did not generate docs natively
                # but generated explicitly with deferral
                allowed_runs_without_has_docs_generated=(
                    {triggered_run_id} if triggered_run_id else set()
                ),
            )
            if not match_run:
                continue

            opendapi_project_info = dbt_cp.opendapi_project_info
            # Download manifest
            dbt_cp.download_artifact(
                opendapi_project_info.manifest_filename,
                match_run["id"],
                opendapi_project_info.manifest_path,
            )

            # Download catalog
            dbt_cp.download_artifact(
                opendapi_project_info.catalog_filename,
                match_run["id"],
                opendapi_project_info.catalog_path,
            )

            # Download production catalog
            if dbt_cp.prod_docs_job_id:
                production_docs_run = dbt_cp.get_latest_run(
                    job_id=dbt_cp.prod_docs_job_id,
                    ci_only=False,
                )
                if production_docs_run:
                    dbt_cp.download_artifact(
                        opendapi_project_info.catalog_filename,
                        production_docs_run["id"],
                        opendapi_project_info.production_catalog_path,
                    )

                    # Merge the PR catalog on top of the production catalog
                    dbt_cp.merge_catalogs()

            dbt_cp.processed = True

        return all(dbt_cp.processed for dbt_cp in dbt_cloud_projects)

    @staticmethod
    def _cleanup_dbt_cloud_file_state(projects: Dict[str, "DBTProjectInfo"]) -> None:
        """Cleanup the dbt cloud file state"""
        for project in projects:
            for filepath in (
                project.manifest_path,
                project.catalog_path,
                project.production_catalog_path,
            ):
                if os.path.exists(filepath):
                    os.remove(filepath)

    def sync_dbt_cloud_artifacts(self, projects: Dict[str, "DBTProject"]) -> bool:
        """Sync the dbt projects from dbt cloud with a retry"""

        if not os.environ.get("DAPI_DBT_CLOUD_API_TOKEN") or not os.environ.get(
            "DAPI_DBT_CLOUD_URL"
        ):
            logger.info("DBT Cloud API token or URL not found")
            return False

        if not self._dbt_commit_sha or not os.environ.get("GITHUB_REPOSITORY"):
            logger.info("GITHUB_HEAD_SHA or GITHUB_REPOSITORY not found")
            return False

        dbt_cloud_projects = DBTCloudProject.get_dbt_cloud_projects(projects)

        # we first check if there are already artifacts
        print_cli_output("Checking if artifacts exist")
        if self._sync_dbt_cloud_artifacts(dbt_cloud_projects, self._dbt_commit_sha, {}):
            print_cli_output("Found artifacts")
            return True

        # if there were no artifacts found,
        # we check if we need to trigger a new run, or if there are some already running
        print_cli_output(
            f"No artifacts found. Ensuring that there is a run for "
            f"{OPENDAPI_DBT_CLOUD_JOB_NAME} for projects "
            f"{', '.join([str(dbt_cp.project_id) for dbt_cp in dbt_cloud_projects])}"
        )
        # NOTE: for now we are only doing head commit - fast follow with base
        runs_by_project = {}
        for dbt_cp in dbt_cloud_projects:
            runs_by_project[dbt_cp.project_id] = dbt_cp.ensure_opendapi_job_initiated(
                self._github_pr_number,
                self._branch_name,
                self._dbt_commit_sha,
                CommitType.HEAD,
            )

        print_cli_output("Done. Beginning to wait for artifacts.")

        # now that we have at least one run in the works,
        # we can keep retrying for a bit till we get the artifacts,
        # retrying for a bit till we get the artifacts
        # By default, we will retry every 30 seconds for 10 minutes

        retry_count = int(os.environ.get("DAPI_DBT_CLOUD_RETRY_COUNT") or 40)
        retry_count = 0 if retry_count < 0 else retry_count
        retry_wait_secs = int(os.environ.get("DAPI_DBT_CLOUD_RETRY_INTERVAL") or 30)
        total_wait_time = retry_count * retry_wait_secs

        while retry_count >= 0:
            print_cli_output("Attempting to sync dbt cloud artifacts")

            if self._sync_dbt_cloud_artifacts(
                dbt_cloud_projects, self._dbt_commit_sha, runs_by_project
            ):
                return True

            print_cli_output("Couldn't find any artifacts")
            if retry_count > 0:
                print_cli_output(f"Retrying {retry_count} more time(s)")
                time.sleep(retry_wait_secs)

            retry_count -= 1

        print_cli_output(
            f"{'>' * 30}\n"
            f"Waited for {total_wait_time} seconds. "
            "However, some of these following runs did not complete successfully. "
            "Rerun this workflow when all the runs eventually succeed."
        )
        for project_id, run in runs_by_project.items():
            print_cli_output(
                f"Project ID: {project_id}, Run URL: {DBTCloudProject.build_run_html_url(run)}"
            )
        return False
