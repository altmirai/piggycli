import app.adapters.blockcypher_adapters as blockcypher


class Explorer:
    def __init__(self, address, provider='blockcypher'):
        self.address = address
        self.provider = provider

    @property
    def confirmed_balance(self):
        address_resource = self.get_btc_main_address_resource()
        return address_resource['confirmed_balance']

    @property
    def spent(self):
        address_resource = self.get_btc_main_address_resource()
        return address_resource['spent']

    @property
    def tx_inputs(self):
        address_resource = self.get_btc_main_address_resource()
        return address_resource['tx_inputs']

    def get_btc_main_address_resource(self):
        if self.provider == 'blockcypher':
            resp = blockcypher.get_btc_main_address_resource(
                address=self.address)
            return {
                'address': resp['address'],
                'confirmed_balance': resp['balance'],
                'spent': resp['spent'],
                'tx_inputs': self.blockcypher_address_tx_inputs(resp['txrefs'])
            }
        else:
            return None

    def blockcypher_address_tx_inputs(self, txrefs):
        tx_inputs = []
        if bool(txrefs):
            for txref in txrefs:
                tx = {}
                tx['output_no'] = txref['tx_output_n']
                tx['outpoint_index'] = (txref['tx_output_n']).to_bytes(
                    4, byteorder='little', signed=False)
                hash = bytearray.fromhex(txref['tx_hash'])
                hash.reverse()
                tx['outpoint_hash'] = hash
                tx_inputs.append(tx)
        return tx_inputs
