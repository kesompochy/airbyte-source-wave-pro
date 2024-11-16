from datetime import datetime

from pytest import fixture

from YOUR_PACKAGE.source import IncrementalYOUR_PACKAGE_Stream


@fixture
def patch_incremental_base_class(mocker):
    mocker.patch.object(IncrementalYOUR_PACKAGE_Stream, "path", "v1/example_endpoint")
    mocker.patch.object(
        IncrementalYOUR_PACKAGE_Stream, "primary_key", "test_primary_key"
    )
    mocker.patch.object(IncrementalYOUR_PACKAGE_Stream, "__abstractmethods__", set())


def test_cursor_field(patch_incremental_base_class):
    stream = IncrementalYOUR_PACKAGE_Stream()
    assert stream.cursor_field == "updated_at"


def test_get_updated_state(patch_incremental_base_class):
    stream = IncrementalYOUR_PACKAGE_Stream()
    inputs = {
        "current_stream_state": {},
        "latest_record": {"updated_at": "2024-03-20T00:00:00Z"},
    }
    assert stream.get_updated_state(**inputs) == {"updated_at": "2024-03-20T00:00:00Z"}


def test_supports_incremental(patch_incremental_base_class):
    stream = IncrementalYOUR_PACKAGE_Stream()
    assert stream.supports_incremental


def test_stream_checkpoint_interval(patch_incremental_base_class):
    stream = IncrementalYOUR_PACKAGE_Stream()
    assert stream.state_checkpoint_interval == 500
