"""MCP server for Yandex Metrika API."""

import json
import logging
import os
import sys

from mcp.server.fastmcp import FastMCP

from .metrika_api import MetrikaAPI

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", stream=sys.stderr)
log = logging.getLogger(__name__)

mcp = FastMCP("yandex-metrika")


def _get_api() -> MetrikaAPI:
    token = os.getenv("YANDEX_METRIKA_TOKEN")
    if not token:
        raise RuntimeError("YANDEX_METRIKA_TOKEN environment variable is required")
    return MetrikaAPI(token)


def _j(data) -> str:
    return json.dumps(data, ensure_ascii=False)


# ── Reporting API ─────────────────────────────────────────────────


@mcp.tool()
def ym_stat_data(
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
    accuracy: str = "",
    timezone: str = "",
    lang: str = "",
    include_undefined: bool = False,
) -> str:
    """Получение данных — табличный отчёт (GET /stat/v1/data).

    Возвращает статистические данные в табличном виде. Поддерживает фильтрацию,
    сортировку и пагинацию.

    Args:
        ids: Counter IDs, comma-separated (e.g. "12345,67890")
        metrics: Metrics, comma-separated (e.g. "ym:s:visits,ym:s:users")
        dimensions: Dimensions, comma-separated (e.g. "ym:s:browser")
        date1: Start date (YYYY-MM-DD or "6daysAgo", default "6daysAgo")
        date2: End date (YYYY-MM-DD or "today", default "today")
        filters: Filter expression (e.g. "ym:s:browser=='Chrome'")
        limit: Max rows to return (1-100000, default 100)
        offset: Offset for pagination (default 1)
        sort: Sort field with optional - prefix (e.g. "-ym:s:visits")
        preset: Report preset name
        accuracy: Accuracy level (low/medium/high/full or 0.0-1.0)
        timezone: Timezone offset (e.g. "+03:00")
        lang: Language (ru/en/tr)
        include_undefined: Include undefined values
    """
    api = _get_api()
    params: dict = {"ids": ids, "metrics": metrics, "limit": limit, "offset": offset}
    if dimensions:
        params["dimensions"] = dimensions
    if date1:
        params["date1"] = date1
    if date2:
        params["date2"] = date2
    if filters:
        params["filters"] = filters
    if sort:
        params["sort"] = sort
    if preset:
        params["preset"] = preset
    if accuracy:
        params["accuracy"] = accuracy
    if timezone:
        params["timezone"] = timezone
    if lang:
        params["lang"] = lang
    if include_undefined:
        params["include_undefined"] = "true"
    return _j(api.get_stat_data(params))


@mcp.tool()
def ym_stat_data_bytime(
    ids: str,
    metrics: str,
    dimensions: str = "",
    date1: str = "",
    date2: str = "",
    group: str = "day",
    filters: str = "",
    limit: int = 100,
    offset: int = 1,
    sort: str = "",
    lang: str = "",
    top_keys: int = 7,
) -> str:
    """Получение данных — отчёт по времени (GET /stat/v1/data/bytime).

    Возвращает данные с разбивкой по временным интервалам.

    Args:
        ids: Counter IDs, comma-separated
        metrics: Metrics, comma-separated
        dimensions: Dimensions, comma-separated
        date1: Start date (YYYY-MM-DD, default "6daysAgo")
        date2: End date (YYYY-MM-DD, default "today")
        group: Time grouping — all/auto/minutes/hour/day/week/month/quarter/year
        filters: Filter expression
        limit: Max rows (default 100)
        offset: Pagination offset (default 1)
        sort: Sort field
        lang: Language (ru/en/tr)
        top_keys: Number of top keys (max 30, default 7)
    """
    api = _get_api()
    params: dict = {"ids": ids, "metrics": metrics, "group": group, "limit": limit, "offset": offset}
    if dimensions:
        params["dimensions"] = dimensions
    if date1:
        params["date1"] = date1
    if date2:
        params["date2"] = date2
    if filters:
        params["filters"] = filters
    if sort:
        params["sort"] = sort
    if lang:
        params["lang"] = lang
    if top_keys != 7:
        params["top_keys"] = top_keys
    return _j(api.get_stat_data_bytime(params))


