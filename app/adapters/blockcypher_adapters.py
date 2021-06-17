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
