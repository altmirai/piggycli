import requests


def get_btc_main_address_resource(address):
    resp = requests.get(f"https://blockchain.info/rawaddr/{address}")
    breakpoint()
