import tests.data as data
from tests.mocks import instance
from unittest.mock import patch
import boto3

import botocore.session
from botocore.stub import Stubber, ANY
import pytest


@pytest.fixture
def create_key_pair():
    client = botocore.session.get_session().create_client('ec2')
    stubber = Stubber(client)
    stubber.add_response(
        'create_key_pair',
        data.create_key_pair_resp,
        {'KeyName': ANY}
    )
    yield stubber, client


@pytest.fixture
def describe_clusters():
    client = botocore.session.get_session().create_client('cloudhsmv2')
    stubber = Stubber(client)
    stubber.add_response(
        'describe_clusters',
        data.describe_clusters_resp,
        {}
    )

    yield stubber, client


@pytest.fixture
def describe_cluster():
    client = botocore.session.get_session().create_client('cloudhsmv2')
    stubber = Stubber(client)
    stubber.add_response(
        'describe_clusters',
        data.describe_clusters_resp,
        {'Filters': {'clusterIds': [ANY]}}
    )

    yield stubber, client


@pytest.fixture
def create_hsm():
    client = botocore.session.get_session().create_client('cloudhsmv2')
    stubber = Stubber(client)
    stubber.add_response(
        'create_hsm',
        data.create_hsm_resp,
        {'ClusterId': ANY, 'AvailabilityZone': ANY}
    )

    yield stubber, client


@pytest.fixture
def delete_hsm():
    client = botocore.session.get_session().create_client('cloudhsmv2')
    stubber = Stubber(client)
    stubber.add_response(
        'delete_hsm',
        data.delete_hsm_resp,
        {'ClusterId': ANY, 'HsmId': ANY}
    )

    yield stubber, client


@pytest.fixture
def describe_instances():
    client = botocore.session.get_session().create_client('ec2')
    stubber = Stubber(client)
    stubber.add_response(
        'describe_instances',
        data.describe_instances_resp,
        {}
    )

    yield stubber, client


@pytest.fixture
def Mocked_Instance():
    with patch('app.models.instance_model.Instance', return_value=instance, autospec=True) as mocked_instance:
        yield mocked_instance


@pytest.fixture
def describe_key_pairs():
    pass

# @ pytest.fixture
# def ssh_key_ec2_test_all():
#     client = botocore.session.get_session().create_client('ec2')
#     with Stubber(client) as stubber:
#         stubber.add_response(
#             'describe_key_pairs',
#             t.ssh_key_describe_resp,
#             {}
#         )
#         yield client
