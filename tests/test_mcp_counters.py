import json
import pytest
from unittest.mock import patch, AsyncMock
from mcp.shared.memory import create_connected_server_and_client_session
from mcp_server_yandex_metrika.server import mcp
from mcp_server_yandex_metrika.models import CountersResponse, CounterResponse, SuccessResponse


@pytest.mark.anyio
async def test_ym_counters():
    mock = {"rows": 2, "counters": [{"id": 1, "name": "A", "status": "Active"}, {"id": 2, "name": "B"}]}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.list_counters = AsyncMock(return_value=mock)
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_counters", {})
            assert not r.isError
            parsed = CountersResponse(**json.loads(r.content[0].text))
            assert parsed.rows == 2
            assert len(parsed.counters) == 2
            assert parsed.counters[0].id == 1
            assert parsed.counters[0].name == "A"


@pytest.mark.anyio
async def test_ym_counters_with_search():
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.list_counters = AsyncMock(return_value={"rows": 1, "counters": [{"id": 1, "name": "shop"}]})
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_counters", {"search_string": "shop", "permission": "own"})
            assert not r.isError


@pytest.mark.anyio
async def test_ym_counter():
    mock = {"counter": {"id": 12345, "name": "Test", "site": "example.com", "status": "Active", "time_zone_name": "Europe/Moscow"}}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.get_counter = AsyncMock(return_value=mock)
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_counter", {"counter_id": 12345})
            assert not r.isError
            parsed = CounterResponse(**json.loads(r.content[0].text))
            assert parsed.counter.id == 12345
            assert parsed.counter.name == "Test"
            assert parsed.counter.site == "example.com"


@pytest.mark.anyio
async def test_ym_counter_create():
    mock = {"counter": {"id": 99999, "name": "New Site", "site2": {"site": "new.com"}}}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.create_counter = AsyncMock(return_value=mock)
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "counter_create",
                "params_json": json.dumps({"name": "New Site", "site": "new.com"}),
            })
            assert not r.isError
            parsed = CounterResponse(**json.loads(r.content[0].text))
            assert parsed.counter.id == 99999


@pytest.mark.anyio
async def test_ym_counter_update():
    mock = {"counter": {"id": 12345, "name": "Updated"}}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.update_counter = AsyncMock(return_value=mock)
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "counter_update",
                "params_json": json.dumps({"counter_id": 12345, "name": "Updated"}),
            })
            assert not r.isError
            parsed = CounterResponse(**json.loads(r.content[0].text))
            assert parsed.counter.name == "Updated"


@pytest.mark.anyio
async def test_ym_counter_delete():
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.delete_counter = AsyncMock(return_value={"success": True})
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "counter_delete",
                "params_json": json.dumps({"counter_id": 12345}),
            })
            assert not r.isError
            parsed = SuccessResponse(**json.loads(r.content[0].text))
            assert parsed.success is True


@pytest.mark.anyio
async def test_ym_counter_undelete():
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.undelete_counter = AsyncMock(return_value={"success": True})
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "counter_undelete",
                "params_json": json.dumps({"counter_id": 12345}),
            })
            assert not r.isError
            parsed = SuccessResponse(**json.loads(r.content[0].text))
            assert parsed.success is True
