import httpx
import json
import os
from . import config
from . import workspace_variables as variables

from enum import Enum
from app.clients.logger import logger


class org(Enum):
    DEV = "travismsmith"


class client:
    def __init__(self, env, workspace):
        logger.debug("New TF Client Created")
        self.organization = org[env].value
        self.workspace = workspace
        self.workspace_id = self.get_workspace_id()
        # vars = variables.get_variables(self.workspace_id)
        # test = variables.get_variable_by_key("test", self.workspace_id)
        # logger.warn(test)
        # variables.delete_variable(test)
        # testcreate = variables.create_variable("testcreate", "value", self.workspace_id)
        # testcreate.value = 'updated'

    def get_workspace_id(self):
        logger.debug("Start: get_workspace_id")
        url = "%s/organizations/%s/workspaces/%s" % (
            config.tf_endpoint,
            self.organization,
            self.workspace,
        )
        response = httpx.get(url, headers=config.headers)
        logger.debug(response.json())
        return response.json()["data"]["id"]

    def create_cv(self, file):
        data = {
            "data": {
                "type": "configuration-versions",
                "attributes": {"auto-queue-runs": False},
            }
        }
        url = "%s/workspaces/%s/configuration-versions/" % (
            config.tf_endpoint,
            self.workspace_id,
        )
        response = httpx.post(url, headers=config.headers, json=data)
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error(
                f"Error response {exc.response.status_code} while requesting {exc.request.url!r}."
            )

        upload_response = httpx.put(
            response.json()["data"]["attributes"]["upload-url"], content=file.file
        )
        logger.debug("End: create_cv")
        return response.json()["data"]["id"]

    def create_run(self, cv, speculative=True):
        data = {
            "data": {
                "attributes": {"message": "Custom message", "plan-only": speculative},
                "type": "runs",
                "relationships": {
                    "workspace": {
                        "data": {"type": "workspaces", "id": self.workspace_id}
                    },
                    "configuration-version": {
                        "data": {"type": "configuration-versions", "id": cv}
                    },
                },
            }
        }

        url = "%s/runs/" % (config.tf_endpoint)
        response = httpx.post(url, headers=config.headers, json=data)
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error(
                f"Error response {exc.response.status_code} while requesting {exc.request.url!r}."
            )
        return response.json()

    def get_run(self, run_id):
        url = "%s/runs/%s" % (config.tf_endpoint, run_id)
        response = httpx.get(url, headers=config.headers)
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error(
                f"Error response {exc.response.status_code} while requesting {exc.request.url!r}."
            )
        return response.json()

    def apply_run(self, run_id):
        url = "%s/runs/%s/actions/apply" % (config.tf_endpoint, run_id)
        response = httpx.post(url, headers=config.headers)
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error(
                f"Error response {exc.response.status_code} while requesting {exc.request.url!r}."
            )
        return response.json()
    
    def get_plan(self, plan_id):
        url = "%s/plans/%s" % (config.tf_endpoint, plan_id)
        response = httpx.get(url, headers=config.headers)
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error(
                f"Error response {exc.response.status_code} while requesting {exc.request.url!r}."
            )
        return response.json()

    def get_plan_output(self, run_id):
        url = "%s/runs/%s/plan/json-output" % (config.tf_endpoint, run_id)
        response = httpx.get(url, headers=config.headers, follow_redirects=True)
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error(
                f"Error response {exc.response.status_code} while requesting {exc.request.url!r}."
            )
        return response.json()

    def get_apply(self, plan_id):
        url = "%s/applies/%s" % (config.tf_endpoint, plan_id)
        response = httpx.get(url, headers=config.headers)
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error(
                f"Error response {exc.response.status_code} while requesting {exc.request.url!r}."
            )
        return response.json()

    def get_apply_output(self, run_id):
        url = "%s/runs/%s/apply/json-output" % (config.tf_endpoint, run_id)
        response = httpx.get(url, headers=config.headers, follow_redirects=True)
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error(
                f"Error response {exc.response.status_code} while requesting {exc.request.url!r}."
            )
        return response.json()