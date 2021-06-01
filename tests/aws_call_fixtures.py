import tests.data as data

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
