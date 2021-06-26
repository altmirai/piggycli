import json
import os


class CredentialsData:
    def __init__(self, **kwargs):
        self.base_path = kwargs['base_path']
        self.cluster_path = kwargs['cluster_path']
        self.aws_region = kwargs['aws_region']
        self.ssh_key_name = kwargs['ssh_key_name']
        self.cluster_id = kwargs['cluster_id']
        self.aws_access_key_id = kwargs['aws_access_key_id']
        self.aws_secret_access_key = kwargs['aws_secret_access_key']
        self.customer_ca_key_password = kwargs['customer_ca_key_password']
        self.crypto_officer_password = kwargs['crypto_officer_password']
        self.crypto_user_username = kwargs['crypto_user_username']
        self.crypto_user_password = kwargs['crypto_user_password']
        self.instance_id = kwargs['instance_id']


def get_credentials_data(**kwargs):
    credentials_data = CredentialsData(**kwargs)
    return credentials_data.__dict__


def set_env_var(var, value):
    with open('.env', 'r') as file:
        env_vars_json = file.read()

    env_vars = json.loads(env_vars_json)
    env_vars[var] = value

    with open('.env', 'w') as file:
        file.write(json.dumps(env_vars))

    return


def read_env_vars():
    with open('.env', 'r') as file:
        env_vars_json = file.read()
    env_vars = json.loads(env_vars_json)
    return env_vars


class Credentials:
    def __init__(self, credentials_file_path, data):
        self.credentials_file_path = credentials_file_path
        self.data = data

    @classmethod
    def create(cls, credentials_file_path, data):

        _write_credentials_to_file(
            credentials_file_path=credentials_file_path, data=data)

        set_env_var(var='PATH', value=credentials_file_path)

        credentials = Credentials(
            credentials_file_path=credentials_file_path, data=data)

        return credentials

    @classmethod
    def read(cls, credentials_file_path):
        with open(credentials_file_path, 'r') as file:
            json_file_data = file.read()
        file_data = json.loads(json_file_data)
        data = get_credentials_data(**file_data)
        credentials = Credentials(
            credentials_file_path=credentials_file_path, data=data)

        return credentials

    def update(self, **kwargs):
        credentials_data = CredentialsData(**self.data)
        for key, value in kwargs.items():
            setattr(credentials_data, key, value)
        self.data = credentials_data.__dict__
        _write_credentials_to_file(
            credentials_file_path=self.credentials_file_path, data=self.data)
        return self

    def delete(self):
        return


def _write_credentials_to_file(credentials_file_path, data):
    if os.path.exists(data['cluster_path']) is False:
        os.mkdir(data['cluster_path'])
    with open(credentials_file_path, 'w') as file:
        file.write(json.dumps(data))

    return
