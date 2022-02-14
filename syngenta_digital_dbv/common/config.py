import json
import secrets
from botocore.exceptions import ClientError
import boto3


class Config:

    def __init__(self, **kwargs):
        self.endpoint = kwargs['endpoint']
        self.database = kwargs['database']
        self.user = kwargs['user']
        self.password = kwargs['password']
        self.port = kwargs['port']
        self.reset_root = kwargs['reset_root']
        self.seed = kwargs.get('seed', False)
        self.param_found = False
        self.random_password = secrets.token_urlsafe(16)

        self.ssm = boto3.client('ssm')
        self.ssm_param = kwargs.get('ssm_param')

        self.secrets_manager = boto3.client('secretsmanager')
        self.secrets_param = kwargs.get('secrets_param')

        assert not (self.ssm_param and self.secrets_param), "Must only specify ssm or secret manager parameters."

    def _build_config_existing(self):
        return {
            'endpoint': self.endpoint,
            'database': self.database,
            'user': self.user,
            'password': self.password,
            'port': self.port,
        }

    def _build_config_new(self):
        return {
            'endpoint': self.endpoint,
            'database': self.database,
            'user': self.user,
            'password': self.random_password,
            'port': self.port,
        }

    def get_config(self):
        config = self.__get_param()
        if config:
            return config
        return self._build_config_existing()

    def upload_config(self):
        if self.ssm_param:
            if not self.param_found:
                self.ssm.put_parameter(
                    Name=self.ssm_param,
                    Type='SecureString',
                    Value=json.dumps(self._build_config_new())
                )

        elif self.secrets_param:
            if not self.param_found:
                self.secrets_manager.create_secret(
                    Name=self.secrets_param,
                    SecretString=json.dumps(self._build_config_new())
                )
            else:
                self.secrets_manager.update_secret(
                    SecretId=self.secrets_param,
                    SecretString=json.dumps(self._build_config_new())
                )

    def __get_param(self):
        if self.ssm_param:
            try:
                result = self.ssm.get_parameter(Name=self.ssm_param, WithDecryption=True)
                ssm_config = json.loads(result['Parameter']['Value'])
            except self.ssm.exceptions.ParameterNotFound:
                return None
            else:
                self.param_found = True
                return ssm_config

        elif self.secrets_param:
            try:
                result = self.secrets_manager.get_secret_value(SecretId=self.secrets_param)
                secrets_config = json.loads(result['SecretString'])
            except ClientError as e:
                if e.response['Error']['Code'] == 'ResourceNotFoundException':
                    return None
                else:
                    raise e
            else:
                self.param_found = True
                return secrets_config

        return None
