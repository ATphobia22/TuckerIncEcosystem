from __future__ import annotations

import pytest

from tuckerinc82.openviking_boundary import OpenVikingBoundary


def test_openviking_is_external_service_boundary() -> None:
    boundary = OpenVikingBoundary("https://openviking.example")
    assert boundary.resource_uri("resources/project") == "viking://resources/project"
    with pytest.raises(ValueError):
        boundary.resource_uri("/")
