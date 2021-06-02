from app.models.hsm_model import HSM
import tests.data as data
import boto3


def test_create(create_hsm):
    stubber, client = create_hsm
    with stubber:
        hsm = HSM.create(
            cluster_id=data.cluster_id,
            availability_zone=data.azs[0],
            client=client
        )

    assert hsm.id == data.hsm_id
    assert hsm.cluster_id == data.cluster_id


def test_state(describe_cluster):
    stubber, client = describe_cluster
    with stubber:
        hsm = HSM(
            id=data.hsm_id,
            cluster_id=data.cluster_id,
            client=client
        )
        state = hsm.state

    assert state == 'ACTIVE'


def test_read(describe_cluster):
    stubber, client = describe_cluster
    with stubber:
        hsm = HSM(
            id=data.hsm_id,
            cluster_id=data.cluster_id,
            client=client
        )
        read_data = hsm.read()

    assert read_data['ClusterId'] == data.cluster_id
    assert read_data['HsmId'] == data.hsm_id


def test_destroy(delete_hsm):
    stubber, client = delete_hsm
    with stubber:
        hsm = HSM(
            id=data.hsm_id,
            cluster_id=data.cluster_id,
            client=client
        )
        resp = hsm.destroy()

    assert resp == data.hsm_id
