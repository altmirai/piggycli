from click.testing import CliRunner
import tests.data as data
from app.routes import click
from app.models.credentials_model import read_env_vars
import os


def test_set_up_credentials(credentials):
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
    assert os.path.isdir(os.path.join(data.test_path, '.piggy'))
    assert os.path.exists(os.path.join(
        data.test_path, '.piggy', 'credentials.json'))
    assert read_env_vars()['PATH'] == data.test_path
