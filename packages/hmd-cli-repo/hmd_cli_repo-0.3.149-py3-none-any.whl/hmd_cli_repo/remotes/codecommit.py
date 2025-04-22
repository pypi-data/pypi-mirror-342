import os
from typing import Dict, List

from cement import App
from git import Repo
from hmd_cli_tools.hmd_cli_tools import get_session
from hmd_cli_tools.okta_tools import get_auth_token
from hmd_lib_naming.hmd_lib_naming import HmdNamingClient, Service

from . import RemoteRepositoryFactory


def _get_codecommit_client():
    profile = os.environ.get("HMD_CC_AWS_PROFILE")
    aws_region = os.environ.get("HMD_CC_AWS_REGION")

    session = get_session(aws_region=aws_region, profile=profile)

    return session.client("codecommit"), aws_region


class CodeCommitRemote(RemoteRepositoryFactory):
    requires_build_trigger = True

    def __init__(self, app: App) -> None:
        super().__init__(app)

    def create_remote_repo(self, repo_dir: str, repo_info: Dict) -> str:
        codecommit, aws_region = _get_codecommit_client()
        repo_name = repo_info.get("project_name", repo_dir.split(os.sep)[-1])
        repo_desc = repo_info.get("description", repo_name)
        repo_metadata = codecommit.create_repository(
            repositoryName=repo_name, repositoryDescription=repo_desc
        )

        repo_url = repo_metadata["repositoryMetadata"]["cloneUrlSsh"]

        repo_origin = f"codecommit::{aws_region}://{repo_name}"

        r = Repo(repo_dir)

        if "origin" in r.remotes and r.remotes.origin.exists():
            r.remotes.origin.set_url(
                repo_origin, r.remotes.origin.url, allow_unsafe_protocols=True
            )
        else:
            r.create_remote("origin", repo_origin, allow_unsafe_protocols=True)

        if "codecommit" in r.remotes and r.remotes.codecommit.exists():
            r.remotes.codecommit.set_url(
                repo_origin, r.remotes.codecommit.url, allow_unsafe_protocols=True
            )
        else:
            r.create_remote("codecommit", repo_origin, allow_unsafe_protocols=True)

        r.git.push("--set-upstream", "origin", "main")

        return repo_url

    def list_remote_repos(self) -> List[str]:
        codecommit, aws_region = _get_codecommit_client()

        repos = codecommit.list_repositories()

        return list(
            map(
                lambda repo: f"codecommit::{aws_region}://{repo['repositoryName']}",
                repos["repositories"],
            )
        )

    def configure(self) -> Dict:
        return {
            "HMD_CC_AWS_PROFILE": {"prompt": "Enter the AWS Profile:"},
            "HMD_CC_AWS_REGION": {"prompt": "Enter the AWS Region:"},
        }