@mcp.tool()
def ym_stat_data_drilldown(
    ids: str,
    metrics: str,
    dimensions: str = "",
    date1: str = "",
    date2: str = "",
    filters: str = "",
    limit: int = 100,
    offset: int = 1,
    sort: str = "",
    parent_id: str = "",
    lang: str = "",
) -> str:
    """Получение данных — drill down отчёт (GET /stat/v1/data/drilldown).

    Возвращает данные с раскрытием вложенных уровней.

    Args:
        ids: Counter IDs, comma-separated
        metrics: Metrics, comma-separated
        dimensions: Dimensions, comma-separated
        date1: Start date
        date2: End date
        filters: Filter expression
        limit: Max rows (default 100)
        offset: Pagination offset (default 1)
        sort: Sort field
        parent_id: Parent ID for drill down (JSON array of keys)
        lang: Language
    """
    api = _get_api()
    params: dict = {"ids": ids, "metrics": metrics, "limit": limit, "offset": offset}
    if dimensions:
        params["dimensions"] = dimensions
    if date1:
        params["date1"] = date1
    if date2:
        params["date2"] = date2
    if filters:
        params["filters"] = filters
    if sort:
        params["sort"] = sort
    if parent_id:
        params["parent_id"] = parent_id
    if lang:
        params["lang"] = lang
    return _j(api.get_stat_data_drilldown(params))


@mcp.tool()
def ym_stat_data_comparison(
    ids: str,
    metrics: str,
    dimensions: str = "",
    date1_a: str = "",
    date2_a: str = "",
    date1_b: str = "",
    date2_b: str = "",
    filters_a: str = "",
    filters_b: str = "",
    limit: int = 100,
    offset: int = 1,
    sort: str = "",
    lang: str = "",
) -> str:
    """Сравнение сегментов (GET /stat/v1/data/comparison).

    Сравнение данных между двумя сегментами или периодами.

    Args:
        ids: Counter IDs, comma-separated
        metrics: Metrics, comma-separated
        dimensions: Dimensions, comma-separated
        date1_a: Start date for segment A
        date2_a: End date for segment A
        date1_b: Start date for segment B
        date2_b: End date for segment B
        filters_a: Filter for segment A
        filters_b: Filter for segment B
        limit: Max rows (default 100)
        offset: Pagination offset (default 1)
        sort: Sort field
        lang: Language
    """
    api = _get_api()
    params: dict = {"ids": ids, "metrics": metrics, "limit": limit, "offset": offset}
    if dimensions:
        params["dimensions"] = dimensions
    if date1_a:
        params["date1_a"] = date1_a
    if date2_a:
        params["date2_a"] = date2_a
    if date1_b:
        params["date1_b"] = date1_b
    if date2_b:
        params["date2_b"] = date2_b
    if filters_a:
        params["filters_a"] = filters_a
    if filters_b:
        params["filters_b"] = filters_b
    if sort:
        params["sort"] = sort
    if lang:
        params["lang"] = lang
    return _j(api.get_stat_data_comparison(params))


@mcp.tool()
def ym_stat_data_comparison_drilldown(
    ids: str,
    metrics: str,
    dimensions: str = "",
    date1_a: str = "",
    date2_a: str = "",
    date1_b: str = "",
    date2_b: str = "",
    filters_a: str = "",
    filters_b: str = "",
    limit: int = 100,
    offset: int = 1,
    sort: str = "",
    parent_id: str = "",
    lang: str = "",
) -> str:
    """Сравнение сегментов drill down (GET /stat/v1/data/comparison/drilldown).

    Args:
        ids: Counter IDs, comma-separated
        metrics: Metrics, comma-separated
        dimensions: Dimensions, comma-separated
        date1_a: Start date for segment A
        date2_a: End date for segment A
        date1_b: Start date for segment B
        date2_b: End date for segment B
        filters_a: Filter for segment A
        filters_b: Filter for segment B
        limit: Max rows (default 100)
        offset: Pagination offset (default 1)
        sort: Sort field
        parent_id: Parent ID for drill down
        lang: Language
    """
    api = _get_api()
    params: dict = {"ids": ids, "metrics": metrics, "limit": limit, "offset": offset}
    if dimensions:
        params["dimensions"] = dimensions
    if date1_a:
        params["date1_a"] = date1_a
    if date2_a:
        params["date2_a"] = date2_a
    if date1_b:
        params["date1_b"] = date1_b
    if date2_b:
        params["date2_b"] = date2_b
    if filters_a:
        params["filters_a"] = filters_a
    if filters_b:
        params["filters_b"] = filters_b
    if sort:
        params["sort"] = sort
    if parent_id:
        params["parent_id"] = parent_id
    if lang:
        params["lang"] = lang
    return _j(api.get_stat_data_comparison_drilldown(params))


# ── Counters ──────────────────────────────────────────────────────


@mcp.tool()
def ym_counters(
    search_string: str = "",
    permission: str = "",
    status: str = "",
    counter_type: str = "",
    favorite: bool = False,
    per_page: int = 100,
    offset: int = 1,
    sort: str = "",
) -> str:
    """Список счётчиков (GET /management/v1/counters).

    Args:
        search_string: Search by counter name or site
        permission: Filter — own/view/edit
        status: Filter — Active/Deleted
        counter_type: Filter — simple/partner
        favorite: Only favorites
        per_page: Results per page (default 100, max 1000)
        offset: Pagination offset (default 1)
        sort: Sort — None/Default/Visits/Hits/Uniques/Name
    """
    api = _get_api()
    params: dict = {"per_page": per_page, "offset": offset}
    if search_string:
        params["search_string"] = search_string
    if permission:
        params["permission"] = permission
    if status:
        params["status"] = status
    if counter_type:
        params["type"] = counter_type
    if favorite:
        params["favorite"] = "true"
    if sort:
        params["sort"] = sort
    return _j(api.list_counters(params))


