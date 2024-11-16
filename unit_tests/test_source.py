from unittest.mock import MagicMock

from YOUR_PACKAGE.source import SourceYOUR_PACKAGE


def test_check_connection(mocker):
    source = SourceYOUR_PACKAGE()
    logger_mock = MagicMock()
    config = {
        # Add your test config here
    }

    requests_mock = mocker.patch("requests.get")
    requests_mock.return_value.status_code = 200
    assert source.check_connection(logger_mock, config) == (True, None)

    requests_mock.return_value.status_code = 403
    requests_mock.return_value.text = "Unauthorized"
    assert source.check_connection(logger_mock, config) == (
        False,
        "HTTP 403: Unauthorized",
    )

    requests_mock.side_effect = Exception("Connection error")
    assert source.check_connection(logger_mock, config) == (False, "Connection error")


def test_streams(mocker):
    source = SourceYOUR_PACKAGE()
    config = {
        # Add your test config here
    }
    streams = source.streams(config)
    expected_streams_number = 1  # Adjust based on your implementation
    assert len(streams) == expected_streams_number
