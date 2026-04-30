import json
import pytest
from unittest.mock import patch, AsyncMock
from mcp.shared.memory import create_connected_server_and_client_session
from mcp_server_yandex_metrika.server import mcp
from mcp_server_yandex_metrika.models import GoalsResponse, GoalResponse, SuccessResponse


@pytest.mark.anyio
async def test_ym_goals():
    mock = {"goals": [
        {"id": 1, "name": "Purchase", "type": "url", "conditions": [{"type": "contain", "url": "/thank"}]},
        {"id": 2, "name": "Deep visit", "type": "number", "depth": 5},
    ]}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.list_goals = AsyncMock(return_value=mock)
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_goals", {"counter_id": 12345})
            assert not r.isError
            parsed = GoalsResponse(**json.loads(r.content[0].text))
            assert len(parsed.goals) == 2
            assert parsed.goals[0].type == "url"
            assert parsed.goals[0].conditions[0].url == "/thank"
            assert parsed.goals[1].depth == 5


@pytest.mark.anyio
async def test_ym_goal():
    mock = {"goal": {"id": 1, "name": "Purchase", "type": "url", "default_price": 500.0, "is_favorite": True}}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.get_goal = AsyncMock(return_value=mock)
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "goal",
                "params_json": json.dumps({"counter_id": 12345, "goal_id": 1}),
            })
            assert not r.isError
            parsed = GoalResponse(**json.loads(r.content[0].text))
            assert parsed.goal.id == 1
            assert parsed.goal.default_price == 500.0
            assert parsed.goal.is_favorite is True


@pytest.mark.anyio
async def test_ym_goal_create():
    mock = {"goal": {"id": 99, "name": "New Goal", "type": "url", "goal_source": "user"}}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.create_goal = AsyncMock(return_value=mock)
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "goal_create",
                "params_json": json.dumps({
                    "counter_id": 12345, "name": "New Goal", "goal_type": "url",
                    "conditions_json": '[{"type":"contain","url":"/done"}]',
                }),
            })
            assert not r.isError
            parsed = GoalResponse(**json.loads(r.content[0].text))
            assert parsed.goal.id == 99
            assert parsed.goal.goal_source == "user"


@pytest.mark.anyio
async def test_ym_goal_update():
    mock = {"goal": {"id": 1, "name": "Updated", "type": "url"}}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.update_goal = AsyncMock(return_value=mock)
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "goal_update",
                "params_json": json.dumps({"counter_id": 12345, "goal_id": 1, "name": "Updated"}),
            })
            assert not r.isError
            parsed = GoalResponse(**json.loads(r.content[0].text))
            assert parsed.goal.name == "Updated"


@pytest.mark.anyio
async def test_ym_goal_delete():
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.delete_goal = AsyncMock(return_value={"success": True})
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "goal_delete",
                "params_json": json.dumps({"counter_id": 12345, "goal_id": 1}),
            })
            assert not r.isError
            parsed = SuccessResponse(**json.loads(r.content[0].text))
            assert parsed.success is True
