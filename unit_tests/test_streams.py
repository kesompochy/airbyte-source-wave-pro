from unittest.mock import MagicMock

import pytest

from airbyte_source_wave_pro.source import (
    WaveAuthenticator,
    WaveAWSCostsStream,
    WaveAzureCostsStream,
    WaveGCPCostsStream,
)


@pytest.fixture
def auth():
    return WaveAuthenticator(
        token_refresh_endpoint="https://test.com/token",
        client_id="test_client_id",
        client_secret="test_client_secret",
    )


@pytest.fixture
def config():
    return {"billing_group_id": "test_group", "start_date": "20240101"}


def test_aws_stream(auth, config):
    stream = WaveAWSCostsStream(authenticator=auth, config=config)
    assert stream.vendor == "aws"
    assert stream.cursor_field == "date"
    assert "date" in stream.primary_key
    assert stream.path() == "/m/blue/cost/v1/aws/costs:read"


def test_gcp_stream(auth, config):
    stream = WaveGCPCostsStream(authenticator=auth, config=config)
    assert stream.vendor == "gcp"
    assert "sku" in stream.primary_key
    assert stream.path() == "/m/blue/cost/v1/gcp/costs:read"


def test_azure_stream(auth, config):
    stream = WaveAzureCostsStream(authenticator=auth, config=config)
    assert stream.vendor == "azure"
    assert "subscriptionId" in stream.primary_key
    assert stream.path() == "/m/blue/cost/v1/azure/costs:read"


def test_request_body_json(auth, config):
    stream = WaveAWSCostsStream(authenticator=auth, config=config)
    body = stream.request_body_json()
    assert "startTime" in body
    assert "endTime" in body
    assert body["billingGroupId"] == "test_group"


def test_parse_response(auth, config, mocker):
    stream = WaveAWSCostsStream(authenticator=auth, config=config)
    response_mock = mocker.MagicMock()
    response_mock.iter_lines.return_value = [
        b'{"result": {"aws": {"date": "2024-01-01", "cost": 100}}}'
    ]

    records = list(stream.parse_response(response_mock))
    assert len(records) == 1
    assert records[0]["date"] == "2024-01-01"
    assert records[0]["cost"] == 100
