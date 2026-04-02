from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from keelim_knowledge.mcp import tools


TOOL_REGISTRY: dict[str, Callable[..., Any]] = {
    "list_subprojects": tools.list_subprojects,
    "find_entity": tools.find_entity,
    "find_endpoint": tools.find_endpoint,
    "find_service": tools.find_service,
    "find_bounded_context": tools.find_bounded_context,
    "find_workflow": tools.find_workflow,
    "get_neighbors": tools.get_neighbors,
    "find_path": tools.find_path,
    "trace_data_flow": tools.trace_data_flow,
    "check_graph_health": tools.check_graph_health,
    "analyze_entity_impact": tools.analyze_entity_impact,
}


def available_tools() -> list[str]:
    return sorted(TOOL_REGISTRY)


def dispatch(tool_name: str, config_path: str | Path, **kwargs: Any) -> Any:
    try:
        tool = TOOL_REGISTRY[tool_name]
    except KeyError as exc:
        raise KeyError(f"Unknown tool: {tool_name}") from exc
    return tool(config_path, **kwargs)
