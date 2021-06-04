import tests.data as data
from tests.mocks import instance
from unittest.mock import patch

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
def list_buckets_true():
    client = botocore.session.get_session().create_client(
        's3', region_name=data.aws_region)
    stubber = Stubber(client)
    stubber.add_response(
        'list_buckets',
        data.list_buckets_true_resp,
        {}
    )

    yield stubber, client


@pytest.fixture
def list_buckets_false():
    client = botocore.session.get_session().create_client(
        's3', region_name=data.aws_region)
    stubber = Stubber(client)
    stubber.add_response(
        'list_buckets',
        data.list_buckets_false_resp,
        {}
    )

    yield stubber, client


@pytest.fixture
def aws_create_bucket():
    client = botocore.session.get_session().create_client(
        's3', region_name=data.aws_region)
    stubber = Stubber(client)
    stubber.add_response(
        'create_bucket',
        data.create_bucket_resp,
        {'Bucket': ANY, 'CreateBucketConfiguration': ANY}
    )

    yield stubber, client


@pytest.fixture
def put_object():
    client = botocore.session.get_session().create_client(
        's3', region_name=data.aws_region)
    stubber = Stubber(client)
    stubber.add_response(
        'put_object',
        data.put_object_resp,
        {'Body': ANY, 'Bucket': ANY, 'Key': ANY}
    )

    yield stubber, client


@pytest.fixture
def list_objects():
    client = botocore.session.get_session().create_client(
        's3', region_name=data.aws_region)
    stubber = Stubber(client)
    stubber.add_response(
        'list_objects',
        data.list_objects_resp,
        {'Bucket': ANY}
    )

    yield stubber, client
