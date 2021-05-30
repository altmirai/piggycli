from app.controllers.credentials_controller import CredentialsController
import os
import json


def test_show(credentials, test_data):

    credentials_file_path = os.path.join(
        test_data.test_path, '.piggy', 'credentials.json')

    credentials = CredentialsController()
    resp_json = credentials.show(credentials_file_path=credentials_file_path)
    resp = json.loads(resp_json)

    assert test_data.credentials_kwargs == resp['data']


def test_update(credentials, test_data):

    credentials_file_path = os.path.join(
        test_data.test_path, '.piggy', 'credentials.json')

    credentials = CredentialsController()
    resp_json = credentials.update(
        credentials_file_path=credentials_file_path, crypto_user_password="password2")
    resp = json.loads(resp_json)

    assert resp['data']['crypto_user_password'] == 'password2'


def test_write_to_file(ssh_key, test_data):
    ssh_key_file = ssh_key.write_to_file(
        cluster_id=test_data.cluster_id, path=test_data.test_path)

    assert os.path.exists(ssh_key_file)

    with open(ssh_key_file, 'r') as file:
        ssh_key_material = file.read()

    assert ssh_key_material == test_data.KeyMaterial
