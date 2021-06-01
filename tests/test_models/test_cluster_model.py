from app.models.cluster_model import Cluster
import tests.data as data


def test_Cluster_all(describe_clusters):
    stubber, client = describe_clusters
    with stubber:
        clusters = Cluster.all(client=client)

    assert len(clusters) == 1
    assert clusters[0]['ClusterId'] == data.cluster_id
