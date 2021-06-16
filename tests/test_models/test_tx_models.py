from app.models.signed_tx_model import SignedTx
from app.models.unsigned_tx_model import UnsignedTx
import tests.data as data

from unittest.mock import Mock, patch
import pytest

sending_address = '1DSRQWjbNXLN8ZZZ6gqcGx1WNZeKHEJXDv'
confirmed_balance = 5763656
recipient = '1BHznNt5x9rqMQ1dpWy4fw5y5PSJV3ZR3L'
fee = 104600
vkhandle = '7340043'
skhandle = '7340044'
pem = '-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEbpzYR5GToC0CXSNlRecu3xAjflSmSoh9\n+Gb41bhqD9VUSa2CHfjiVoEW5Sze46axHXrn1eGSAkTiQmcExfWABQ==\n-----END PUBLIC KEY-----\n'
tx_inputs = [
    {
        'output_no': 0,
        'outpoint_index': b'\x00\x00\x00\x00',
        'outpoint_hash': bytearray(
            b"Y:N~v%0\xbc\xcf\xbc\xd9@\xc2K\xc3\x92\xc6\xfb\xe7#\xcf\x8e\xf4\xe8\xa9t\xf5m\x1fE\'\x9d"
        )
    },
    {
        'output_no': 0,
        'outpoint_index': b'\x00\x00\x00\x00',
        'outpoint_hash': bytearray(
            b'qg/\xe5\x86\xbcvS\xc7t\\D\r\xc4\x1dG8\xe9\xab3\xa4|N.x(\xa7v\xaf\x8d\xcfx'
        )
    },
    {
        'output_no': 0,
        'outpoint_index': b'\x00\x00\x00\x00',
        'outpoint_hash': bytearray(
            b'"\x9a\xd5\x904\\^\xac^\xc1\xe6c>\x93mU\xfc\xf8\xab\x17\xf4G[\xae\xd9\x13\xb9\xc6\xe7\x05\x7f_'
        )
    }
]
messages_hex = [
    '0100000003593a4e7e762530bccfbcd940c24bc392c6fbe723cf8ef4e8a974f56d1f45279d000000001976a914887047f28478e316732db0bccd086482c8617e4a88acffffffff71672fe586bc7653c7745c440dc41d4738e9ab33a47c4e2e7828a776af8dcf780000000000ffffffff229ad590345c5eac5ec1e6633e936d55fcf8ab17f4475baed913b9c6e7057f5f0000000000ffffffff01b0595600000000001976a91470e825c3aa5396f6cfe794bcc6ad61ab9dfa6a4088ac0000000001000000',
    '0100000003593a4e7e762530bccfbcd940c24bc392c6fbe723cf8ef4e8a974f56d1f45279d0000000000ffffffff71672fe586bc7653c7745c440dc41d4738e9ab33a47c4e2e7828a776af8dcf78000000001976a914887047f28478e316732db0bccd086482c8617e4a88acffffffff229ad590345c5eac5ec1e6633e936d55fcf8ab17f4475baed913b9c6e7057f5f0000000000ffffffff01b0595600000000001976a91470e825c3aa5396f6cfe794bcc6ad61ab9dfa6a4088ac0000000001000000',
    '0100000003593a4e7e762530bccfbcd940c24bc392c6fbe723cf8ef4e8a974f56d1f45279d0000000000ffffffff71672fe586bc7653c7745c440dc41d4738e9ab33a47c4e2e7828a776af8dcf780000000000ffffffff229ad590345c5eac5ec1e6633e936d55fcf8ab17f4475baed913b9c6e7057f5f000000001976a914887047f28478e316732db0bccd086482c8617e4a88acffffffff01b0595600000000001976a91470e825c3aa5396f6cfe794bcc6ad61ab9dfa6a4088ac0000000001000000'
]
tosign_hex = [
    'af69b4567cbcd15f2c719a62311ef8fe47711e21c038dad27f3fc631baf21f3c', '600da7c38b14b9bfc44a6deba21621555b1aadba9066a1e76fe4a7e48082748f', 'f5aa21d884e6e5b4eac08803640b6546145b2f2bf34a04945ea7685615454f27'
]
test_signatures = [
    '/Users/kyle/GitHub/alt-piggy-bank/piggy-cli/tests/signature_files/signedTx7340043_1.der',
    '/Users/kyle/GitHub/alt-piggy-bank/piggy-cli/tests/signature_files/signedTx7340043_2.der',
    '/Users/kyle/GitHub/alt-piggy-bank/piggy-cli/tests/signature_files/signedTx7340043_3.der'
]

path = data.test_path

explorer = Mock()
explorer.address = sending_address
explorer.confirmed_balance = confirmed_balance
explorer.spent = False
explorer.tx_inputs = tx_inputs

p2pkh = Mock()
p2pkh.address = sending_address
p2pkh.confirmed_balance = confirmed_balance

address = Mock()
address.pub_key_handle = vkhandle
address.private_key_handle = skhandle
address.pub_key_pem = pem


@pytest.fixture
def signatures():
    signatures = []
    for sig_file in test_signatures:
        with open(sig_file, 'rb') as file:
            signature = file.read()
        signatures.append(signature)

    yield signatures


@patch('app.models.unsigned_tx_model.Explorer', return_value=explorer, autospec=True)
@patch('app.models.unsigned_tx_model.P2PKH', return_value=p2pkh, autospec=True)
def test_unsigned_tx(mock_Explorer, mock_P2PKH):
    unsigned_tx = UnsignedTx(pem=pem, recipient=recipient, fee=fee, value=(
        confirmed_balance-fee), change_address=None)

    resp_messages_hex = []
    for message in unsigned_tx.messages:

        resp_messages_hex.append(message['message'].hex())

    resp_tosign_hex = []
    for elem in unsigned_tx.to_sign:
        resp_tosign_hex.append(elem.hex())

    assert resp_messages_hex == messages_hex
    assert resp_tosign_hex == tosign_hex


@patch('app.models.unsigned_tx_model.Explorer', return_value=explorer, autospec=True)
@patch('app.models.unsigned_tx_model.P2PKH', return_value=p2pkh, autospec=True)
def test_signed_tx(mock_Explorer, mock_P2PKH, credentials, signatures):
    unsigned_tx = UnsignedTx(pem=pem, recipient=recipient, fee=fee, value=(
        confirmed_balance-fee), change_address=None)

    with patch('app.models.signed_tx_model._get_signatures', return_value=signatures, autospec=True):
        signed_tx = SignedTx.create(
            unsigned_tx=unsigned_tx,
            address=address,
            credentials=credentials,
            ip_address=data.public_ip_address,
            eni_ip=data.eni_ip,
            path=data.test_path
        )

    signed_tx.hex

    breakpoint()
