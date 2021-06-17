from app.models.address_model import Address, bucket_exists, create_bucket
import tests.data as data

from unittest.mock import patch


def test_create(pub_key):
    address = Address.create(pub_key=pub_key)

    assert address.address == data.address


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
        with patch('app.models.address_model.bucket_exists', return_value=True, autospec=True):
            resp = address.save(
                bucket=data.bucket_name,
                s3=mock_client,
                region=data.aws_region
            )

    assert resp == address.id


def test_all(list_objects, address):
    stubber, client = list_objects
    with stubber:
        with patch.object(Address, 'find', return_value=address):
            addresses = Address.all(bucket=data.bucket_name, s3=client)

    assert addresses[0].id == address.id


def test_find(get_object):
    stubber, client = get_object
    with stubber:
        address = Address.find(
            bucket=data.bucket_name,
            s3=client, id=data.address_id
        )

    assert address.address == data.address


def test_confirmed_balance(address):
    assert address.confirmed_balance == data.confirmed_balance
