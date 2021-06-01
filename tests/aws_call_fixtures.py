import tests.data as data
import datetime

import botocore.session
from botocore.stub import Stubber, ANY
import pytest

create_key_pair_resp = {
    'KeyFingerprint': data.KeyFingerprint,
    'KeyMaterial': data.KeyMaterial,
    'KeyName': data.KeyName,
    'KeyPairId': data.KeyPairId
}


@pytest.fixture
def create_key_pair():
    client = botocore.session.get_session().create_client('ec2')
    stubber = Stubber(client)
    stubber.add_response(
        'create_key_pair',
        create_key_pair_resp,
        {'KeyName': ANY}
    )
    yield stubber, client


describe_clusters_resp = {
    'Clusters':
    [
        {
            'BackupPolicy': 'DEFAULT',
            'BackupRetentionPolicy': {
                'Type': 'DAYS',
                'Value': '90'
            },
            'ClusterId': data.cluster_id,
            'Hsms': [], 'HsmType': 'hsm1.medium',
            'SecurityGroup': 'sg-0778d7aa573ae2427',
            'State': 'ACTIVE',
            'SubnetMapping': {
                'us-east-2a': 'subnet-03fce2972dfdfe9b8',
                'us-east-2b': 'subnet-0ba1722070b8dd5c4',
                'us-east-2c': 'subnet-0ec0911a438c139ea'
            },
            'VpcId': '',
            'Certificates':
            {
                'ClusterCsr': data.pem_csr,
                'HsmCertificate': '',
                'AwsHardwareCertificate': '',
                'ManufacturerHardwareCertificate': '',
                'ClusterCertificate': ''
            },
                'TagList':
                [
                    {
                        'Key': 'Name',
                        'Value': 'cloudhsm_cluster'
                    }
            ]
        }
    ]
}


@pytest.fixture
def describe_clusters():
    client = botocore.session.get_session().create_client('cloudhsmv2')
    stubber = Stubber(client)
    stubber.add_response(
        'describe_clusters',
        describe_clusters_resp,
        {}
    )

    yield stubber, client


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
