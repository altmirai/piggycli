from app.models.pub_key_model import PubKey
from app.models.instance_model import Instance
from app.models.cluster_model import Cluster
from unittest.mock import patch
import tests.data as data
import boto3


@patch('app.models.pub_key_model.ssh.gen_ecc_key_pair', return_value=data.gen_ecc_key_pair_resp, autospec=True)
def test_create(mock_gen_ecc_key_pair):
    pub_key = PubKey.create(
        ip_address=data.public_ip_address,
        ssh_key_file_path=data.ssh_key_file_path,
        eni_ip=data.eni_ip,
        crypto_user_username=data.crypto_user_username,
        crypto_user_password=data.crypto_user_password,
        label=data.label
    )

    assert pub_key.label == data.label
    assert pub_key.handle == data.handle
    assert pub_key.pem == data.pem
    assert pub_key.private_key_handle == data.private_key_handle
