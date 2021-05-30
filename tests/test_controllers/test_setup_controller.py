import app.controllers.setup_controller as setup
from app.models.ssh_key_model import SSHKey
from conftest import CredentialsData
import botocore.session
from botocore.stub import Stubber, ANY
import os
from unittest.mock import patch, Mock
import boto3
from tests.mocks import tf, ssh_key, cluster, instance, hsm, certs

t = CredentialsData()

test_setup_vars = {
    'aws_region': 'us-east-2',
    'aws_access_key_id': 'AKIA3PBN5ZODEY7MAREB',
    'aws_secret_access_key': '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',
    'ec2': botocore.session.get_session().create_client('ec2'),
    'cloudhsmv2': botocore.session.get_session().create_client('cloudhsmv2'),
    'resource': boto3.resource('ec2'),
    'path': '/Users/kyle/GitHub/alt-piggy-bank/piggy-cli/tests/test_files',
    'customer_ca_key_password': 'password1',
    'crypto_officer_password': 'password1',
    'crypto_user_username': 'cryptosuer',
    'crypto_user_password': 'password'
}

create_key_pair_resp = {'KeyFingerprint': '08:c9:28:e5:24:38:d5:ef:9b:a1:76:22:9f:00:0c:eb:47:16:59:cd', 'KeyMaterial': '-----BEGIN RSA PRIVATE KEY-----\nMIIEpQIBAAKCAQEAkOrCB3e0Fj/Cv797THZn5YgxIPywNdlg284rMSshrLl8QC83\n0ck0K9CP3Y+rCuHGx7t/2tCtl66uKlwOPFvWGDi+akonkUeVqnV8U1z5jNhI8SwY\niXtcFX0twIGHaaxYQrWZvOUAnmE8JUGd7Pysy4Sy7/ZEldXwEN3fN2NIPRnQwii7\nS5tv573C2am2MMXtwEKtQi3uWgPu//maXqoM0/PuxTDk9DUKnN88nvNBMoTlHr1P\nl9QsHMPyXvJ/+TTPdVybXwMvv1KgCMeGid43CPu7SFa8trx9DuvSY03TwYyhZIp6\nMsPZot6pu+opRXgF7SkSpp/+ABPoA836sPF0+wIDAQABAoIBAAESi68Mdru3axSK\nMTpmoewz7tEkrZUob6wQwYcSn6QslzvOXaZiy80LNRVZq9VfyF3QCGkxJCe8NjPA\nDKbrsxDo0pfsxpAvrG7fgbUIOhyNuTR3tBLIY+0QyRbknoDsspaDy4h3VWLWq2BH\nNQj88bZr2/skomtNcwJc8frx9CXnmR1erB8d7UybKFiYL4ggM/MVQbdn66ZpmKCK\naZ774lbgdiwp8YZp1ANFw7zBr1MTqXKLmghtYZoornRUVk2c3OPUII62jmarUaqn\nKL+q2198j0axDsmFCAALTbmxjo//XWxwTeaRNwsi0hqeENEy1ywtidn1A8eHJaOi\nvGlV6LkCgYEA4rabAGB7OQTunGj6BiQBN8AnG/1B77HBA/VRy3YUHdPaBYtldLuX\nZrQKuE3l13uX0whXr+BQVDtDiegocz4r41/MR9uUoQFHnsL25D+A44xveT2scTHm\nBHpUprq8ti4XyNJGpnZXSxQCRzhcGnJItvfOaQWW+slEnR4RUuWCdjUCgYEAo6Mn\nmT+NyNCfJHWvF951fvRi7liktRzIcIL7Hu4gDkTTJ7U/Ms3OgQTsQ6VIfNeotAYC\nFe/GVb+SB91MnnCFwPbwt1vIwdLGvKtAUq3OQvE8Jv1LCC3XQJcRv/tJuP6lLz1t\nWNF59Uz0Ar6VN9tIctdribKGP6Dxg32OLlrV5G8CgYEAotnQlYC4gsjMLYYqsuaC\nCW35qd1N08O3hgRd8OysnpBi98Cd7DAkHR4O5TzvcM3SzUAc3LUgfqDjbthY1g8+\nr2FM+AD+zniA3cXmWyZSiyGBoXFvwQ+6zlShIfLZQ3PwmcyR+1jec4u35zjQ0B5v\npR50InRlc1fH9aR3hThfclECgYEAh+bv80GqIpbJJQGsKnmyQX78TxFFsbk26uKN\nZxHDg7Y7XCYWV74/fD23bzLtMen2DZVT1B4wLXUN9gQgJxIys6EjKFVNNVQ1g+oC\nYOhCfqxVFdiVoTRZKiaNMlGj18V9MO+mSfangEep/EGGMj6nO+GXSWQARQYIrvju\nxabhL3cCgYEAlPAbQgqljbfs6pIG5eEKHNLXaCZxFeZDQ+PQ9CYBsCL0nPo0e1iw\nHNFx2A/BN0hEZxiOO0LnDV5paFhAd+rFhSvxdgwhOBvxU1TDwcNCoyqpbJ57BB3e\n5d+ShkCu0K3LbKn65ZAtvJCB9yleu5VUIt6i+q/aaPLcWTcf+YxVDfM=\n-----END RSA PRIVATE KEY-----',
                        'KeyName': 'Piggy_SSH_Key_0194afd1', 'KeyPairId': 'key-0a070814c64fa0e65', 'ResponseMetadata': {'RequestId': '56d9520a-80e8-4603-9a92-6a78c3ef42ca', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '56d9520a-80e8-4603-9a92-6a78c3ef42ca', 'cache-control': 'no-cache, no-store', 'strict-transport-security': 'max-age=31536000; includeSubDomains', 'content-type': 'text/xml;charset=UTF-8', 'content-length': '2103', 'vary': 'accept-encoding', 'date': 'Sat, 22 May 2021 00:23:15 GMT', 'server': 'AmazonEC2'}, 'RetryAttempts': 0}}


