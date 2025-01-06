from unittest.mock import MagicMock

import pytest

from airbyte_source_wave_pro.source import (
    SourceWave,
    WaveAuthenticator,
    WaveAWSCostsStream,
    WaveAzureCostsStream,
    WaveGCPCostsStream,
)


def test_check_connection(mocker):
    source = SourceWave()
    logger_mock = MagicMock()
    config = {
        "client_id": "test_client_id",
        "client_secret": "test_client_secret",
        "billing_group_id": "test_billing_group",
    }

    # Mock the token response
    requests_mock = mocker.patch("requests.post")
    requests_mock.return_value.status_code = 200
    requests_mock.return_value.json.return_value = {
        "access_token": "test_token",
        "expires_in": 3600,
    }

    assert source.check_connection(logger_mock, config) == (True, None)

    # Test failure case
    requests_mock.side_effect = Exception("Connection error")
    assert source.check_connection(logger_mock, config) == (
        False,
        "Error while refreshing access token: Connection error",
    )


def test_streams():
    source = SourceWave()
    config = {
        "client_id": "test_client_id",
        "client_secret": "test_client_secret",
        "billing_group_id": "test_billing_group",
    }
    streams = source.streams(config)

    assert len(streams) == 3  # AWS, GCP, Azure
    assert isinstance(streams[0], WaveAWSCostsStream)
    assert isinstance(streams[1], WaveGCPCostsStream)
    assert isinstance(streams[2], WaveAzureCostsStream)
