from app.controllers.addresses_controller import AddressController
from app.models.pub_key_model import PubKey
from tests.mocks import instance, cluster, pub_key
from unittest.mock import patch
import tests.data as data


def test_bucket_name(credentials):
    controller = AddressController(config=credentials)
    resp = controller.bucket_name
    assert resp == 'cluster-lbtkdldygfh-bucket'


def test_eni_ip(credentials):
    controller = AddressController(config=credentials)
