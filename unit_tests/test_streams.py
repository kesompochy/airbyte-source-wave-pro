from http import HTTPStatus
from unittest.mock import MagicMock

import pytest

from YOUR_PACKAGE.source import YOUR_PACKAGE_Stream


@pytest.fixture
def patch_base_class(mocker):
    mocker.patch.object(YOUR_PACKAGE_Stream, "path", "v1/example_endpoint")
    mocker.patch.object(YOUR_PACKAGE_Stream, "primary_key", "test_primary_key")
    mocker.patch.object(YOUR_PACKAGE_Stream, "__abstractmethods__", set())


def test_request_params(patch_base_class):
    stream = YOUR_PACKAGE_Stream()
    inputs = {"stream_slice": None, "stream_state": None, "next_page_token": None}
    expected_params = {}
    assert stream.request_params(**inputs) == expected_params


def test_next_page_token(patch_base_class):
    stream = YOUR_PACKAGE_Stream()
    response = MagicMock()
    response.json.return_value = {}
    assert stream.next_page_token(response) is None


def test_parse_response(patch_base_class):
    stream = YOUR_PACKAGE_Stream()
    response = MagicMock()
    expected_parsed_object = {}
    assert next(stream.parse_response(response)) == expected_parsed_object


@pytest.mark.parametrize(
    ("http_status", "should_retry"),
    [
        (HTTPStatus.OK, False),
        (HTTPStatus.BAD_REQUEST, False),
        (HTTPStatus.TOO_MANY_REQUESTS, True),
        (HTTPStatus.INTERNAL_SERVER_ERROR, True),
    ],
)
def test_should_retry(patch_base_class, http_status, should_retry):
    response_mock = MagicMock()
    response_mock.status_code = http_status
    stream = YOUR_PACKAGE_Stream()
    assert stream.should_retry(response_mock) == should_retry
