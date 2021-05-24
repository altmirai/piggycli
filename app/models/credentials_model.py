import json
import os


class CredentialsData:
    def __init__(self, **kwargs):
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
        self.path = self.credentials_file_path.replace(os.path.join(
            '/', '.piggy', 'credentials.json'), '')
        self.data = data
        self._write_credentials_to_file()
        set_env_var(var='PATH', value=self.path)

    @classmethod
    def create(cls, **kwargs):
        path = kwargs['path']
        data = get_credentials_data(**kwargs)
        credentials_file_path = os.path.join(
            path, '.piggy', 'credentials.json')
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
        self._write_credentials_to_file()
        return self

    def delete(self):
        return

    def _create_dot_piggy_dir(self):
        piggy_path = os.path.join(self.path, '.piggy')
        if os.path.isdir(piggy_path) is False:
            os.mkdir(piggy_path)
        return

    def _write_credentials_to_file(self):
        self._create_dot_piggy_dir()
        with open(self.credentials_file_path, 'w') as file:
            file.write(json.dumps(self.data))
        return
