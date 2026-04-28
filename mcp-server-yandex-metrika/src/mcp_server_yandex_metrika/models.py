"""Pydantic-модели для API Яндекс Метрики.

Использование:
    from mcp_server_yandex_metrika.models import Counter, Goal, Segment
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


# ── Base ──────────────────────────────────────────────────────────


class MetrikaBaseModel(BaseModel):
    """Базовая модель. extra='allow' сохраняет недокументированные поля API."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")


# ── Counter ───────────────────────────────────────────────────────


class CodeOptions(MetrikaBaseModel):
    """Настройки кода счётчика."""

    async_flag: Optional[bool] = None
    visor: Optional[bool] = None
    clickmap: Optional[bool] = None
    ecommerce: Optional[bool] = None


class Site(MetrikaBaseModel):
    """Сайт счётчика."""

    site: Optional[str] = None


class CounterBrief(MetrikaBaseModel):
    """Краткая информация о счётчике (из GET /management/v1/counters)."""

    id: int
    name: Optional[str] = None
    site: Optional[str] = None
    site2: Optional[Site] = None
    type: Optional[str] = None
    status: Optional[str] = None
    owner_login: Optional[str] = None
    permission: Optional[str] = None
    create_time: Optional[str] = None
    code_status: Optional[str] = None
    mirrors2: Optional[list[Site]] = None
    goals_count: Optional[int] = None
    favorite: Optional[bool] = None


class CounterFull(MetrikaBaseModel):
    """Полная информация о счётчике (из GET /management/v1/counter/{id})."""

    id: Optional[int] = None
    name: Optional[str] = None
    site: Optional[str] = None
    site2: Optional[Site] = None
    type: Optional[str] = None
    status: Optional[str] = None
    owner_login: Optional[str] = None
    permission: Optional[str] = None
    create_time: Optional[str] = None
    code_status: Optional[str] = None
    code_options: Optional[CodeOptions] = None
    mirrors2: Optional[list[Site]] = None
    time_zone_name: Optional[str] = None
    time_zone_offset: Optional[int] = None
    favorite: Optional[bool] = None
    goals: Optional[list] = None
    filters: Optional[list] = None
    operations: Optional[list] = None
    grants: Optional[list] = None


class CounterRequest(MetrikaBaseModel):
    """Запрос на создание/изменение счётчика."""

    counter: dict


class CountersResponse(MetrikaBaseModel):
    """Ответ списка счётчиков."""

    rows: Optional[int] = None
    counters: Optional[list[CounterBrief]] = None


class CounterResponse(MetrikaBaseModel):
    """Ответ с одним счётчиком."""

    counter: Optional[CounterFull] = None


# ── Goal ──────────────────────────────────────────────────────────


class GoalCondition(MetrikaBaseModel):
    """Условие цели."""

    type: Optional[str] = None
    url: Optional[str] = None


class Goal(MetrikaBaseModel):
    """Цель счётчика."""

    id: Optional[int] = None
    name: Optional[str] = None
    type: Optional[str] = None
    default_price: Optional[float] = None
    is_favorite: Optional[bool] = None
    goal_source: Optional[str] = None
    conditions: Optional[list[GoalCondition]] = None
    depth: Optional[int] = None
    duration: Optional[int] = None
    steps: Optional[list] = None
    flag: Optional[str] = None
    hide_phone_number: Optional[bool] = None


class GoalRequest(MetrikaBaseModel):
    """Запрос на создание/изменение цели."""

    goal: Goal


class GoalsResponse(MetrikaBaseModel):
    """Ответ списка целей."""

    goals: Optional[list[Goal]] = None


class GoalResponse(MetrikaBaseModel):
    """Ответ с одной целью."""

    goal: Optional[Goal] = None


# ── Filter ────────────────────────────────────────────────────────


class FilterE(MetrikaBaseModel):
    """Фильтр счётчика."""

    id: Optional[int] = None
    attr: Optional[str] = None
    type: Optional[str] = None
    value: Optional[str] = None
    action: Optional[str] = None
    status: Optional[str] = None
    start_ip: Optional[str] = None
    end_ip: Optional[str] = None
    with_subdomains: Optional[bool] = None


class FilterRequest(MetrikaBaseModel):
    """Запрос на создание/изменение фильтра."""

    filter: FilterE


