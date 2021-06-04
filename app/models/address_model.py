from app.models.s3_model import S3
import hashlib
from base58 import b58encode_check
from ecdsa import VerifyingKey


class Address(S3):
    def __init__(self, id, pub_key_pem, pub_key_handle, private_key_handle):
        self.id = id
        self.pub_key_pem = pub_key_pem
        self.pub_key_handle = pub_key_handle
        self.private_key_handle = private_key_handle

    @classmethod
    def create(cls, pub_key):
        return cls(
            id=pub_key.label,
            pub_key_pem=pub_key.pem,
            pub_key_handle=pub_key.handle,
            private_key_handle=pub_key.private_key_handle,
        )

    @property
    def address(self):
        p2pkh = P2PKH(pem=self.pub_key_pem)
        return p2pkh.address


class P2PKH:
    def __init__(self, pem):
        self.public_key = pem

    @property
    def btc_public_key(self):
        vk = VerifyingKey.from_pem(self.public_key)
        btc_public_key = bytes.fromhex('04') + vk.to_string()

        return btc_public_key.hex()

    @property
    def address(self):
        sha256 = hashlib.sha256(bytes.fromhex(self.btc_public_key)).digest()

        ripemd160_hash = hashlib.new('ripemd160')
        ripemd160_hash.update(sha256)
        ripemd160 = ripemd160_hash.digest()

        hashed_btc_public_key = bytes.fromhex('00') + ripemd160

        addr = b58encode_check(hashed_btc_public_key).decode('utf-8')

        return addr
