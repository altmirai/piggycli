from app.controllers.tx_controller import TxController
from unittest.mock import patch, Mock
import tests.data as data

from tests.data.mocks import address, instance, cluster, unsigned_tx, signed_tx


def test_object(credentials):
    controller = TxController(config=credentials)

    assert controller.credentials.data == credentials.data


@patch('app.controllers.tx_controller.UnsignedTx', return_value=unsigned_tx, autospec=True)
@patch('app.controllers.tx_controller.Instance', return_value=instance, autospec=True)
@patch('app.controllers.tx_controller.Cluster', return_value=cluster, autospec=True)
@patch('app.controllers.tx_controller.SignedTx.create', return_value=signed_tx, autospec=True)
def test_create(mock_UnsignedTx, mock_Instance, mock_Cluster, mock_SignedTx, credentials):
    controller = TxController(config=credentials)
    resp = controller.create(
        address=address,
        recipient=data.recipient,
        fee=data.fee,
        value=data.value
    )

    assert resp == data.tx_hex


# @patch(
#     'app.adapters.blockcypher_adapters.blockcypher.get_address_details',
#     return_value=data.sending_address_blockcypher_resp,
#     autospec=True)
# @patch('app.controllers.tx_controller._is_address_valid', return_value=True, autospec=True)
# def test_validate(mock_is_address_valid, mock_get_address_details, credentials, get_object):
#     stubber, client = get_object
#     controller = TxController(config=credentials)
#         resp = controller.validate(
#             all=True,
#             address_id=data.address_id,
#             recipient=data.recipient,
#             fee=data.fee,
#             value=data.value,
#             change_address=None
#         )

#     breakpoint()
