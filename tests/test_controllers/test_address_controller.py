from app.controllers.addresses_controller import AddressController
from app.models.pub_key_model import PubKey
from tests.mocks import instance, cluster, pub_key
from unittest.mock import patch
import tests.data as data
from tests.mocks import cluster, instance
import os


def test_bucket_name(credentials):
    controller = AddressController(config=credentials)
    resp = controller.bucket_name
    assert resp == 'cluster-lbtkdldygfh-bucket'


def test_eni_ip(credentials):
    with patch('app.controllers.addresses_controller.Cluster', return_value=cluster, autospec=True):
        controller = AddressController(config=credentials)
        resp = controller.eni_ip
    assert resp == data.eni_ip


def test_ssh_key_file(credentials):
    controller = AddressController(config=credentials)
    resp = controller.ssh_key_file
    assert resp == data.ssh_key_file


def test_ip_address(credentials):
    with patch('app.controllers.addresses_controller.Instance', return_value=instance, autospec=True):
        controller = AddressController(config=credentials)
        resp = controller.ip_address
    assert resp == data.public_ip_address
