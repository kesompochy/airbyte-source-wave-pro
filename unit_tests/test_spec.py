from YOUR_PACKAGE.source import SourceYOUR_PACKAGE


def test_spec_matches_source():
    source = SourceYOUR_PACKAGE()
    spec = source.spec(None)

    # Test your spec validation here
    assert spec.connectionSpecification["type"] == "object"

    # Test your config validation here
    config = {
        # Add your test config here
    }

    stream = source.streams(config)[0]
    # Add your stream property assertions here
