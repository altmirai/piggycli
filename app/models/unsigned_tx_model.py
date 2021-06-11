from app.utilities.bitcoin.tx_scripts import TxOutputScript, PubKeyScript
from app.utilities.bitcoin.addresses import P2PKH

import hashlib


class UnsignedTx:

    def __init__(self, pem, recipient, fee, value, change_address):
        self.p2pkh = P2PKH(pem)
        self.address = self.p2pkh.address
        self.confirmed_balance = self.p2pkh.confirmed_balance
        self.tx_outs = TxOutputScript(
            self.address, self.confirmed_balance, recipient, fee, value, change_address)
        self.pub_key_script = PubKeyScript(self.address)

    @property
    def messages(self):
        messages = []
        for tx in self.tx_inputs:
            msg = bytearray()
            msg += self.version
            msg += self.tx_in_count
            for tx_in in self.tx_inputs:
                msg += self.previous_output(tx_in)
                if tx == tx_in:
                    msg += self.pub_key_script.bytes
                    msg += self.pub_key_script.script
                else:
                    msg += self.placeholder
                msg += self.sequence
            msg += self.tx_out_count
            for tx_output in self.tx_outs.outputs:
                msg += tx_output
            msg += self.lock_time
            msg += self.hash_code

            messages.append({'message': msg, 'tx_input': tx})

        return messages

    @property
    def to_sign(self):
        to_signs = []
        for msg in self.messages:
            to_signs.append(hashlib.sha256(msg['message']).digest())
        return to_signs

    @property
    def tx_inputs(self):

    @property
    def version(self):
        return (1).to_bytes(4, byteorder="little", signed=True)

    @property
    def tx_in_count(self):
        return (len(self.tx_inputs)).to_bytes(1, byteorder="little", signed=False)

    def previous_output(self, tx_in):
        output = bytearray()
        output += tx_in['outpoint_hash']
        output += tx_in['outpoint_index']
        return output

    @property
    def placeholder(self):
        return (0).to_bytes(1, byteorder='little', signed=False)

    @property
    def sequence(self):
        return bytes.fromhex("ffffffff")

    @property
    def tx_out_count(self):
        return (len(self.tx_outs.outputs)).to_bytes(1, byteorder="little", signed=False)

    @property
    def lock_time(self):
        return (0).to_bytes(4, byteorder="little", signed=False)

    @property
    def hash_code(self):
        return (1).to_bytes(4, byteorder='little', signed=False)
