"""Тесты MCP: аккаунты, представители, примечания, фильтры доступа."""

import json
import pytest
from unittest.mock import patch
from mcp.shared.memory import create_connected_server_and_client_session
from mcp_server_yandex_metrika.server import mcp
from mcp_server_yandex_metrika.models import (
    AccountsResponse, SuccessResponse,
    DelegatesResponse,
    ChartAnnotationsResponse, ChartAnnotationResponse,
    AccessFiltersResponse, AccessFilterResponse,
)


# ── Accounts ──────────────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_accounts():
    mock = {"accounts": [{"user_login": "user1", "created_at": "2024-01-01"}, {"user_login": "user2"}]}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.list_accounts.return_value = mock
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_accounts", {})
            assert not r.isError
            parsed = AccountsResponse(**json.loads(r.content[0].text))
            assert len(parsed.accounts) == 2
            assert parsed.accounts[0].user_login == "user1"


@pytest.mark.anyio
async def test_ym_account_delete():
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.delete_account.return_value = {"success": True}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_account_delete", {"user_login": "testuser"})
            assert not r.isError
            parsed = SuccessResponse(**json.loads(r.content[0].text))
            assert parsed.success is True


# ── Delegates ─────────────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_delegates():
    mock = {"delegates": [{"user_login": "delegate1", "comment": "assistant"}]}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.list_delegates.return_value = mock
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_delegates", {})
            assert not r.isError
            parsed = DelegatesResponse(**json.loads(r.content[0].text))
            assert parsed.delegates[0].user_login == "delegate1"


@pytest.mark.anyio
async def test_ym_delegate_add():
    mock = {"delegates": [{"user_login": "newdelegate"}]}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.add_delegate.return_value = mock
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_delegate_add", {"user_login": "newdelegate"})
            assert not r.isError
            parsed = DelegatesResponse(**json.loads(r.content[0].text))
            assert parsed.delegates[0].user_login == "newdelegate"


@pytest.mark.anyio
async def test_ym_delegate_delete():
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.delete_delegate.return_value = {"success": True}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_delegate_delete", {"user_login": "delegate1"})
            assert not r.isError
            parsed = SuccessResponse(**json.loads(r.content[0].text))
            assert parsed.success is True


# ── Chart Annotations ─────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_chart_annotations():
    mock = {"chart_annotations": [{"id": 1, "date": "2024-01-15", "title": "Release v2.0", "group": "A"}]}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.list_chart_annotations.return_value = mock
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_chart_annotations", {"counter_id": 12345})
            assert not r.isError
            parsed = ChartAnnotationsResponse(**json.loads(r.content[0].text))
            assert parsed.chart_annotations[0].title == "Release v2.0"
            assert parsed.chart_annotations[0].group == "A"


@pytest.mark.anyio
async def test_ym_chart_annotation_create():
    mock = {"chart_annotation": {"id": 99, "date": "2024-03-01", "title": "Deploy", "group": "B"}}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.create_chart_annotation.return_value = mock
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_chart_annotation_create", {"counter_id": 12345, "date": "2024-03-01", "title": "Deploy", "group": "B"})
            assert not r.isError
            parsed = ChartAnnotationResponse(**json.loads(r.content[0].text))
            assert parsed.chart_annotation.id == 99
            assert parsed.chart_annotation.group == "B"


@pytest.mark.anyio
async def test_ym_chart_annotation_delete():
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.delete_chart_annotation.return_value = {"success": True}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_chart_annotation_delete", {"counter_id": 12345, "annotation_id": 1})
            assert not r.isError
            parsed = SuccessResponse(**json.loads(r.content[0].text))
            assert parsed.success is True


# ── Access Filters ────────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_access_filters():
    mock = {"access_filters": [{"id": 1, "name": "Region filter", "expression": "ym:s:regionCity==213"}]}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.list_access_filters.return_value = mock
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_access_filters", {"counter_id": 12345})
            assert not r.isError
            parsed = AccessFiltersResponse(**json.loads(r.content[0].text))
            assert parsed.access_filters[0].name == "Region filter"


@pytest.mark.anyio
async def test_ym_access_filter_create():
    mock = {"access_filter": {"id": 99, "name": "Moscow", "expression": "ym:s:regionCity==213"}}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.create_access_filter.return_value = mock
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_access_filter_create", {"counter_id": 12345, "name": "Moscow", "expression": "ym:s:regionCity==213"})
            assert not r.isError
            parsed = AccessFilterResponse(**json.loads(r.content[0].text))
            assert parsed.access_filter.id == 99


@pytest.mark.anyio
async def test_ym_access_filter_delete():
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.delete_access_filter.return_value = {"success": True}
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_access_filter_delete", {"counter_id": 12345, "access_filter_id": 1})
            assert not r.isError
            parsed = SuccessResponse(**json.loads(r.content[0].text))
            assert parsed.success is True