@mcp.tool()
def ym_counter(counter_id: int, field: str = "") -> str:
    """Информация о счётчике (GET /management/v1/counter/{counterId}).

    Args:
        counter_id: Counter ID
        field: Extra fields — goals,mirrors,grants,filters,operation
    """
    api = _get_api()
    return _j(api.get_counter(counter_id, field))


@mcp.tool()
def ym_counter_create(name: str, site: str, time_zone_name: str = "Europe/Moscow") -> str:
    """Создание счётчика (POST /management/v1/counters).

    Args:
        name: Counter name
        site: Website domain (e.g. "example.com")
        time_zone_name: Timezone (default "Europe/Moscow")
    """
    api = _get_api()
    payload = {
        "counter": {
            "name": name,
            "site2": {"site": site},
            "time_zone_name": time_zone_name,
        }
    }
    return _j(api.create_counter(payload))


@mcp.tool()
def ym_counter_update(counter_id: int, name: str = "", site: str = "", time_zone_name: str = "") -> str:
    """Изменение счётчика (PUT /management/v1/counter/{counterId}).

    Args:
        counter_id: Counter ID
        name: New counter name
        site: New website domain
        time_zone_name: New timezone
    """
    api = _get_api()
    counter: dict = {}
    if name:
        counter["name"] = name
    if site:
        counter["site2"] = {"site": site}
    if time_zone_name:
        counter["time_zone_name"] = time_zone_name
    return _j(api.update_counter(counter_id, {"counter": counter}))


@mcp.tool()
def ym_counter_delete(counter_id: int) -> str:
    """Удаление счётчика (DELETE /management/v1/counter/{counterId}).

    Args:
        counter_id: Counter ID
    """
    api = _get_api()
    return _j(api.delete_counter(counter_id))


@mcp.tool()
def ym_counter_undelete(counter_id: int) -> str:
    """Восстановление удалённого счётчика (POST /management/v1/counter/{counterId}/undelete).

    Args:
        counter_id: Counter ID
    """
    api = _get_api()
    return _j(api.undelete_counter(counter_id))


# ── Goals ─────────────────────────────────────────────────────────


@mcp.tool()
def ym_goals(counter_id: int, use_deleted: bool = False) -> str:
    """Список целей счётчика (GET /management/v1/counter/{counterId}/goals).

    13 типов целей: action, chat, email, file, messenger, number, payment_system,
    phone, search, social, step, url, visit_duration.

    Args:
        counter_id: Counter ID
        use_deleted: Include deleted goals
    """
    api = _get_api()
    return _j(api.list_goals(counter_id, use_deleted))


@mcp.tool()
def ym_goal(counter_id: int, goal_id: int) -> str:
    """Информация о цели (GET /management/v1/counter/{counterId}/goal/{goalId}).

    Args:
        counter_id: Counter ID
        goal_id: Goal ID
    """
    api = _get_api()
    return _j(api.get_goal(counter_id, goal_id))


@mcp.tool()
def ym_goal_create(
    counter_id: int,
    name: str,
    goal_type: str,
    conditions_json: str = "",
    depth: int = 0,
    duration: int = 0,
    default_price: float = 0,
    is_favorite: bool = False,
) -> str:
    """Создание цели (POST /management/v1/counter/{counterId}/goals).

    Args:
        counter_id: Counter ID
        name: Goal name
        goal_type: Type — url/number/step/action/visit_duration/phone/email/search/messenger/file/social/chat/payment_system
        conditions_json: Conditions as JSON array (e.g. '[{"type":"contain","url":"/thank"}]')
        depth: Page depth (for "number" type)
        duration: Visit duration in seconds (for "visit_duration" type)
        default_price: Default goal value
        is_favorite: Mark as favorite
    """
    api = _get_api()
    goal: dict = {"name": name, "type": goal_type}
    if conditions_json:
        goal["conditions"] = json.loads(conditions_json)
    if depth:
        goal["depth"] = depth
    if duration:
        goal["duration"] = duration
    if default_price:
        goal["default_price"] = default_price
    if is_favorite:
        goal["is_favorite"] = True
    return _j(api.create_goal(counter_id, {"goal": goal}))


