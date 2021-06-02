from app.models.cluster_model import Cluster
import tests.data as data
#


def test_Cluster_all(describe_clusters):
    stubber, client = describe_clusters
    with stubber:
        clusters = Cluster.all(client=client)

    assert len(clusters) == 1
    assert clusters[0]['ClusterId'] == data.cluster_id


def test_hsms(describe_cluster):
    stubber, client = describe_cluster
    with stubber:
        cluster = Cluster(client=client, id=data.cluster_id)
        hsms = cluster.hsms

    assert hsms[0]['HsmId'] == data.hsm_id


def test_azs(describe_cluster):
    stubber, client = describe_cluster
    with stubber:
        cluster = Cluster(client=client, id=data.cluster_id)
        azs = cluster.azs

    assert azs == data.azs


def test_csr(describe_cluster):
    stubber, client = describe_cluster
    with stubber:
        cluster = Cluster(client=client, id=data.cluster_id)
        csr = cluster.csr

    assert csr == data.pem_csr


def test_state(describe_cluster):
    stubber, client = describe_cluster
    with stubber:
        cluster = Cluster(client=client, id=data.cluster_id)
        state = cluster.state

    assert state == 'ACTIVE'


def test_read(describe_cluster):
    stubber, client = describe_cluster
    with stubber:
        cluster = Cluster(client=client, id=data.cluster_id)
        read_data = cluster.read()

    assert read_data['ClusterId'] == data.cluster_id


def test_initialize():
    pass


def test_activate():
    pass
