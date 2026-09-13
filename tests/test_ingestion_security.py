import pytest

from tuckerinc82.ingestion import IngestionError
from tuckerinc82.registry import is_registered_https_url


def test_registered_endpoint_requires_exact_path():
    assert is_registered_https_url(
        "usgs-03378500",
        "https://waterservices.usgs.gov/nwis/iv/?format=json&sites=03378500&parameterCd=00065",
    ) is True
    assert is_registered_https_url(
        "usgs-03378500",
        "https://waterservices.usgs.gov/nwis/iv/other",
    ) is False


def test_invalid_source_request_is_rejected_before_network_call():
    with pytest.raises(IngestionError, match="not registered"):
        from tuckerinc82.ingestion import fetch_json_source

        fetch_json_source(
            source_id="usgs-03378500",
            source_url="https://example.com/unsafe",
            cadence="near_realtime",
            schema_version="1.0",
            geographic_scope="Posey County, Indiana",
            ttl_seconds=900,
        )
