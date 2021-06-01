from app.models.credentials_model import Credentials
import tests.data as data
import os
import json


def test_create(credentials):
    assert credentials.data['aws_region'] == data.aws_region
    assert credentials.data['ssh_key_name'] == data.ssh_key_name
    assert credentials.data['cluster_id'] == data.cluster_id
    assert credentials.data['aws_access_key_id'] == data.aws_access_key_id
    assert credentials.data['aws_secret_access_key'] == data.aws_secret_access_key
    assert credentials.data['customer_ca_key_password'] == data.customer_ca_key_password
    assert credentials.data['crypto_officer_password'] == data.crypto_officer_password
    assert credentials.data['crypto_user_username'] == data.crypto_user_username
    assert credentials.data['crypto_user_password'] == data.crypto_user_password
    assert credentials.data['instance_id'] == data.instance_id


def test_read(credentials):
    credentials1 = Credentials.read(
        credentials_file_path=data.credentials_file_path)

    assert credentials.data == credentials1.data


def test_update(credentials):
    credentials.update(crypto_user_password='password2')

    assert credentials.data['crypto_user_password'] == 'password2'

    with open(data.credentials_file_path, 'r') as file:
        json_file_data = file.read()
    file_data = json.loads(json_file_data)

    assert file_data['crypto_user_password'] == 'password2'
