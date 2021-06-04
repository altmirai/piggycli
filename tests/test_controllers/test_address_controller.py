from app.controllers.addresses_controller import AddressController
from app.models.pub_key_model import PubKey
from tests.mocks import instance, cluster, pub_key
from unittest.mock import patch
import tests.data as data


def test_create(credentials):
    with patch('app.controllers.addresses_controller.PubKey.create', return_value=pub_key, autospec=True) as _:
        controller = AddressController(credentials=credentials)
        address = controller.create(
            ip_address=data.public_ip_address, ssh_key_file=data.ssh_key_file, eni_ip=data.eni_ip)

        assert address.address == data.address
