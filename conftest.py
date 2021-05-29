from app.models.credentials_model import Credentials, read_env_vars, set_env_var
import pytest
import os


class CredentialsData:
    def __init__(self):
        self.test_path = '/Users/kyle/GitHub/alt-piggy-bank/piggy-cli/tests/test_files'
        self.production_path = '/Users/kyle/GitHub/alt-piggy-bank/piggy-cli/production_files'
        self.aws_region = 'us-east-2'
        self.ssh_key_name = 'Piggy_SSH_Key_cf865bae'
        self.cluster_id = 'cluster-lbtkdldygfh'
        self.instance_id = 'i-051bdb2ae099024a5'
        self.aws_access_key_id = 'AKIA5YNNN4JH6JDQF5XH'
        self.aws_secret_access_key = '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'
        self.customer_ca_key_password = 'password1'
        self.crypto_officer_password = 'password1'
        self.crypto_user_username = 'cryptouser'
        self.crypto_user_password = 'password1'

    @property
    def credentials_kwargs(self):
        data = self.__dict__
        arguments = {}
        for k, v in data.items():
            if k != 'test_path' and k != 'production_path':
                arguments[k] = v
        return arguments


t = CredentialsData()


def pytest_sessionstart(session):
    set_env_var(var='PATH', value=t.test_path)


@pytest.fixture
def credentials():
    credentials = Credentials.create(path=t.test_path, **t.credentials_kwargs)
    yield credentials
    os.remove(os.path.join(t.test_path, '.piggy', 'credentials.json'))
    os.rmdir(os.path.join(t.test_path, '.piggy'))


@pytest.fixture
def test_data():
    return CredentialsData()


def pytest_sessionfinish(session, exitstatus):
    set_env_var(var='PATH', value=t.production_path)


# def tear_down_credentials():
#     for k, v in starting_env_vars.items():
#         set_env_var(var=k, value=v)


# def test_set_up_credentials():
#     credentials = set_up_credentials()
#     assert credentials.data == t.credentials_kwargs
#     assert os.path.isdir(os.path.join(t.path, '.piggy'))
#     assert os.path.exists(os.path.join(t.path, '.piggy', 'credentials.json'))
#     assert read_env_vars()['PATH'] == t.path


# def test_tear_down_credentials():
#     tear_down_credentials()
#     assert read_env_vars() == starting_env_vars
#     assert os.path.exists(os.path.join(
#         t.path, '.piggy', 'credentials.json')) is False
#     assert os.path.isdir(os.path.join(t.path, '.piggy')) is False
