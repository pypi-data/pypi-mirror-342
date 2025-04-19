import os
from typing import Any, Dict, Optional, Tuple, Union

import git
from beautifultable import BeautifulTable
from requests import Response
from ruamel.yaml import YAML
from ruamel.yaml.constructor import DuplicateKeyError
from ruamel.yaml.error import YAMLError

from netorca_sdk.auth import NetorcaAuth
from netorca_sdk.config import (
    LIST_CONSUMER_SUBMISSIONS_ENDPOINT,
    SUBMIT_CONSUMER_SUBMISSION_ENDPOINT,
    VALIDATE_CONSUMER_SUBMISSION_ENDPOINT,
)
from netorca_sdk.exceptions import (
    NetorcaAPIError,
    NetorcaAuthenticationError,
    NetorcaException,
    NetorcaGatewayError,
    NetorcaNotFoundError,
    NetorcaServerUnavailableError,
    NetOrcaWrongYAMLFormat,
)
from netorca_sdk.junit_reporter import JUnitReporter


class ConsumerSubmission:
    def __init__(
        self,
        netorca_api_key: str,
        netorca_validate_only: Union[bool, str] = True,
        repository_url: str = "./",
        use_config: bool = False,
        verify_ssl: bool = True,
    ):
        self.netorca_api_key = netorca_api_key
        self.netorca_validate_only = True if netorca_validate_only is True or netorca_validate_only == "True" else False
        self.repository_path = repository_url
        self.use_config = use_config
        self.config: Optional[Dict[str, Any]] = None
        self.consumer_submission: Optional[Dict[str, Any]] = None
        self.auth: NetorcaAuth
        self.verify_ssl = verify_ssl

    def load_from_repository(
        self, repository_path: str = None, netorca_directory: str = ".netorca", repository_config: dict = None
    ) -> None:
        """
        Check if valid and load request and config from consumer's repository.

        Note: Only one allowed extensions in netorca_directory directory is *.yaml/*.yml

        Args:
            repository_path: str    path to consumer repository

        Returns: None
        :param repository_path:     path to consumer repository
        :param netorca_directory:   netorca directory name, defaults to ".netorca"
        :param repository_config:      optional: you can specify config from dictionary instead of config.y(a)ml
        """

        if not repository_path:
            repository_path = self.repository_path
        repository_exists = os.path.isdir(repository_path)
        if not repository_exists:
            raise NetorcaException(f"{repository_path} directory does not exist.")

        netorca_exists = os.path.isdir(f"{repository_path}/{netorca_directory}")
        if not netorca_exists:
            raise NetorcaException(f"{netorca_directory} directory does not exist.")

        dotnetorca_path = f"{repository_path}/{netorca_directory}"
        if repository_config:
            netorca_global = repository_config.get("netorca_global", {})
            if not netorca_global:
                raise NetorcaException("No netorca_global.base_url provided.")

            self.config = repository_config
            self.auth = self.get_auth()
        else:
            # check and load config from file if it exists
            config_path_yaml = f"{repository_path}/{netorca_directory}/config.yaml"
            config_path_yml = f"{repository_path}/{netorca_directory}/config.yml"

            if os.path.exists(config_path_yml):
                config_path = config_path_yml
            elif os.path.exists(config_path_yaml):
                config_path = config_path_yaml
            else:
                raise NetorcaException("No config file in the repository.")

            config = self.load_yaml_file(config_path)
            netorca_global = config.get("netorca_global", {})

            if not netorca_global:
                raise NetorcaException("No netorca_global.base_url provided.")

            config["netorca_global"]["commit_id"] = self.get_commit_id(repository_path)
            self.config = config
            self.auth = self.get_auth()

        _tmp_consumer_submission = {}
        # check and load consumer request
        for filename in os.listdir(dotnetorca_path):
            if filename == "config.yaml" or filename == "config.yml":
                continue

            f = os.path.join(dotnetorca_path, filename)
            # checking if it is a file and is *.yaml/*.yml
            if not (os.path.isfile(f) and (f.endswith(".yaml") or f.endswith(".yml"))):
                continue

            app = self.load_yaml_file(f)

            if not isinstance(app, dict):
                raise NetorcaException(f"Invalid format in file: {filename}. The file should contain a dictionary.")

            for key, content in app.items():
                if key in _tmp_consumer_submission:
                    raise NetorcaException(f"Application with name {key} already exists in different yaml declaration.")
                metadata = content.get("metadata", {})
                services = content.get("services", {})

                _tmp_consumer_submission[key] = {"metadata": metadata, "services": services if services else {}}
        self.consumer_submission = _tmp_consumer_submission

    @staticmethod
    def get_commit_id(repo_path: str) -> str:
        try:
            repo = git.Repo(repo_path, search_parent_directories=True)
            latest_commit = repo.head.commit
            latest_commit_id = latest_commit.hexsha
            return latest_commit_id
        except git.exc.InvalidGitRepositoryError:
            return ""

    @staticmethod
    def load_yaml_file(file_path: str) -> dict:
        """
        Load a YAML file from the given path using ruamel.yaml.
        Disallows duplicate keys, raising an error if found.
        Args:
            file_path: str, path to YAML file
        Returns:
            dict: The loaded YAML data as a dictionary
        Raises:
            NetOrcaWrongYAMLFormat: If parsing fails or if a duplicate key is detected.
        """
        file_name = os.path.basename(file_path)
        yaml_parser = YAML()
        yaml_parser.allow_duplicate_keys = False

        try:
            with open(file_path, "r") as stream:
                loaded_yaml = yaml_parser.load(stream)
                return loaded_yaml if loaded_yaml is not None else {}
        except DuplicateKeyError as exc:
            raise NetOrcaWrongYAMLFormat(f"Error while parsing file '{file_name}': Duplicate key found. {exc}")
        except YAMLError as exc:
            raise NetOrcaWrongYAMLFormat(f"Error while parsing file '{file_name}': {exc}")
        except Exception as exc:
            raise NetOrcaWrongYAMLFormat(f"Error while parsing file '{file_name}': {str(exc)}")

    def get_auth(self) -> NetorcaAuth:
        if not self.config:
            raise NetorcaException("Cannot authenticate before loading repository config.")

        netorca_fqdn = self.config.get("netorca_global", {}).get("base_url")
        self.auth = NetorcaAuth(fqdn=netorca_fqdn, api_key=self.netorca_api_key, verify_ssl=self.verify_ssl)
        return self.auth

    def get_team(self) -> dict:
        if self.use_config:
            team_name = (self.config or {}).get("netorca_global", {}).get("metadata", {}).get("team_name")
            if not team_name:
                raise NetorcaException("netorca_global.team_name is empty.")
            return {"name": team_name}

        teams = self.auth.get_teams_info()
        if teams:
            return teams[0]
        return {}

    def prepare_request(self) -> dict:
        team = self.get_team()
        metadata = (self.config or {}).get("netorca_global", {}).get("metadata", {})
        if not (team and self.config and self.consumer_submission and self.auth):
            raise NetorcaException("Team, config and consumer request should be fetched at this stage.")

        full_request = {team["name"]: self.consumer_submission}

        if metadata is not None:
            full_request[team["name"]]["metadata"] = metadata

        return full_request if full_request else {}

    def validate(self, pretty_print: bool = False, partial: bool = False) -> Tuple[bool, dict]:
        """
        Validate consume request.
        NOTE: Data must be first imported with load_from_repository method
        Parameters:
            pretty_print:   (optional) pretty print errors, default: False
            partial:        (optional) partial validation, default: False
        Returns:
            Tuple[bool, str]    ->  is_valid, validation_errors
        """
        if not self.consumer_submission:
            print("No application detected. Validation skipped.")
            return False, {}
        if not (self.config and self.auth):
            raise NetorcaException("Use load_from_repository(repository_path) method to load configuration.")
        VALIDATE_REQUEST_PATH = f"{self.auth.fqdn}{VALIDATE_CONSUMER_SUBMISSION_ENDPOINT}"
        full_request = self.prepare_request()

        if partial:
            response = self.auth.patch(url=VALIDATE_REQUEST_PATH, data=full_request)
        else:
            response = self.auth.post(url=VALIDATE_REQUEST_PATH, data=full_request)

        response = self.check_status_code(response)
        if response.get("is_valid"):
            return True, {}
        errors = response.get("errors")

        if pretty_print:
            # Publish errors on Merge Request
            reporter = JUnitReporter()
            reporter.write(errors)

            ConsumerSubmission.pretty_print_errors(errors)
        return False, errors

    def submit(self, partial: bool = False) -> Union[Tuple[bool, Dict[Any, Any]], Tuple[bool, str]]:
        """
        Validate and submit consumer request.
        NOTE: Data must be first imported with load_from_repository method

        Parameters:
            partial:        (optional) partial submission, default: False
        Returns:
            bool, str    ->  submission successful, submission messages
        """
        if not self.consumer_submission:
            print("No application detected. Submission skipped.")
            return False, "No application detected. Submission skipped."
        is_valid = self.validate(pretty_print=True, partial=partial)
        if not is_valid[0]:
            return False, "Consumer request is invalid and cannot be submitted."

        commit_id = (self.config or {}).get("netorca_global", {}).get("commit_id")
        SUBMIT_REQUEST_PATH = f"{self.auth.fqdn}{SUBMIT_CONSUMER_SUBMISSION_ENDPOINT}" + (
            f"?commit_id={commit_id}" if commit_id else ""
        )
        full_request = self.prepare_request()
        if partial:
            response = self.auth.patch(url=SUBMIT_REQUEST_PATH, data=full_request)
        else:
            response = self.auth.post(url=SUBMIT_REQUEST_PATH, data=full_request)

        if response.status_code == 201:
            return True, "Submitted successfully."
        if response.status_code == 200:
            return True, "Submitted successfully, no changes detected"
        return False, self.check_status_code(response)

    def get_submissions(self, limit: int = 10, ordering: str = "created") -> dict:
        """Return submissions from Netorca API sorted by specified key.

        Args:
            limit (int, optional): Number of records returned. Defaults to 10.
            ordering (str, optional): Key to sort by. Defaults to "created" - created date, oldest first.

        Returns:
            dict: Response from Netorca API.
        """

        request_url = f"{self.auth.fqdn}{LIST_CONSUMER_SUBMISSIONS_ENDPOINT}?limit={limit}&ordering={ordering}"

        response = self.auth.get(url=request_url)

        response = self.check_status_code(response)
        return response

    def get_response(self) -> Union[Tuple[bool, str], Tuple[bool, dict]]:
        self.load_from_repository()
        return self.submit() if not self.netorca_validate_only else self.validate(pretty_print=True)

    @staticmethod
    def pretty_print_errors(errors: dict) -> None:
        """
        Pretty print errors
        """

        table = BeautifulTable(maxwidth=100)
        table.set_style(BeautifulTable.STYLE_SEPARATED)
        table.columns.header = ["Team", "Field", "Reason"]
        for item1, value1 in errors.items():
            if isinstance(value1, str) or isinstance(value1, list):
                table.rows.append([item1, "", value1])
            elif isinstance(value1, dict):
                for item2, value2 in value1.items():
                    if isinstance(value2, str) or isinstance(value2, list):
                        table.rows.append([item1, item2, value2])

                        if table.rows:
                            print("-" * 100)
                            print(f"Team: {item1} validation errors")
                            print("-" * 100)
                            print(table)
                            print()
                        break

        for item1, value1 in errors.items():
            if isinstance(value1, dict):
                for item2, value2 in value1.items():
                    table = BeautifulTable(maxwidth=100)
                    table.set_style(BeautifulTable.STYLE_SEPARATED)
                    table.columns.header = ["Application", "Service", "ServiceItem", "Field", "Reason"]

                    if isinstance(value2, dict):
                        for item3, value3 in value2.items():
                            if isinstance(value3, str):
                                table.rows.append([item2, "", "", item3, value3])
                            elif isinstance(value3, list):
                                for err in value3:
                                    table.rows.append([item2, "", "", item3, err])
                            elif isinstance(value3, dict):
                                for item4, value4 in value3.items():
                                    if isinstance(value4, str) or isinstance(value4, list):
                                        table.rows.append([item2, item3, "", item4, value4])
                                    elif isinstance(value4, dict):
                                        for item5, value5 in value4.items():
                                            if isinstance(value5, str) or isinstance(value5, list):
                                                table.rows.append([item2, item3, item4, item5, value5])

                        if table.rows:
                            print("-" * 100)
                            print(f"Application: {item2} validation errors")
                            print("-" * 100)
                            print(table)
                            print()

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
