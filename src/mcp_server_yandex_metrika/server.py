"""MCP server for Yandex Metrika API."""

import json
import logging
import os
import sys
import tempfile

from mcp.server.fastmcp import FastMCP

from .actions import ACTIONS
from .metrika_api import MetrikaAPI

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", stream=sys.stderr)
log = logging.getLogger(__name__)

mcp = FastMCP(
    "yandex-metrika",
    instructions=(
        "Yandex Metrika API server. "
        "Use ym_search to discover available actions and their parameter schemas. "
        "Use ym_execute to run actions by ID. "
        "Use ym_execute_file for actions that read/write files (uploads, downloads). "
        "Counter ID is required for most actions — pass it in params_json as counter_id."
    ),
)

_api: MetrikaAPI | None = None


def _get_api() -> MetrikaAPI:
    global _api
    if _api is None:
        token = os.getenv("YANDEX_METRIKA_TOKEN")
        if not token:
            raise RuntimeError("YANDEX_METRIKA_TOKEN environment variable is required")
        _api = MetrikaAPI(token)
    return _api


def _to_json(data) -> str:
    return json.dumps(data, ensure_ascii=False)


def _parse_json(text: str, label: str = "JSON") -> any:
    """Parse JSON string with a human-readable error on failure."""
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Invalid {label}: {e}")


def _safe_output_path(path: str) -> str:
    """Resolve and validate output path — only home or system temp allowed."""
    resolved = os.path.realpath(path)
    home = os.path.realpath(os.path.expanduser("~"))

    tmp_dirs = {os.path.realpath(tempfile.gettempdir())}
    if os.path.isdir("/tmp"):
        tmp_dirs.add(os.path.realpath("/tmp"))

    is_under_home = resolved.startswith(home + os.sep)
    is_under_tmp = any(resolved.startswith(d + os.sep) for d in tmp_dirs)

    if not (is_under_home or is_under_tmp):
        raise RuntimeError(f"Output path must be under home or temp directory: {path}")

    if is_under_home and os.sep + "." in resolved[len(home):]:
        raise RuntimeError(f"Writing to hidden files/directories is not allowed: {path}")

    return resolved


# ── Action dispatch ────────────────────────────────────────────────


async def execute_action(action_id: str, raw_params: dict) -> str:
    """Validate params and execute a non-file action. Returns JSON string."""
    act = ACTIONS.get(action_id)
    if not act:
        raise RuntimeError(f"Unknown action: {action_id}. Use ym_search to find actions.")
    if act.is_file:
        raise RuntimeError(f"Action '{action_id}' works with files. Use ym_execute_file instead.")

    if act.params_model:
        validated = act.params_model.model_validate(raw_params)
        params = validated.model_dump()
    else:
        params = raw_params

    result = await act.call_fn(_get_api(), None, params)
    return _to_json(result)


async def execute_file_action(action_id: str, raw_params: dict, file_path: str) -> str:
    """Execute a file action (download or upload). Returns JSON string."""
    act = ACTIONS.get(action_id)
    if not act:
        raise RuntimeError(f"Unknown action: {action_id}. Use ym_search to find actions.")
    if not act.is_file:
        raise RuntimeError(f"Action '{action_id}' does not use files. Use ym_execute instead.")

    safe_path = _safe_output_path(file_path)

    if act.params_model:
        validated = act.params_model.model_validate(raw_params)
        params = validated.model_dump()
    else:
        params = raw_params

    # Upload actions: read file and pass bytes
    if "upload" in action_id:
        with open(safe_path, "rb") as f:
            params["file_data"] = f.read()
        result = await act.call_fn(_get_api(), None, params)
        return _to_json(result)

    # Download actions: get bytes and write to file
    data = await act.call_fn(_get_api(), None, params)
    with open(safe_path, "wb") as f:
        f.write(data)
    return _to_json({"path": safe_path, "size": len(data)})


def _search_actions(query: str, domain: str = "", max_results: int = 10) -> list[dict]:
    """Search actions by query with optional domain filter."""
    query_lower = query.lower()
    tokens = query_lower.split()

    scored: list[tuple[int, dict]] = []
    for action in ACTIONS.values():
        if domain and action.domain != domain:
            continue

        score = 0

        if query_lower == action.id:
            score = 1000

        for token in tokens:
            if token in action.id:
                score += 10
            if token in action.description.lower():
                score += 5
            for kw in action.keywords:
                if token in kw:
                    score += 8
            if token == action.domain:
                score += 3

        if score > 0:
            entry: dict = {
                "id": action.id,
                "domain": action.domain,
                "description": action.description,
                "is_file": action.is_file,
                "is_destructive": action.is_destructive,
            }
            if action.params_model:
                entry["params_schema"] = action.params_model.model_json_schema()
            scored.append((score, entry))

    scored.sort(key=lambda x: -x[0])
    return [entry for _, entry in scored[:max_results]]


