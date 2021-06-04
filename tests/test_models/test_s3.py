from app.models.s3_model import S3, bucket_exists, create_bucket
import tests.data as data
import boto3


def test_bucket_exists(list_buckets_true):
    stubber, client = list_buckets_true
    with stubber:
        resp = bucket_exists(bucket=data.bucket_name, s3=client)

    assert resp == True


def test_bucket_exists(list_buckets_false):
    stubber, client = list_buckets_false
    with stubber:
        resp = bucket_exists(bucket=data.bucket_name, s3=client)

    assert resp == False


def test_create_bucket(aws_create_bucket):
    stubber, client = aws_create_bucket
    with stubber:
        resp = create_bucket(
            bucket=data.bucket_name,
            s3=client,
            region=data.aws_region
        )

    assert resp == data.create_bucket_resp['Location']


def test_address_save(address):
    s3 = boto3.client('s3', region_name=data.aws_region)
    resp = address.save(bucket=data.bucket_name, s3=s3, region=data.aws_region)
