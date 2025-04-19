import json
import re
from typing import Any, Dict, Optional

import requests
import urllib3
from requests import Response

from netorca_sdk.config import API_VERSION, AUTH_ENDPOINT, TEAM_ENDPOINT
from netorca_sdk.exceptions import (
    NetorcaAPIError,
    NetorcaAuthenticationError,
    NetorcaException,
    NetorcaGatewayError,
    NetorcaNotFoundError,
    NetorcaServerUnavailableError,
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class NetorcaAuth:
    def __init__(
        self,
        fqdn: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        api_key: Optional[str] = None,
        verify_ssl: bool = True,
    ) -> None:
        self.username = username
        self.password = password
        self.api_key = api_key
        self.fqdn = self.validate_base_url(fqdn)
        self.headers = {"content-type": "application/json"}
        self.verify_ssl = verify_ssl

        if self.username and self.password:
            self.token = self.get_auth_token()
            self.headers["Authorization"] = f"Token {self.token}"
        elif self.api_key:
            self.headers["Authorization"] = f"Api-Key {self.api_key}"
        else:
            raise NetorcaException("Failed to authenticate. You must provide either (username and password) or API KEY")

    def _request(
        self, method: str, url: str, data: Optional[Dict[Any, Any]] = None, filters: Optional[Dict[Any, Any]] = None
    ) -> Response:
        """
        Internal method to handle HTTP requests.
        :param method: HTTP method (GET, POST, etc.)
        :param url: API endpoint URL
        :param data: Request payload (must be a dictionary if provided)
        :param filters: Query parameters
        """
        if not url:
            raise NetorcaException("URL not provided!")

        if filters:
            if not isinstance(filters, dict):
                raise NetorcaException("Filters must be a dictionary.")
            url += "?" + "&".join([f"{k}={json.dumps(v) if isinstance(v, dict) else v}" for k, v in filters.items()])

        if data is not None and not isinstance(data, dict):
            raise NetorcaException("Request data must be a dictionary.")
        try:
            response = requests.request(
                method, url, headers=self.headers, data=json.dumps(data) if data else None, verify=self.verify_ssl
            )
            if 200 <= response.status_code < 500:
                return response
            raise NetorcaAPIError(
                f"Failed {method} request. "
                f"URL: {url} "
                f"Response: {response.status_code}. "
                f"Content: {response.content}"
            )
        except requests.exceptions.SSLError:
            raise NetorcaException(f"SSL Error during {method} request to {url}")
        except json.JSONDecodeError:
            raise NetorcaAPIError(f"Failed to decode JSON response from {url}")
        except requests.exceptions.RequestException as e:
            raise NetorcaAPIError(f"Request Error during {method} request to {url}: {str(e)}")

    def get(self, url: str, filters: Optional[Dict[str, Any]] = None) -> Response:
        return self._request("GET", url, filters=filters)

    def post(self, url: str, data: Dict[str, Any]) -> Response:
        return self._request("POST", url, data=data)

    def put(self, url: str, data: Dict[str, Any]) -> Response:
        return self._request("PUT", url, data=data)

    def patch(self, url: str, data: Dict[str, Any]) -> Response:
        return self._request("PATCH", url, data=data)

    def delete(self, url: str) -> Response:
        return self._request("DELETE", url)

    def options(self, url: str) -> Response:
        return self._request("OPTIONS", url)

    def get_auth_token(self) -> str:
        AUTH_URL = f"{self.fqdn}{AUTH_ENDPOINT}"

        data = {"username": self.username, "password": self.password}
        response = self.post(url=AUTH_URL, data=data)
        if response.status_code == 200:
            return response.json().get("token", "")
        raise NetorcaException(f"Authentication failed due response status_code: {response.status_code}")

    def refresh_auth_token(self) -> str:
        return self.get_auth_token()

    @staticmethod
    def validate_base_url(base_url: str) -> str:
        if not base_url:
            raise NetorcaException("`netorca_global.base_url` is empty.")
        base_url = base_url.strip()
        base_url = re.sub(r"/+$", "", base_url)
        base_url = re.sub(f"{API_VERSION}/*$", f"{API_VERSION}", base_url)
        if not base_url.endswith(f"{API_VERSION}"):
            base_url += f"{API_VERSION}"
        return base_url

    def get_teams_info(self) -> list:
        """Get team info for given user"""
        TEAM_URL = f"{self.fqdn}{TEAM_ENDPOINT}"
        response = self.get(url=TEAM_URL)
        if response.status_code == 200:
            return response.json()["results"]
        elif response.status_code == 403:
            raise NetorcaAPIError("Access denied.")
        elif response.status_code == 404:
            raise NetorcaNotFoundError("endpoint not found.")
        elif response.status_code == 401:
            raise NetorcaAuthenticationError("Authentication failed.")
        elif response.status_code == 502:
            raise NetorcaGatewayError("Load balancer or webserver is down.")
        elif response.status_code == 503:
            raise NetorcaServerUnavailableError("Server is temporarily unavailable.")
        else:
            raise NetorcaAPIError(f"Error {response.status_code}")

    def upload_file(
        self,
        url: str,
        file_path: str,
        upload_filename: str,
        field_name: str = "file",
        content_type: str = "application/octet-stream",
    ) -> Response:
        headers = {"Authorization": self.headers["Authorization"]}

        try:
            with open(file_path, "rb") as file_obj:
                files = {field_name: (upload_filename, file_obj, content_type)}
                response = requests.post(url, files=files, headers=headers, verify=self.verify_ssl)
                return response

        except requests.exceptions.SSLError as e:
            raise NetorcaException(f"SSL Error during file upload: {e}")
        except requests.exceptions.RequestException as e:
            raise NetorcaException(f"File upload failed to {url}. Error: {e}")
        except Exception as e:
            raise NetorcaException(f"Unexpected error during file upload to {url}: {e}")

    def __str__(self) -> str:
        return f"Username: {self.username}, netorca instance: {self.fqdn}."

    def __repr__(self) -> str:
        return f"Username: {self.username}, netorca instance: {self.fqdn}."
