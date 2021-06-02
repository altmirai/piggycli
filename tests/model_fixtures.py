from app.models.credentials_model import Credentials
from app.models.cluster_model import Cluster
import tests.data as data
from tests.mocks import tf
import os
from unittest.mock import patch
import pytest


@pytest.fixture
def credentials():
    credentials = Credentials.create(
        path=data.test_path,
        aws_region=data.aws_region,
        ssh_key_name=data.ssh_key_name,
        cluster_id=data.cluster_id,
        instance_id=data.instance_id,
        aws_access_key_id=data.aws_access_key_id,
        aws_secret_access_key=data.aws_secret_access_key,
        customer_ca_key_password=data.customer_ca_key_password,
        crypto_officer_password=data.crypto_officer_password,
        crypto_user_username=data.crypto_user_username,
        crypto_user_password=data.crypto_user_password
    )
    yield credentials
    os.remove(os.path.join(data.test_path, '.piggy', 'credentials.json'))
    os.rmdir(os.path.join(data.test_path, '.piggy'))


@pytest.fixture
def cluster():
    cluster = Cluster(client=data.cloudhsmv2, id=data.cluster_id)
    yield cluster
    os.remove(os.path.join(data.test_path, '.piggy', 'credentials.json'))
    os.rmdir(os.path.join(data.test_path, '.piggy'))


@pytest.fixture
def hsm():
    pass
