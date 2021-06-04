import boto3


class S3:

    @classmethod
    def all(cls, bucket, s3):
        breakpoint()

    def save(self, bucket, s3, region):
        if bucket_exists(bucket=bucket, s3=s3) is False:
            create_bucket(bucket=bucket, s3=s3, region=region)
        breakpoint()
        pass


def bucket_exists(bucket, s3):
    resp = s3.list_buckets()
    for bucket in resp['Buckets']:
        if bucket['Name'] == bucket:
            return True
    return False


def create_bucket(bucket, s3, region):
    location = {'LocationConstraint': region}
    resp = s3.create_bucket(
        Bucket=bucket, CreateBucketConfiguration=location)

    return resp['Location']
