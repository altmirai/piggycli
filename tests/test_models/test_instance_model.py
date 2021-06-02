from app.models.instance_model import Instance
from tests.mocks import instance
import tests.data as data
from unittest.mock import patch, Mock
import boto3


def test_all(describe_instances):
    stubber, client = describe_instances
    with stubber:
        resp = Instance.all(client=client)

    assert resp[0]['InstanceId'] == data.instance_id
    assert resp[0]['KeyName'] == data.ssh_key_name


def test_public_ip_address(Mocked_Instance):
    instance = Mocked_Instance(id=data.instance_id, resource=data.resource)

    assert instance.public_ip_address == data.public_ip_address


def test_state(Mocked_Instance):
    instance = Mocked_Instance(id=data.instance_id, resource=data.resource)

    assert instance.state == 'running'


def test_install_packages(Mocked_Instance):
    instance = Mocked_Instance(id=data.instance_id, resource=data.resource)
    pass


def test_start(Mocked_Instance):
    instance = Mocked_Instance(id=data.instance_id, resource=data.resource)
    pass


def test_stop(Mocked_Instance):
    instance = Mocked_Instance(id=data.instance_id, resource=data.resource)
    pass
