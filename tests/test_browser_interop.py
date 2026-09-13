from __future__ import annotations

import pytest

from tuckerinc82.chrome_ai import capability_descriptor
from tuckerinc82.turbovec_boundary import TurboVecBoundary
from tuckerinc82.webmcp import GovernedWebMCPRegistry, WebMCPTool


def test_optional_turbovec_boundary_does_not_import_eagerly() -> None:
    boundary = TurboVecBoundary(dimension=8)
    assert isinstance(boundary.available, bool)
    with pytest.raises(RuntimeError):
        boundary.search([], k=1)


def test_chrome_capability_is_explicitly_client_side() -> None:
    descriptor = capability_descriptor()
    assert descriptor["client_only"] is True


def test_webmcp_consequential_tool_requires_confirmation() -> None:
    registry = GovernedWebMCPRegistry()
    registry.register(
        WebMCPTool(
            name="dangerous",
            description="Example consequential action",
            input_schema={"type": "object"},
            read_only=False,
            consequential=True,
        ),
        lambda: "done",
    )
    with pytest.raises(PermissionError):
        registry.execute("dangerous", {})
    assert registry.execute("dangerous", {}, user_confirmed=True) == "done"
