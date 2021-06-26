from app.models.credentials_model import Credentials
from app.models.cluster_model import Cluster
from app.models.pub_key_model import PubKey
from app.models.address_model import Address
from app.models.unsigned_tx_model import UnsignedTx
from app.models.signed_tx_model import SignedTx

import tests.data as data
from tests.data import mocks
import os
from unittest.mock import patch
import pytest


@pytest.fixture
def credentials():
    if os.path.exists(data.test_cluster_path) is False:
        os.mkdir(data.test_cluster_path)

    credentials_file_path = os.path.join(
        data.test_cluster_path, 'credentials.json')
    _data = {
        'base_path': data.test_base_path,
        'cluster_path': data.test_cluster_path,
        'aws_region': data.aws_region,
        'aws_access_key_id': data.aws_access_key_id,
        'aws_secret_access_key': data.aws_secret_access_key,
        'customer_ca_key_password': data.customer_ca_key_password,
        'crypto_officer_password': data.crypto_officer_password,
        'crypto_user_username': data.crypto_user_username,
        'crypto_user_password': data.crypto_user_password,
        'cluster_id': data.cluster_id,
        'instance_id': data.instance_id,
        'ssh_key_name': data.ssh_key_name
    }
    credentials = Credentials.create(
        credentials_file_path=credentials_file_path,
        data=_data
    )
    yield credentials
    os.remove(credentials_file_path)


@pytest.fixture
def config():
    class Config:
        def __init__(self):
            self.path = '/Users/kyle/GitHub/alt-piggy-bank/piggy-cli/production_files'
            self.credentials_file_path = '/Users/kyle/GitHub/alt-piggy-bank/piggy-cli/production_files/credentials.json'
            self.creds_exist = True

    config = Config()

    yield config


@pytest.fixture
def cluster():
    cluster = Cluster(client=data.cloudhsmv2, id=data.cluster_id)
    yield cluster
    os.remove(os.path.join(data.test_path, 'credentials.json'))


@pytest.fixture
def pub_key():
    pub_key = PubKey(
        label=data.label,
        handle=data.handle,
        pem=data.pem,
        private_key_handle=data.private_key_handle
    )
    yield pub_key


@pytest.fixture
def address():
    address = Address(
        id=data.address_id,
        address=data.address,
        pub_key_pem=data.pub_key_pem,
        pub_key_handle=data.pub_key_handle,
        private_key_handle=data.private_key_handle,
        confirmed_balance=data.confirmed_balance,
        txrefs=data.txrefs,
        spent=data.spent
    )
    yield address


@pytest.fixture
def unsigned_tx_no_change():
    unsigned_tx = UnsignedTx(
        address=mocks.address,
        recipient=data.recipient,
        fee=data.fee,
        value=data.value,
        change_address=None
    )

    yield unsigned_tx


@pytest.fixture
def signed_tx_no_change():
    signed_tx = SignedTx(
        pem=data.pem,
        unsigned_tx=mocks.unsigned_tx,
        signatures=data.signatures
    )

    yield signed_tx
