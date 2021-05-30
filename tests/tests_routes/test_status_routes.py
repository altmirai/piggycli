from click.testing import CliRunner
from app.routes import click
from app.models.credentials_model import read_env_vars
import os


def test_set_up_credentials(credentials, test_data):
    assert credentials.data == test_data.credentials_kwargs
    assert os.path.isdir(os.path.join(test_data.test_path, '.piggy'))
    assert os.path.exists(os.path.join(
        test_data.test_path, '.piggy', 'credentials.json'))
    assert read_env_vars()['PATH'] == test_data.test_path
