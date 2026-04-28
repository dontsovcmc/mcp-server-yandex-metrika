"""Тесты MCP: Logs API и импорт данных."""

import json
import pytest
from unittest.mock import patch
from mcp.shared.memory import create_connected_server_and_client_session
from mcp_server_yandex_metrika.server import mcp
from mcp_server_yandex_metrika.models import (
    LogRequestsResponse, LogRequestResponse, LogRequestEvaluationResponse,
    UploadListResponse,
)


# ── Logs API ──────────────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_log_requests():
    mock = {"requests": [
        {"request_id": 1, "counter_id": 12345, "source": "visits", "status": "processed", "date1": "2024-01-01", "date2": "2024-01-31"},
        {"request_id": 2, "source": "hits", "status": "created"},
    ]}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.list_log_requests.return_value = mock
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_log_requests", {"counter_id": 12345})
            assert not r.isError
            parsed = LogRequestsResponse(**json.loads(r.content[0].text))
            assert len(parsed.requests) == 2
            assert parsed.requests[0].source == "visits"
            assert parsed.requests[0].status == "processed"


@pytest.mark.anyio
async def test_ym_log_request():
    mock = {"log_request": {"request_id": 42, "counter_id": 12345, "source": "visits", "fields": ["ym:s:date", "ym:s:visitID"], "status": "processed", "size": 1048576}}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.get_log_request.return_value = mock
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_log_request", {"counter_id": 12345, "request_id": 42})
            assert not r.isError
            parsed = LogRequestResponse(**json.loads(r.content[0].text))
            assert parsed.log_request.request_id == 42
            assert parsed.log_request.fields == ["ym:s:date", "ym:s:visitID"]
            assert parsed.log_request.size == 1048576


@pytest.mark.anyio
async def test_ym_log_request_create():
    mock = {"log_request": {"request_id": 100, "source": "visits", "status": "created"}}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.create_log_request.return_value = mock
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_log_request_create", {
                "counter_id": 12345, "date1": "2024-01-01", "date2": "2024-01-31",
                "fields": "ym:s:date,ym:s:visitID", "source": "visits",
            })
            assert not r.isError
            parsed = LogRequestResponse(**json.loads(r.content[0].text))
            assert parsed.log_request.request_id == 100
            assert parsed.log_request.status == "created"


@pytest.mark.anyio
async def test_ym_log_request_evaluate():
    mock = {"log_request_evaluation": {"possible": True, "max_possible_day_quantity": 60}}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.evaluate_log_request.return_value = mock
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_log_request_evaluate", {
                "counter_id": 12345, "date1": "2024-01-01", "date2": "2024-01-31",
                "fields": "ym:s:date", "source": "visits",
            })
            assert not r.isError
            parsed = LogRequestEvaluationResponse(**json.loads(r.content[0].text))
            assert parsed.log_request_evaluation.possible is True
            assert parsed.log_request_evaluation.max_possible_day_quantity == 60


@pytest.mark.anyio
async def test_ym_log_request_clean():
    mock = {"log_request": {"request_id": 1, "status": "cleaned_by_user"}}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.clean_log_request.return_value = mock
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_log_request_clean", {"counter_id": 12345, "request_id": 1})
            assert not r.isError
            parsed = LogRequestResponse(**json.loads(r.content[0].text))
            assert parsed.log_request.status == "cleaned_by_user"


@pytest.mark.anyio
async def test_ym_log_request_cancel():
    mock = {"log_request": {"request_id": 1, "status": "canceled"}}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.cancel_log_request.return_value = mock
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_log_request_cancel", {"counter_id": 12345, "request_id": 1})
            assert not r.isError
            parsed = LogRequestResponse(**json.loads(r.content[0].text))
            assert parsed.log_request.status == "canceled"


# ── Upload ────────────────────────────────────────────────────────


@pytest.mark.anyio
async def test_ym_offline_conversions_uploads():
    mock = {"uploadings": [{"id": 1, "status": "PROCESSED", "source_quantity": 100}]}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.list_offline_conversion_uploads.return_value = mock
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_offline_conversions_uploads", {"counter_id": 12345})
            assert not r.isError
            parsed = UploadListResponse(**json.loads(r.content[0].text))
            assert parsed.uploadings[0].status == "PROCESSED"
            assert parsed.uploadings[0].source_quantity == 100


@pytest.mark.anyio
async def test_ym_calls_uploads():
    mock = {"uploadings": [{"id": 1, "status": "IN_PROGRESS"}]}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.list_calls_uploads.return_value = mock
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_calls_uploads", {"counter_id": 12345})
            assert not r.isError
            parsed = UploadListResponse(**json.loads(r.content[0].text))
            assert parsed.uploadings[0].status == "IN_PROGRESS"


@pytest.mark.anyio
async def test_ym_offline_conversion_upload_info():
    mock = {"uploading": {"id": 42, "status": "PROCESSED", "source_quantity": 500}}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.get_offline_conversion_upload.return_value = mock
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_offline_conversion_upload_info", {"counter_id": 12345, "upload_id": 42})
            assert not r.isError
            data = json.loads(r.content[0].text)
            from mcp_server_yandex_metrika.models import UploadResponse
            parsed = UploadResponse(**data)
            assert parsed.uploading.id == 42


@pytest.mark.anyio
async def test_ym_calls_upload_info():
    mock = {"uploading": {"id": 10, "status": "PROCESSED"}}
    with patch("mcp_server_yandex_metrika.server.MetrikaAPI") as M:
        M.return_value.get_calls_upload.return_value = mock
        async with create_connected_server_and_client_session(mcp._mcp_server) as s:
            r = await s.call_tool("ym_calls_upload_info", {"counter_id": 12345, "upload_id": 10})
            assert not r.isError
            data = json.loads(r.content[0].text)
            from mcp_server_yandex_metrika.models import UploadResponse
            parsed = UploadResponse(**data)
            assert parsed.uploading.status == "PROCESSED"