@mcp.tool()
def ym_goal_update(counter_id: int, goal_id: int, name: str = "", goal_type: str = "", conditions_json: str = "") -> str:
    """Изменение цели (PUT /management/v1/counter/{counterId}/goal/{goalId}).

    Args:
        counter_id: Counter ID
        goal_id: Goal ID
        name: New goal name
        goal_type: New goal type
        conditions_json: New conditions as JSON array
    """
    api = _get_api()
    goal: dict = {}
    if name:
        goal["name"] = name
    if goal_type:
        goal["type"] = goal_type
    if conditions_json:
        goal["conditions"] = json.loads(conditions_json)
    return _j(api.update_goal(counter_id, goal_id, {"goal": goal}))


@mcp.tool()
def ym_goal_delete(counter_id: int, goal_id: int) -> str:
    """Удаление цели (DELETE /management/v1/counter/{counterId}/goal/{goalId}).

    Args:
        counter_id: Counter ID
        goal_id: Goal ID
    """
    api = _get_api()
    return _j(api.delete_goal(counter_id, goal_id))


# ── Filters ───────────────────────────────────────────────────────


@mcp.tool()
def ym_filters(counter_id: int) -> str:
    """Список фильтров счётчика (GET /management/v1/counter/{counterId}/filters).

    Args:
        counter_id: Counter ID
    """
    api = _get_api()
    return _j(api.list_filters(counter_id))


@mcp.tool()
def ym_filter(counter_id: int, filter_id: int) -> str:
    """Информация о фильтре (GET /management/v1/counter/{counterId}/filter/{filterId}).

    Args:
        counter_id: Counter ID
        filter_id: Filter ID
    """
    api = _get_api()
    return _j(api.get_filter(counter_id, filter_id))


@mcp.tool()
def ym_filter_create(
    counter_id: int,
    attr: str,
    filter_type: str,
    value: str = "",
    action: str = "exclude",
    status: str = "active",
    start_ip: str = "",
    end_ip: str = "",
) -> str:
    """Создание фильтра (POST /management/v1/counter/{counterId}/filters).

    Args:
        counter_id: Counter ID
        attr: Attribute — title/client_ip/url/referer/uniq_id
        filter_type: Type — equal/start/contain/interval/me/only_mirrors/regexp
        value: Filter value
        action: Action — exclude/include
        status: Status — active/disabled
        start_ip: Start IP (for interval type)
        end_ip: End IP (for interval type)
    """
    api = _get_api()
    f: dict = {"attr": attr, "type": filter_type, "action": action, "status": status}
    if value:
        f["value"] = value
    if start_ip:
        f["start_ip"] = start_ip
    if end_ip:
        f["end_ip"] = end_ip
    return _j(api.create_filter(counter_id, {"filter": f}))


@mcp.tool()
def ym_filter_update(counter_id: int, filter_id: int, attr: str = "", filter_type: str = "", value: str = "", action: str = "", status: str = "") -> str:
    """Изменение фильтра (PUT /management/v1/counter/{counterId}/filter/{filterId}).

    Args:
        counter_id: Counter ID
        filter_id: Filter ID
        attr: Attribute — title/client_ip/url/referer/uniq_id
        filter_type: Type — equal/start/contain/interval/me/only_mirrors/regexp
        value: Filter value
        action: Action — exclude/include
        status: Status — active/disabled
    """
    api = _get_api()
    f: dict = {}
    if attr:
        f["attr"] = attr
    if filter_type:
        f["type"] = filter_type
    if value:
        f["value"] = value
    if action:
        f["action"] = action
    if status:
        f["status"] = status
    return _j(api.update_filter(counter_id, filter_id, {"filter": f}))


@mcp.tool()
def ym_filter_delete(counter_id: int, filter_id: int) -> str:
    """Удаление фильтра (DELETE /management/v1/counter/{counterId}/filter/{filterId}).

    Args:
        counter_id: Counter ID
        filter_id: Filter ID
    """
    api = _get_api()
    return _j(api.delete_filter(counter_id, filter_id))


# ── Grants ────────────────────────────────────────────────────────


@mcp.tool()
def ym_grants(counter_id: int) -> str:
    """Список разрешений на доступ (GET /management/v1/counter/{counterId}/grants).

    Args:
        counter_id: Counter ID
    """
    api = _get_api()
    return _j(api.list_grants(counter_id))


@mcp.tool()
def ym_grant_create(counter_id: int, user_login: str, perm: str, comment: str = "") -> str:
    """Выдача разрешения (POST /management/v1/counter/{counterId}/grants).

    Args:
        counter_id: Counter ID
        user_login: Yandex login to grant access
        perm: Permission — public_stat/view/edit
        comment: Comment
    """
    api = _get_api()
    grant: dict = {"user_login": user_login, "perm": perm}
    if comment:
        grant["comment"] = comment
    return _j(api.create_grant(counter_id, {"grant": grant}))