class FiltersResponse(MetrikaBaseModel):
    """Ответ списка фильтров."""

    filters: Optional[list[FilterE]] = None


class FilterResponse(MetrikaBaseModel):
    """Ответ с одним фильтром."""

    filter: Optional[FilterE] = None


# ── Grant ─────────────────────────────────────────────────────────


class Grant(MetrikaBaseModel):
    """Разрешение на доступ к счётчику."""

    user_login: Optional[str] = None
    user_uid: Optional[int] = None
    perm: Optional[str] = None
    created_at: Optional[str] = None
    comment: Optional[str] = None
    partner_data_access: Optional[bool] = None
    access_filters: Optional[list] = None


class GrantRequest(MetrikaBaseModel):
    """Запрос на создание/изменение разрешения."""

    grant: Grant


class GrantsResponse(MetrikaBaseModel):
    """Ответ списка разрешений."""

    grants: Optional[list[Grant]] = None


class GrantResponse(MetrikaBaseModel):
    """Ответ с одним разрешением."""

    grant: Optional[Grant] = None


# ── Operation ─────────────────────────────────────────────────────


class OperationE(MetrikaBaseModel):
    """Операция над данными счётчика."""

    id: Optional[int] = None
    action: Optional[str] = None
    attr: Optional[str] = None
    value: Optional[str] = None
    status: Optional[str] = None


class OperationRequest(MetrikaBaseModel):
    """Запрос на создание/изменение операции."""

    operation: OperationE


class OperationsResponse(MetrikaBaseModel):
    """Ответ списка операций."""

    operations: Optional[list[OperationE]] = None


class OperationResponse(MetrikaBaseModel):
    """Ответ с одной операцией."""

    operation: Optional[OperationE] = None


# ── Segment ───────────────────────────────────────────────────────


class Segment(MetrikaBaseModel):
    """API-сегмент."""

    segment_id: Optional[int] = None
    counter_id: Optional[int] = None
    name: Optional[str] = None
    expression: Optional[str] = None
    status: Optional[str] = None
    segment_source: Optional[str] = None
    create_time: Optional[str] = None


class SegmentRequest(MetrikaBaseModel):
    """Запрос на создание/изменение сегмента."""

    segment: Segment


class SegmentsResponse(MetrikaBaseModel):
    """Ответ списка сегментов."""

    segments: Optional[list[Segment]] = None


class SegmentResponse(MetrikaBaseModel):
    """Ответ с одним сегментом."""

    segment: Optional[Segment] = None


# ── Label ─────────────────────────────────────────────────────────


class Label(MetrikaBaseModel):
    """Метка для счётчиков."""

    id: Optional[int] = None
    name: Optional[str] = None


class LabelRequest(MetrikaBaseModel):
    """Запрос на создание/изменение метки."""

    label: Label


class LabelsResponse(MetrikaBaseModel):
    """Ответ списка меток."""

    labels: Optional[list[Label]] = None


class LabelResponse(MetrikaBaseModel):
    """Ответ с одной меткой."""

    label: Optional[Label] = None


# ── Account ───────────────────────────────────────────────────────


class Account(MetrikaBaseModel):
    """Аккаунт."""

    user_login: Optional[str] = None
    created_at: Optional[str] = None


class AccountsResponse(MetrikaBaseModel):
    """Ответ списка аккаунтов."""

    accounts: Optional[list[Account]] = None


# ── Delegate ──────────────────────────────────────────────────────


class Delegate(MetrikaBaseModel):
    """Представитель."""

    user_login: Optional[str] = None
    created_at: Optional[str] = None
    comment: Optional[str] = None


class DelegateRequest(MetrikaBaseModel):
    """Запрос на добавление представителя."""

    delegate: Delegate


class DelegatesResponse(MetrikaBaseModel):
    """Ответ списка представителей."""

    delegates: Optional[list[Delegate]] = None


# ── Chart Annotation ──────────────────────────────────────────────


class ChartAnnotation(MetrikaBaseModel):
    """Примечание на графике."""

    id: Optional[int] = None
    date: Optional[str] = None
    time: Optional[str] = None
    title: Optional[str] = None
    message: Optional[str] = None
    group: Optional[str] = None


