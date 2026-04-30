"""Клиент для API Яндекс Метрики.

Docs: https://yandex.com/dev/metrika
Base URL: https://api-metrika.yandex.net
"""

import logging
import sys

import httpx

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", stream=sys.stderr)
log = logging.getLogger(__name__)

BASE_URL = "https://api-metrika.yandex.net"

_ERROR_MESSAGES = {
    401: "Invalid or expired token. Check YANDEX_METRIKA_TOKEN.",
    403: "Access denied. Check counter permissions.",
    429: "Rate limit exceeded. Wait and retry.",
}


class MetrikaAPI:
    """Асинхронный клиент API Яндекс Метрики."""

    def __init__(self, token: str):
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"OAuth {token}",
                "Content-Type": "application/x-yametrika+json",
            },
            timeout=30,
        )
        log.info("Яндекс Метрика клиент инициализирован")

    async def _get(self, path: str, **kwargs) -> dict:
        resp = await self.client.get(f"{BASE_URL}{path}", **kwargs)
        if not resp.is_success:
            log.debug("GET %s -> %d: %s", path, resp.status_code, resp.text)
            msg = _ERROR_MESSAGES.get(resp.status_code, f"GET {path} -> {resp.status_code}")
            raise RuntimeError(msg)
        return resp.json()

    async def _post(self, path: str, payload: dict | None = None, **kwargs) -> dict:
        resp = await self.client.post(f"{BASE_URL}{path}", json=payload, **kwargs)
        if not resp.is_success:
            log.debug("POST %s -> %d: %s", path, resp.status_code, resp.text)
            msg = _ERROR_MESSAGES.get(resp.status_code, f"POST {path} -> {resp.status_code}")
            raise RuntimeError(msg)
        return resp.json()

    async def _put(self, path: str, payload: dict | None = None, **kwargs) -> dict:
        resp = await self.client.put(f"{BASE_URL}{path}", json=payload, **kwargs)
        if not resp.is_success:
            log.debug("PUT %s -> %d: %s", path, resp.status_code, resp.text)
            msg = _ERROR_MESSAGES.get(resp.status_code, f"PUT {path} -> {resp.status_code}")
            raise RuntimeError(msg)
        return resp.json()

    async def _delete(self, path: str, **kwargs) -> dict:
        resp = await self.client.delete(f"{BASE_URL}{path}", **kwargs)
        if not resp.is_success:
            log.debug("DELETE %s -> %d: %s", path, resp.status_code, resp.text)
            msg = _ERROR_MESSAGES.get(resp.status_code, f"DELETE {path} -> {resp.status_code}")
            raise RuntimeError(msg)
        return resp.json()

    async def _post_file(self, path: str, file_data: bytes, content_type: str = "text/csv", **kwargs) -> dict:
        headers = {**self.client.headers, "Content-Type": content_type}
        resp = await self.client.post(
            f"{BASE_URL}{path}", content=file_data, headers=headers, timeout=60, **kwargs,
        )
        if not resp.is_success:
            log.debug("POST %s -> %d: %s", path, resp.status_code, resp.text)
            msg = _ERROR_MESSAGES.get(resp.status_code, f"POST {path} -> {resp.status_code}")
            raise RuntimeError(msg)
        return resp.json()

    async def _get_raw(self, path: str, **kwargs) -> bytes:
        resp = await self.client.get(f"{BASE_URL}{path}", timeout=60, **kwargs)
        if not resp.is_success:
            log.debug("GET %s -> %d: %s", path, resp.status_code, resp.text)
            msg = _ERROR_MESSAGES.get(resp.status_code, f"GET {path} -> {resp.status_code}")
            raise RuntimeError(msg)
        return resp.content

    # ── Reporting API ─────────────────────────────────────────────────

    async def get_stat_data(self, params: dict) -> dict:
        """Получение данных — табличный отчёт (GET /stat/v1/data)."""
        return await self._get("/stat/v1/data", params=params)

    async def get_stat_data_bytime(self, params: dict) -> dict:
        """Получение данных — отчёт по времени (GET /stat/v1/data/bytime)."""
        return await self._get("/stat/v1/data/bytime", params=params)

    async def get_stat_data_drilldown(self, params: dict) -> dict:
        """Получение данных — drill down (GET /stat/v1/data/drilldown)."""
        return await self._get("/stat/v1/data/drilldown", params=params)

    async def get_stat_data_comparison(self, params: dict) -> dict:
        """Сравнение сегментов (GET /stat/v1/data/comparison)."""
        return await self._get("/stat/v1/data/comparison", params=params)

    async def get_stat_data_comparison_drilldown(self, params: dict) -> dict:
        """Сравнение сегментов drill down (GET /stat/v1/data/comparison/drilldown)."""
        return await self._get("/stat/v1/data/comparison/drilldown", params=params)

    # ── Counters ──────────────────────────────────────────────────────

    async def list_counters(self, params: dict | None = None) -> dict:
        """Список счётчиков (GET /management/v1/counters)."""
        return await self._get("/management/v1/counters", params=params or {})

    async def get_counter(self, counter_id: int, field: str = "") -> dict:
        """Информация о счётчике (GET /management/v1/counter/{counterId})."""
        params = {}
        if field:
            params["field"] = field
        return await self._get(f"/management/v1/counter/{counter_id}", params=params)

    async def create_counter(self, payload: dict) -> dict:
        """Создание счётчика (POST /management/v1/counters)."""
        return await self._post("/management/v1/counters", payload)

    async def update_counter(self, counter_id: int, payload: dict) -> dict:
        """Изменение счётчика (PUT /management/v1/counter/{counterId})."""
        return await self._put(f"/management/v1/counter/{counter_id}", payload)

    async def delete_counter(self, counter_id: int) -> dict:
        """Удаление счётчика (DELETE /management/v1/counter/{counterId})."""
        return await self._delete(f"/management/v1/counter/{counter_id}")

    async def undelete_counter(self, counter_id: int) -> dict:
        """Восстановление счётчика (POST /management/v1/counter/{counterId}/undelete)."""
        return await self._post(f"/management/v1/counter/{counter_id}/undelete")

    # ── Goals ─────────────────────────────────────────────────────────

    async def list_goals(self, counter_id: int, use_deleted: bool = False) -> dict:
        """Список целей (GET /management/v1/counter/{counterId}/goals)."""
        params = {}
        if use_deleted:
            params["useDeleted"] = "true"
        return await self._get(f"/management/v1/counter/{counter_id}/goals", params=params)

    async def get_goal(self, counter_id: int, goal_id: int) -> dict:
        """Информация о цели (GET /management/v1/counter/{counterId}/goal/{goalId})."""
        return await self._get(f"/management/v1/counter/{counter_id}/goal/{goal_id}")

    async def create_goal(self, counter_id: int, payload: dict) -> dict:
        """Создание цели (POST /management/v1/counter/{counterId}/goals)."""
        return await self._post(f"/management/v1/counter/{counter_id}/goals", payload)

    async def update_goal(self, counter_id: int, goal_id: int, payload: dict) -> dict:
        """Изменение цели (PUT /management/v1/counter/{counterId}/goal/{goalId})."""
        return await self._put(f"/management/v1/counter/{counter_id}/goal/{goal_id}", payload)

    async def delete_goal(self, counter_id: int, goal_id: int) -> dict:
        """Удаление цели (DELETE /management/v1/counter/{counterId}/goal/{goalId})."""
        return await self._delete(f"/management/v1/counter/{counter_id}/goal/{goal_id}")

    # ── Filters ───────────────────────────────────────────────────────

    async def list_filters(self, counter_id: int) -> dict:
        """Список фильтров (GET /management/v1/counter/{counterId}/filters)."""
        return await self._get(f"/management/v1/counter/{counter_id}/filters")

    async def get_filter(self, counter_id: int, filter_id: int) -> dict:
        """Информация о фильтре (GET /management/v1/counter/{counterId}/filter/{filterId})."""
        return await self._get(f"/management/v1/counter/{counter_id}/filter/{filter_id}")

    async def create_filter(self, counter_id: int, payload: dict) -> dict:
        """Создание фильтра (POST /management/v1/counter/{counterId}/filters)."""
        return await self._post(f"/management/v1/counter/{counter_id}/filters", payload)

    async def update_filter(self, counter_id: int, filter_id: int, payload: dict) -> dict:
        """Изменение фильтра (PUT /management/v1/counter/{counterId}/filter/{filterId})."""
        return await self._put(f"/management/v1/counter/{counter_id}/filter/{filter_id}", payload)

    async def delete_filter(self, counter_id: int, filter_id: int) -> dict:
        """Удаление фильтра (DELETE /management/v1/counter/{counterId}/filter/{filterId})."""
        return await self._delete(f"/management/v1/counter/{counter_id}/filter/{filter_id}")

    # ── Grants ────────────────────────────────────────────────────────

    async def list_grants(self, counter_id: int) -> dict:
        """Список разрешений (GET /management/v1/counter/{counterId}/grants)."""
        return await self._get(f"/management/v1/counter/{counter_id}/grants")

    async def create_grant(self, counter_id: int, payload: dict) -> dict:
        """Выдача разрешения (POST /management/v1/counter/{counterId}/grants)."""
        return await self._post(f"/management/v1/counter/{counter_id}/grants", payload)

    async def update_grant(self, counter_id: int, payload: dict) -> dict:
        """Изменение разрешения (PUT /management/v1/counter/{counterId}/grant)."""
        return await self._put(f"/management/v1/counter/{counter_id}/grant", payload)

    async def delete_grant(self, counter_id: int, user_login: str = "", user_uid: int = 0) -> dict:
        """Удаление разрешения (DELETE /management/v1/counter/{counterId}/grant)."""
        params: dict = {}
        if user_login:
            params["user_login"] = user_login
        if user_uid:
            params["user_uid"] = user_uid
        return await self._delete(f"/management/v1/counter/{counter_id}/grant", params=params)

    # ── Operations ────────────────────────────────────────────────────

    async def list_operations(self, counter_id: int) -> dict:
        """Список операций (GET /management/v1/counter/{counterId}/operations)."""
        return await self._get(f"/management/v1/counter/{counter_id}/operations")

    async def get_operation(self, counter_id: int, operation_id: int) -> dict:
        """Информация об операции (GET /management/v1/counter/{counterId}/operation/{operationId})."""
        return await self._get(f"/management/v1/counter/{counter_id}/operation/{operation_id}")

    async def create_operation(self, counter_id: int, payload: dict) -> dict:
        """Создание операции (POST /management/v1/counter/{counterId}/operations)."""
        return await self._post(f"/management/v1/counter/{counter_id}/operations", payload)

    async def update_operation(self, counter_id: int, operation_id: int, payload: dict) -> dict:
        """Изменение операции (PUT /management/v1/counter/{counterId}/operation/{operationId})."""
        return await self._put(f"/management/v1/counter/{counter_id}/operation/{operation_id}", payload)

    async def delete_operation(self, counter_id: int, operation_id: int) -> dict:
        """Удаление операции (DELETE /management/v1/counter/{counterId}/operation/{operationId})."""
        return await self._delete(f"/management/v1/counter/{counter_id}/operation/{operation_id}")

    # ── Segments ──────────────────────────────────────────────────────

    async def list_segments(self, counter_id: int) -> dict:
        """Список сегментов (GET /management/v1/counter/{counterId}/apisegment/segments)."""
        return await self._get(f"/management/v1/counter/{counter_id}/apisegment/segments")

    async def get_segment(self, counter_id: int, segment_id: int) -> dict:
        """Информация о сегменте (GET /management/v1/counter/{counterId}/apisegment/segment/{segmentId})."""
        return await self._get(f"/management/v1/counter/{counter_id}/apisegment/segment/{segment_id}")

    async def create_segment(self, counter_id: int, payload: dict) -> dict:
        """Создание сегмента (POST /management/v1/counter/{counterId}/apisegment/segments)."""
        return await self._post(f"/management/v1/counter/{counter_id}/apisegment/segments", payload)

    async def update_segment(self, counter_id: int, segment_id: int, payload: dict) -> dict:
        """Изменение сегмента (PUT /management/v1/counter/{counterId}/apisegment/segment/{segmentId})."""
        return await self._put(f"/management/v1/counter/{counter_id}/apisegment/segment/{segment_id}", payload)

    async def delete_segment(self, counter_id: int, segment_id: int) -> dict:
        """Удаление сегмента (DELETE /management/v1/counter/{counterId}/apisegment/segment/{segmentId})."""
        return await self._delete(f"/management/v1/counter/{counter_id}/apisegment/segment/{segment_id}")

    # ── Labels ────────────────────────────────────────────────────────

    async def list_labels(self) -> dict:
        """Список меток (GET /management/v1/labels)."""
        return await self._get("/management/v1/labels")

    async def create_label(self, payload: dict) -> dict:
        """Создание метки (POST /management/v1/labels)."""
        return await self._post("/management/v1/labels", payload)

    async def update_label(self, label_id: int, payload: dict) -> dict:
        """Изменение метки (PUT /management/v1/label/{labelId})."""
        return await self._put(f"/management/v1/label/{label_id}", payload)

    async def delete_label(self, label_id: int) -> dict:
        """Удаление метки (DELETE /management/v1/label/{labelId})."""
        return await self._delete(f"/management/v1/label/{label_id}")

    async def set_counter_label(self, counter_id: int, label_id: int) -> dict:
        """Привязка метки к счётчику (POST /management/v1/counter/{counterId}/label/{labelId})."""
        return await self._post(f"/management/v1/counter/{counter_id}/label/{label_id}")

    async def unset_counter_label(self, counter_id: int, label_id: int) -> dict:
        """Отвязка метки от счётчика (DELETE /management/v1/counter/{counterId}/label/{labelId})."""
        return await self._delete(f"/management/v1/counter/{counter_id}/label/{label_id}")

    # ── Accounts ──────────────────────────────────────────────────────

    async def list_accounts(self) -> dict:
        """Список аккаунтов (GET /management/v1/accounts)."""
        return await self._get("/management/v1/accounts")

    async def delete_account(self, user_login: str) -> dict:
        """Удаление аккаунта (DELETE /management/v1/account)."""
        return await self._delete("/management/v1/account", params={"user_login": user_login})

    # ── Delegates ─────────────────────────────────────────────────────

    async def list_delegates(self) -> dict:
        """Список представителей (GET /management/v1/delegates)."""
        return await self._get("/management/v1/delegates")

    async def add_delegate(self, payload: dict) -> dict:
        """Добавление представителя (POST /management/v1/delegates)."""
        return await self._post("/management/v1/delegates", payload)

    async def delete_delegate(self, user_login: str) -> dict:
        """Удаление представителя (DELETE /management/v1/delegate)."""
        return await self._delete("/management/v1/delegate", params={"user_login": user_login})

    # ── Chart Annotations ─────────────────────────────────────────────

    async def list_chart_annotations(self, counter_id: int) -> dict:
        """Список примечаний (GET /management/v1/counter/{counterId}/chart_annotations)."""
        return await self._get(f"/management/v1/counter/{counter_id}/chart_annotations")

    async def create_chart_annotation(self, counter_id: int, payload: dict) -> dict:
        """Создание примечания (POST /management/v1/counter/{counterId}/chart_annotations)."""
        return await self._post(f"/management/v1/counter/{counter_id}/chart_annotations", payload)

    async def update_chart_annotation(self, counter_id: int, annotation_id: int, payload: dict) -> dict:
        """Изменение примечания (PUT /management/v1/counter/{counterId}/chart_annotation/{id})."""
        return await self._put(f"/management/v1/counter/{counter_id}/chart_annotation/{annotation_id}", payload)

    async def delete_chart_annotation(self, counter_id: int, annotation_id: int) -> dict:
        """Удаление примечания (DELETE /management/v1/counter/{counterId}/chart_annotation/{id})."""
        return await self._delete(f"/management/v1/counter/{counter_id}/chart_annotation/{annotation_id}")

    # ── Access Filters ────────────────────────────────────────────────

    async def list_access_filters(self, counter_id: int) -> dict:
        """Список фильтров доступа (GET /management/v1/counter/{counterId}/access_filters)."""
        return await self._get(f"/management/v1/counter/{counter_id}/access_filters")

    async def create_access_filter(self, counter_id: int, payload: dict) -> dict:
        """Создание фильтра доступа (POST /management/v1/counter/{counterId}/access_filters)."""
        return await self._post(f"/management/v1/counter/{counter_id}/access_filters", payload)

    async def update_access_filter(self, counter_id: int, access_filter_id: int, payload: dict) -> dict:
        """Изменение фильтра доступа (PUT /management/v1/counter/{counterId}/access_filter/{id})."""
        return await self._put(f"/management/v1/counter/{counter_id}/access_filter/{access_filter_id}", payload)

    async def delete_access_filter(self, counter_id: int, access_filter_id: int, delete_grants: bool = False) -> dict:
        """Удаление фильтра доступа (DELETE /management/v1/counter/{counterId}/access_filter/{id})."""
        params: dict = {}
        if delete_grants:
            params["delete_grants"] = "true"
        return await self._delete(
            f"/management/v1/counter/{counter_id}/access_filter/{access_filter_id}", params=params,
        )

    # ── Logs API ──────────────────────────────────────────────────────

    async def list_log_requests(self, counter_id: int) -> dict:
        """Список запросов логов (GET /management/v1/counter/{counterId}/logrequests)."""
        return await self._get(f"/management/v1/counter/{counter_id}/logrequests")

    async def get_log_request(self, counter_id: int, request_id: int) -> dict:
        """Информация о запросе логов (GET /management/v1/counter/{counterId}/logrequest/{requestId})."""
        return await self._get(f"/management/v1/counter/{counter_id}/logrequest/{request_id}")

    async def create_log_request(self, counter_id: int, params: dict) -> dict:
        """Создание запроса логов (POST /management/v1/counter/{counterId}/logrequests)."""
        return await self._post(f"/management/v1/counter/{counter_id}/logrequests", params=params)

    async def clean_log_request(self, counter_id: int, request_id: int) -> dict:
        """Очистка обработанных логов (POST /management/v1/counter/{counterId}/logrequest/{requestId}/clean)."""
        return await self._post(f"/management/v1/counter/{counter_id}/logrequest/{request_id}/clean")

    async def cancel_log_request(self, counter_id: int, request_id: int) -> dict:
        """Отмена запроса логов (POST /management/v1/counter/{counterId}/logrequest/{requestId}/cancel)."""
        return await self._post(f"/management/v1/counter/{counter_id}/logrequest/{request_id}/cancel")

    async def evaluate_log_request(self, counter_id: int, params: dict) -> dict:
        """Оценка возможности запроса (GET /management/v1/counter/{counterId}/logrequests/evaluate)."""
        return await self._get(f"/management/v1/counter/{counter_id}/logrequests/evaluate", params=params)

    async def download_log_part(self, counter_id: int, request_id: int, part_number: int) -> bytes:
        """Скачивание части лога (GET .../logrequest/{requestId}/part/{partNumber}/download)."""
        return await self._get_raw(
            f"/management/v1/counter/{counter_id}/logrequest/{request_id}/part/{part_number}/download",
        )

    # ── Offline Conversions ───────────────────────────────────────────

    async def upload_offline_conversions(self, counter_id: int, file_data: bytes) -> dict:
        """Загрузка оффлайн-конверсий (POST /management/v1/counter/{counterId}/offline_conversions/upload)."""
        return await self._post_file(
            f"/management/v1/counter/{counter_id}/offline_conversions/upload", file_data,
        )

    async def get_offline_conversion_upload(self, counter_id: int, upload_id: int) -> dict:
        """Информация о загрузке конверсий (GET .../offline_conversions/uploading/{id})."""
        return await self._get(
            f"/management/v1/counter/{counter_id}/offline_conversions/uploading/{upload_id}",
        )

    async def list_offline_conversion_uploads(self, counter_id: int) -> dict:
        """Список загрузок конверсий (GET .../offline_conversions/findAll_1)."""
        return await self._get(f"/management/v1/counter/{counter_id}/offline_conversions/findAll_1")

    # ── Calls ─────────────────────────────────────────────────────────

    async def upload_calls(self, counter_id: int, file_data: bytes) -> dict:
        """Загрузка звонков (POST /management/v1/counter/{counterId}/offline_conversions/upload_calls)."""
        return await self._post_file(
            f"/management/v1/counter/{counter_id}/offline_conversions/upload_calls", file_data,
        )

    async def get_calls_upload(self, counter_id: int, upload_id: int) -> dict:
        """Информация о загрузке звонков (GET .../offline_conversions/calls_uploading/{id})."""
        return await self._get(
            f"/management/v1/counter/{counter_id}/offline_conversions/calls_uploading/{upload_id}",
        )

    async def list_calls_uploads(self, counter_id: int) -> dict:
        """Список загрузок звонков (GET .../offline_conversions/findAllCallUploadings)."""
        return await self._get(
            f"/management/v1/counter/{counter_id}/offline_conversions/findAllCallUploadings",
        )

    # ── Expenses ──────────────────────────────────────────────────────

    async def upload_expenses(
        self, counter_id: int, file_data: bytes, comment: str = "", provider: str = "",
    ) -> dict:
        """Загрузка расходов (POST /management/v1/counter/{counterId}/expense/upload)."""
        params: dict = {}
        if comment:
            params["comment"] = comment
        if provider:
            params["provider"] = provider
        return await self._post_file(
            f"/management/v1/counter/{counter_id}/expense/upload", file_data, **{"params": params},
        )

    # ── User Parameters ───────────────────────────────────────────────

    async def upload_user_params(self, counter_id: int, file_data: bytes, action: str = "update") -> dict:
        """Загрузка параметров пользователей (POST .../user_params/uploadings/upload)."""
        return await self._post_file(
            f"/management/v1/counter/{counter_id}/user_params/uploadings/upload",
            file_data,
            **{"params": {"action": action}},
        )
