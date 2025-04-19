import os
from string import Template
from typing import Any, Dict, Optional, Union

from requests import RequestException, Response

from netorca_sdk.auth import NetorcaAuth
from netorca_sdk.config import SUBMIT_SERVICEOWNER_SUBMISSION_DOCS_ENDPOINT, URL_PREFIX
from netorca_sdk.exceptions import (
    NetorcaAPIError,
    NetorcaAuthenticationError,
    NetorcaException,
    NetorcaGatewayError,
    NetorcaInvalidContextError,
    NetorcaNotFoundError,
    NetorcaServerUnavailableError,
    NetorcaValueError,
)
from netorca_sdk.validations import ContextIn


class Netorca:
    """
    Netorca

    A class to manage API calls to various endpoints in the Netorca API using the provided authentication method.

    Attributes:
    - auth (NetorcaAuth): The authentication object used for making API requests.
    - endpoints (Dict): A dictionary containing the supported API endpoints and their corresponding methods.

    Methods:

    __init__(self, auth: NetorcaAuth)
    Initializes the NetorcaEndpointCaller with the provided authentication object.

    caller(self, endpoint: str, operation: str, id: Union[str, int] = None, filters: Dict = None, data: Dict = None, context: ContextIn = None) -> Dict
    Performs the specified operation on the specified endpoint using the provided arguments.

    _get(self, endpoint: str, id: Union[str, int] = None, filters: Dict = None, context: ContextIn = None) -> Dict
    Performs a GET request on the specified endpoint using the provided arguments.

    _create(self, endpoint: str, data: Dict, context: ContextIn = None) -> Dict
    Performs a CREATE request on the specified endpoint using the provided arguments.

    _update(self, endpoint: str, id: Union[str, int], data: Dict, context: ContextIn = None) -> Dict
    Performs an UPDATE request on the specified endpoint using the provided arguments.

    _delete(self, endpoint: str, id: Union[str, int], context: ContextIn = None) -> Dict
    Performs a DELETE request on the specified endpoint using the provided arguments.

    create_url(self, endpoint: str, context: ContextIn = ContextIn.SERVICEOWNER.value, id: Union[str, int] = None)
    Creates the appropriate URL for the specified endpoint, context, and optional ID.
    """

    def __init__(
        self,
        auth: NetorcaAuth = None,
        fqdn: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        api_key: Optional[str] = None,
        verify_ssl: bool = True,
    ):
        """
        Initialize Netorca.

        :param auth: (Optional) An existing authentication instance.
        :param fqdn: (Optional) The base URL of the Netorca API (required if no `auth` is provided).
        :param username: (Optional) Username for authentication.
        :param password: (Optional) Password for authentication.
        :param api_key: (Optional) API key for authentication.
        :param verify_ssl: (Optional) ignore SSL verification flag.
        """
        if auth:
            # Maintain backward compatibility: Use provided `auth` instance
            self.auth = auth
        elif fqdn:
            # New way: Create `NetorcaAuth` internally
            self.auth = NetorcaAuth(
                fqdn=fqdn, username=username, password=password, api_key=api_key, verify_ssl=verify_ssl
            )
        else:
            raise NetorcaException("Either `auth` or `fqdn` must be provided!")

        self.endpoints: Dict[str, Any] = {
            "services": {
                "get": self._get,
                "create": self._create,
                "update": self._update,
                "patch": self._update,
                "delete": self._delete,
            },
            "service_dependant": {
                "get": self._get,
                "url": "services/dependant",
            },
            "services_validate": {
                "create": self._create,
                "url": "services/validate",
            },
            "service_docs": {
                "get": self._get,
                "url": "services/{id}/docs",
            },
            "service_tags": {
                "get": self._get,
                "url": "services/tags",
            },
            "service_items": {
                "get": self._get,
            },
            "service_items_dependant": {
                "get": self._get,
                "url": "service_items/dependant",
            },
            "deployed_items": {
                "get": self._get,
                "create": self._create,
                "update": self._update,
                "patch": self._update,
                "delete": self._delete,
            },
            "deployed_items_dependant": {
                "get": self._get,
                "url": "deployed_items/dependant",
            },
            "change_instances": {
                "get": self._get,
                "create": self._create,
                "update": self._update,
                "patch": self._update,
            },
            "change_instances_dependant": {
                "get": self._get,
                "url": "change_instances/dependant",
            },
            "change_instances_referenced": {
                "get": self._get,
                "url": "change_instances/referenced",
            },
            "change_instance_history": {
                "get": self._get,
                "url": "change_instances/{id}/history",
            },
            "service_configs": {
                "get": self._get,
                "create": self._create,
            },
            "charges": {
                "get": self._get,
                "patch": self._update,
                "update": self._update,
                "prefix": "marketplace",
            },
            "charges_accumulated": {
                "get": self._get,
                "url": "charges/accumulated",
                "prefix": "marketplace",
            },
            "applications": {
                "get": self._get,
                "url": "applications",
            },
            "submissions": {
                "get": self._get,
                "url": "submissions",
            },
            "submission_validate": {
                "create": self._create,
                "update": self._update,
                "url": "submissions/validate",
            },
            "submission_submit": {
                "create": self._create,
                "update": self._update,
                "url": "submissions/submit",
            },
            "healthcheck_trigger_service_item": {
                "get": self._get,
                "url": "healthchecks/trigger/service_item/{id}",
                "prefix": "external",
            },
            "healthcheck_trigger_service": {
                "get": self._get,
                "url": "healthchecks/trigger/service/{id}",
                "prefix": "external",
            },
            "healthchecks": {
                "get": self._get,
                "create": self._create,
                "url": "healthchecks",
                "prefix": "external",
            },
            "webhooks": {
                "get": self._get,
                "create": self._create,
                "update": self._update,
                "patch": self._update,
                "delete": self._delete,
                "url": "webhooks",
                "prefix": "external",
            },
            "webhook_trigger": {
                "create": self._create,
                "url": "webhooks/{id}/trigger",
                "prefix": "external",
            },
        }

    def caller(
        self,
        endpoint: str,
        operation: str,
        id: Union[str, int] = None,
        filters: Dict = None,
        data: Optional[Dict[str, Any]] = None,
        context: Optional[str] = None,
    ) -> Dict:
        if endpoint not in self.endpoints:
            raise NetorcaValueError(f"Invalid endpoint: {endpoint}")

        if operation not in self.endpoints[endpoint]:
            raise NetorcaValueError(f"Invalid operation: {operation}")

        if operation == "create":
            return self.endpoints[endpoint][operation](endpoint, data=data, context=context)
        elif operation in {"update", "patch"}:
            return self.endpoints[endpoint][operation](endpoint, id=id, data=data, context=context)
        elif operation == "delete":
            return self.endpoints[endpoint][operation](endpoint, id=id, context=context)
        else:
            return self.endpoints[endpoint][operation](endpoint, id=id, filters=filters, context=context)

    def _get(
        self, endpoint: str, id: Union[str, int] = None, filters: Dict = None, context: Optional[str] = None
    ) -> Dict:
        try:
            url = self.create_url(endpoint=endpoint, context=context, id=id)
            response = self.auth.get(url=url, filters=filters)
            return self.check_status(response, endpoint)

        except RequestException as e:
            raise NetorcaException(f"Could not fetch data from {endpoint} with error: {e}")
        except NetorcaException as e:
            raise NetorcaException(f"Error on API GET {e}")

    def _create(self, endpoint: str, data: Dict, context: Optional[str] = None) -> Dict:
        try:
            url = self.create_url(endpoint=endpoint, context=context)
            response = self.auth.post(url=url, data=data)
            return self.check_status(response, endpoint)

        except RequestException as e:
            raise NetorcaException(f"Could not fetch data from {endpoint} with error: {e}")
        except NetorcaException as e:
            raise NetorcaException(f"Error on API POST {e}")

    def _update(self, endpoint: str, id: Union[str, int], data: Dict, context: Optional[str] = None) -> Dict:
        try:
            url = self.create_url(endpoint=endpoint, context=context, id=id)
            response = self.auth.patch(url=url, data=data)
            return self.check_status(response, endpoint)

        except RequestException as e:
            raise NetorcaException(f"Could not fetch data from {endpoint} with error: {e}")
        except NetorcaException as e:
            raise NetorcaException(f"Error on API PUT {e}")

    def _delete(self, endpoint: str, id: Union[str, int], context: Optional[str] = None) -> Dict:
        try:
            url = self.create_url(endpoint=endpoint, context=context, id=id)
            response = self.auth.delete(url=url)
            return self.check_status(response, endpoint)

        except RequestException as e:
            raise NetorcaException(f"Could not fetch data from {endpoint} with error: {e}")
        except NetorcaException as e:
            raise NetorcaException(f"Error on API DELETE {e}")

    def create_url(
        self, endpoint: str, context: Optional[str] = ContextIn.SERVICEOWNER.value, id: Union[str, int] = None
    ) -> str:
        context = ContextIn.SERVICEOWNER.value if context is None else context
        if context not in [ContextIn.SERVICEOWNER.value, ContextIn.CONSUMER.value]:
            raise NetorcaInvalidContextError(
                f"{context} is not a valid ContextIn value. Options are {ContextIn.SERVICEOWNER.value} and {ContextIn.CONSUMER.value}"
            )
        endpoints: Dict[str, Any] = self.endpoints if isinstance(self.endpoints, dict) else {}
        custom_url: str = endpoints.get(endpoint, {}).get("url", "")
        url_prefix: str = endpoints.get(endpoint, {}).get("prefix", URL_PREFIX)

        if custom_url:
            if "{id}" in custom_url and not id:
                raise NetorcaValueError(f"id is required for endpoint: {endpoint}")
            path = (
                f"{custom_url.format(id=str(id))}/"
                if "{id}" in custom_url
                else f"{custom_url}/{str(id)}/"
                if id
                else f"{custom_url}/"
            )
        else:
            path = f"{endpoint}/{str(id)}/" if id else f"{endpoint}/"

        url = f"{self.auth.fqdn}/{url_prefix}/{context}/{path}"
        return url

    @staticmethod
    def check_status(response: Response, endpoint: str) -> Dict[Any, Any]:
        """
        Checks the HTTP response status code and raises appropriate exceptions.

        :param response: The HTTP response object.
        :param endpoint: The API endpoint for error context.
        :return: Parsed JSON response if the request was successful.
        :raises: Various exceptions based on the status code.
        """
        status_code = response.status_code

        if status_code in {200, 201}:
            try:
                return response.json()
            except ValueError:
                return {"response_text": response.text}
        elif status_code == 204:
            return {"status": "deleted"}
        elif status_code == 400:
            raise NetorcaAPIError(f"Bad request for {endpoint}. Reason: {response.text}")
        elif status_code == 403:
            raise NetorcaAPIError(f"Access denied for {endpoint}.")
        elif status_code == 404:
            raise NetorcaNotFoundError(f"{endpoint} not found.")
        elif status_code == 401:
            raise NetorcaAuthenticationError("Authentication failed.")
        elif status_code == 502:
            raise NetorcaGatewayError("Load balancer or webserver is down.")
        elif status_code == 503:
            raise NetorcaServerUnavailableError("Server is temporarily unavailable.")
        else:
            raise NetorcaAPIError(f"Unexpected error {status_code} for {endpoint}.")
        return {}

    def create_deployed_item(self, change_instance_id: int, description: dict) -> dict:
        data = {"deployed_item": description}
        return self.caller("change_instances", "patch", id=change_instance_id, data=data)

    def get_deployed_item(self, change_instance_id: int) -> dict:
        return self.caller("deployed_items", "get", id=change_instance_id)

    def get_deployed_items(self, filters: dict = None, context: Optional[str] = None) -> dict:
        return self.caller("deployed_items", "get", context=context, filters=filters)

    def get_service_items(self, filters: dict = None, context: Optional[str] = None) -> dict:
        return self.caller("service_items", "get", context=context, filters=filters)

    def get_services(self, filters: dict = None) -> dict:
        return self.caller("services", "get", filters=filters)

    def create_service(self, data: dict) -> dict:
        return self.caller("services", "create", data=data)

    def update_service(self, service_id: int, data: dict) -> dict:
        return self.caller("services", "update", id=service_id, data=data)

    def get_service_item(self, service_item_id: int) -> dict:
        return self.caller("service_items", "get", id=service_item_id)

    def get_change_instance(self, change_instance_id: int) -> dict:
        return self.caller("change_instances", "get", id=change_instance_id)

    def get_change_instances_dependant(self) -> dict:
        return self.caller("change_instances_dependant", "get")

    def get_change_instances(self, filters: dict = None, context: Optional[str] = None) -> dict:
        return self.caller("change_instances", "get", context=context, filters=filters)

    def update_change_instance(self, change_instance_id: int, data: dict) -> dict:
        return self.caller("change_instances", "update", id=change_instance_id, data=data)

    def get_service_config(self, service_config_id: int) -> dict:
        return self.caller("service_configs", "get", id=service_config_id)

    def get_service_configs(self, filters: dict = None) -> dict:
        return self.caller("service_configs", "get", filters=filters)

    def create_service_config(self, data: dict) -> dict:
        return self.caller("service_configs", "create", data=data)

    def get_service_items_dependant(self, filters: dict = None) -> dict:
        return self.caller("service_items_dependant", "get", filters=filters)

    def get_charges(self, filters: dict = None, context: Optional[str] = None) -> dict:
        return self.caller("charges", "get", filters=filters, context=context)

    def update_charges(self, charge_id: int, data: dict) -> dict:
        return self.caller("charges", "patch", id=charge_id, data=data)

    def get_deployed_items_dependant(self, filters: dict = None) -> dict:
        return self.caller("deployed_items_dependant", "get", filters=filters)

    def validate_service(self, data: dict) -> dict:
        return self.caller("services_validate", "create", data=data)

    def get_service_docs(self, service_id: int) -> dict:
        return self.caller("service_docs", "get", id=service_id)

    def create_service_docs(self, service_id: int, file_path: str, name: str) -> dict:
        try:
            if not os.path.isfile(file_path):
                raise NetorcaException(f"File not found: {file_path}")
            docs_path = Template(SUBMIT_SERVICEOWNER_SUBMISSION_DOCS_ENDPOINT).substitute(id=service_id)
            url = f"{self.auth.fqdn}{docs_path}"
            upload_filename = f"{name}.md"

            response = self.auth.upload_file(
                url=url,
                file_path=file_path,
                upload_filename=upload_filename,
                field_name="md_file",
                content_type="text/markdown",
            )

            return self.check_status(response, f"services/{service_id}/docs")

        except RequestException as e:
            raise NetorcaException(f"Could not upload service docs for service_id={service_id}. Error: {e}")
        except Exception as e:
            raise NetorcaException(f"Unexpected error during service docs upload: {e}")

    def get_service_tags(self) -> dict:
        return self.caller("service_tags", "get")

    def get_applications(self, filters: Optional[Dict[str, Any]] = None, context: Optional[str] = None) -> dict:
        return self.caller("applications", "get", filters=filters, context=context)

    def get_submissions(self, filters: Optional[Dict[str, Any]] = None, context: Optional[str] = None) -> dict:
        return self.caller("submissions", "get", filters=filters, context=context)

    def healthcheck_trigger_service_item(self, service_item_id: int, context: Optional[str] = None) -> dict:
        return self.caller("healthcheck_trigger_service_item", "get", id=service_item_id, context=context)

    def healthcheck_trigger_service(self, service_id: int, context: Optional[str] = None) -> dict:
        return self.caller("healthcheck_trigger_service", "get", id=service_id, context=context)

    def change_instance_history(self, change_instance_id: int, context: Optional[str] = None) -> dict:
        return self.caller("change_instance_history", "get", id=change_instance_id, context=context)

    def get_service_dependant(self, context: Optional[str] = None) -> dict:
        return self.caller("service_dependant", "get", context=context)

    def create_healthcheck(self, data: dict, context: Optional[str] = None) -> dict:
        return self.caller("healthchecks", "create", data=data, context=context)

    def create_webhook(self, data: dict) -> dict:
        return self.caller("webhooks", "create", data=data)

    def webhook_trigger(self, webhook_id: int) -> dict:
        return self.caller("webhook_trigger", "create", id=webhook_id)

    def submission_validate(self, data: dict, partial:bool=False, context: Optional[str] = None) -> dict:
        method = "update" if partial else "create"
        return self.caller("submission_validate", method, data=data, context=context)

    def submission_submit(self, data: dict, partial:bool=False, context: Optional[str] = None) -> dict:
        method = "update" if partial else "create"
        return self.caller("submission_submit", method, data=data, context=context)
