from app.utilities.bitcoin.addresses import P2PKH

import hashlib
from base58 import b58encode_check
from ecdsa import VerifyingKey
import json


class Address():
    def __init__(self, id, pub_key_pem, pub_key_handle, private_key_handle):
        self.id = id
        self.pub_key_pem = pub_key_pem
        self.pub_key_handle = pub_key_handle
        self.private_key_handle = private_key_handle

    @classmethod
    def all(cls, bucket, s3):
        addresses = []
        resp = s3.list_objects(Bucket=bucket)
        keys = resp['Contents']
        for key in keys:
            address = cls.find(bucket=bucket, s3=s3, id=key['Key'])
            addresses.append(address)
        return addresses

    @classmethod
    def find(cls, bucket, s3, id):
        resp = s3.get_object(Bucket=bucket, Key=id)
        resp_data_json = resp['Body'].read().decode()
        resp_data = json.loads(resp_data_json)
        address = cls(
            id=id,
            pub_key_pem=resp_data['pub_key_pem'],
            pub_key_handle=resp_data['pub_key_handle'],
            private_key_handle=resp_data['private_key_handle']
        )

        return address

    @classmethod
    def create(cls, pub_key):
        return cls(
            id=pub_key.label,
            pub_key_pem=pub_key.pem,
            pub_key_handle=pub_key.handle,
            private_key_handle=pub_key.private_key_handle,
        )

    def save(self, bucket, s3, region):
        if bucket_exists(bucket=bucket, s3=s3) is False:
            create_bucket(bucket=bucket, s3=s3, region=region)
        key = self.id
        data_json = json.dumps(
            {
                'pub_key_handle': self.pub_key_handle,
                'private_key_handle': self.private_key_handle,
                'pub_key_pem': self.pub_key_pem,
                'address': self.address
            }
        )
        data_bytes = bytes(data_json, 'UTF-8')
        resp = s3.put_object(
            Body=data_bytes,
            Bucket=bucket,
            Key=key
        )
        assert resp['ResponseMetadata'][
            'HTTPStatusCode'] == 200, f'Failed to save address: {self.id} to bucket: {bucket}'
        return self.id

    @property
    def address(self):
        address = P2PKH(pem=self.pub_key_pem)
        return address.address

    @property
    def confirmed_balance(self):
        address = P2PKH(pem=self.pub_key_pem)
        return address.confirmed_balance

    @property
    def spent(self):
        address = P2PKH(pem=self.pub_key_pem)
        return address.spent


def bucket_exists(bucket, s3):
    resp = s3.list_buckets()
    for _bucket in resp['Buckets']:
        if _bucket['Name'] == bucket:
            return True
    return False


def create_bucket(bucket, s3, region):
    location = {'LocationConstraint': region}
    resp = s3.create_bucket(
        Bucket=bucket,
        CreateBucketConfiguration=location
    )

    return resp['Location']
