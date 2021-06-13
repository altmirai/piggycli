from tests.mocks import address_controller
from app.routes import click

from click.testing import CliRunner
import tests.data as data
from unittest.mock import patch
import time
import json
import os
import re


def runner_stdout_to_dict(stdout):
    stdout = re.split('\n|, |: ', stdout)
    stdout = [x for x in stdout if x]
    stdout = {stdout[i]: stdout[i + 1] for i in range(0, len(stdout), 2)}
    return stdout


@patch('app.routes.click.AddressController', return_value=address_controller, autospec=True)
def test_list(mock_AddressController, credentials):
    runner = CliRunner()
    result = runner.invoke(click.address, ['list'])
    stdout = runner_stdout_to_dict(stdout=result.stdout)

    assert stdout['id'] == data.address_id
    assert stdout['address'] == data.address
    assert stdout['confirmed_balance'] == str(data.confirmed_balance)
    assert stdout['spent'] == str(data.spent)
