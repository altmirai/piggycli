from app.models.credentials_model import Credentials, set_env_var
import pytest
import os
import json


def test_data():
    return {
        'credentials':
        {
            'aws_region': 'us-east-2',
            'ssh_key_name': 'Piggy_SSH_Key_91e285d1',
            "cluster_id": "cluster-e6kouniaxtf",
            'aws_access_key_id': 'MLTnp708EbxF7/9iQT29juEw77rlN931wyjls6Vp',
            'aws_secret_access_key': 'AKIA3PBN5ZODEY7MAREB',
            'customer_ca_key_password': 'password1',
            'crypto_officer_password': 'password1',
            'crypto_user_username': 'cryptouser',
            'crypto_user_password': 'password1'
        },
        'bad_file': {
            'ssh_key_name': 'Piggy_SSH_Key_91e285d1',
            "cluster_id": "cluster-e6kouniaxtf",
            'aws_access_key_id': 'MLTnp708EbxF7/9iQT29juEw77rlN931wyjls6Vp',
            'aws_secret_access_key': 'AKIA3PBN5ZODEY7MAREB',
            'customer_ca_key_password': 'password1',
            'crypto_officer_password': 'password1',
            'crypto_user_username': 'cryptouser',
            'crypto_user_password': 'password1'

        }
    }


test_path = os.getcwd()


def test_credentials_data():
    data = test_data()['credentials']
    credentials = Credentials.create(path=test_path, **data)

    assert credentials.data == data

    os.remove(os.path.join(test_path, '.piggy', 'credentials.json'))
    os.rmdir(os.path.join(test_path, '.piggy'))
    set_env_var(var='PATH', value=None)


def test_create_dot_piggy_dir():
    data = test_data()['credentials']
    credentials = Credentials.create(path=test_path, **data)

    assert os.path.isdir(os.path.join(test_path, '.piggy'))

    os.remove(os.path.join(test_path, '.piggy', 'credentials.json'))
    os.rmdir(os.path.join(test_path, '.piggy'))
    set_env_var(var='PATH', value=None)


def test_write_credentials_to_file():
    data = test_data()['credentials']
    credentials = Credentials.create(path=test_path, **data)

    assert os.path.exists(os.path.join(
        test_path, '.piggy', 'credentials.json'))

    with open(os.path.join(test_path, '.piggy', 'credentials.json'), 'r') as file:
        json_file_data = file.read()
    file_data = json.loads(json_file_data)

    assert file_data == data

    os.remove(os.path.join(test_path, '.piggy', 'credentials.json'))
    os.rmdir(os.path.join(test_path, '.piggy'))
    set_env_var(var='PATH', value=None)


def test_missing_attribute():
    data = test_data()['credentials']
    deleted_key = 'crypto_user_password'
    del data[deleted_key]
    with pytest.raises(KeyError) as error:
        credentials = Credentials.create(path=test_path, **data)

    assert error.value.args[0] == deleted_key


def test_read():
    data = test_data()['credentials']
    credentials = Credentials.create(path=test_path, **data)
    credentials1 = Credentials.read(
        credentials_file_path=os.path.join(test_path, '.piggy', 'credentials.json'))

    assert credentials.data == credentials1.data

    os.remove(os.path.join(test_path, '.piggy', 'credentials.json'))
    os.rmdir(os.path.join(test_path, '.piggy'))
    set_env_var(var='PATH', value=None)


def test_bad_file():
    data = test_data()['bad_file']
    with pytest.raises(KeyError) as error:
        credentials = Credentials.create(path=test_path, **data)

    assert error.value.args[0] == 'aws_region'


def test_update():
    data = test_data()['credentials']
    credentials = Credentials.create(path=test_path, **data)
    credentials.update(crypto_user_password='password2')

    assert credentials.data['crypto_user_password'] == 'password2'

    with open(os.path.join(test_path, '.piggy', 'credentials.json'), 'r') as file:
        json_file_data = file.read()
    file_data = json.loads(json_file_data)

    assert file_data['crypto_user_password'] == 'password2'

    os.remove(os.path.join(test_path, '.piggy', 'credentials.json'))
    os.rmdir(os.path.join(test_path, '.piggy'))
    set_env_var(var='PATH', value=None)