class ChartAnnotationRequest(MetrikaBaseModel):
    """Запрос на создание/изменение примечания."""

    chart_annotation: ChartAnnotation


class ChartAnnotationsResponse(MetrikaBaseModel):
    """Ответ списка примечаний."""

    chart_annotations: Optional[list[ChartAnnotation]] = None


class ChartAnnotationResponse(MetrikaBaseModel):
    """Ответ с одним примечанием."""

    chart_annotation: Optional[ChartAnnotation] = None


# ── Access Filter ─────────────────────────────────────────────────


class AccessFilter(MetrikaBaseModel):
    """Фильтр доступа."""

    id: Optional[int] = None
    name: Optional[str] = None
    expression: Optional[str] = None
    interface_value: Optional[str] = None


class AccessFilterRequest(MetrikaBaseModel):
    """Запрос на создание/изменение фильтра доступа."""

    access_filter: AccessFilter


class AccessFiltersResponse(MetrikaBaseModel):
    """Ответ списка фильтров доступа."""

    access_filters: Optional[list[AccessFilter]] = None


class AccessFilterResponse(MetrikaBaseModel):
    """Ответ с одним фильтром доступа."""

    access_filter: Optional[AccessFilter] = None


# ── Log Request ───────────────────────────────────────────────────


class LogRequest(MetrikaBaseModel):
    """Запрос логов (Logs API)."""

    request_id: Optional[int] = None
    counter_id: Optional[int] = None
    source: Optional[str] = None
    date1: Optional[str] = None
    date2: Optional[str] = None
    fields: Optional[list[str]] = None
    status: Optional[str] = None
    size: Optional[int] = None
    attribution: Optional[str] = None
    parts: Optional[list] = None


class LogRequestResponse(MetrikaBaseModel):
    """Ответ с информацией о запросе логов."""

    log_request: Optional[LogRequest] = None


class LogRequestsResponse(MetrikaBaseModel):
    """Ответ списка запросов логов."""

    requests: Optional[list[LogRequest]] = None


class LogRequestEvaluation(MetrikaBaseModel):
    """Оценка возможности запроса логов."""

    possible: Optional[bool] = None
    max_possible_day_quantity: Optional[int] = None


class LogRequestEvaluationResponse(MetrikaBaseModel):
    """Ответ оценки запроса логов."""

    log_request_evaluation: Optional[LogRequestEvaluation] = None


# ── Report Data ───────────────────────────────────────────────────


class ReportQuery(MetrikaBaseModel):
    """Параметры запроса отчёта."""

    ids: Optional[list[int]] = None
    dimensions: Optional[list[str]] = None
    metrics: Optional[list[str]] = None
    sort: Optional[list[str]] = None
    date1: Optional[str] = None
    date2: Optional[str] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    filters: Optional[str] = None
    preset: Optional[str] = None


class StatRow(MetrikaBaseModel):
    """Строка табличного отчёта."""

    dimensions: Optional[list[dict]] = None
    metrics: Optional[list[float]] = None


class ReportResponse(MetrikaBaseModel):
    """Ответ табличного отчёта."""

    query: Optional[ReportQuery] = None
    data: Optional[list[StatRow]] = None
    total_rows: Optional[int] = None
    total_rows_rounded: Optional[bool] = None
    sampled: Optional[bool] = None
    sample_share: Optional[float] = None
    sample_size: Optional[int] = None
    sample_space: Optional[int] = None
    data_lag: Optional[int] = None
    totals: Optional[list[float]] = None
    min: Optional[list[float]] = None
    max: Optional[list[float]] = None


class DrillDownRow(MetrikaBaseModel):
    """Строка drill down отчёта."""

    dimension: Optional[dict] = None
    metrics: Optional[list[float]] = None
    expand: Optional[bool] = None


class DrillDownReportResponse(MetrikaBaseModel):
    """Ответ drill down отчёта."""

    query: Optional[ReportQuery] = None
    data: Optional[list[DrillDownRow]] = None
    total_rows: Optional[int] = None
    totals: Optional[list[float]] = None
    min: Optional[list[float]] = None
    max: Optional[list[float]] = None
    sampled: Optional[bool] = None
    sample_share: Optional[float] = None
    sample_size: Optional[int] = None
    sample_space: Optional[int] = None
    data_lag: Optional[int] = None


