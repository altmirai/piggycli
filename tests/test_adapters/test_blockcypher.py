from app.adapters import Explorer
import tests.data as data

from unittest.mock import patch


@patch(
    'app.adapters.blockcypher_adapters.blockcypher.get_address_details',
    return_value=data.sending_address_blockcypher_resp,
    autospec=True)
def test_get_address_data(mock_get_address_details):
    explorer = Explorer(address=data.address)

    assert explorer.address == data.address
    assert explorer.confirmed_balance == data.confirmed_balance
    assert explorer.spent == data.spent
    assert explorer.txrefs == data.txrefs
