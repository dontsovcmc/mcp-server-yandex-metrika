"""Тесты MCP: фильтры, гранты, операции, сегменты, метки."""

import json
import pytest
from unittest.mock import patch, AsyncMock
from mcp.shared.memory import create_connected_server_and_client_session
from mcp_server_yandex_metrika.server import mcp
from mcp_server_yandex_metrika.models import (
    FiltersResponse, FilterResponse, SuccessResponse,
    GrantsResponse, GrantResponse,
    OperationsResponse, OperationResponse,
    SegmentsResponse, SegmentResponse,
    LabelsResponse, LabelResponse,
)


# ── Filters ───────────────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_filters():
    mock = {"filters": [{"id": 1, "attr": "client_ip", "type": "equal", "value": "10.0.0.1", "action": "exclude", "status": "active"}]}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.list_filters = AsyncMock(return_value=mock)
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "filters",
                "params_json": json.dumps({"counter_id": 12345}),
            })
            assert not r.isError
            parsed = FiltersResponse(**json.loads(r.content[0].text))
            assert len(parsed.filters) == 1
            assert parsed.filters[0].attr == "client_ip"
            assert parsed.filters[0].action == "exclude"


@pytest.mark.anyio
async def test_ym_filter():
    mock = {"filter": {"id": 1, "attr": "url", "type": "contain", "value": "/admin"}}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.get_filter = AsyncMock(return_value=mock)
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "filter",
                "params_json": json.dumps({"counter_id": 12345, "filter_id": 1}),
            })
            assert not r.isError
            parsed = FilterResponse(**json.loads(r.content[0].text))
            assert parsed.filter.value == "/admin"


@pytest.mark.anyio
async def test_ym_filter_create():
    mock = {"filter": {"id": 99, "attr": "url", "type": "contain", "value": "/test", "action": "exclude", "status": "active"}}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.create_filter = AsyncMock(return_value=mock)
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "filter_create",
                "params_json": json.dumps({"counter_id": 12345, "attr": "url", "filter_type": "contain", "value": "/test"}),
            })
            assert not r.isError
            parsed = FilterResponse(**json.loads(r.content[0].text))
            assert parsed.filter.id == 99


@pytest.mark.anyio
async def test_ym_filter_delete():
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.delete_filter = AsyncMock(return_value={"success": True})
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "filter_delete",
                "params_json": json.dumps({"counter_id": 12345, "filter_id": 1}),
            })
            assert not r.isError
            parsed = SuccessResponse(**json.loads(r.content[0].text))
            assert parsed.success is True


# ── Grants ────────────────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_grants():
    mock = {"grants": [{"user_login": "analyst", "perm": "view", "comment": "read-only"}]}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.list_grants = AsyncMock(return_value=mock)
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_grants", {"counter_id": 12345})
            assert not r.isError
            parsed = GrantsResponse(**json.loads(r.content[0].text))
            assert parsed.grants[0].user_login == "analyst"
            assert parsed.grants[0].perm == "view"


@pytest.mark.anyio
async def test_ym_grant_create():
    mock = {"grant": {"user_login": "newuser", "perm": "edit"}}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.create_grant = AsyncMock(return_value=mock)
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "grant_create",
                "params_json": json.dumps({"counter_id": 12345, "user_login": "newuser", "perm": "edit"}),
            })
            assert not r.isError
            parsed = GrantResponse(**json.loads(r.content[0].text))
            assert parsed.grant.perm == "edit"


@pytest.mark.anyio
async def test_ym_grant_delete():
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.delete_grant = AsyncMock(return_value={"success": True})
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "grant_delete",
                "params_json": json.dumps({"counter_id": 12345, "user_login": "testuser"}),
            })
            assert not r.isError
            parsed = SuccessResponse(**json.loads(r.content[0].text))
            assert parsed.success is True


