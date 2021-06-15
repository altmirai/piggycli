# from app.models.unsigned_tx_model import UnsignedTx
# from tests.data import unsigned_tx_data

# data = unsigned_tx_data()

# pem = '-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEEEYV4CBaW1Jc9COEwA7fGRgwAYJBpErv\nNT/OSW8sjgNACFj+Q0wy+rkWNlA0nZzIXi/N62dcCoXcs0W+BE9dHg==\n-----END PUBLIC KEY-----\n'
# confirmed_balance = 226323


# def test_create_send_all():
#     unsigned_tx = UnsignedTx(
#         pem=pem,
#         recipient=data.recipient_addr_address,
#         fee=20000,
#         value=(confirmed_balance-20000),
#         change_address=None
#     )
#     breakpoint()
