import json
import os
from unittest.mock import MagicMock, patch

import boto3
import pytest
from moto import mock_aws

from init_catalogs.__main__ import cli, create_catalogs


@pytest.fixture
def s3_bucket():
    with mock_aws():
        s3 = boto3.client("s3", region_name="us-east-1")
        bucket_name = "test-bucket"
        s3.create_bucket(Bucket=bucket_name)
        os.environ["BUCKET_NAME"] = bucket_name
        yield bucket_name


def test_create_catalogs(s3_bucket, tmpdir):
    # Set the ROOT_KEY_PATH environment variable
    root_key_path = os.getenv("ROOT_KEY_PATH", "git-harvester")

    # Run the create_catalogs function
    create_catalogs()

    # Verify that the files were uploaded to the S3 bucket
    s3 = boto3.client("s3")
    uploaded_files = s3.list_objects_v2(Bucket=s3_bucket)["Contents"]
    uploaded_keys = [file["Key"] for file in uploaded_files]

    assert f"{root_key_path}/public.json" in uploaded_keys
    assert f"{root_key_path}/commercial.json" in uploaded_keys
    assert f"{root_key_path}/user.json" in uploaded_keys


# @patch('click.Context')
@patch("init_catalogs.__main__.create_catalogs")
@patch("pulsar.Client")
@patch.dict("os.environ", {"BUCKET_NAME": "test-bucket", "PULSAR_URL": "pulsar://localhost:6650"})
def test_cli(mock_client_class, mock_create_catalogs):
    # Create variables
    test_topic = "harvested"

    # Create mocks
    mock_producer = MagicMock()
    mock_client = MagicMock()
    mock_client.create_producer.return_value = mock_producer
    mock_client_class.return_value = mock_client
    mock_create_catalogs.return_value = None

    # Load expected message output data
    harvested_dict = {
        "id": "resource-catalogue/load-default-catalogs",
        "workspace": "default_workspace",
        "repository": "",
        "branch": "main",
        "bucket_name": "test-bucket",
        "updated_keys": [],
        "added_keys": [
            "git-harvester/public.json",
            "git-harvester/commercial.json",
            "git-harvester/user.json",
        ],
        "deleted_keys": [],
        "source": "/",
        "target": "/",
    }

    expected_message = json.dumps(harvested_dict)

    cli()

    ##############
    # Assertions #
    ##############

    # Check create_producer is only called once with the expected inputs
    mock_client.create_producer.assert_called_once_with(
        topic=test_topic, producer_name="intial-workspace-harvest"
    )

    # Check send is only called once with the expected output message
    mock_producer.send.assert_called_once_with(expected_message.encode("utf-8"))

    # Check catalogs were created in S3
    mock_create_catalogs.assert_called_once()
