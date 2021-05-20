import json
import os


class CredentialsData:
    def __init__(self, **kwargs):
        self.aws_region = kwargs['aws_region']
        self.ssh_key_name = kwargs['ssh_key_name']
        self.cluster_id = kwargs['cluster_id']
        self.credentials_file_path = kwargs['credentials_file_path']
        self.aws_access_key_id = kwargs['aws_access_key_id']
        self.aws_secret_access_key = kwargs['aws_secret_access_key']
        self.customer_ca_key_password = kwargs['customer_ca_key_password']
        self.crypto_officer_password = kwargs['crypto_officer_password']
        self.crypto_user_username = kwargs['crypto_user_username']
        self.crypto_user_password = kwargs['crypto_user_password']


# def home_directory():
#     home_dir = os.environ.get('HOME')
#     return home_dir


# def path():
#     credentials_path = os.path.join(home_directory(), '.piggy')
#     return credentials_path


def get_credentials_data(**kwargs):
    credentials_data = CredentialsData(**kwargs)
    return credentials_data.__dict__


class Credentials:
    def __init__(self, credentials_file_path, data):
        self.credentials_file_path = credentials_file_path
        self.data = data

        self._create_dot_piggy_dir()
        self._write_credentials_to_file()
        self._set_credentials_path_env_var()

    @classmethod
    def create(cls, credentials_file_path, **kwargs):
        data = get_credentials_data(**kwargs)
        credentials = Credentials(
            credentials_file_path=credentials_file_path, data=data)
        return credentials

    @classmethod
    def create_from_file(cls, file_path):
        with open(file_path, 'r') as file:
            json_file_data = file.read()
        file_data = json.loads(json_file_data)
        data = get_credentials_data(**file_data)

        credentials_file_path = file_path.replace(os.path.join(
            '/', '.piggy', 'credentials.json'), '')

        credentials = Credentials(
            credentials_file_path=credentials_file_path, data=data)
        return credentials

    def read(self):
        return

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
        piggy_path = os.path.join(self.credentials_path, '.piggy')
        if os.path.isdir(piggy_path) is False:
            os.mkdir(piggy_path)
        return

    def _write_credentials_to_file(self):
        path = os.path.join(self.credentials_path,
                            '.piggy', 'credentials.json')
        with open(path, 'w') as file:
            file.write(json.dumps(self.data))
        return

    def _set_credentials_path_env_var(self):
        os.environ['PIGGY_CREDENTIALS_PATH'] = self.credentials_path
        return
