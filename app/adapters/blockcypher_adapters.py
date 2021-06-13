import requests
import json

base_url = 'https://api.blockcypher.com'
version = 'v1'


def get_btc_main_address_resource(address):
    url = f'{base_url}/{version}/btc/main/addrs/{address}'
    resp = requests.get(url, timeout=5)
    data = json.loads(resp._content.decode())

    return {
        'address': data['address'],
        'balance': data['balance'],
        'txrefs': data.get('txrefs'),
        'spent': is_spent(data=data)
    }


def is_spent(data):
    txrefs = data.get('txrefs')
    if bool(txrefs):
        for txref in txrefs:
            if txref['spent'] == True:
                return True

    return False
