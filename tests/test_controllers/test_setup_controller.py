import app.controllers.setup_controller as setup
from tests.data.mocks import tf, ssh_key, cluster, instance, hsm, certs
import tests.data as data

from unittest.mock import patch
import os


@patch('app.controllers.setup_controller.os.system', return_value=0, autospec=True)
def test_check_packages(mock_system):
    assert setup._check_packages(packages=['aws', 'terraform'])


def test_get_ssh_key(create_key_pair):
    stubber, client = create_key_pair
    with stubber:
        key = setup._get_ssh_key(client=client)
    assert key.name == data.create_key_pair_resp['KeyName']
    assert key.material == data.create_key_pair_resp['KeyMaterial']


@patch('app.controllers.setup_controller.Tf', return_value=tf, autospec=True)
def test_build_infrastructure(mock_Tf):
    resp = setup._build_infrastructure(
        region=data.aws_region,
        ssh_key_name=data.ssh_key_name,
        aws_access_key_id=data.aws_access_key_id,
        aws_secret_access_key=data.aws_secret_access_key
    )
    assert resp == tf.build()


@patch('app.controllers.setup_controller.Cluster', return_value=cluster, autospec=True)
def test_cluster(mock_Cluster):
    cluster = setup._cluster(
        client=data.cloudhsmv2, id=data.cluster_id)
    assert cluster.id == data.cluster_id


def test_set_path():
    resp = setup._set_path(path=os.path.join(data.test_path, cluster.id))
    assert resp == '/Users/kyle/GitHub/alt-piggy-bank/piggy-cli/tests/test_files/cluster-lbtkdldygfh'


test_setup_vars = {
    'aws_region': data.aws_region,
    'aws_access_key_id': data.aws_access_key_id,
    'aws_secret_access_key': data.aws_secret_access_key,
    'ec2': data.ec2,
    'cloudhsmv2': data.cloudhsmv2,
    'resource': data.resource,
    'path': data.test_path,
    'customer_ca_key_password': data.customer_ca_key_password,
    'crypto_officer_password': data.crypto_officer_password,
    'crypto_user_username': data.crypto_user_username,
    'crypto_user_password': data.crypto_user_password
}


@patch('app.controllers.setup_controller._get_ssh_key', return_value=ssh_key, autospec=True)
@patch('app.controllers.setup_controller._build_infrastructure', return_value=data.build_infra_resp, autospec=True)
@patch('app.controllers.setup_controller._cluster', return_value=cluster, autospec=True)
@patch('app.controllers.setup_controller._instance', return_value=instance, autospec=True)
@patch('app.controllers.setup_controller._hsm', return_value=hsm, autospec=True)
@patch('app.controllers.setup_controller._certs', return_value=certs, autospec=True)
@patch('app.controllers.setup_controller._upload_customer_ca_cert', return_value=True, autospec=True)
@patch('app.controllers.setup_controller._initialize_cluster', return_value=True, autospec=True)
@patch('app.controllers.setup_controller._activate_cluster', return_value=True, autospec=True)
def test_run(*args):
    test_setup = setup.Setup(**test_setup_vars)
    resp = test_setup.run()
    assert resp['cluster_id'] == cluster.id
    assert resp['ssh_key_name'] == ssh_key.name
    assert resp['ssh_key_pem'] == ssh_key.material
    assert resp['instance_id'] == instance.id

    cluster_folder = os.path.join(data.test_path, cluster.id)
    files = os.listdir(cluster_folder)
    for file in files:
        os.remove(os.path.join(cluster_folder, file))
    os.rmdir(cluster_folder)