class ComparisonRow(MetrikaBaseModel):
    """Строка сравнительного отчёта."""

    dimensions: Optional[list[dict]] = None
    metrics: Optional[dict] = None


class ComparisonReportResponse(MetrikaBaseModel):
    """Ответ сравнительного отчёта."""

    query: Optional[ReportQuery] = None
    data: Optional[list[ComparisonRow]] = None
    total_rows: Optional[int] = None
    totals: Optional[dict] = None
    sampled: Optional[bool] = None
    sample_share: Optional[float] = None
    sample_size: Optional[int] = None
    sample_space: Optional[int] = None
    data_lag: Optional[int] = None


class ByTimeRow(MetrikaBaseModel):
    """Строка отчёта по времени."""

    dimensions: Optional[list[dict]] = None
    metrics: Optional[list[list[float]]] = None


class ByTimeReportResponse(MetrikaBaseModel):
    """Ответ отчёта по времени."""

    query: Optional[ReportQuery] = None
    data: Optional[list[ByTimeRow]] = None
    total_rows: Optional[int] = None
    totals: Optional[list[list[float]]] = None
    sampled: Optional[bool] = None
    sample_share: Optional[float] = None
    sample_size: Optional[int] = None
    sample_space: Optional[int] = None
    data_lag: Optional[int] = None


# ── Upload Responses ──────────────────────────────────────────────


class UploadInfo(MetrikaBaseModel):
    """Информация о загрузке данных."""

    id: Optional[int] = None
    create_time: Optional[str] = None
    source_quantity: Optional[int] = None
    line_quantity: Optional[int] = None
    provider: Optional[str] = None
    comment: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    content_id_type: Optional[str] = None
    action: Optional[str] = None


class UploadResponse(MetrikaBaseModel):
    """Ответ загрузки данных."""

    uploading: Optional[UploadInfo] = None


class UploadListResponse(MetrikaBaseModel):
    """Ответ списка загрузок."""

    uploadings: Optional[list[UploadInfo]] = None


# ── Success Response ──────────────────────────────────────────────


class SuccessResponse(MetrikaBaseModel):
    """Стандартный ответ успешной операции."""

    success: Optional[bool] = None


# ── Exports ───────────────────────────────────────────────────────

__all__ = [
    # Base
    "MetrikaBaseModel",
    # Counter
    "CodeOptions",
    "Site",
    "CounterBrief",
    "CounterFull",
    "CounterRequest",
    "CountersResponse",
    "CounterResponse",
    # Goal
    "GoalCondition",
    "Goal",
    "GoalRequest",
    "GoalsResponse",
    "GoalResponse",
    # Filter
    "FilterE",
    "FilterRequest",
    "FiltersResponse",
    "FilterResponse",
    # Grant
    "Grant",
    "GrantRequest",
    "GrantsResponse",
    "GrantResponse",
    # Operation
    "OperationE",
    "OperationRequest",
    "OperationsResponse",
    "OperationResponse",
    # Segment
    "Segment",
    "SegmentRequest",
    "SegmentsResponse",
    "SegmentResponse",
    # Label
    "Label",
    "LabelRequest",
    "LabelsResponse",
    "LabelResponse",
    # Account
    "Account",
    "AccountsResponse",
    # Delegate
    "Delegate",
    "DelegateRequest",
    "DelegatesResponse",
    # Chart Annotation
    "ChartAnnotation",
    "ChartAnnotationRequest",
    "ChartAnnotationsResponse",
    "ChartAnnotationResponse",
    # Access Filter
    "AccessFilter",
    "AccessFilterRequest",
    "AccessFiltersResponse",
    "AccessFilterResponse",
    # Log Request
    "LogRequest",
    "LogRequestResponse",
    "LogRequestsResponse",
    "LogRequestEvaluation",
    "LogRequestEvaluationResponse",
    # Report
    "ReportQuery",
    "StatRow",
    "ReportResponse",
    "DrillDownRow",
    "DrillDownReportResponse",
    "ComparisonRow",
    "ComparisonReportResponse",
    "ByTimeRow",
    "ByTimeReportResponse",
    # Upload
    "UploadInfo",
    "UploadResponse",
    "UploadListResponse",
    # Common
    "SuccessResponse",
]
