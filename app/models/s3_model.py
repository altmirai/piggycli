import json


class S3:

    @classmethod
    def all(cls, bucket, s3):
        addresses = []
        resp = s3.list_objects(Bucket=bucket)
        keys = resp['Contents']
        for key in keys:
            resp = s3.get_object(Bucket=bucket, Key=key['Key'])
            resp_data_json = resp['Body'].read().decode()
            resp_data = json.loads(resp_data_json)
            address = cls(
                id=key['Key'],
                pub_key_pem=resp_data['pub_key_pem'],
                pub_key_handle=resp_data['pub_key_handle'],
                private_key_handle=resp_data['private_key_handle']
            )
            addresses.append(address)

        breakpoint()

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
        breakpoint()

        pass

    def update(self):
        pass

    def read(self):
        pass

    def delete(self):
        pass


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
