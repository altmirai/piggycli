from app.controllers.tx_controller import TxController

pem = '-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEEEYV4CBaW1Jc9COEwA7fGRgwAYJBpErv\nNT/OSW8sjgNACFj+Q0wy+rkWNlA0nZzIXi/N62dcCoXcs0W+BE9dHg==\n-----END PUBLIC KEY-----\n'
address_id = 'addr-2f8558248c33'


# def test_tx(config):
#     controller = TxController(config=config)
#     resp = controller.create(
#         address_id=address_id,
#         recipient='1CpuPq63tVhL5vhAhL2GLFYkMZT7DBrv9J',
#         fee=10000
#     )
