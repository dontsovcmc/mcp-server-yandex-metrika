import json
import pytest
from unittest.mock import patch, AsyncMock
from mcp.shared.memory import create_connected_server_and_client_session
from mcp_server_yandex_metrika.server import mcp
from mcp_server_yandex_metrika.models import ReportResponse, DrillDownReportResponse, ComparisonReportResponse, ByTimeReportResponse

MOCK_REPORT = {
    "query": {"ids": [12345], "metrics": ["ym:s:visits"]},
    "data": [{"dimensions": [{"name": "Chrome"}], "metrics": [100.0]}],
    "total_rows": 1, "sampled": False, "totals": [100.0],
}


@pytest.mark.anyio
async def test_ym_stat_data():
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.get_stat_data = AsyncMock(return_value=MOCK_REPORT)
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_stat_data", {"ids": "12345", "metrics": "ym:s:visits"})
            assert not r.isError
            data = json.loads(r.content[0].text)
            parsed = ReportResponse(**data)
            assert parsed.total_rows == 1
            assert parsed.data[0].metrics == [100.0]
            assert parsed.sampled is False


@pytest.mark.anyio
async def test_ym_stat_data_with_filters():
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.get_stat_data = AsyncMock(return_value=MOCK_REPORT)
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_stat_data", {
                "ids": "12345", "metrics": "ym:s:visits",
                "dimensions": "ym:s:browser", "date1": "2024-01-01", "date2": "2024-01-31",
                "filters": "ym:s:browser=='Chrome'", "sort": "-ym:s:visits",
            })
            assert not r.isError
            parsed = ReportResponse(**json.loads(r.content[0].text))
            assert parsed.totals == [100.0]


@pytest.mark.anyio
async def test_ym_stat_data_bytime():
    mock = {
        "query": {"ids": [12345]}, "total_rows": 1,
        "data": [{"dimensions": [{"name": "Chrome"}], "metrics": [[10.0, 20.0]]}],
        "totals": [[30.0, 40.0]], "sampled": False,
    }
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.get_stat_data_bytime = AsyncMock(return_value=mock)
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_stat_data_bytime", {"ids": "12345", "metrics": "ym:s:visits"})
            assert not r.isError
            parsed = ByTimeReportResponse(**json.loads(r.content[0].text))
            assert parsed.data[0].metrics == [[10.0, 20.0]]
            assert parsed.totals == [[30.0, 40.0]]


@pytest.mark.anyio
async def test_ym_stat_data_drilldown():
    mock = {
        "data": [{"dimension": {"name": "Chrome"}, "metrics": [100.0], "expand": True}],
        "total_rows": 1, "totals": [100.0],
    }
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.get_stat_data_drilldown = AsyncMock(return_value=mock)
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "stat_data_drilldown",
                "params_json": json.dumps({"ids": "12345", "metrics": "ym:s:visits"}),
            })
            assert not r.isError
            parsed = DrillDownReportResponse(**json.loads(r.content[0].text))
            assert parsed.data[0].expand is True
            assert parsed.data[0].metrics == [100.0]


@pytest.mark.anyio
async def test_ym_stat_data_comparison():
    mock = {
        "data": [{"dimensions": [{"name": "Chrome"}], "metrics": {"a": [100.0], "b": [200.0]}}],
        "total_rows": 1, "totals": {"a": [100.0], "b": [200.0]},
    }
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.get_stat_data_comparison = AsyncMock(return_value=mock)
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "stat_data_comparison",
                "params_json": json.dumps({"ids": "12345", "metrics": "ym:s:visits"}),
            })
            assert not r.isError
            parsed = ComparisonReportResponse(**json.loads(r.content[0].text))
            assert parsed.totals["a"] == [100.0]


@pytest.mark.anyio
async def test_ym_stat_data_comparison_drilldown():
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.get_stat_data_comparison_drilldown = AsyncMock(return_value=MOCK_REPORT)
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_execute", {
                "action": "stat_data_comparison_drilldown",
                "params_json": json.dumps({"ids": "12345", "metrics": "ym:s:visits"}),
            })
            assert not r.isError
