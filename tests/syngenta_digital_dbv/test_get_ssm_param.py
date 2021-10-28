import unittest
from unittest import mock
import json

from moto import mock_ssm

from syngenta_digital_dbv.common.config import Config


class TestConfig(unittest.TestCase):

    def setUp(self):
        self.Config = Config(
            endpoint="endpoint",
            database="database",
            user="user",
            password="passwor",
            port="port",
            reset_root=False
        )

    @mock_ssm
    def test_get_ssm_param(self):
        self.Config.ssm_param = True

        self.Config.ssm = mock.MagicMock()
        self.Config.ssm.get_parameter.return_value = {"Parameter": {"Value": '{"name": "my_value"}'}}

        self.assertEqual(self.Config._Config__get_ssm_param(), {"name": "my_value"})

    def test_build_secret(self):
        actual = self.Config.build_secret()

        expected = json.dumps(
            {
                "host": self.Config.endpoint,
                "database": self.Config.database,
                "username": self.Config.user,
                "password": self.Config.random_password,
                "port": self.Config.port
            }
        )

        self.assertEqual(expected, actual)
