import tests.data.vars as var

import json
import datetime
from dateutil.tz import tzutc
from botocore.response import StreamingBody
import io

sending_address_blockcypher_resp = {
    'address': '1CpuPq63tVhL5vhAhL2GLFYkMZT7DBrv9J',
    'total_received': 190000,
    'total_sent': 0,
    'balance': 190000,
    'unconfirmed_balance': 0,
    'final_balance': 190000,
    'n_tx': 2,
    'unconfirmed_n_tx': 0,
    'final_n_tx': 2,
    'txrefs': [
        {
            'tx_hash': '995e70e4c78fe60d26c5f6904204b2d4e819aa63686a10eeca97cb17b76151fa',
            'block_height': 687813,
            'tx_input_n': -1,
            'tx_output_n': 0,
            'value': 90000,
            'ref_balance': 190000,
            'spent': False,
            'confirmations': 145,
            'confirmed': datetime.datetime(2021, 6, 16, 14, 24, 4, tzinfo=tzutc()),
            'double_spend': False
        },
        {
            'tx_hash': '429eca7b6cc576a2aa9acefc05bf8c21c92a4aeceae0d03d1d45aff964e6e50b',
            'block_height': 687809,
            'tx_input_n': -1,
            'tx_output_n': 1,
            'value': 100000,
            'ref_balance': 100000,
            'spent': False,
            'confirmations': 149, 'confirmed': datetime.datetime(2021, 6, 16, 13, 41, 40, tzinfo=tzutc()),
            'double_spend': False
        }
    ],
    'tx_url': 'https://api.blockcypher.com/v1/btc/main/txs/',
    'unconfirmed_txrefs': []}

recipient_address_blockcypher_resp = {
    'address': '1Pzc72SMoaxWZhkAqZFFjGRKnCHMBLTWs8',
    'total_received': 0,
    'total_sent': 0,
    'balance': 0,
    'unconfirmed_balance': 0,
    'final_balance': 0,
    'n_tx': 0,
    'unconfirmed_n_tx': 0,
    'final_n_tx': 0,
    'tx_url': 'https://api.blockcypher.com/v1/btc/main/txs/',
    'txrefs': [],
    'unconfirmed_txrefs': []
}


create_key_pair_resp = {
    'KeyFingerprint': var.KeyFingerprint,
    'KeyMaterial': var.KeyMaterial,
    'KeyName': var.KeyName,
    'KeyPairId': var.KeyPairId
}

describe_clusters_resp = {
    'Clusters':
    [
        {
            'BackupPolicy': 'DEFAULT',
            'BackupRetentionPolicy': {
                'Type': 'DAYS',
                'Value': '90'
            },
            'ClusterId': var.cluster_id,
            'Hsms': [
                {
                    'AvailabilityZone': 'us-east-2a',
                    'ClusterId': var.cluster_id,
                    'SubnetId': 'subnet-03fce2972dfdfe9b8',
                    'EniId': 'eni-08ff8a68aae5933c1',
                    'EniIp': '10.0.1.6',
                    'HsmId': var.hsm_id,
                    'State': 'ACTIVE',
                    'StateMessage': 'HSM created.'
                }
            ], 'HsmType': 'hsm1.medium',
            'SecurityGroup': 'sg-0778d7aa573ae2427',
            'State': 'ACTIVE',
            'SubnetMapping': {
                'us-east-2a': 'subnet-03fce2972dfdfe9b8',
                'us-east-2b': 'subnet-0ba1722070b8dd5c4',
                'us-east-2c': 'subnet-0ec0911a438c139ea'
            },
            'VpcId': '',
            'Certificates':
            {
                'ClusterCsr': var.pem_csr,
                'HsmCertificate': '',
                'AwsHardwareCertificate': '',
                'ManufacturerHardwareCertificate': '',
                'ClusterCertificate': ''
            },
                'TagList':
                [
                    {
                        'Key': 'Name',
                        'Value': 'cloudhsm_cluster'
                    }
            ]
        }
    ]
}


build_infra_resp = {
    'cluster_id': var.cluster_id,
    'vpc_id': var.vpc_id,
    'instance_id': var.instance_id
}

create_hsm_resp = {
    'Hsm':
    {
        'AvailabilityZone': 'us-east-2a',
        'ClusterId': var.cluster_id,
        'SubnetId': 'subnet-03fce2972dfdfe9b8',
        'HsmId': var.hsm_id,
        'State': 'CREATE_IN_PROGRESS'
    }
}

