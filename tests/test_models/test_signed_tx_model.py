from app.models.signed_tx_model import SignedTx
import tests.data as data

from unittest.mock import patch


@patch('app.models.signed_tx_model._get_signatures', return_value=data.signatures, autospec=False)
def test_create(mocked_get_signatures, unsigned_tx_no_change, address, credentials):

    signed_tx = SignedTx.create(
        unsigned_tx=unsigned_tx_no_change,
        address=address,
        credentials=credentials,
        eni_ip=data.eni_ip,
        ip_address=data.public_ip_address
    )

    assert signed_tx.pem == data.pem
    assert signed_tx.signatures == data.signatures
    assert signed_tx.hex == data.tx_hex