@mcp.tool()
def ym_grant_update(counter_id: int, user_login: str, perm: str, comment: str = "") -> str:
    """Изменение разрешения (PUT /management/v1/counter/{counterId}/grant).

    Args:
        counter_id: Counter ID
        user_login: Yandex login
        perm: New permission — public_stat/view/edit
        comment: New comment
    """
    api = _get_api()
    grant: dict = {"user_login": user_login, "perm": perm}
    if comment:
        grant["comment"] = comment
    return _j(api.update_grant(counter_id, {"grant": grant}))


@mcp.tool()
def ym_grant_delete(counter_id: int, user_login: str) -> str:
    """Удаление разрешения (DELETE /management/v1/counter/{counterId}/grant).

    Args:
        counter_id: Counter ID
        user_login: Yandex login to revoke access
    """
    api = _get_api()
    return _j(api.delete_grant(counter_id, user_login=user_login))


# ── Operations ────────────────────────────────────────────────────


@mcp.tool()
def ym_operations(counter_id: int) -> str:
    """Список операций (GET /management/v1/counter/{counterId}/operations).

    Args:
        counter_id: Counter ID
    """
    api = _get_api()
    return _j(api.list_operations(counter_id))


@mcp.tool()
def ym_operation(counter_id: int, operation_id: int) -> str:
    """Информация об операции (GET /management/v1/counter/{counterId}/operation/{operationId}).

    Args:
        counter_id: Counter ID
        operation_id: Operation ID
    """
    api = _get_api()
    return _j(api.get_operation(counter_id, operation_id))


@mcp.tool()
def ym_operation_create(counter_id: int, action: str, attr: str, value: str) -> str:
    """Создание операции (POST /management/v1/counter/{counterId}/operations).

    Args:
        counter_id: Counter ID
        action: Action — cut_fragment/cut_parameter/cut_all_parameters/merge_https_and_http/to_lower/replace_domain
        attr: Attribute — referer/url
        value: Value for the operation
    """
    api = _get_api()
    return _j(api.create_operation(counter_id, {"operation": {"action": action, "attr": attr, "value": value}}))


@mcp.tool()
def ym_operation_update(counter_id: int, operation_id: int, action: str = "", attr: str = "", value: str = "", status: str = "") -> str:
    """Изменение операции (PUT /management/v1/counter/{counterId}/operation/{operationId}).

    Args:
        counter_id: Counter ID
        operation_id: Operation ID
        action: Action
        attr: Attribute
        value: Value
        status: Status — active/disabled
    """
    api = _get_api()
    op: dict = {}
    if action:
        op["action"] = action
    if attr:
        op["attr"] = attr
    if value:
        op["value"] = value
    if status:
        op["status"] = status
    return _j(api.update_operation(counter_id, operation_id, {"operation": op}))


@mcp.tool()
def ym_operation_delete(counter_id: int, operation_id: int) -> str:
    """Удаление операции (DELETE /management/v1/counter/{counterId}/operation/{operationId}).

    Args:
        counter_id: Counter ID
        operation_id: Operation ID
    """
    api = _get_api()
    return _j(api.delete_operation(counter_id, operation_id))


# ── Segments ──────────────────────────────────────────────────────


@mcp.tool()
def ym_segments(counter_id: int) -> str:
    """Список сегментов (GET /management/v1/counter/{counterId}/apisegment/segments).

    Args:
        counter_id: Counter ID
    """
    api = _get_api()
    return _j(api.list_segments(counter_id))


@mcp.tool()
def ym_segment(counter_id: int, segment_id: int) -> str:
    """Информация о сегменте (GET .../apisegment/segment/{segmentId}).

    Args:
        counter_id: Counter ID
        segment_id: Segment ID
    """
    api = _get_api()
    return _j(api.get_segment(counter_id, segment_id))


@mcp.tool()
def ym_segment_create(counter_id: int, name: str, expression: str) -> str:
    """Создание сегмента (POST /management/v1/counter/{counterId}/apisegment/segments).

    Args:
        counter_id: Counter ID
        name: Segment name (1-255 chars)
        expression: Segment expression (1-65535 chars, e.g. "ym:s:browser=='Chrome'")
    """
    api = _get_api()
    return _j(api.create_segment(counter_id, {"segment": {"name": name, "expression": expression}}))


@mcp.tool()
def ym_segment_update(counter_id: int, segment_id: int, name: str = "", expression: str = "") -> str:
    """Изменение сегмента (PUT .../apisegment/segment/{segmentId}).

    Args:
        counter_id: Counter ID
        segment_id: Segment ID
        name: New segment name
        expression: New segment expression
    """
    api = _get_api()
    seg: dict = {}
    if name:
        seg["name"] = name
    if expression:
        seg["expression"] = expression
    return _j(api.update_segment(counter_id, segment_id, {"segment": seg}))


@mcp.tool()
def ym_segment_delete(counter_id: int, segment_id: int) -> str:
    """Удаление сегмента (DELETE .../apisegment/segment/{segmentId}).

    Args:
        counter_id: Counter ID
        segment_id: Segment ID
    """
    api = _get_api()
    return _j(api.delete_segment(counter_id, segment_id))


