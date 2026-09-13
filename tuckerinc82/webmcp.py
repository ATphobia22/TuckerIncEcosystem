from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class WebMCPTool:
    name: str
    description: str
    input_schema: dict[str, Any]
    read_only: bool = True
    consequential: bool = False

    def as_browser_registration(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": self.input_schema,
            "annotations": {"readOnlyHint": self.read_only},
        }


class GovernedWebMCPRegistry:
    """Server-side declaration registry for tools exposed by a browser client.

    WebMCP itself is browser-native. This registry deliberately does not emulate
    an MCP transport; it provides policy metadata and schema material for the
    frontend to register with document.modelContext.
    """

    def __init__(self) -> None:
        self._tools: dict[str, tuple[WebMCPTool, Callable[..., Any]]] = {}

    def register(self, tool: WebMCPTool, handler: Callable[..., Any]) -> None:
        if tool.name in self._tools:
            raise ValueError(f"duplicate WebMCP tool: {tool.name}")
        if tool.consequential and tool.read_only:
            raise ValueError("consequential tools cannot be marked read-only")
        self._tools[tool.name] = (tool, handler)

    def manifest(self) -> list[dict[str, Any]]:
        return [tool.as_browser_registration() for tool, _ in self._tools.values()]

    def execute(self, name: str, arguments: dict[str, Any], *, user_confirmed: bool = False) -> Any:
        tool, handler = self._tools[name]
        if tool.consequential and not user_confirmed:
            raise PermissionError("consequential WebMCP action requires explicit user confirmation")
        return handler(**arguments)
