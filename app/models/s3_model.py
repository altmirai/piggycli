import json


class S3:

    @classmethod
    def all(cls, bucket, s3):
        breakpoint()

    def save(self, bucket, s3, region):
        if bucket_exists(bucket=bucket, s3=s3) is False:
            create_bucket(bucket=bucket, s3=s3, region=region)
        data_json = json.dumps(self.__dict__)
        data_bytes = bytes(data_json, 'UTF-8')
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
        Bucket=bucket, CreateBucketConfiguration=location)

    return resp['Location']
