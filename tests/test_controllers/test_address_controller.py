from app.controllers.addresses_controller import AddressController
from app.models.address_model import Address
from app.models.instance_model import Instance
from app.models.pub_key_model import PubKey
from tests.mocks import instance, cluster, pub_key, address
from unittest.mock import patch, Mock
import tests.data as data
from tests.mocks import cluster, instance
import os


@patch.object(Address, 'all', return_value=[address], autospec=True)
def test_index(mock_Address, credentials):
    controller = AddressController(config=credentials)
    resp = controller.index()
    assert resp['data']['addresses'][0].address == data.address


@patch.object(PubKey, 'create', return_value=pub_key, autospec=True)
@patch('app.controllers.addresses_controller.Instance', return_value=instance, autospec=True)
@patch('app.controllers.addresses_controller.Cluster', return_value=cluster, autospec=True)
@patch.object(Address, 'create', return_value=address, autospec=True)
def test_create(mock_PubKey, mock_Instance, mock_Cluster, mock_Address, credentials):
    controller = AddressController(config=credentials)
    resp = controller.create()
    assert resp['data']['address'].address == data.address


@patch.object(Address, 'find', return_value=address, autospec=True)
def test_show(mock_Adddress, credentials):
    controller = AddressController(config=credentials)
    resp = controller.show(id=data.address_id)
    assert resp['data']['address'].address == data.address


def test_ip_address(credentials):
    with patch('app.controllers.addresses_controller.Instance', return_value=instance, autospec=True):
        controller = AddressController(config=credentials)
        resp = controller.ip_address
    assert resp == data.public_ip_address


def test_ssh_key_file(credentials):
    controller = AddressController(config=credentials)
    resp = controller.ssh_key_file
    assert resp == data.ssh_key_file


def test_eni_ip(credentials):
    with patch('app.controllers.addresses_controller.Cluster', return_value=cluster, autospec=True):
        controller = AddressController(config=credentials)
        resp = controller.eni_ip
    assert resp == data.eni_ip


def test_bucket_name(credentials):
    controller = AddressController(config=credentials)
    resp = controller.bucket_name
    assert resp == 'cluster-lbtkdldygfh-bucket'
