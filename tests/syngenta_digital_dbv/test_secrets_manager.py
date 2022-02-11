import os
import unittest
from unittest import mock

from botocore.exceptions import ClientError

from syngenta_digital_dbv.common import config

PATCH_DICT = {
    "AWS_DEFAULT_REGION": "us-east-2"
}


class TestConfigSecretParam(unittest.TestCase):

    @mock.patch.dict(os.environ, PATCH_DICT)
    def setUp(self):
        self.Config = config.Config(
            endpoint="endpoint",
            database="database",
            user="user",
            password="passwor",
            port="port",
            reset_root=False
        )

    @mock.patch.dict(os.environ, PATCH_DICT)
    def test_get_secret_param(self):
        self.Config.secrets_param = "my-secret-param"
        self.Config.secrets_manager = mock.MagicMock()
        self.Config.secrets_manager.get_secret_value.return_value = {"SecretString": '{"name": "my_value"}'}
        self.assertEqual(self.Config._Config__get_param(), {"name": "my_value"})

    @mock.patch.dict(os.environ, PATCH_DICT)
    def test_upload_config_secret_manager_update(self):
        self.Config.secrets_param = "my-secret-param"
        self.Config.ssm = mock.MagicMock()
        self.Config.secrets_manager = mock.MagicMock()

        self.Config.random_password = "random password"

        self.Config.secrets_manager = mock.MagicMock()
        self.Config.secrets_manager.get_secret_value.return_value = {"SecretString": '{"name": "my_value"}'}

        self.Config._Config__get_param()
        self.Config.upload_config()

        self.Config.ssm.assert_not_called()

        self.Config.secrets_manager.update_secret.assert_called_with(
            SecretId='my-secret-param',
            SecretString='{"endpoint": "endpoint", "database": "database", "user": "user", "password": "random password", "port": "port"}'
        )

        self.Config.secrets_manager.create_secret.assert_not_called()

    @mock.patch.dict(os.environ, PATCH_DICT)
    def test_upload_config_secret_manager_create(self):
        self.Config.secrets_param = "my-secret-param"
        self.Config.ssm = mock.MagicMock()
        self.Config.secrets_manager = mock.MagicMock()

        self.Config.random_password = "random password"

        self.Config.secrets_manager = mock.MagicMock()
        self.Config.secrets_manager.get_secret_value.side_effect = ClientError(
            {"Error": {"Code": 'ResourceNotFoundException'}}, 'test')

        self.Config._Config__get_param()
        self.Config.upload_config()

        self.Config.ssm.assert_not_called()

        self.Config.secrets_manager.create_secret.assert_called_with(
            Name='my-secret-param',
            SecretString='{"endpoint": "endpoint", "database": "database", "user": "user", "password": "random password", "port": "port"}'
        )

        self.Config.secrets_manager.update_secret.assert_not_called()
