from app.models.s3_model import S3, bucket_exists, create_bucket
import tests.data as data
import boto3


def test_bucket_exists(list_buckets):
    stubber, client = list_buckets
    with stubber:
        resp = bucket_exists(bucket_name=data.bucket_name, client=client)

    assert resp == (data.bucket_name in data.list_buckets_resp['Buckets'])


def test_create_bucket(aws_create_bucket):
    stubber, client = aws_create_bucket
    with stubber:
        resp = create_bucket(
            bucket_name=data.bucket_name,
            client=client,
            region=data.aws_region
        )

    assert resp == data.create_bucket_resp['Location']