# ── Labels ────────────────────────────────────────────────────────


@mcp.tool()
def ym_labels() -> str:
    """Список меток (GET /management/v1/labels)."""
    api = _get_api()
    return _j(api.list_labels())


@mcp.tool()
def ym_label_create(name: str) -> str:
    """Создание метки (POST /management/v1/labels).

    Args:
        name: Label name (0-255 chars)
    """
    api = _get_api()
    return _j(api.create_label({"label": {"name": name}}))


@mcp.tool()
def ym_label_update(label_id: int, name: str) -> str:
    """Изменение метки (PUT /management/v1/label/{labelId}).

    Args:
        label_id: Label ID
        name: New label name
    """
    api = _get_api()
    return _j(api.update_label(label_id, {"label": {"name": name}}))


@mcp.tool()
def ym_label_delete(label_id: int) -> str:
    """Удаление метки (DELETE /management/v1/label/{labelId}).

    Args:
        label_id: Label ID
    """
    api = _get_api()
    return _j(api.delete_label(label_id))


@mcp.tool()
def ym_counter_label_set(counter_id: int, label_id: int) -> str:
    """Привязка метки к счётчику (POST /management/v1/counter/{counterId}/label/{labelId}).

    Args:
        counter_id: Counter ID
        label_id: Label ID
    """
    api = _get_api()
    return _j(api.set_counter_label(counter_id, label_id))


@mcp.tool()
def ym_counter_label_unset(counter_id: int, label_id: int) -> str:
    """Отвязка метки от счётчика (DELETE /management/v1/counter/{counterId}/label/{labelId}).

    Args:
        counter_id: Counter ID
        label_id: Label ID
    """
    api = _get_api()
    return _j(api.unset_counter_label(counter_id, label_id))


# ── Accounts ──────────────────────────────────────────────────────


@mcp.tool()
def ym_accounts() -> str:
    """Список аккаунтов (GET /management/v1/accounts)."""
    api = _get_api()
    return _j(api.list_accounts())


@mcp.tool()
def ym_account_delete(user_login: str) -> str:
    """Удаление аккаунта (DELETE /management/v1/account).

    Args:
        user_login: Yandex login to delete
    """
    api = _get_api()
    return _j(api.delete_account(user_login))


# ── Delegates ─────────────────────────────────────────────────────


@mcp.tool()
def ym_delegates() -> str:
    """Список представителей (GET /management/v1/delegates)."""
    api = _get_api()
    return _j(api.list_delegates())


@mcp.tool()
def ym_delegate_add(user_login: str, comment: str = "") -> str:
    """Добавление представителя (POST /management/v1/delegates).

    Args:
        user_login: Yandex login to add as delegate
        comment: Comment
    """
    api = _get_api()
    delegate: dict = {"user_login": user_login}
    if comment:
        delegate["comment"] = comment
    return _j(api.add_delegate({"delegate": delegate}))


@mcp.tool()
def ym_delegate_delete(user_login: str) -> str:
    """Удаление представителя (DELETE /management/v1/delegate).

    Args:
        user_login: Yandex login to remove
    """
    api = _get_api()
    return _j(api.delete_delegate(user_login))


# ── Chart Annotations ─────────────────────────────────────────────


@mcp.tool()
def ym_chart_annotations(counter_id: int) -> str:
    """Список примечаний на графике (GET /management/v1/counter/{counterId}/chart_annotations).

    Args:
        counter_id: Counter ID
    """
    api = _get_api()
    return _j(api.list_chart_annotations(counter_id))


@mcp.tool()
def ym_chart_annotation_create(counter_id: int, date: str, title: str, message: str = "", group: str = "A") -> str:
    """Создание примечания (POST /management/v1/counter/{counterId}/chart_annotations).

    Args:
        counter_id: Counter ID
        date: Date (YYYY-MM-DD)
        title: Annotation title
        message: Annotation message
        group: Group — A/B/C/D/E/HOLIDAY
    """
    api = _get_api()
    ann: dict = {"date": date, "title": title, "group": group}
    if message:
        ann["message"] = message
    return _j(api.create_chart_annotation(counter_id, {"chart_annotation": ann}))


@mcp.tool()
def ym_chart_annotation_update(counter_id: int, annotation_id: int, date: str = "", title: str = "", message: str = "", group: str = "") -> str:
    """Изменение примечания (PUT .../chart_annotation/{annotationId}).

    Args:
        counter_id: Counter ID
        annotation_id: Annotation ID
        date: New date
        title: New title
        message: New message
        group: New group
    """
    api = _get_api()
    ann: dict = {}
    if date:
        ann["date"] = date
    if title:
        ann["title"] = title
    if message:
        ann["message"] = message
    if group:
        ann["group"] = group
    return _j(api.update_chart_annotation(counter_id, annotation_id, {"chart_annotation": ann}))


