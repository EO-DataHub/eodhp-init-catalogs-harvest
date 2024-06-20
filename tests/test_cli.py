import json
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from init_catalogs.__main__ import cli


# @patch('click.Context')
@patch("os.getenv")
@patch("pulsar.Client")
def test_cli(mock_client_class, mock_getenv):
    # Create variables
    ctx_dict = {"CLIENT": None, "TOPIC": None}
    test_topic = "harvested"
    # Create mocks
    mock_producer = MagicMock()
    mock_client = MagicMock()
    mock_client.create_producer.return_value = mock_producer
    mock_client_class.return_value = mock_client
    mock_getenv.return_value = "pulsar://localhost:6650"

    # Load expected message output data
    with open("init-catalogs.json") as f:
        harvested_dict = json.load(f)
    expected_message = json.dumps(harvested_dict)

    runner = CliRunner()
    result = cli(ctx_dict)

    ##############
    # Assertions #
    ##############

    # Check values set correctly
    assert ctx_dict["CLIENT"] == mock_client
    assert ctx_dict["TOPIC"] == test_topic

    # Check create_producer is only called once with the expected inputs
    mock_client.create_producer.assert_called_once_with(
        topic=test_topic, producer_name="intial-workspace-harvest"
    )

    # Check send is only called once with the expected output message
    mock_producer.send.assert_called_once_with(expected_message.encode("utf-8"))
