import httpx
import json
from . import config

from enum import Enum
from app.clients.logger import logger


class Variable:
    def __init__(
        self,
        key,
        value,
        workspace,
        id="",
        sensitive=False,
        category="env",
        hcl=False,
        description="",
        created="",
        version="",
    ):
        self._id = id
        self._key = key
        self._value = value
        self._sensitive = sensitive
        self._category = category
        self._hcl = hcl
        self._description = description
        self._created = created
        self._version = version
        self._workspace = workspace

    @property
    def id(self):
        return self._id

    @property
    def created(self):
        return self._created

    @property
    def version(self):
        return self._version

    @property
    def workspace(self):
        return self._workspace

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        self._key = key
        update_variable(self)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        update_variable(self)

    @property
    def sensitive(self):
        return self._sensitive

    @sensitive.setter
    def sensitive(self, sensitive):
        self._sensitive = sensitive
        update_variable(self)

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        self._category = category
        update_variable(self)

    @property
    def hcl(self):
        return self._hcl

    @hcl.setter
    def hcl(self, hcl):
        self._hcl = hcl
        update_variable(self)

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description
        update_variable(self)

    def __repr__(self):
        return self._key


def get_variables(workspace_id):
    logger.debug("Start: get_variables")

    variables = []
    url = "%s/workspaces/%s/vars" % (config.tf_endpoint, workspace_id)
    response = httpx.get(url, headers=config.headers)
    for variable in response.json()["data"]:
        new_variable = __parse_variable_json(variable)
        variables.append(new_variable)
        logger.debug("Found Variable: %s" % (new_variable))
    logger.debug("End: get_variables")

    return variables


def create_variable(
    key,
    value,
    workspace,
    description="",
    category="terraform",
    hcl=False,
    sensitive=False,
):
    logger.debug("Start: create_variable")
    attributes = {
        "key": key,
        "value": value,
        "description": description,
        "category": category,
        "hcl": hcl,
        "sensitive": sensitive,
    }
    data = {"data": {"type": "vars", "attributes": attributes}}
    url = "%s/workspaces/%s/vars/" % (config.tf_endpoint, workspace)
    response = httpx.post(url, headers=config.headers, json=data)
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        logger.error(
            f"Error response {exc.response.status_code} while requesting {exc.request.url!r}."
        )
    logger.debug("End: create_variable")
    return __parse_variable_json(response.json()["data"])


def get_variable_by_key(key, workspace_id):
    logger.debug("Start: get_variable_by_key")
    vars = get_variables(workspace_id)
    variable = [var for var in vars if var.key == key][0]
    logger.debug("End: get_variable_by_key")
    return variable


def update_variable(variable):
    logger.debug("Start: update_variable")
    attributes = {
        "key": variable._key,
        "value": variable.value,
        "description": variable.description,
        "category": variable.category,
        "hcl": variable.hcl,
        "sensitive": variable.sensitive,
    }
    data = {"data": {"type": "vars", "id": variable.id, "attributes": attributes}}
    logger.debug(json.dumps(data))
    url = "%s/workspaces/%s/vars/%s" % (
        config.tf_endpoint,
        variable.workspace,
        variable.id,
    )
    response = httpx.patch(url, headers=config.headers, json=data)
    logger.debug(response.content)
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        logger.error(
            f"Error response {exc.response.status_code} while requesting {exc.request.url!r}."
        )
    logger.debug("End: update_variable")
    return __parse_variable_json(response.json()["data"])


def delete_variable(variable):
    logger.debug("Start: delete_variable")
    url = "%s/workspaces/%s/vars/%s" % (
        config.tf_endpoint,
        variable.workspace,
        variable.id,
    )
    response = httpx.delete(url, headers=config.headers)
    logger.debug("End: delete_variable")


def __parse_variable_json(data):
    logger.debug("Start: parse_variable_json")
    variable = Variable(
        key=data["attributes"]["key"],
        value=data["attributes"]["value"],
        workspace=data["relationships"]["workspace"]["data"]["id"],
        id=data["id"],
        sensitive=data["attributes"]["sensitive"],
        category=data["attributes"]["category"],
        hcl=data["attributes"]["hcl"],
        description=data["attributes"]["description"],
        created=data["attributes"]["created-at"],
        version=data["attributes"]["version-id"],
    )
    logger.debug("Start: parse_variable_json")
    return variable
