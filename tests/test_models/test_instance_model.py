from app.models.instance_model import Instance
import tests.data as data
import boto3


def test_all(describe_instances):
    stubber, client = describe_instances
    with stubber:
        resp = Instance.all(client=client)

    assert resp[0]['InstanceId'] == data.instance_id
    assert resp[0]['KeyName'] == data.ssh_key_name
