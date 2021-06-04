from app.models.s3_model import S3, bucket_exists, create_bucket
from app.models.address_model import Address
from unittest.mock import patch
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


def test_address_save(put_object, address):
    stubber, mock_client = put_object
    with stubber:
        with patch('app.models.s3_model.bucket_exists', return_value=True, autospec=True):
            resp = address.save(
                bucket=data.bucket_name,
                s3=mock_client,
                region=data.aws_region
            )

    assert resp == address.id


# def test_real_save(address):
#     s3 = boto3.client('s3', region_name=data.aws_region)
#     resp = address.save(bucket=data.bucket_name, s3=s3, region=data.aws_region)

def test_all(list_objects, address):
    stubber, client = list_objects
    with stubber:
        with patch.object(Address, 'find', return_value=address):
            addresses = Address.all(bucket=data.bucket_name, s3=client)

    assert addresses[0].id == address.id


def test_find():
    s3 = boto3.client('s3', region_name=data.aws_region)
    address = Address.find(bucket=data.bucket_name, s3=s3, id=data.address_id)
