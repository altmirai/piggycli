from app.models.credentials_model import Credentials, set_env_var, read_env_vars
from tests.test_data import CredentialsData
import pytest
import os
import json

t = CredentialsData()

starting_env_vars = read_env_vars()


def set_up_credentials():
    credentials = Credentials.create(path=t.path, **t.credentials_kwargs)
    return credentials


def tear_down_credentials():
    os.remove(os.path.join(t.path, '.piggy', 'credentials.json'))
    os.rmdir(os.path.join(t.path, '.piggy'))
    set_env_var(var='PATH', value=None)
    for k, v in starting_env_vars.items():
        set_env_var(var=k, value=v)


def test_set_up_credentials():
    credentials = set_up_credentials()
    assert credentials.data == t.credentials_kwargs
    assert os.path.isdir(os.path.join(t.path, '.piggy'))
    assert os.path.exists(os.path.join(t.path, '.piggy', 'credentials.json'))
    assert read_env_vars()['PATH'] == t.path


def test_tear_down_credentials():
    tear_down_credentials()
    assert read_env_vars() == starting_env_vars
    assert os.path.exists(os.path.join(
        t.path, '.piggy', 'credentials.json')) is False
    assert os.path.isdir(os.path.join(t.path, '.piggy')) is False


def test_missing_attribute():
    data = t.credentials_kwargs
    deleted_key = 'crypto_user_password'
    del data[deleted_key]
    with pytest.raises(KeyError) as error:
        credentials = Credentials.create(path=t.path, **data)

    assert error.value.args[0] == deleted_key


def test_read():
    credentials = Credentials.create(path=t.path, **t.credentials_kwargs)
    credentials1 = Credentials.read(
        credentials_file_path=os.path.join(t.path, '.piggy', 'credentials.json'))

    assert credentials.data == credentials1.data

    os.remove(os.path.join(t.path, '.piggy', 'credentials.json'))
    os.rmdir(os.path.join(t.path, '.piggy'))
    set_env_var(var='PATH', value=None)


def test_update():
    credentials = Credentials.create(path=t.path, **t.credentials_kwargs)
    credentials.update(crypto_user_password='password2')

    assert credentials.data['crypto_user_password'] == 'password2'

    with open(os.path.join(t.path, '.piggy', 'credentials.json'), 'r') as file:
        json_file_data = file.read()
    file_data = json.loads(json_file_data)

    assert file_data['crypto_user_password'] == 'password2'

    os.remove(os.path.join(t.path, '.piggy', 'credentials.json'))
    os.rmdir(os.path.join(t.path, '.piggy'))
    set_env_var(var='PATH', value=None)