# ── Meta-tools ─────────────────────────────────────────────────────


@mcp.tool(annotations={"readOnlyHint": True})
async def ym_search(query: str, domain: str = "") -> str:
    """Find available actions by intent. Optional domain filter:
    reporting, counters, goals, filters, grants, operations, segments,
    labels, accounts, delegates, annotations, access_filters, logs, uploads.
    Returns action ID, description, and JSON Schema of parameters."""
    return _to_json(_search_actions(query, domain))


@mcp.tool(annotations={"readOnlyHint": False})
async def ym_execute(action: str, params_json: str = "{}") -> str:
    """Execute action by ID. params_json validated against action schema.
    Use ym_search to discover actions and their schemas first."""
    raw = _parse_json(params_json, "params_json")
    return await execute_action(action, raw)


@mcp.tool(annotations={"readOnlyHint": False})
async def ym_execute_file(action: str, file_path: str, params_json: str = "{}") -> str:
    """Execute action that reads or writes a file (uploads/downloads).
    file_path must be under ~/... or /tmp/...
    Use ym_search to discover file actions (is_file=true)."""
    raw = _parse_json(params_json, "params_json")
    return await execute_file_action(action, raw, file_path)


# ── Promoted tools ─────────────────────────────────────────────────


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def ym_counters(
    search_string: str = "",
    permission: str = "",
    status: str = "",
    per_page: int = 100,
    offset: int = 1,
) -> str:
    """List counters. Optional filters: search_string, permission (own/view/edit),
    status (Active/Deleted), per_page, offset."""
    params: dict = {"per_page": per_page, "offset": offset}
    if search_string:
        params["search_string"] = search_string
    if permission:
        params["permission"] = permission
    if status:
        params["status"] = status
    api = _get_api()
    return _to_json(await api.list_counters(params))


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def ym_counter(counter_id: int, field: str = "") -> str:
    """Get counter details. field: goals,mirrors,grants,filters,operation."""
    api = _get_api()
    return _to_json(await api.get_counter(counter_id, field))


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def ym_stat_data(
    ids: str,
    metrics: str,
    dimensions: str = "",
    date1: str = "",
    date2: str = "",
    filters: str = "",
    limit: int = 100,
    offset: int = 1,
    sort: str = "",
    preset: str = "",
) -> str:
    """Table report (GET /stat/v1/data). ids and metrics are comma-separated.
    Example: ids='12345', metrics='ym:s:visits,ym:s:users',
    dimensions='ym:s:browser', date1='7daysAgo', date2='today'."""
    api = _get_api()
    params: dict = {"ids": ids, "metrics": metrics, "limit": limit, "offset": offset}
    for key, val in [
        ("dimensions", dimensions), ("date1", date1), ("date2", date2),
        ("filters", filters), ("sort", sort), ("preset", preset),
    ]:
        if val:
            params[key] = val
    return _to_json(await api.get_stat_data(params))


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def ym_stat_data_bytime(
    ids: str,
    metrics: str,
    dimensions: str = "",
    date1: str = "",
    date2: str = "",
    group: str = "day",
    limit: int = 100,
) -> str:
    """Time-series report (GET /stat/v1/data/bytime).
    group: all/auto/minutes/hour/day/week/month/quarter/year."""
    api = _get_api()
    params: dict = {"ids": ids, "metrics": metrics, "group": group, "limit": limit}
    for key, val in [("dimensions", dimensions), ("date1", date1), ("date2", date2)]:
        if val:
            params[key] = val
    return _to_json(await api.get_stat_data_bytime(params))


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def ym_goals(counter_id: int) -> str:
    """List goals for a counter."""
    api = _get_api()
    return _to_json(await api.list_goals(counter_id))


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def ym_segments(counter_id: int) -> str:
    """List segments for a counter."""
    api = _get_api()
    return _to_json(await api.list_segments(counter_id))


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def ym_grants(counter_id: int) -> str:
    """List access grants for a counter."""
    api = _get_api()
    return _to_json(await api.list_grants(counter_id))


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def ym_log_requests(counter_id: int) -> str:
    """List log API requests for a counter."""
    api = _get_api()
    return _to_json(await api.list_log_requests(counter_id))


@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def ym_labels() -> str:
    """List all labels."""
    api = _get_api()
    return _to_json(await api.list_labels())
