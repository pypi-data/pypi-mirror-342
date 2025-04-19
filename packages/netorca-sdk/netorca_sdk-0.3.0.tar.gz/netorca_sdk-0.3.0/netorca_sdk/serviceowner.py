import json
import os
from collections import defaultdict
from string import Template
from typing import Any, DefaultDict, Dict, Optional, Tuple

from beautifultable import BeautifulTable
from requests import Response

from netorca_sdk.auth import NetorcaAuth
from netorca_sdk.config import (
    SUBMIT_SERVICEOWNER_SUBMISSION_DOCS_ENDPOINT,
    SUBMIT_SERVICEOWNER_SUBMISSION_ENDPOINT,
    VALIDATE_SERVICEOWNER_SUBMISSION_ENDPOINT,
)
from netorca_sdk.exceptions import (
    NetorcaAPIError,
    NetorcaAuthenticationError,
    NetorcaException,
    NetorcaGatewayError,
    NetorcaNotFoundError,
    NetorcaServerUnavailableError,
)


class ServiceOwnerSubmission:
    def __init__(self, netorca_api_key: str, verify_ssl: bool = True) -> None:
        self.netorca_api_key = netorca_api_key
        self.config: Optional[Dict[str, Any]] = None
        self.serviceowner_submission: Dict[str, Any]
        self.auth: Optional[NetorcaAuth] = None
        self.verify_ssl = verify_ssl

    def load_from_repository(
        self, repository_path: str, netorca_directory: str = ".netorca", repository_config: dict = None
    ) -> None:
        """
        Check if valid and load submission and config from service owner's repository.
        Repository must contain .netorca directory and config.json file.
        Note: Two allowed extensions in .netorca directory are: *.yaml and *.md.

        Args:
            repository_path: str    path to service owner repository

        Returns: None
        :param repository_path:     path to service owner repository
        :param netorca_directory:   netorca directory name, defaults to ".netorca"
        :param repository_config:      optional: you can specify config from dictionary instead of config.json
        """

        repository_exists = os.path.isdir(repository_path)
        if not repository_exists:
            raise NetorcaException(f"{repository_path} directory does not exist.")

        netorca_path = os.path.join(repository_path, netorca_directory)
        netorca_exists = os.path.isdir(netorca_path)
        if not netorca_exists:
            raise NetorcaException(f"{netorca_directory} directory does not exist.")

        if repository_config:
            netorca_global = repository_config.get("netorca_global", {})
            if not netorca_global:
                raise NetorcaException("No netorca_global.base_url provided.")
            self.config = repository_config
            self.auth = self.get_auth()
        else:
            config_path = os.path.join(netorca_path, "config.json")
            self.config = self.read_json_file(config_path)
            netorca_global = self.config.get("netorca_global", {})
            if not netorca_global:
                raise NetorcaException("No netorca_global.base_url provided.")
            self.auth = self.get_auth()

        _tmp_serviceowner_submission: DefaultDict = defaultdict()
        for filename in os.listdir(netorca_path):
            if filename == "config.json":
                continue

            file_path = os.path.join(netorca_path, filename)
            if not os.path.isfile(file_path) and not (file_path.endswith(".json") or file_path.endswith(".md")):
                raise NetorcaException(
                    f"ServiceOwner submission file: {file_path} does not exist or must be .json or .md extension"
                )

            if filename.endswith(".json"):
                json_file = self.read_json_file(file_path)
                filename_without_ext = os.path.splitext(filename)[0]
                _tmp_serviceowner_submission.setdefault(filename_without_ext, {})
                _tmp_serviceowner_submission[filename_without_ext]["service"] = json_file

        for filename in os.listdir(netorca_path):
            if filename == "config.json" or not filename.endswith(".md"):
                continue

            file_path = os.path.join(netorca_path, filename)
            filename_without_ext = os.path.splitext(filename)[0]

            if not _tmp_serviceowner_submission.get(filename_without_ext):
                raise NetorcaException(
                    f"'\nYou are trying to add README file: {filename} for non existing service.\n"
                    f"Readme file (.md) must have the same name as service definition file (.json)."
                )

            _tmp_serviceowner_submission[filename_without_ext]["readme"] = file_path

        self.serviceowner_submission = _tmp_serviceowner_submission

    def read_json_file(self, file_path: str) -> Dict[str, Any]:
        try:
            with open(file_path, "r") as stream:
                return json.load(stream)
        except FileNotFoundError as exc:
            raise NetorcaException(f"File not found: {file_path}. Exception: {exc}")
        except PermissionError as exc:
            raise NetorcaException(f"Permission error while reading file: {file_path}. Exception: {exc}")
        except json.JSONDecodeError as exc:
            raise NetorcaException(f"Error while parsing file: {file_path}. Exception: {exc.msg}")

    def get_auth(self) -> NetorcaAuth:
        if not self.config:
            raise NetorcaException("Cannot authenticate before loading repository config.")

        netorca_fqdn = self.config.get("netorca_global", {}).get("base_url")
        self.auth = NetorcaAuth(fqdn=netorca_fqdn, api_key=self.netorca_api_key, verify_ssl=self.verify_ssl)
        return self.auth

    def get_team(self) -> Dict[str, Any]:
        teams = []
        if self.auth:
            teams = self.auth.get_teams_info()
        if teams:
            return teams[0]
        return {}

    def validate(self, pretty_print: bool = False, dry_run: bool = False) -> Tuple[bool, str]:
        """
        Validate service owner submission.
        NOTE: Data must be first imported with load_from_repository method

        Returns:
            bool    ->  validation successful
        """
        if self.auth is None:
            raise NetorcaException("Use load_from_repository(repository_path) method to load configuration.")
        dry_run_str = "?dry_run=true" if dry_run else ""
        VALIDATE_SERVICEOWNER_PATH = f"{self.auth.fqdn}{VALIDATE_SERVICEOWNER_SUBMISSION_ENDPOINT}{dry_run_str}"
        invalid_services = []

        if not (self.config and self.serviceowner_submission and self.auth):
            raise NetorcaException("Use load_from_repository(repository_path) method to load configuration.")

        for service_filename, service_submission in self.serviceowner_submission.items():
            service_name = service_submission.get("service", {}).get("title", "")
            response = self.auth.post(
                url=VALIDATE_SERVICEOWNER_PATH,
                data=service_submission["service"],
            )
            response = self.check_status_code(response)
            if response.get("is_valid"):
                print(f"VALIDATION SUCCESSFUL for service: {service_name}, in file: {service_filename}.")
            else:
                invalid_services.append({"service": service_name, "file": service_filename})
                errors = response.get("errors")
                if pretty_print and errors:
                    ServiceOwnerSubmission.pretty_print_errors(service_filename, errors)

        if invalid_services:
            invalid_services_str_list = [f"{item['service']} (file: {item['file']})" for item in invalid_services]
            print("INVALID SERVICES: " + ", ".join(invalid_services_str_list))
            return False, "Invalid services: " + ", ".join([item["file"] for item in invalid_services])
        return True, "Services validated successfully."

    def submit(self) -> Tuple[bool, str]:
        """
        Validate and submit consumer submission.
        NOTE: Data must be first imported with load_from_repository method

        Returns:
            bool, str    ->  is submission successful, submission messages
        """
        if not self.auth:
            raise NetorcaException("Authentication is  not initialized.")
        SUBMIT_SERVICEOWNER_REQUEST_PATH = f"{self.auth.fqdn}{SUBMIT_SERVICEOWNER_SUBMISSION_ENDPOINT}"
        submitted_services = []
        submitted_readme = []
        is_valid = self.validate(pretty_print=True)

        if not is_valid[0]:
            return False, "Some of your submissions are invalid and were not submitted."

        for service_filename, service_submission in self.serviceowner_submission.items():
            service_name = service_submission.get("service", {}).get("title", "")
            response = self.auth.post(
                url=SUBMIT_SERVICEOWNER_REQUEST_PATH,
                data=service_submission["service"],
            )

            if response.status_code == 201:
                print(
                    f"SUBMITTED service to NetOrca. Service: {service_name} in file: {service_filename} is now available for consumers."
                )
                submitted_services.append(service_filename)
            elif response.status_code == 200:
                print("No updates to service detected")
            else:
                print(f"FAILED to submit service: {service_filename}. Reason: {self.check_status_code(response)}")

            ## README's should always be submitted, regardless of whether the Service has been updated
            # The README could have changed.
            response = self.check_status_code(response)
            if service_submission.get("readme"):
                readme_path = service_submission.get("readme")

                service_id = response["id"] if "id" in response else self.get_service_id_by_name(service_filename)

                docs_path = Template(SUBMIT_SERVICEOWNER_SUBMISSION_DOCS_ENDPOINT).substitute(id=service_id)
                url = f"{self.auth.fqdn}{docs_path}"
                upload_filename = f"{service_filename}.md"

                readme_response = self.auth.upload_file(
                    url=url,
                    file_path=readme_path,
                    upload_filename=upload_filename,
                    field_name="md_file",
                    content_type="text/markdown",
                )
                if readme_response.status_code == 201:
                    print(f"SUBMITTED README file for service: {service_name} in file: {service_filename}.")
                    submitted_readme.append(service_filename)
                elif readme_response.status_code == 200:
                    print(f"UPDATED README file for service: {service_name} in file: {service_filename}.")
                    submitted_readme.append(service_filename)
                else:
                    response = self.check_status_code(readme_response)
                    print(
                        f"FAILED to submit README file for service: {service_name} in file: {service_filename}. Reason: {response}."
                    )
            else:
                print(f"NOTE: Service file {service_filename} does not have a README file. Skipped.")
            print("\nMoving to next service...")
            print()

        if submitted_services or submitted_readme:
            return True, "Submitted services: " + ", ".join(
                submitted_services
            ) + "\n" + "Submitted README's: " + ", ".join(submitted_readme)
        return False, "No services were submitted."

    @staticmethod
    def pretty_print_errors(service_name: str, errors: dict) -> None:
        def append_to_table(service_name: str, item: str, value: str, table: BeautifulTable) -> None:
            if isinstance(value, str) or isinstance(value, list):
                table.rows.append([service_name, item, value])
            elif isinstance(value, dict):
                for key, val in value.items():
                    append_to_table(service_name, key, val, table)

        table = BeautifulTable(maxwidth=100)
        table.set_style(BeautifulTable.STYLE_SEPARATED)
        table.columns.header = ["Schema", "Property", "Reason"]

        for item, value in errors.items():
            append_to_table(service_name, item, value, table)

        if table.rows:
            print("-" * 100)
            print(f"Schema: {service_name} validation errors")
            print("-" * 100)
            print(table)
            print()

    def get_service_id_by_name(self, service_name: str) -> int:
        """
        Get service id from NetOrca based on service name.

        Args:
            service_name: str   service name

        Returns:
            int     ->  service id
        """
        try:
            SUBMIT_SERVICEOWNER_REQUEST_PATH = (
                f"{self.auth.fqdn}{SUBMIT_SERVICEOWNER_SUBMISSION_ENDPOINT}?name={service_name}" if self.auth else ""
            )
            if self.auth:
                response = self.auth.get(url=SUBMIT_SERVICEOWNER_REQUEST_PATH)
                response = self.check_status_code(response)
                service_id = response["results"][0]["id"] if response["results"] else None
                return service_id
            return 0
        except NetorcaException:
            raise NetorcaException(f"Failed to get service id for service: {service_name}.")

    @staticmethod
    def check_status_code(response: Response) -> Dict[Any, Any]:
        if response.status_code in [200, 201, 400]:
            return response.json()
        elif response.status_code == 204:
            return {"status": "deleted"}
        elif response.status_code == 404:
            raise NetorcaNotFoundError("The endpoint not found.")
        elif response.status_code == 401:
            raise NetorcaAuthenticationError("Authentication failed.")
        elif response.status_code == 403:
            raise NetorcaAuthenticationError("Authorization failed.")
        elif response.status_code == 502:
            raise NetorcaGatewayError("Load balancer or webserver is down.")
        elif response.status_code == 503:
            raise NetorcaServerUnavailableError("Server is temporarily unavailable.")
        else:
            if response.content:
                error_message = response.content.decode("utf-8")
            else:
                error_message = "No content in the response."
            raise NetorcaAPIError(f"Error {response.status_code} - {error_message}")
