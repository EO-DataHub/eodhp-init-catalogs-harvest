import json
import logging
import os
import time

import boto3
import pulsar
import pulsar.exceptions
from botocore.exceptions import ClientError

# create logger for stac fastapi ingester
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(filename="stac-fastapi-init-ingest.log", encoding="utf-8", level=logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# set the time converter to UTC
formatter.converter = time.gmtime

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

# Configure root key path in S3
ROOT_KEY_PATH = os.getenv("ROOT_KEY_PATH", "git-harvester")


def create_catalogs():
    """
    Create initial catalogs for the workspace.
    """
    logger.info("Creating initial catalogs")

    s3_client = boto3.client("s3")
    bucket_name = os.getenv("BUCKET_NAME", "")

    # Get files from folder
    for root, _, files in os.walk("catalogs"):
        for file in files:
            file_path = os.path.join(root, file)
            file_name = os.path.basename(file_path)
            key = ROOT_KEY_PATH + "/" + file_name
            logger.info(f"Uploading file '{file_path}' to bucket '{bucket_name}' with key '{key}'")
            try:
                s3_client.head_object(Bucket=bucket_name, Key=key)
                logger.info(f"File '{key}' already exists in bucket '{bucket_name}'")
            except ClientError as e:
                if e.response["Error"]["Code"] == "404":
                    s3_client.upload_file(file_path, bucket_name, key)
                    logger.info(
                        f"File '{file_path}' uploaded to bucket '{bucket_name}' with key '{key}'"
                    )
                else:
                    logger.error(
                        f"Error checking if file '{key}' exists in bucket '{bucket_name}': {e}"
                    )


def cli():
    """
    Publish message to Pulsar broker.
    """
    pulsar_url = os.getenv("PULSAR_URL", "")
    client: pulsar.Client = pulsar.Client(pulsar_url)
    topic: str = "harvested"
    logger.info(f"""Connecting to broker '{pulsar_url}' with topic '{topic}'""")

    prefix = "intial-workspace-harvest"

    producer: pulsar.Producer = client.create_producer(topic=topic, producer_name=prefix)

    # First create the catalogs in S3
    create_catalogs()

    with open("init-catalogs.json") as f:
        harvested_dict = json.load(f)
        harvested_dict["bucket_name"] = os.getenv("BUCKET_NAME", "")
        harvested_dict["added_keys"] = [
            added_key.replace("{ROOT_KEY_PATH}", ROOT_KEY_PATH)
            for added_key in harvested_dict["added_keys"]
        ]
        harvested_dict["updated_keys"] = [
            updated_key.replace("{ROOT_KEY_PATH}", ROOT_KEY_PATH)
            for updated_key in harvested_dict["updated_keys"]
        ]
        harvested_dict["deleted_keys"] = [
            deleted_key.replace("{ROOT_KEY_PATH}", ROOT_KEY_PATH)
            for deleted_key in harvested_dict["deleted_keys"]
        ]
    harvested_string = json.dumps(harvested_dict)

    try:
        msg = harvested_string
        logger.info("Publishing message")
        logger.info(msg)
        producer.send(msg.encode("utf-8"))
    finally:
        producer.close()
        client.close()


if __name__ == "__main__":
    cli()
