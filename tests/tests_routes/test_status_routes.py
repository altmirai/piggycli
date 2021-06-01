from click.testing import CliRunner
import tests.data as data
from app.routes import click
from app.models.credentials_model import read_env_vars
import os


def test_set_up_credentials(credentials):
    assert credentials.data == data.credentials_kwargs
    assert os.path.isdir(os.path.join(data.test_path, '.piggy'))
    assert os.path.exists(os.path.join(
        data.test_path, '.piggy', 'credentials.json'))
    assert read_env_vars()['PATH'] == data.test_path