delete_hsm_resp = {'HsmId': var.hsm_id}

describe_instances_resp = {
    'Reservations':
    [
        {
            'Groups': [],
            'Instances':
            [
                {
                    'AmiLaunchIndex': 0,
                    'ImageId': 'ami-077e31c4939f6a2f3',
                    'InstanceId': var.instance_id,
                    'InstanceType': 't2.micro',
                    'KeyName': var.ssh_key_name,
                    'Monitoring':
                    {
                        'State': 'disabled'
                    },
                        'Placement':
                        {
                            'AvailabilityZone': 'us-east-2a',
                            'GroupName': '',
                            'Tenancy': 'default'
                    },
                            'PrivateDnsName': 'ip-10-0-0-190.us-east-2.compute.internal',
                            'PrivateIpAddress': '10.0.0.190',
                            'ProductCodes': [],
                            'PublicDnsName': '',
                            'State':
                            {
                                'Code': 80,
                                'Name': 'stopped'
                    },
                                'StateTransitionReason': 'User initiated (2021-05-29 01:28:54 GMT)',
                                'SubnetId': 'subnet-01e5b0f8e5be3bf01',
                                'VpcId': var.vpc_id,
                                'Architecture': 'x86_64',
                                'BlockDeviceMappings':
                                [
                                    {
                                        'DeviceName': '/dev/xvda',
                                        'Ebs':
                                        {
                                            'AttachTime': datetime.datetime(2021, 5, 29, 0, 38, 36, tzinfo=tzutc()),
                                            'DeleteOnTermination': True,
                                            'Status': 'attached',
                                            'VolumeId': 'vol-025692bd4913d872c'
                                        }
                                    }
                    ],
                    'ClientToken': 'E8515C74-B4FC-4655-980B-8F4394DF4F16',
                    'EbsOptimized': False,
                    'EnaSupport': True,
                    'Hypervisor': 'xen',
                    'NetworkInterfaces':
                    [
                        {
                            'Attachment':
                            {
                                'AttachTime': datetime.datetime(2021, 5, 29, 0, 38, 35, tzinfo=tzutc()),
                                'AttachmentId': 'eni-attach-0c4c6ca6d1ebf5835',
                                'DeleteOnTermination': True,
                                'DeviceIndex': 0,
                                'Status': 'attached',
                                'NetworkCardIndex': 0
                            },
                            'Description': '',
                            'Groups':
                            [
                                {
                                    'GroupName': 'cloudhsm-cluster-2f2ynawbwz5-sg',
                                    'GroupId': 'sg-0778d7aa573ae2427'
                                },
                                {
                                    'GroupName': 'default',
                                    'GroupId': 'sg-0259648b4083884a5'
                                }
                            ],
                            'Ipv6Addresses': [],
                            'MacAddress': '02:49:e2:cf:b8:f0',
                            'NetworkInterfaceId': 'eni-043e068e735e6279a',
                            'OwnerId': '945793393231',
                            'PrivateDnsName': 'ip-10-0-0-190.us-east-2.compute.internal',
                            'PrivateIpAddress': '10.0.0.190',
                            'PrivateIpAddresses':
                            [
                                {
                                    'Primary': True,
                                    'PrivateDnsName': 'ip-10-0-0-190.us-east-2.compute.internal',
                                    'PrivateIpAddress': '10.0.0.190'
                                }
                            ],
                            'SourceDestCheck': True,
                            'Status': 'in-use',
                            'SubnetId': 'subnet-01e5b0f8e5be3bf01',
                            'VpcId': 'vpc-062a43279040c9896',
                            'InterfaceType': 'interface'
                        }
                    ],
                    'RootDeviceName': '/dev/xvda',
                    'RootDeviceType': 'ebs',
                    'SecurityGroups':
                    [
                        {
                            'GroupName': 'cloudhsm-cluster-2f2ynawbwz5-sg',
                            'GroupId': 'sg-0778d7aa573ae2427'
                        },
                        {
                            'GroupName': 'default',
                            'GroupId': 'sg-0259648b4083884a5'
                        }
                    ],
                    'SourceDestCheck': True,
                    'StateReason':
                    {
                        'Code': 'Client.UserInitiatedShutdown',
                        'Message': 'Client.UserInitiatedShutdown: User initiated shutdown'
                    },
                    'VirtualizationType': 'hvm',
                    'CpuOptions':
                    {
                        'CoreCount': 1,
                        'ThreadsPerCore': 1
                    },
                    'CapacityReservationSpecification':
                    {
                        'CapacityReservationPreference': 'open'
                    },
                    'HibernationOptions':
                    {
                        'Configured': False
                    },
                    'MetadataOptions':
                    {
                        'State': 'applied',
                        'HttpTokens': 'optional',
                        'HttpPutResponseHopLimit': 1,
                        'HttpEndpoint': 'enabled'
                    },
                    'EnclaveOptions':
                    {
                        'Enabled': False
                    }
                }
            ],
            'OwnerId': '945793393231',
            'ReservationId': 'r-0a28e490b4e1ccd0e'
        }
    ],
}

