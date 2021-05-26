from click.testing import CliRunner
from app.routes import click
from app.models.credentials_model import Credentials, set_env_var, read_env_vars
from tests.test_data import CredentialsData
import os

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


def test_status():
    set_up_credentials()
    runner = CliRunner()
    result = runner.invoke(click.status)

    assert result.exit_code == 0
    tear_down_credentials()
