from moto import mock_aws
import pytest
from pangu.aws.session import Session

@mock_aws
def test_get_credentials_with_moto():
    session = Session()
    creds = session.get_credentials()
    assert isinstance(creds, dict)
    assert "access_key" in creds
    assert "secret_key" in creds
    assert "token" in creds
    assert creds["access_key"]
    assert creds["secret_key"]

@mock_aws
def test_list_regions_with_moto():
    session = Session()
    regions = session.list_regions(service_name="ec2")
    assert isinstance(regions, list)
    assert "us-east-1" in regions or len(regions) > 0

@mock_aws
def test_list_partitions_with_moto():
    session = Session()
    partitions = session.list_partitions()
    assert isinstance(partitions, list)
    assert "aws" in partitions

@mock_aws
def test_list_services_with_moto():
    session = Session()
    services = session.list_services()
    assert isinstance(services, list)
    assert "ec2" in services or len(services) > 0