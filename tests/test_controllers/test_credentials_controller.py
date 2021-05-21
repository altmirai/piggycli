from app.controllers.credentials_controller import CredentialsController
from app.models.credentials_model import Credentials, set_env_var
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
            'credentials_file_path': '/Users/kyle/.piggy/credentials',
            'aws_access_key_id': 'MLTnp708EbxF7/9iQT29juEw77rlN931wyjls6Vp',
            'aws_secret_access_key': 'AKIA3PBN5ZODEY7MAREB',
            'customer_ca_key_password': 'password1',
            'crypto_officer_password': 'password1',
            'crypto_user_username': 'cryptouser',
            'crypto_user_password': 'password1'

        }
    }


test_path = os.getcwd()


def clean_up():
    os.remove(os.path.join(test_path, '.piggy', 'credentials.json'))
    os.rmdir(os.path.join(test_path, '.piggy'))
    set_env_var(var='PATH', value=None)


def test_create():
    credentials = CredentialsController()
    data = test_data()['credentials']
    resp_json = credentials.create(path=test_path, **data)
    resp = json.loads(resp_json)

    assert data == resp['data']

    clean_up()


def test_show():
    data = test_data()['credentials']
    credentials = Credentials.create(path=test_path, **data)

    credentials_file_path = os.path.join(
        test_path, '.piggy', 'credentials.json')

    credentials = CredentialsController()
    resp_json = credentials.show(credentials_file_path=credentials_file_path)
    resp = json.loads(resp_json)

    assert data == resp['data']

    clean_up()


def test_update():
    data = test_data()['credentials']
    credentials = Credentials.create(path=test_path, **data)

    credentials_file_path = os.path.join(
        test_path, '.piggy', 'credentials.json')

    credentials = CredentialsController()
    resp_json = credentials.update(
        credentials_file_path=credentials_file_path, crypto_user_password="password2")
    resp = json.loads(resp_json)

    assert resp['data']['crypto_user_password'] == 'password2'

    clean_up()
