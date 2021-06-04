from app.models.address_model import Address
from tests.mocks import instance, cluster
import tests.data as data


def test_create(pub_key, credentials):
    address = Address.create(pub_key=pub_key, credentials=credentials)

    assert address.address == data.address