@mcp.tool()
def ym_chart_annotation_delete(counter_id: int, annotation_id: int) -> str:
    """Удаление примечания (DELETE .../chart_annotation/{annotationId}).

    Args:
        counter_id: Counter ID
        annotation_id: Annotation ID
    """
    api = _get_api()
    return _j(api.delete_chart_annotation(counter_id, annotation_id))


# ── Access Filters ────────────────────────────────────────────────


@mcp.tool()
def ym_access_filters(counter_id: int) -> str:
    """Список фильтров доступа (GET /management/v1/counter/{counterId}/access_filters).

    Args:
        counter_id: Counter ID
    """
    api = _get_api()
    return _j(api.list_access_filters(counter_id))


@mcp.tool()
def ym_access_filter_create(counter_id: int, name: str, expression: str, interface_value: str = "") -> str:
    """Создание фильтра доступа (POST /management/v1/counter/{counterId}/access_filters).

    Args:
        counter_id: Counter ID
        name: Filter name (1-255 chars)
        expression: Filter expression (1-65535 chars)
        interface_value: Interface value (1-65535 chars)
    """
    api = _get_api()
    af: dict = {"name": name, "expression": expression}
    if interface_value:
        af["interface_value"] = interface_value
    return _j(api.create_access_filter(counter_id, {"access_filter": af}))


@mcp.tool()
def ym_access_filter_update(counter_id: int, access_filter_id: int, name: str = "", expression: str = "", interface_value: str = "") -> str:
    """Изменение фильтра доступа (PUT .../access_filter/{accessFilterId}).

    Args:
        counter_id: Counter ID
        access_filter_id: Access filter ID
        name: New name
        expression: New expression
        interface_value: New interface value
    """
    api = _get_api()
    af: dict = {}
    if name:
        af["name"] = name
    if expression:
        af["expression"] = expression
    if interface_value:
        af["interface_value"] = interface_value
    return _j(api.update_access_filter(counter_id, access_filter_id, {"access_filter": af}))


@mcp.tool()
def ym_access_filter_delete(counter_id: int, access_filter_id: int, delete_grants: bool = False) -> str:
    """Удаление фильтра доступа (DELETE .../access_filter/{accessFilterId}).

    Args:
        counter_id: Counter ID
        access_filter_id: Access filter ID
        delete_grants: Also delete associated grants
    """
    api = _get_api()
    return _j(api.delete_access_filter(counter_id, access_filter_id, delete_grants))


# ── Logs API ──────────────────────────────────────────────────────


@mcp.tool()
def ym_log_requests(counter_id: int) -> str:
    """Список запросов логов (GET /management/v1/counter/{counterId}/logrequests).

    Args:
        counter_id: Counter ID
    """
    api = _get_api()
    return _j(api.list_log_requests(counter_id))


@mcp.tool()
def ym_log_request(counter_id: int, request_id: int) -> str:
    """Информация о запросе логов (GET .../logrequest/{requestId}).

    Args:
        counter_id: Counter ID
        request_id: Log request ID
    """
    api = _get_api()
    return _j(api.get_log_request(counter_id, request_id))


@mcp.tool()
def ym_log_request_create(
    counter_id: int,
    date1: str,
    date2: str,
    fields: str,
    source: str,
    attribution: str = "LASTSIGN",
) -> str:
    """Создание запроса логов (POST /management/v1/counter/{counterId}/logrequests).

    Args:
        counter_id: Counter ID
        date1: Start date (YYYY-MM-DD)
        date2: End date (YYYY-MM-DD)
        fields: Fields, comma-separated (e.g. "ym:s:date,ym:s:visitID,ym:s:watchIDs")
        source: Data source — "hits" or "visits"
        attribution: Attribution model — FIRST/LAST/LASTSIGN/LAST_YANDEX_DIRECT_CLICK/CROSS_DEVICE_LAST_SIGNIFICANT/AUTOMATIC
    """
    api = _get_api()
    params = {
        "date1": date1,
        "date2": date2,
        "fields": fields,
        "source": source,
        "attribution": attribution,
    }
    return _j(api.create_log_request(counter_id, params))


@mcp.tool()
def ym_log_request_clean(counter_id: int, request_id: int) -> str:
    """Очистка обработанных логов (POST .../logrequest/{requestId}/clean).

    Args:
        counter_id: Counter ID
        request_id: Log request ID
    """
    api = _get_api()
    return _j(api.clean_log_request(counter_id, request_id))


@mcp.tool()
def ym_log_request_cancel(counter_id: int, request_id: int) -> str:
    """Отмена запроса логов (POST .../logrequest/{requestId}/cancel).

    Args:
        counter_id: Counter ID
        request_id: Log request ID
    """
    api = _get_api()
    return _j(api.cancel_log_request(counter_id, request_id))