gen_ecc_key_pair_resp = {
    'data':
    {
        'label': var.label,
        'handle': var.handle,
        'private_key_handle': var.private_key_handle,
        'pem': var.pem
    },
    'status_code': 200
}

list_buckets_false_resp = {'Buckets': [], 'Owner': {
    'ID': '6db94838fea6a8498fd800ac2ea3eea867a95870a8e8b263770a751e580c166e'}}

create_bucket_resp = {
    'Location': f'http: //{var.cluster_id}-bucket.s3.amazonaws.com /'}

list_buckets_true_resp = {
    'Buckets':
    [
        {
            'Name': 'cluster-lbtkdldygfh-bucket',
                    'CreationDate': datetime.datetime(2021, 6, 4, 15, 31, 27, tzinfo=tzutc())
        }
    ],
    'Owner':
    {
        'ID': '6db94838fea6a8498fd800ac2ea3eea867a95870a8e8b263770a751e580c166e'
    }
}


list_objects_resp = {
    'Contents':
    [
        {
            'Key': var.address_id,
            'LastModified': datetime.datetime(2021, 6, 4, 16, 52, 31, tzinfo=tzutc()),
            'ETag': '"bde5d79445637dfa506e3de03d137c32"',
            'Size': 308,
            'StorageClass':
            'STANDARD',
            'Owner':
            {
                'ID': '6db94838fea6a8498fd800ac2ea3eea867a95870a8e8b263770a751e580c166e'
            }
        }
    ],
    'Name': 'cluster-lbtkdldygfh-bucket',
    'Prefix': '',
    'MaxKeys': 1000,
    'EncodingType': 'url'
}

obj_data = {
    'pub_key_handle': var.pub_key_handle,
    'private_key_handle': var.private_key_handle,
    'pub_key_pem': var.pub_key_pem,
    'address': var.address
}

body_encoded = json.dumps(obj_data).encode('UTF-8')

body = StreamingBody(io.BytesIO(body_encoded), len(body_encoded))

get_object_resp = {
    'AcceptRanges': 'bytes',
    'LastModified': datetime.datetime(2021, 6, 4, 16, 52, 31, tzinfo=tzutc()),
    'ContentLength': 308,
    'ETag': '"bde5d79445637dfa506e3de03d137c32"',
            'ContentType': 'binary/octet-stream',
            'Metadata': {},
            'Body': body
}


put_object_resp = {
    'ResponseMetadata':
    {
        'RequestId': 'XC168DY8X89V84N7',
        'HostId': '05BOjg6ZL25KfjxZOCbHso7oXzgCAgkHuOdt+PcV1MQmPM/QmaXQPIcJg3+loo8o4ein4P7GmAI=',
        'HTTPStatusCode': 200,
        'HTTPHeaders':
        {
            'x-amz-id-2': '05BOjg6ZL25KfjxZOCbHso7oXzgCAgkHuOdt+PcV1MQmPM/QmaXQPIcJg3+loo8o4ein4P7GmAI=',
            'x-amz-request-id': 'XC168DY8X89V84N7',
            'date': 'Fri, 04 Jun 2021 19:55:51 GMT',
            'etag': '"bde5d79445637dfa506e3de03d137c32"',
            'server': 'AmazonS3',
            'content-length': '0'
        },
            'RetryAttempts': 0
    },
    'ETag': '"bde5d79445637dfa506e3de03d137c32"'
}

address_list = [
    {
        'id': 'addr-2f8558248c33',
        'pub_key_pem': '-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEEEYV4CBaW1Jc9COEwA7fGRgwAYJBpErv\nNT/OSW8sjgNACFj+Q0wy+rkWNlA0nZzIXi/N62dcCoXcs0W+BE9dHg==\n-----END PUBLIC KEY-----\n',
        'pub_key_handle': '2359320',
        'private_key_handle': '2359319',

    }
]
