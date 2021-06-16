import blockcypher
import json


def _get_api_key():
    with open('.env', 'r') as file:
        json_data = file.read()
    data = json.loads(json_data)
    return data['BLOCKCYPHER_API_TOKEN']


api_key = _get_api_key()


def address_data(address):
    try:
        resp = blockcypher.get_address_details(address=address)
        # breakpoint()
        # resp = {'address': '12c5gjCuHNxJMGLChzdvy3sjZxJVd7R1rm', 'balance': 226323, 'txrefs': [{'tx_hash': '23b6ccf2a8a636c7f49cc6efac1475c8059c5dad59265bb120f8a3fa8aca5567', 'block_height': 687327, 'tx_input_n': -1,
        # 'tx_output_n': 67, 'value': 226323, 'ref_balance': 226323, 'spent': False, 'confirmations': 424, 'double_spend': False}], 'spent': False}
        return {
            'address': resp['address'],
            'confirmed_balance': resp['balance'],
            'txrefs': resp.get('txrefs'),
            'spent': is_spent(data=resp)
        }

    except AssertionError as e:
        raise AddressNotValid(e.args[0])

    except Exception as e:
        raise Exception(e.args[0])


def is_spent(data):
    if data['total_sent'] > 0:
        return True
    else:
        return False


class AddressNotValid(Exception):
    pass
