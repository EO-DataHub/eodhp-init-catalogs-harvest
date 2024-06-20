import json
import logging
import os
import time

import pulsar
import pulsar.exceptions

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


def cli(ctx_dict: dict):
    """
    Publish message to Pulsar broker.
    """
    pulsar_url = os.getenv("PULSAR_URL", "")
    ctx_dict["CLIENT"] = pulsar.Client(pulsar_url)
    ctx_dict["TOPIC"] = "harvested"
    logger.info(f"""Connecting to broker '{pulsar_url}' with topic '{ctx_dict["TOPIC"]}'""")

    prefix = "intial-workspace-harvest"

    client: pulsar.Client = ctx_dict["CLIENT"]
    topic: str = ctx_dict["TOPIC"]

    producer: pulsar.Producer = client.create_producer(topic=topic, producer_name=prefix)

    with open("init-catalogs.json") as f:
        harvested_dict = json.load(f)
    harvested_string = json.dumps(harvested_dict)

    try:
        msg = harvested_string
        logger.info(f"Publishing message")
        logger.info(msg)
        producer.send(msg.encode("utf-8"))
    finally:
        producer.close()
        client.close()


if __name__ == "__main__":
    cli(ctx_dict={})