# ── Operations ────────────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_operations():
    mock = {"operations": [{"id": 1, "action": "cut_parameter", "attr": "url", "value": "utm_source", "status": "active"}]}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.list_operations = AsyncMock(return_value=mock)
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "operations",
                "params_json": json.dumps({"counter_id": 12345}),
            })
            assert not r.isError
            parsed = OperationsResponse(**json.loads(r.content[0].text))
            assert parsed.operations[0].action == "cut_parameter"
            assert parsed.operations[0].value == "utm_source"


@pytest.mark.anyio
async def test_ym_operation_create():
    mock = {"operation": {"id": 99, "action": "to_lower", "attr": "url", "value": ""}}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.create_operation = AsyncMock(return_value=mock)
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "operation_create",
                "params_json": json.dumps({"counter_id": 12345, "action": "to_lower", "attr": "url", "value": ""}),
            })
            assert not r.isError
            parsed = OperationResponse(**json.loads(r.content[0].text))
            assert parsed.operation.id == 99


@pytest.mark.anyio
async def test_ym_operation_delete():
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.delete_operation = AsyncMock(return_value={"success": True})
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "operation_delete",
                "params_json": json.dumps({"counter_id": 12345, "operation_id": 1}),
            })
            assert not r.isError
            parsed = SuccessResponse(**json.loads(r.content[0].text))
            assert parsed.success is True


# ── Segments ──────────────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_segments():
    mock = {"segments": [{"segment_id": 1, "counter_id": 12345, "name": "Chrome", "expression": "ym:s:browser=='Chrome'", "status": "active", "segment_source": "api"}]}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.list_segments = AsyncMock(return_value=mock)
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_segments", {"counter_id": 12345})
            assert not r.isError
            parsed = SegmentsResponse(**json.loads(r.content[0].text))
            assert parsed.segments[0].name == "Chrome"
            assert parsed.segments[0].segment_source == "api"


@pytest.mark.anyio
async def test_ym_segment_create():
    mock = {"segment": {"segment_id": 99, "name": "Mobile", "expression": "ym:s:deviceCategory=='mobile'"}}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.create_segment = AsyncMock(return_value=mock)
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "segment_create",
                "params_json": json.dumps({
                    "counter_id": 12345, "name": "Mobile",
                    "expression": "ym:s:deviceCategory=='mobile'",
                }),
            })
            assert not r.isError
            parsed = SegmentResponse(**json.loads(r.content[0].text))
            assert parsed.segment.segment_id == 99


@pytest.mark.anyio
async def test_ym_segment_delete():
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.delete_segment = AsyncMock(return_value={"success": True})
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "segment_delete",
                "params_json": json.dumps({"counter_id": 12345, "segment_id": 1}),
            })
            assert not r.isError
            parsed = SuccessResponse(**json.loads(r.content[0].text))
            assert parsed.success is True


# ── Labels ────────────────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_labels():
    mock = {"labels": [{"id": 1, "name": "Production"}, {"id": 2, "name": "Staging"}]}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.list_labels = AsyncMock(return_value=mock)
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_labels", {})
            assert not r.isError
            parsed = LabelsResponse(**json.loads(r.content[0].text))
            assert len(parsed.labels) == 2
            assert parsed.labels[0].name == "Production"


@pytest.mark.anyio
async def test_ym_label_create():
    mock = {"label": {"id": 99, "name": "New Label"}}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.create_label = AsyncMock(return_value=mock)
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "label_create",
                "params_json": json.dumps({"name": "New Label"}),
            })
            assert not r.isError
            parsed = LabelResponse(**json.loads(r.content[0].text))
            assert parsed.label.id == 99


@pytest.mark.anyio
async def test_ym_label_delete():
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.delete_label = AsyncMock(return_value={"success": True})
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "label_delete",
                "params_json": json.dumps({"label_id": 1}),
            })
            assert not r.isError
            parsed = SuccessResponse(**json.loads(r.content[0].text))
            assert parsed.success is True


@pytest.mark.anyio
async def test_ym_counter_label_set():
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.set_counter_label = AsyncMock(return_value={"success": True})
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "counter_label_set",
                "params_json": json.dumps({"counter_id": 12345, "label_id": 1}),
            })
            assert not r.isError
