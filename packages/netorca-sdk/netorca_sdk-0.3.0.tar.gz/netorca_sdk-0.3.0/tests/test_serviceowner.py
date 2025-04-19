import json
import os
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import MagicMock, patch

from requests.exceptions import SSLError

from netorca_sdk.config import API_VERSION
from netorca_sdk.exceptions import (
    NetorcaAPIError,
    NetorcaAuthenticationError,
    NetorcaException,
    NetorcaGatewayError,
    NetorcaNotFoundError,
    NetorcaServerUnavailableError,
)
from netorca_sdk.serviceowner import ServiceOwnerSubmission


class TestServiceOwnerSubmission(unittest.TestCase):
    def setUp(self) -> None:
        self.netorca_api_key = "api_key"
        self.service_owner_submission = ServiceOwnerSubmission(self.netorca_api_key)

        # Create a temporary directory and set up test files
        self.test_dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.test_dir, ".netorca"))

        with open(os.path.join(self.test_dir, ".netorca", "config.json"), "w") as f:
            f.write('{"netorca_global": {"base_url": "https://example.com"}}')

        with open(os.path.join(self.test_dir, ".netorca", "service1.json"), "w") as f:
            f.write('{"key": "value"}')

        with open(os.path.join(self.test_dir, ".netorca", "service1.md"), "w") as f:
            f.write("# Service 1 Documentation")

        # Mock the NetorcaAuth.post method and requests.post method
        self.mock_post_patcher = patch("netorca_sdk.auth.NetorcaAuth.post")
        self.mock_post = self.mock_post_patcher.start()
        self.mock_requests_post_patcher = patch("requests.post")
        self.mock_requests_post = self.mock_requests_post_patcher.start()

    def tearDown(self) -> None:
        # Remove temporary directory and its contents
        shutil.rmtree(self.test_dir)

        # Stop the patchers
        self.mock_post_patcher.stop()
        self.mock_requests_post_patcher.stop()

    def test_load_from_repository(self) -> None:
        with self.assertRaises(NetorcaException):
            self.service_owner_submission.load_from_repository("/non_existent_path")

        self.service_owner_submission.load_from_repository(self.test_dir)
        self.assertIsNotNone(self.service_owner_submission.config)
        self.assertIsNotNone(self.service_owner_submission.serviceowner_submission)

    def test_load_from_repository_valid_path(self) -> None:
        self.service_owner_submission.load_from_repository(self.test_dir)
        self.assertIsNotNone(self.service_owner_submission.config)
        self.assertIsNotNone(self.service_owner_submission.serviceowner_submission)

    def test_load_from_repository_invalid_path(self) -> None:
        with self.assertRaises(NetorcaException):
            self.service_owner_submission.load_from_repository("/non_existent_path")

    def test_get_auth(self) -> None:
        with self.assertRaises(NetorcaException):
            self.service_owner_submission.get_auth()

        self.service_owner_submission.load_from_repository(self.test_dir)
        auth = self.service_owner_submission.get_auth()
        self.assertIsNotNone(auth)

    def test_get_team(self) -> None:
        with patch("netorca_sdk.auth.NetorcaAuth.get_teams_info") as mock_get_teams_info:
            mock_get_teams_info.return_value = [{"id": 1, "name": "team1"}]
            self.service_owner_submission.load_from_repository(self.test_dir)
            team = self.service_owner_submission.get_team()
            self.assertEqual(team, {"id": 1, "name": "team1"})

    def test_validate(self) -> None:
        with patch("netorca_sdk.auth.NetorcaAuth.post") as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {"is_valid": True}

            with self.assertRaises(NetorcaException):
                self.service_owner_submission.validate()

            self.service_owner_submission.load_from_repository(self.test_dir)
            is_valid, errors = self.service_owner_submission.validate()
            self.assertTrue(is_valid)
            self.assertEqual(errors, "Services validated successfully.")

    def test_validate_invalid_submission(self) -> None:
        self.mock_post.return_value.status_code = 200
        self.mock_post.return_value.json.return_value = {"is_valid": False, "errors": {"key": "Invalid key"}}

        self.service_owner_submission.load_from_repository(self.test_dir)
        is_valid, errors = self.service_owner_submission.validate()
        self.assertFalse(is_valid)
        self.assertIn("Invalid services:", errors)
        self.assertIn("service1", errors)

    def test_submit(self) -> None:
        with patch("netorca_sdk.auth.NetorcaAuth.post") as mock_post:
            mock_post.return_value.status_code = 201
            with patch("requests.post") as mock_requests_post:
                mock_requests_post.return_value.status_code = 200

                mock_auth = MagicMock()
                mock_auth.fqdn = "https://example.com"
                self.service_owner_submission.auth = mock_auth

                with self.assertRaises(NetorcaException):
                    self.service_owner_submission.submit()

    def test_create_without_metadata(self) -> None:
        # Create a temporary directory for the test
        with tempfile.TemporaryDirectory() as temp_dir:
            netorca_path = os.path.join(temp_dir, ".netorca")
            os.mkdir(netorca_path)
            config_path = os.path.join(netorca_path, "config.json")

            # Create a config.json file without metadata
            config_no_metadata = {
                "netorca_global": {"base_url": "https://example.com"},
                "services": [
                    {
                        "service_name": "service1",
                        "repository_url": "https://github.com/user/repo",
                    }
                ],
            }

            with open(config_path, "w") as f:
                json.dump(config_no_metadata, f)

            # Initialize the ServiceOwnerSubmission object and load the config
            service_owner_submission = ServiceOwnerSubmission(netorca_api_key=self.netorca_api_key)
            service_owner_submission.load_from_repository(temp_dir)

            # Check if the config was loaded correctly
            self.assertIsNotNone(service_owner_submission)
            self.assertEqual(service_owner_submission.config, config_no_metadata)
            self.assertIsNotNone(service_owner_submission.auth)

    def test_create_only_readme(self) -> None:
        # Create a temporary directory for the test
        with tempfile.TemporaryDirectory() as temp_dir:
            netorca_path = os.path.join(temp_dir, ".netorca")
            os.mkdir(netorca_path)

            with open(os.path.join(temp_dir, ".netorca", "config.json"), "w") as f:
                f.write('{"netorca_global": {"base_url": "https://example.com"}}')

            with open(os.path.join(temp_dir, ".netorca", "service1.json"), "w") as f:
                f.write('{"key": "value"}')

            # Initialize the ServiceOwnerSubmission object and load the config without readme
            service_owner_submission = ServiceOwnerSubmission(netorca_api_key=self.netorca_api_key)
            service_owner_submission.load_from_repository(temp_dir)
            self.assertIsNotNone(service_owner_submission)
            self.assertIsNotNone(service_owner_submission.auth)

            # Add readme to the existing submission
            with open(os.path.join(temp_dir, ".netorca", "service1.md"), "w") as f:
                f.write("# Service 1 Documentation")
            service_owner_submission.load_from_repository(temp_dir)

            # Check if the config was loaded correctly
            self.assertIsNotNone(service_owner_submission)

    @patch("requests.post")
    def test_submit_only_readme_ssl_error(self, mock_requests_post: MagicMock) -> None:
        # Simulate SSL error during README upload
        mock_requests_post.side_effect = SSLError("SSL certificate verify failed")

        with tempfile.TemporaryDirectory() as temp_dir:
            netorca_path = os.path.join(temp_dir, ".netorca")
            os.mkdir(netorca_path)

            # Write config file
            with open(os.path.join(netorca_path, "config.json"), "w") as f:
                f.write('{"netorca_global": {"base_url": "https://example.com"}}')

            # Write service file (initial load without README)
            with open(os.path.join(netorca_path, "service1.json"), "w") as f:
                f.write('{"service": {"title": "service1"}}')

            # Load the submission without README
            service_owner_submission = ServiceOwnerSubmission(netorca_api_key=self.netorca_api_key)
            service_owner_submission.load_from_repository(temp_dir)

            self.assertIsNotNone(service_owner_submission)
            self.assertIsNotNone(service_owner_submission.auth)

            # Now write the README
            with open(os.path.join(netorca_path, "service1.md"), "w") as f:
                f.write("# Service 1 Documentation")

            # Re-load the repo to include the README
            service_owner_submission.load_from_repository(temp_dir)

            # Patch validate method to always return valid
            with patch.object(service_owner_submission, "validate", return_value=(True, "")):
                # Patch the `post` method of the already-initialized auth object
                assert service_owner_submission.auth is not None
                with patch.object(service_owner_submission.auth, "post") as mock_auth_post:
                    mock_auth_post.return_value.status_code = 201
                    mock_auth_post.return_value.json.return_value = {"id": "123"}

                    # Call submit and expect SSL exception from README upload
                    with self.assertRaises(NetorcaException) as context:
                        service_owner_submission.submit()

                    self.assertIn(
                        "SSL Error during file upload: SSL certificate verify failed", context.exception.args[0]
                    )

    def test_pretty_print_errors(self) -> None:
        service_name = "test_service"
        errors = {
            "prop1": "Error message 1",
            "prop2": ["Error message 2", "Error message 3"],
            "nested": {
                "prop3": "Error message 4",
                "prop4": "Error message 5",
            },
        }

        with StringIO() as buf, redirect_stdout(buf):
            ServiceOwnerSubmission.pretty_print_errors(service_name, errors)
            output = buf.getvalue()

        # Check if service name and error messages are present in the output
        self.assertIn(service_name, output)
        self.assertIn("Error message 1", output)
        self.assertIn("Error message 2", output)
        self.assertIn("Error message 3", output)
        self.assertIn("Error message 4", output)
        self.assertIn("Error message 5", output)

    def test_read_json_file(self) -> None:
        # Test a non-existent file
        with self.assertRaises(NetorcaException):
            self.service_owner_submission.read_json_file("non_existent_file.json")

        # Test a valid JSON file
        valid_json_file_path = os.path.join(self.test_dir, "valid_json.json")
        with open(valid_json_file_path, "w") as f:
            f.write('{"key": "value"}')

        valid_data = self.service_owner_submission.read_json_file(valid_json_file_path)
        self.assertEqual(valid_data, {"key": "value"})

        # Test an invalid JSON file
        invalid_json_file_path = os.path.join(self.test_dir, "invalid_json.json")
        with open(invalid_json_file_path, "w") as f:
            f.write('{"key": "value",}')

        with self.assertRaises(NetorcaException):
            self.service_owner_submission.read_json_file(invalid_json_file_path)

    def test_get_service_id_by_name_valid(self) -> None:
        self.service_owner_submission.load_from_repository(self.test_dir)
        base_url = "https://example.com"
        # Ensure the mock post method is targeted for get_service_id_by_name
        with patch.object(self.service_owner_submission.auth, "get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {"results": [{"id": 123}]}

            service_id = self.service_owner_submission.get_service_id_by_name("service_name")
            self.assertEqual(service_id, 123)
            mock_get.assert_called_once_with(
                url=f"{base_url}{API_VERSION}/orcabase/serviceowner/services/?name=service_name"
            )


class TestCheckStatusCode(unittest.TestCase):
    def test_200_status_code(self) -> None:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "mock_data"}
        result = ServiceOwnerSubmission.check_status_code(mock_response)
        self.assertEqual(result, {"data": "mock_data"})

    def test_204_status_code(self) -> None:
        mock_response = MagicMock()
        mock_response.status_code = 204
        result = ServiceOwnerSubmission.check_status_code(mock_response)
        self.assertEqual(result, {"status": "deleted"})

    def test_404_status_code(self) -> None:
        mock_response = MagicMock()
        mock_response.status_code = 404
        with self.assertRaises(NetorcaNotFoundError):
            ServiceOwnerSubmission.check_status_code(mock_response)

    def test_400_status_code(self) -> None:
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"error": "Bad Request"}
        result = ServiceOwnerSubmission.check_status_code(mock_response)
        self.assertEqual(result, {"error": "Bad Request"})

    def test_401_status_code(self) -> None:
        mock_response = MagicMock()
        mock_response.status_code = 401
        with self.assertRaises(NetorcaAuthenticationError):
            ServiceOwnerSubmission.check_status_code(mock_response)

    def test_403_status_code(self) -> None:
        mock_response = MagicMock()
        mock_response.status_code = 403
        with self.assertRaises(NetorcaAuthenticationError):
            ServiceOwnerSubmission.check_status_code(mock_response)

    def test_502_status_code(self) -> None:
        mock_response = MagicMock()
        mock_response.status_code = 502
        with self.assertRaises(NetorcaGatewayError):
            ServiceOwnerSubmission.check_status_code(mock_response)

    def test_503_status_code(self) -> None:
        mock_response = MagicMock()
        mock_response.status_code = 503
        with self.assertRaises(NetorcaServerUnavailableError):
            ServiceOwnerSubmission.check_status_code(mock_response)

    def test_other_status_code(self) -> None:
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.content = b"Internal Server Error"
        with self.assertRaises(NetorcaAPIError):
            ServiceOwnerSubmission.check_status_code(mock_response)


if __name__ == "__main__":
    unittest.main()
