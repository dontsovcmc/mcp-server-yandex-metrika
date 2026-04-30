"""Action registry for MCP server search/execute pattern.

Maps each MetrikaAPI method to an Action with metadata for discovery
(ym_search) and dispatch (ym_execute).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Callable

from pydantic import BaseModel

from .models import (
    AccessFilterCreateParams,
    AccessFilterUpdateParams,
    AnnotationCreateParams,
    AnnotationUpdateParams,
    CounterCreateParams,
    CounterUpdateParams,
    DelegateAddParams,
    FilterCreateParams,
    FilterUpdateParams,
    GoalCreateParams,
    GoalUpdateParams,
    GrantCreateParams,
    LabelCreateParams,
    LogRequestCreateParams,
    LogRequestEvaluateParams,
    OperationCreateParams,
    OperationUpdateParams,
    SegmentCreateParams,
    SegmentUpdateParams,
    StatByTimeParams,
    StatComparisonParams,
    StatDataParams,
    StatDrilldownParams,
)

if TYPE_CHECKING:
    from .metrika_api import MetrikaAPI


def _parse_json(text: str, label: str = "JSON") -> list | dict:
    """Parse JSON string with a human-readable error on failure."""
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Invalid {label}: {e}")


# ── Action dataclass ─────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class Action:
    """Single dispatchable action in the registry."""

    id: str
    domain: str
    description: str
    params_model: type[BaseModel] | None
    call_fn: Callable
    is_destructive: bool = False
    is_file: bool = False
    keywords: list[str] = field(default_factory=list)


# ── Reporting call functions ─────────────────────────────────────


async def _stat_data(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    params = {"ids": p["ids"], "metrics": p["metrics"], "limit": p["limit"], "offset": p["offset"]}
    for key in ("dimensions", "date1", "date2", "filters", "sort", "preset", "accuracy", "timezone", "lang"):
        if p.get(key):
            params[key] = p[key]
    if p.get("include_undefined"):
        params["include_undefined"] = "true"
    return await api.get_stat_data(params)


async def _stat_data_bytime(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    params = {
        "ids": p["ids"],
        "metrics": p["metrics"],
        "group": p.get("group", "day"),
        "limit": p["limit"],
        "offset": p["offset"],
    }
    for key in ("dimensions", "date1", "date2", "filters", "sort", "lang"):
        if p.get(key):
            params[key] = p[key]
    if p.get("top_keys", 7) != 7:
        params["top_keys"] = p["top_keys"]
    return await api.get_stat_data_bytime(params)


async def _stat_data_drilldown(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    params = {"ids": p["ids"], "metrics": p["metrics"], "limit": p["limit"], "offset": p["offset"]}
    for key in ("dimensions", "date1", "date2", "filters", "sort", "parent_id", "lang"):
        if p.get(key):
            params[key] = p[key]
    return await api.get_stat_data_drilldown(params)


async def _stat_data_comparison(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    params = {"ids": p["ids"], "metrics": p["metrics"], "limit": p["limit"], "offset": p["offset"]}
    for key in ("dimensions", "date1_a", "date2_a", "date1_b", "date2_b", "filters_a", "filters_b", "sort", "lang"):
        if p.get(key):
            params[key] = p[key]
    return await api.get_stat_data_comparison(params)


async def _stat_data_comparison_drilldown(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    params = {"ids": p["ids"], "metrics": p["metrics"], "limit": p["limit"], "offset": p["offset"]}
    for key in (
        "dimensions", "date1_a", "date2_a", "date1_b", "date2_b",
        "filters_a", "filters_b", "sort", "parent_id", "lang",
    ):
        if p.get(key):
            params[key] = p[key]
    return await api.get_stat_data_comparison_drilldown(params)


# ── Counters call functions ──────────────────────────────────────


async def _counters(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    params: dict = {}
    for key in ("search_string", "permission", "status", "per_page", "offset"):
        if p.get(key):
            params[key] = p[key]
    return await api.list_counters(params)


async def _counter(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.get_counter(p["counter_id"], p.get("field", ""))


async def _counter_create(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    payload = {
        "counter": {
            "name": p["name"],
            "site2": {"site": p["site"]},
            "time_zone_name": p.get("time_zone_name", "Europe/Moscow"),
        }
    }
    return await api.create_counter(payload)


async def _counter_update(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    counter: dict = {}
    if p.get("name"):
        counter["name"] = p["name"]
    if p.get("site"):
        counter["site2"] = {"site": p["site"]}
    if p.get("time_zone_name"):
        counter["time_zone_name"] = p["time_zone_name"]
    return await api.update_counter(p["counter_id"], {"counter": counter})


async def _counter_delete(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.delete_counter(p["counter_id"])


async def _counter_undelete(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.undelete_counter(p["counter_id"])


# ── Goals call functions ─────────────────────────────────────────


async def _goals(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.list_goals(p["counter_id"], p.get("use_deleted", False))


async def _goal(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.get_goal(p["counter_id"], p["goal_id"])


async def _goal_create(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    goal: dict = {"name": p["name"], "type": p["goal_type"]}
    if p.get("conditions_json"):
        goal["conditions"] = _parse_json(p["conditions_json"], "conditions_json")
    if p.get("depth"):
        goal["depth"] = p["depth"]
    if p.get("duration"):
        goal["duration"] = p["duration"]
    if p.get("default_price"):
        goal["default_price"] = p["default_price"]
    if p.get("is_favorite"):
        goal["is_favorite"] = True
    return await api.create_goal(p["counter_id"], {"goal": goal})


async def _goal_update(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    goal: dict = {}
    if p.get("name"):
        goal["name"] = p["name"]
    if p.get("goal_type"):
        goal["type"] = p["goal_type"]
    if p.get("conditions_json"):
        goal["conditions"] = _parse_json(p["conditions_json"], "conditions_json")
    if p.get("depth"):
        goal["depth"] = p["depth"]
    if p.get("duration"):
        goal["duration"] = p["duration"]
    if p.get("default_price"):
        goal["default_price"] = p["default_price"]
    if p.get("is_favorite"):
        goal["is_favorite"] = True
    return await api.update_goal(p["counter_id"], p["goal_id"], {"goal": goal})


async def _goal_delete(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.delete_goal(p["counter_id"], p["goal_id"])


# ── Filters call functions ───────────────────────────────────────


async def _filters(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.list_filters(p["counter_id"])


async def _filter(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.get_filter(p["counter_id"], p["filter_id"])


async def _filter_create(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    f: dict = {
        "attr": p["attr"], "type": p["filter_type"],
        "action": p.get("action", "exclude"), "status": p.get("status", "active"),
    }
    if p.get("value"):
        f["value"] = p["value"]
    if p.get("start_ip"):
        f["start_ip"] = p["start_ip"]
    if p.get("end_ip"):
        f["end_ip"] = p["end_ip"]
    return await api.create_filter(p["counter_id"], {"filter": f})


async def _filter_update(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    f: dict = {}
    if p.get("attr"):
        f["attr"] = p["attr"]
    if p.get("filter_type"):
        f["type"] = p["filter_type"]
    if p.get("value"):
        f["value"] = p["value"]
    if p.get("action"):
        f["action"] = p["action"]
    if p.get("status"):
        f["status"] = p["status"]
    if p.get("start_ip"):
        f["start_ip"] = p["start_ip"]
    if p.get("end_ip"):
        f["end_ip"] = p["end_ip"]
    return await api.update_filter(p["counter_id"], p["filter_id"], {"filter": f})


async def _filter_delete(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.delete_filter(p["counter_id"], p["filter_id"])


# ── Grants call functions ────────────────────────────────────────


async def _grants(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.list_grants(p["counter_id"])


async def _grant_create(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    grant: dict = {"user_login": p["user_login"], "perm": p["perm"]}
    if p.get("comment"):
        grant["comment"] = p["comment"]
    return await api.create_grant(p["counter_id"], {"grant": grant})


async def _grant_update(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    grant: dict = {"user_login": p["user_login"], "perm": p["perm"]}
    if p.get("comment"):
        grant["comment"] = p["comment"]
    return await api.update_grant(p["counter_id"], {"grant": grant})


async def _grant_delete(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.delete_grant(p["counter_id"], user_login=p["user_login"])


# ── Operations call functions ────────────────────────────────────


async def _operations(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.list_operations(p["counter_id"])


async def _operation(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.get_operation(p["counter_id"], p["operation_id"])


async def _operation_create(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.create_operation(
        p["counter_id"],
        {"operation": {"action": p["action"], "attr": p["attr"], "value": p["value"]}},
    )


async def _operation_update(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    op: dict = {}
    if p.get("action"):
        op["action"] = p["action"]
    if p.get("attr"):
        op["attr"] = p["attr"]
    if p.get("value"):
        op["value"] = p["value"]
    if p.get("status"):
        op["status"] = p["status"]
    return await api.update_operation(p["counter_id"], p["operation_id"], {"operation": op})


async def _operation_delete(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.delete_operation(p["counter_id"], p["operation_id"])


# ── Segments call functions ──────────────────────────────────────


async def _segments(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.list_segments(p["counter_id"])


async def _segment(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.get_segment(p["counter_id"], p["segment_id"])


async def _segment_create(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.create_segment(
        p["counter_id"],
        {"segment": {"name": p["name"], "expression": p["expression"]}},
    )


async def _segment_update(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    seg: dict = {}
    if p.get("name"):
        seg["name"] = p["name"]
    if p.get("expression"):
        seg["expression"] = p["expression"]
    return await api.update_segment(p["counter_id"], p["segment_id"], {"segment": seg})


async def _segment_delete(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.delete_segment(p["counter_id"], p["segment_id"])


# ── Labels call functions ────────────────────────────────────────


async def _labels(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.list_labels()


async def _label_create(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.create_label({"label": {"name": p["name"]}})


async def _label_update(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.update_label(p["label_id"], {"label": {"name": p["name"]}})


async def _label_delete(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.delete_label(p["label_id"])


async def _counter_label_set(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.set_counter_label(p["counter_id"], p["label_id"])


async def _counter_label_unset(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.unset_counter_label(p["counter_id"], p["label_id"])


# ── Accounts call functions ──────────────────────────────────────


async def _accounts(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.list_accounts()


async def _account_delete(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.delete_account(p["user_login"])


# ── Delegates call functions ─────────────────────────────────────


async def _delegates(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.list_delegates()


async def _delegate_add(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    delegate: dict = {"user_login": p["user_login"]}
    if p.get("comment"):
        delegate["comment"] = p["comment"]
    return await api.add_delegate({"delegate": delegate})


async def _delegate_delete(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.delete_delegate(p["user_login"])


# ── Annotations call functions ───────────────────────────────────


async def _chart_annotations(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.list_chart_annotations(p["counter_id"])


async def _chart_annotation_create(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    ann: dict = {"date": p["date"], "title": p["title"], "group": p.get("group", "A")}
    if p.get("message"):
        ann["message"] = p["message"]
    return await api.create_chart_annotation(p["counter_id"], {"chart_annotation": ann})


async def _chart_annotation_update(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    ann: dict = {}
    if p.get("date"):
        ann["date"] = p["date"]
    if p.get("title"):
        ann["title"] = p["title"]
    if p.get("message"):
        ann["message"] = p["message"]
    if p.get("group"):
        ann["group"] = p["group"]
    return await api.update_chart_annotation(p["counter_id"], p["annotation_id"], {"chart_annotation": ann})


async def _chart_annotation_delete(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.delete_chart_annotation(p["counter_id"], p["annotation_id"])


# ── Access Filters call functions ────────────────────────────────


async def _access_filters(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.list_access_filters(p["counter_id"])


async def _access_filter_create(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    af: dict = {"name": p["name"], "expression": p["expression"]}
    if p.get("interface_value"):
        af["interface_value"] = p["interface_value"]
    return await api.create_access_filter(p["counter_id"], {"access_filter": af})


async def _access_filter_update(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    af: dict = {}
    if p.get("name"):
        af["name"] = p["name"]
    if p.get("expression"):
        af["expression"] = p["expression"]
    if p.get("interface_value"):
        af["interface_value"] = p["interface_value"]
    return await api.update_access_filter(p["counter_id"], p["access_filter_id"], {"access_filter": af})


async def _access_filter_delete(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.delete_access_filter(
        p["counter_id"], p["access_filter_id"], delete_grants=p.get("delete_grants", False),
    )


# ── Logs call functions ──────────────────────────────────────────


async def _log_requests(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.list_log_requests(p["counter_id"])


async def _log_request(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.get_log_request(p["counter_id"], p["request_id"])


async def _log_request_create(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    params = {
        "date1": p["date1"],
        "date2": p["date2"],
        "fields": p["fields"],
        "source": p["source"],
        "attribution": p.get("attribution", "LASTSIGN"),
    }
    return await api.create_log_request(p["counter_id"], params)


async def _log_request_clean(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.clean_log_request(p["counter_id"], p["request_id"])


async def _log_request_cancel(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.cancel_log_request(p["counter_id"], p["request_id"])


async def _log_request_evaluate(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    params = {"date1": p["date1"], "date2": p["date2"], "fields": p["fields"], "source": p["source"]}
    return await api.evaluate_log_request(p["counter_id"], params)


async def _log_request_download(api: MetrikaAPI, cid: int | None, p: dict) -> bytes:
    return await api.download_log_part(p["counter_id"], p["request_id"], p["part_number"])


# ── Uploads call functions ───────────────────────────────────────


async def _offline_conversions_upload(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.upload_offline_conversions(p["counter_id"], p["file_data"])


async def _offline_conversions_uploads(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.list_offline_conversion_uploads(p["counter_id"])


async def _offline_conversion_upload_info(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.get_offline_conversion_upload(p["counter_id"], p["upload_id"])


async def _calls_upload(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.upload_calls(p["counter_id"], p["file_data"])


async def _calls_uploads(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.list_calls_uploads(p["counter_id"])


async def _calls_upload_info(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.get_calls_upload(p["counter_id"], p["upload_id"])


async def _expenses_upload(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.upload_expenses(
        p["counter_id"], p["file_data"], comment=p.get("comment", ""), provider=p.get("provider", ""),
    )


async def _user_params_upload(api: MetrikaAPI, cid: int | None, p: dict) -> dict:
    return await api.upload_user_params(p["counter_id"], p["file_data"], action=p.get("action", "update"))


# ── Action registry ─────────────────────────────────────────────

_ACTIONS_LIST: list[Action] = [
    # ── Reporting ────────────────────────────────────────────────
    Action(
        id="stat_data",
        domain="reporting",
        description="Table report (GET /stat/v1/data). Returns statistical data with dimensions, metrics, filters.",
        params_model=StatDataParams,
        call_fn=_stat_data,
        keywords=["report", "table", "statistics", "visits", "users", "pageviews", "отчёт", "статистика"],
    ),
    Action(
        id="stat_data_bytime",
        domain="reporting",
        description="Time-series report (GET /stat/v1/data/bytime). Returns data split by time intervals.",
        params_model=StatByTimeParams,
        call_fn=_stat_data_bytime,
        keywords=["time", "timeseries", "bytime", "график", "время"],
    ),
    Action(
        id="stat_data_drilldown",
        domain="reporting",
        description="Drill down report (GET /stat/v1/data/drilldown). Expands nested dimension levels.",
        params_model=StatDrilldownParams,
        call_fn=_stat_data_drilldown,
        keywords=["drilldown", "drill", "expand", "раскрытие"],
    ),
    Action(
        id="stat_data_comparison",
        domain="reporting",
        description="Comparison report (GET /stat/v1/data/comparison). Compare two segments or date ranges.",
        params_model=StatComparisonParams,
        call_fn=_stat_data_comparison,
        keywords=["comparison", "compare", "сравнение", "сегменты"],
    ),
    Action(
        id="stat_data_comparison_drilldown",
        domain="reporting",
        description="Comparison drill down (GET /stat/v1/data/comparison/drilldown). Compare with nested expansion.",
        params_model=StatComparisonParams,
        call_fn=_stat_data_comparison_drilldown,
        keywords=["comparison", "drilldown"],
    ),
    # ── Counters ─────────────────────────────────────────────────
    Action(
        id="counters",
        domain="counters",
        description="List counters (GET /management/v1/counters). Search and filter your Metrika counters.",
        params_model=None,
        call_fn=_counters,
        keywords=["list", "счётчики"],
    ),
    Action(
        id="counter",
        domain="counters",
        description="Get counter info (GET /management/v1/counter/{id}). Full details about a counter.",
        params_model=None,
        call_fn=_counter,
        keywords=["get", "info", "счётчик"],
    ),
    Action(
        id="counter_create",
        domain="counters",
        description="Create counter (POST /management/v1/counters). Set up a new Metrika counter.",
        params_model=CounterCreateParams,
        call_fn=_counter_create,
        keywords=["create", "new", "создать"],
    ),
    Action(
        id="counter_update",
        domain="counters",
        description="Update counter (PUT /management/v1/counter/{id}). Modify counter settings.",
        params_model=CounterUpdateParams,
        call_fn=_counter_update,
        keywords=["update", "edit", "изменить"],
    ),
    Action(
        id="counter_delete",
        domain="counters",
        description="Delete counter (DELETE /management/v1/counter/{id}). Remove a counter.",
        params_model=None,
        call_fn=_counter_delete,
        is_destructive=True,
        keywords=["delete", "удалить"],
    ),
    Action(
        id="counter_undelete",
        domain="counters",
        description="Undelete counter (POST /management/v1/counter/{id}/undelete). Restore a deleted counter.",
        params_model=None,
        call_fn=_counter_undelete,
        keywords=["undelete", "restore", "восстановить"],
    ),
    # ── Goals ────────────────────────────────────────────────────
    Action(
        id="goals",
        domain="goals",
        description="List goals (GET /management/v1/counter/{id}/goals). All goals of a counter.",
        params_model=None,
        call_fn=_goals,
        keywords=["list", "цели"],
    ),
    Action(
        id="goal",
        domain="goals",
        description="Get goal (GET /management/v1/counter/{id}/goal/{goalId}). Single goal details.",
        params_model=None,
        call_fn=_goal,
        keywords=["get", "цель"],
    ),
    Action(
        id="goal_create",
        domain="goals",
        description="Create goal (POST /management/v1/counter/{id}/goals). Add a conversion goal.",
        params_model=GoalCreateParams,
        call_fn=_goal_create,
        keywords=["create", "создать"],
    ),
    Action(
        id="goal_update",
        domain="goals",
        description="Update goal (PUT /management/v1/counter/{id}/goal/{goalId}). Modify goal settings.",
        params_model=GoalUpdateParams,
        call_fn=_goal_update,
        keywords=["update", "edit", "изменить"],
    ),
    Action(
        id="goal_delete",
        domain="goals",
        description="Delete goal (DELETE /management/v1/counter/{id}/goal/{goalId}). Remove a goal.",
        params_model=None,
        call_fn=_goal_delete,
        is_destructive=True,
        keywords=["delete", "удалить"],
    ),
    # ── Filters ──────────────────────────────────────────────────
    Action(
        id="filters",
        domain="filters",
        description="List filters (GET /management/v1/counter/{id}/filters). Counter data filters.",
        params_model=None,
        call_fn=_filters,
        keywords=["list", "фильтры"],
    ),
    Action(
        id="filter",
        domain="filters",
        description="Get filter (GET /management/v1/counter/{id}/filter/{filterId}). Single filter details.",
        params_model=None,
        call_fn=_filter,
        keywords=["get", "фильтр"],
    ),
    Action(
        id="filter_create",
        domain="filters",
        description="Create filter (POST /management/v1/counter/{id}/filters). Add a data filter.",
        params_model=FilterCreateParams,
        call_fn=_filter_create,
        keywords=["create"],
    ),
    Action(
        id="filter_update",
        domain="filters",
        description="Update filter (PUT /management/v1/counter/{id}/filter/{filterId}). Modify filter settings.",
        params_model=FilterUpdateParams,
        call_fn=_filter_update,
        keywords=["update"],
    ),
    Action(
        id="filter_delete",
        domain="filters",
        description="Delete filter (DELETE /management/v1/counter/{id}/filter/{filterId}). Remove a filter.",
        params_model=None,
        call_fn=_filter_delete,
        is_destructive=True,
        keywords=["delete"],
    ),
    # ── Grants ───────────────────────────────────────────────────
    Action(
        id="grants",
        domain="grants",
        description="List grants (GET /management/v1/counter/{id}/grants). Access permissions for a counter.",
        params_model=None,
        call_fn=_grants,
        keywords=["list", "permissions", "разрешения"],
    ),
    Action(
        id="grant_create",
        domain="grants",
        description="Create grant (POST /management/v1/counter/{id}/grants). Grant access to a user.",
        params_model=GrantCreateParams,
        call_fn=_grant_create,
        keywords=["create", "grant"],
    ),
    Action(
        id="grant_update",
        domain="grants",
        description="Update grant (PUT /management/v1/counter/{id}/grant). Change user permissions.",
        params_model=GrantCreateParams,
        call_fn=_grant_update,
        keywords=["update"],
    ),
    Action(
        id="grant_delete",
        domain="grants",
        description="Delete grant (DELETE /management/v1/counter/{id}/grant). Revoke user access.",
        params_model=None,
        call_fn=_grant_delete,
        is_destructive=True,
        keywords=["delete", "revoke"],
    ),
    # ── Operations ───────────────────────────────────────────────
    Action(
        id="operations",
        domain="operations",
        description="List operations (GET /management/v1/counter/{id}/operations). URL/referer transformations.",
        params_model=None,
        call_fn=_operations,
        keywords=["list", "операции"],
    ),
    Action(
        id="operation",
        domain="operations",
        description="Get operation (GET /management/v1/counter/{id}/operation/{opId}). Single operation details.",
        params_model=None,
        call_fn=_operation,
        keywords=["get"],
    ),
    Action(
        id="operation_create",
        domain="operations",
        description="Create operation (POST /management/v1/counter/{id}/operations). Add a URL transformation.",
        params_model=OperationCreateParams,
        call_fn=_operation_create,
        keywords=["create"],
    ),
    Action(
        id="operation_update",
        domain="operations",
        description="Update operation (PUT /management/v1/counter/{id}/operation/{opId}). Modify a transformation.",
        params_model=OperationUpdateParams,
        call_fn=_operation_update,
        keywords=["update"],
    ),
    Action(
        id="operation_delete",
        domain="operations",
        description="Delete operation (DELETE /management/v1/counter/{id}/operation/{opId}). Remove a transformation.",
        params_model=None,
        call_fn=_operation_delete,
        is_destructive=True,
        keywords=["delete"],
    ),
    # ── Segments ─────────────────────────────────────────────────
    Action(
        id="segments",
        domain="segments",
        description="List segments (GET /management/v1/counter/{id}/apisegment/segments). API segments.",
        params_model=None,
        call_fn=_segments,
        keywords=["list", "сегменты"],
    ),
    Action(
        id="segment",
        domain="segments",
        description="Get segment (GET .../apisegment/segment/{segId}). Single segment details.",
        params_model=None,
        call_fn=_segment,
        keywords=["get", "сегмент"],
    ),
    Action(
        id="segment_create",
        domain="segments",
        description="Create segment (POST .../apisegment/segments). Define a new user segment.",
        params_model=SegmentCreateParams,
        call_fn=_segment_create,
        keywords=["create"],
    ),
    Action(
        id="segment_update",
        domain="segments",
        description="Update segment (PUT .../apisegment/segment/{segId}). Modify segment definition.",
        params_model=SegmentUpdateParams,
        call_fn=_segment_update,
        keywords=["update"],
    ),
    Action(
        id="segment_delete",
        domain="segments",
        description="Delete segment (DELETE .../apisegment/segment/{segId}). Remove a segment.",
        params_model=None,
        call_fn=_segment_delete,
        is_destructive=True,
        keywords=["delete"],
    ),
    # ── Labels ───────────────────────────────────────────────────
    Action(
        id="labels",
        domain="labels",
        description="List labels (GET /management/v1/labels). Counter labels/tags.",
        params_model=None,
        call_fn=_labels,
        keywords=["list", "метки"],
    ),
    Action(
        id="label_create",
        domain="labels",
        description="Create label (POST /management/v1/labels). Add a new counter label.",
        params_model=LabelCreateParams,
        call_fn=_label_create,
        keywords=["create"],
    ),
    Action(
        id="label_update",
        domain="labels",
        description="Update label (PUT /management/v1/label/{labelId}). Rename a label.",
        params_model=LabelCreateParams,
        call_fn=_label_update,
        keywords=["update"],
    ),
    Action(
        id="label_delete",
        domain="labels",
        description="Delete label (DELETE /management/v1/label/{labelId}). Remove a label.",
        params_model=None,
        call_fn=_label_delete,
        is_destructive=True,
        keywords=["delete"],
    ),
    Action(
        id="counter_label_set",
        domain="labels",
        description="Assign label to counter (POST /management/v1/counter/{id}/label/{labelId}).",
        params_model=None,
        call_fn=_counter_label_set,
        keywords=["set", "assign", "привязать"],
    ),
    Action(
        id="counter_label_unset",
        domain="labels",
        description="Remove label from counter (DELETE /management/v1/counter/{id}/label/{labelId}).",
        params_model=None,
        call_fn=_counter_label_unset,
        keywords=["unset", "remove", "отвязать"],
    ),
    # ── Accounts ─────────────────────────────────────────────────
    Action(
        id="accounts",
        domain="accounts",
        description="List accounts (GET /management/v1/accounts). Linked Metrika accounts.",
        params_model=None,
        call_fn=_accounts,
        keywords=["list", "аккаунты"],
    ),
    Action(
        id="account_delete",
        domain="accounts",
        description="Delete account (DELETE /management/v1/account). Unlink an account.",
        params_model=None,
        call_fn=_account_delete,
        is_destructive=True,
        keywords=["delete"],
    ),
    # ── Delegates ────────────────────────────────────────────────
    Action(
        id="delegates",
        domain="delegates",
        description="List delegates (GET /management/v1/delegates). Account representatives.",
        params_model=None,
        call_fn=_delegates,
        keywords=["list", "представители"],
    ),
    Action(
        id="delegate_add",
        domain="delegates",
        description="Add delegate (POST /management/v1/delegates). Grant representative access.",
        params_model=DelegateAddParams,
        call_fn=_delegate_add,
        keywords=["add", "create"],
    ),
    Action(
        id="delegate_delete",
        domain="delegates",
        description="Delete delegate (DELETE /management/v1/delegate). Revoke representative access.",
        params_model=None,
        call_fn=_delegate_delete,
        is_destructive=True,
        keywords=["delete", "remove"],
    ),
    # ── Annotations ──────────────────────────────────────────────
    Action(
        id="chart_annotations",
        domain="annotations",
        description="List chart annotations (GET .../chart_annotations). Notes on time-series charts.",
        params_model=None,
        call_fn=_chart_annotations,
        keywords=["list", "примечания", "annotations"],
    ),
    Action(
        id="chart_annotation_create",
        domain="annotations",
        description="Create chart annotation (POST .../chart_annotations). Add a chart note.",
        params_model=AnnotationCreateParams,
        call_fn=_chart_annotation_create,
        keywords=["create"],
    ),
    Action(
        id="chart_annotation_update",
        domain="annotations",
        description="Update chart annotation (PUT .../chart_annotation/{id}). Modify a chart note.",
        params_model=AnnotationUpdateParams,
        call_fn=_chart_annotation_update,
        keywords=["update"],
    ),
    Action(
        id="chart_annotation_delete",
        domain="annotations",
        description="Delete chart annotation (DELETE .../chart_annotation/{id}). Remove a chart note.",
        params_model=None,
        call_fn=_chart_annotation_delete,
        is_destructive=True,
        keywords=["delete"],
    ),
    # ── Access Filters ───────────────────────────────────────────
    Action(
        id="access_filters",
        domain="access_filters",
        description="List access filters (GET .../access_filters). Data access restrictions.",
        params_model=None,
        call_fn=_access_filters,
        keywords=["list", "фильтры доступа"],
    ),
    Action(
        id="access_filter_create",
        domain="access_filters",
        description="Create access filter (POST .../access_filters). Add data access restriction.",
        params_model=AccessFilterCreateParams,
        call_fn=_access_filter_create,
        keywords=["create"],
    ),
    Action(
        id="access_filter_update",
        domain="access_filters",
        description="Update access filter (PUT .../access_filter/{id}). Modify access restriction.",
        params_model=AccessFilterUpdateParams,
        call_fn=_access_filter_update,
        keywords=["update"],
    ),
    Action(
        id="access_filter_delete",
        domain="access_filters",
        description="Delete access filter (DELETE .../access_filter/{id}). Remove access restriction.",
        params_model=None,
        call_fn=_access_filter_delete,
        is_destructive=True,
        keywords=["delete"],
    ),
    # ── Logs ─────────────────────────────────────────────────────
    Action(
        id="log_requests",
        domain="logs",
        description="List log requests (GET .../logrequests). Logs API request queue.",
        params_model=None,
        call_fn=_log_requests,
        keywords=["list", "logs", "логи"],
    ),
    Action(
        id="log_request",
        domain="logs",
        description="Get log request (GET .../logrequest/{requestId}). Log request status and details.",
        params_model=None,
        call_fn=_log_request,
        keywords=["get", "log"],
    ),
    Action(
        id="log_request_create",
        domain="logs",
        description="Create log request (POST .../logrequests). Request raw visit/hit logs.",
        params_model=LogRequestCreateParams,
        call_fn=_log_request_create,
        keywords=["create", "request"],
    ),
    Action(
        id="log_request_clean",
        domain="logs",
        description="Clean log request (POST .../logrequest/{requestId}/clean). Remove processed log data.",
        params_model=None,
        call_fn=_log_request_clean,
        keywords=["clean", "очистить"],
    ),
    Action(
        id="log_request_cancel",
        domain="logs",
        description="Cancel log request (POST .../logrequest/{requestId}/cancel). Abort a pending log request.",
        params_model=None,
        call_fn=_log_request_cancel,
        keywords=["cancel", "отменить"],
    ),
    Action(
        id="log_request_evaluate",
        domain="logs",
        description="Evaluate log request (GET .../logrequests/evaluate). Check if log request is possible.",
        params_model=LogRequestEvaluateParams,
        call_fn=_log_request_evaluate,
        keywords=["evaluate", "оценить"],
    ),
    Action(
        id="log_request_download",
        domain="logs",
        description="Download log part (GET .../logrequest/{requestId}/part/{partNumber}/download). Get TSV data.",
        params_model=None,
        call_fn=_log_request_download,
        is_file=True,
        keywords=["download", "скачать"],
    ),
    # ── Uploads ──────────────────────────────────────────────────
    Action(
        id="offline_conversions_upload",
        domain="uploads",
        description="Upload offline conversions (POST .../offline_conversions/upload). CSV with conversions.",
        params_model=None,
        call_fn=_offline_conversions_upload,
        is_file=True,
        keywords=["upload", "конверсии", "conversions"],
    ),
    Action(
        id="offline_conversions_uploads",
        domain="uploads",
        description="List offline conversion uploads (GET .../offline_conversions/findAll_1). Upload history.",
        params_model=None,
        call_fn=_offline_conversions_uploads,
        keywords=["list", "uploads"],
    ),
    Action(
        id="offline_conversion_upload_info",
        domain="uploads",
        description="Get offline conversion upload info (GET .../offline_conversions/uploading/{id}). Upload status.",
        params_model=None,
        call_fn=_offline_conversion_upload_info,
        keywords=["info", "status"],
    ),
    Action(
        id="calls_upload",
        domain="uploads",
        description="Upload calls (POST .../offline_conversions/upload_calls). CSV with call data.",
        params_model=None,
        call_fn=_calls_upload,
        is_file=True,
        keywords=["upload", "звонки", "calls"],
    ),
    Action(
        id="calls_uploads",
        domain="uploads",
        description="List call uploads (GET .../offline_conversions/findAllCallUploadings). Call upload history.",
        params_model=None,
        call_fn=_calls_uploads,
        keywords=["list", "uploads"],
    ),
    Action(
        id="calls_upload_info",
        domain="uploads",
        description="Get call upload info (GET .../offline_conversions/calls_uploading/{id}). Call upload status.",
        params_model=None,
        call_fn=_calls_upload_info,
        keywords=["info", "status"],
    ),
    Action(
        id="expenses_upload",
        domain="uploads",
        description="Upload expenses (POST .../expense/upload). CSV with ad spend data.",
        params_model=None,
        call_fn=_expenses_upload,
        is_file=True,
        keywords=["upload", "расходы", "expenses"],
    ),
    Action(
        id="user_params_upload",
        domain="uploads",
        description="Upload user parameters (POST .../user_params/uploadings/upload). CSV with user attributes.",
        params_model=None,
        call_fn=_user_params_upload,
        is_file=True,
        keywords=["upload", "параметры", "user_params"],
    ),
]

ACTIONS: dict[str, Action] = {a.id: a for a in _ACTIONS_LIST}