@mcp.tool()
def ym_log_request_evaluate(counter_id: int, date1: str, date2: str, fields: str, source: str) -> str:
    """Оценка возможности запроса логов (GET .../logrequests/evaluate).

    Args:
        counter_id: Counter ID
        date1: Start date
        date2: End date
        fields: Fields, comma-separated
        source: Data source — "hits" or "visits"
    """
    api = _get_api()
    params = {"date1": date1, "date2": date2, "fields": fields, "source": source}
    return _j(api.evaluate_log_request(counter_id, params))


@mcp.tool()
def ym_log_request_download(counter_id: int, request_id: int, part_number: int, output_path: str) -> str:
    """Скачивание части лога (GET .../logrequest/{requestId}/part/{partNumber}/download).

    Args:
        counter_id: Counter ID
        request_id: Log request ID
        part_number: Part number (0-indexed)
        output_path: Absolute path to save TSV file
    """
    api = _get_api()
    data = api.download_log_part(counter_id, request_id, part_number)
    with open(output_path, "wb") as f:
        f.write(data)
    return _j({"path": os.path.abspath(output_path), "size": len(data)})


# ── Offline Conversions ───────────────────────────────────────────


@mcp.tool()
def ym_offline_conversions_upload(counter_id: int, file_path: str) -> str:
    """Загрузка оффлайн-конверсий из CSV (POST .../offline_conversions/upload).

    CSV columns: Target, DateTime, UserId/ClientId/Yclid, Price, Currency.

    Args:
        counter_id: Counter ID
        file_path: Absolute path to CSV file
    """
    api = _get_api()
    with open(file_path, "rb") as f:
        data = f.read()
    return _j(api.upload_offline_conversions(counter_id, data))


@mcp.tool()
def ym_offline_conversions_uploads(counter_id: int) -> str:
    """Список загрузок оффлайн-конверсий (GET .../offline_conversions/findAll_1).

    Args:
        counter_id: Counter ID
    """
    api = _get_api()
    return _j(api.list_offline_conversion_uploads(counter_id))


@mcp.tool()
def ym_offline_conversion_upload_info(counter_id: int, upload_id: int) -> str:
    """Информация о загрузке конверсий (GET .../offline_conversions/uploading/{id}).

    Args:
        counter_id: Counter ID
        upload_id: Upload ID
    """
    api = _get_api()
    return _j(api.get_offline_conversion_upload(counter_id, upload_id))


# ── Calls ─────────────────────────────────────────────────────────


@mcp.tool()
def ym_calls_upload(counter_id: int, file_path: str) -> str:
    """Загрузка звонков из CSV (POST .../offline_conversions/upload_calls).

    Args:
        counter_id: Counter ID
        file_path: Absolute path to CSV file
    """
    api = _get_api()
    with open(file_path, "rb") as f:
        data = f.read()
    return _j(api.upload_calls(counter_id, data))


@mcp.tool()
def ym_calls_uploads(counter_id: int) -> str:
    """Список загрузок звонков (GET .../offline_conversions/findAllCallUploadings).

    Args:
        counter_id: Counter ID
    """
    api = _get_api()
    return _j(api.list_calls_uploads(counter_id))


@mcp.tool()
def ym_calls_upload_info(counter_id: int, upload_id: int) -> str:
    """Информация о загрузке звонков (GET .../offline_conversions/calls_uploading/{id}).

    Args:
        counter_id: Counter ID
        upload_id: Upload ID
    """
    api = _get_api()
    return _j(api.get_calls_upload(counter_id, upload_id))


# ── Expenses ──────────────────────────────────────────────────────


@mcp.tool()
def ym_expenses_upload(counter_id: int, file_path: str, comment: str = "", provider: str = "") -> str:
    """Загрузка расходов из CSV (POST /management/v1/counter/{counterId}/expense/upload).

    CSV columns: Date, UTMSource, Expenses; optional: UTMMedium, UTMCampaign, Currency, Clicks.

    Args:
        counter_id: Counter ID
        file_path: Absolute path to CSV file
        comment: Upload comment
        provider: Provider name (default "default")
    """
    api = _get_api()
    with open(file_path, "rb") as f:
        data = f.read()
    return _j(api.upload_expenses(counter_id, data, comment, provider))


# ── User Parameters ───────────────────────────────────────────────


@mcp.tool()
def ym_user_params_upload(counter_id: int, file_path: str, action: str = "update") -> str:
    """Загрузка параметров пользователей из CSV (POST .../user_params/uploadings/upload).

    Args:
        counter_id: Counter ID
        file_path: Absolute path to CSV file
        action: Action — update/delete_keys
    """
    api = _get_api()
    with open(file_path, "rb") as f:
        data = f.read()
    return _j(api.upload_user_params(counter_id, data, action))