build_infra_resp = {'cluster_id': 'cluster-lbtkdldygfh',
                    'vpc_id': 'vpc-06f745fe81ec3c1a8', 'instance_id': 'i-051bdb2ae099024a5'}


@patch('app.controllers.setup_controller.os.system', return_value=0, autospec=True)
def test_check_packages(mock_system):
    assert setup._check_packages(packages=['aws', 'terraform'])


def test_get_ssh_key():
    client = botocore.session.get_session().create_client('ec2')
    with Stubber(client) as stubber:
        stubber.add_response(
            'create_key_pair', create_key_pair_resp, {'KeyName': ANY})
        key = setup._get_ssh_key(client=client)
    assert key.name == create_key_pair_resp['KeyName']
    assert key.material == create_key_pair_resp['KeyMaterial']


@patch('app.controllers.setup_controller.Tf', return_value=tf, autospec=True)
def test_build_infrastructure(mock_Tf):
    resp = setup._build_infrastructure(
        region=t.aws_region,
        ssh_key_name=t.ssh_key_name,
        aws_access_key_id=t.aws_access_key_id,
        aws_secret_access_key=t.aws_secret_access_key
    )
    assert resp == tf.build()


@patch('app.controllers.setup_controller.Cluster', return_value=cluster, autospec=True)
def test_cluster(mock_Cluster):
    cluster = setup._cluster(
        client=test_setup_vars['cloudhsmv2'], id=t.cluster_id)
    assert cluster.id == t.cluster_id


def test_set_path():
    resp = setup._set_path(path=t.test_path, cluster=cluster)
    assert resp == '/Users/kyle/GitHub/alt-piggy-bank/piggy-cli/tests/test_files/cluster-lbtkdldygfh'


@patch('app.controllers.setup_controller._get_ssh_key', return_value=ssh_key, autospec=True)
@patch('app.controllers.setup_controller._build_infrastructure', return_value=build_infra_resp, autospec=True)
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

    os.remove(os.path.join(
        test_setup_vars['path'], cluster.id, 'customerCA.key'))
    os.remove(os.path.join(
        test_setup_vars['path'], cluster.id, 'customerCA.crt'))
    os.remove(os.path.join(
        test_setup_vars['path'], cluster.id, f'{cluster.id}_ClusterCSR.csr'))
    os.remove(os.path.join(
        test_setup_vars['path'], cluster.id, f'{cluster.id}_CustomerHSMCertificate.crt'))
    os.rmdir(os.path.join(test_setup_vars['path'], cluster.id))