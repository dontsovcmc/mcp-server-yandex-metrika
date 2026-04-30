"""Pydantic-модели для API Яндекс Метрики.

Использование:
    from mcp_server_yandex_metrika.models import Counter, Goal, Segment
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


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


# ── Parameter Models (for action registry) ───────────────────────


class StatDataParams(BaseModel):
    """Parameters for GET /stat/v1/data — table report."""

    model_config = ConfigDict(extra="allow")

    ids: str = Field(
        ...,
        description="Counter IDs, comma-separated (e.g. '12345,67890')",
    )
    metrics: str = Field(
        ...,
        description=(
            "Metrics, comma-separated"
            " (e.g. 'ym:s:visits,ym:s:users,ym:s:pageviews')"
        ),
    )
    dimensions: str = Field(
        default="",
        description="Dimensions, comma-separated (e.g. 'ym:s:browser')",
    )
    date1: str = Field(
        default="",
        description=(
            "Start date: YYYY-MM-DD or relative"
            " ('today','yesterday','6daysAgo')"
        ),
    )
    date2: str = Field(
        default="",
        description="End date: YYYY-MM-DD or relative ('today','yesterday')",
    )
    filters: str = Field(
        default="",
        description="Filter expression (e.g. \"ym:s:browser=='Chrome'\")",
    )
    limit: int = Field(
        default=100,
        ge=1,
        le=100000,
        description="Max rows to return (1-100000)",
    )
    offset: int = Field(
        default=1,
        ge=1,
        description="Offset for pagination (starts from 1)",
    )
    sort: str = Field(
        default="",
        description="Sort field with optional - prefix (e.g. '-ym:s:visits')",
    )
    preset: str = Field(
        default="",
        description="Report preset name",
    )
    accuracy: str = Field(
        default="",
        description="Accuracy: 'low','medium','high','full' or 0.0-1.0",
    )
    lang: str = Field(
        default="",
        description="Language: 'ru', 'en', 'tr'",
    )
    include_undefined: bool = Field(
        default=False,
        description="Include undefined values in report",
    )
    timezone: str = Field(
        default="",
        description="Timezone offset (e.g. '+03:00')",
    )


class StatByTimeParams(BaseModel):
    """Parameters for GET /stat/v1/data/bytime — time-series report."""

    model_config = ConfigDict(extra="allow")

    ids: str = Field(
        ...,
        description="Counter IDs, comma-separated (e.g. '12345,67890')",
    )
    metrics: str = Field(
        ...,
        description=(
            "Metrics, comma-separated"
            " (e.g. 'ym:s:visits,ym:s:users,ym:s:pageviews')"
        ),
    )
    dimensions: str = Field(
        default="",
        description="Dimensions, comma-separated (e.g. 'ym:s:browser')",
    )
    date1: str = Field(
        default="",
        description=(
            "Start date: YYYY-MM-DD or relative"
            " ('today','yesterday','6daysAgo')"
        ),
    )
    date2: str = Field(
        default="",
        description="End date: YYYY-MM-DD or relative ('today','yesterday')",
    )
    filters: str = Field(
        default="",
        description="Filter expression (e.g. \"ym:s:browser=='Chrome'\")",
    )
    limit: int = Field(
        default=100,
        ge=1,
        le=100000,
        description="Max rows to return (1-100000)",
    )
    offset: int = Field(
        default=1,
        ge=1,
        description="Offset for pagination (starts from 1)",
    )
    sort: str = Field(
        default="",
        description="Sort field with optional - prefix (e.g. '-ym:s:visits')",
    )
    lang: str = Field(
        default="",
        description="Language: 'ru', 'en', 'tr'",
    )
    group: str = Field(
        default="day",
        description=(
            "Time grouping:"
            " all/auto/minutes/hour/day/week/month/quarter/year"
        ),
    )
    top_keys: int = Field(
        default=7,
        ge=1,
        le=30,
        description="Number of top keys (1-30)",
    )


class StatDrilldownParams(BaseModel):
    """Parameters for GET /stat/v1/data/drilldown — drill down report."""

    model_config = ConfigDict(extra="allow")

    ids: str = Field(
        ...,
        description="Counter IDs, comma-separated (e.g. '12345,67890')",
    )
    metrics: str = Field(
        ...,
        description=(
            "Metrics, comma-separated"
            " (e.g. 'ym:s:visits,ym:s:users,ym:s:pageviews')"
        ),
    )
    dimensions: str = Field(
        default="",
        description="Dimensions, comma-separated (e.g. 'ym:s:browser')",
    )
    date1: str = Field(
        default="",
        description=(
            "Start date: YYYY-MM-DD or relative"
            " ('today','yesterday','6daysAgo')"
        ),
    )
    date2: str = Field(
        default="",
        description="End date: YYYY-MM-DD or relative ('today','yesterday')",
    )
    filters: str = Field(
        default="",
        description="Filter expression (e.g. \"ym:s:browser=='Chrome'\")",
    )
    limit: int = Field(
        default=100,
        ge=1,
        le=100000,
        description="Max rows to return (1-100000)",
    )
    offset: int = Field(
        default=1,
        ge=1,
        description="Offset for pagination (starts from 1)",
    )
    sort: str = Field(
        default="",
        description="Sort field with optional - prefix (e.g. '-ym:s:visits')",
    )
    lang: str = Field(
        default="",
        description="Language: 'ru', 'en', 'tr'",
    )
    parent_id: str = Field(
        default="",
        description="Parent ID for drill down (JSON array of keys)",
    )


class StatComparisonParams(BaseModel):
    """Parameters for GET /stat/v1/data/comparison — comparison report."""

    model_config = ConfigDict(extra="allow")

    ids: str = Field(
        ...,
        description="Counter IDs, comma-separated (e.g. '12345,67890')",
    )
    metrics: str = Field(
        ...,
        description=(
            "Metrics, comma-separated"
            " (e.g. 'ym:s:visits,ym:s:users,ym:s:pageviews')"
        ),
    )
    dimensions: str = Field(
        default="",
        description="Dimensions, comma-separated (e.g. 'ym:s:browser')",
    )
    date1_a: str = Field(
        default="",
        description="Segment A start date: YYYY-MM-DD or relative",
    )
    date2_a: str = Field(
        default="",
        description="Segment A end date: YYYY-MM-DD or relative",
    )
    date1_b: str = Field(
        default="",
        description="Segment B start date: YYYY-MM-DD or relative",
    )
    date2_b: str = Field(
        default="",
        description="Segment B end date: YYYY-MM-DD or relative",
    )
    filters_a: str = Field(
        default="",
        description="Filter expression for segment A",
    )
    filters_b: str = Field(
        default="",
        description="Filter expression for segment B",
    )
    limit: int = Field(
        default=100,
        ge=1,
        le=100000,
        description="Max rows to return (1-100000)",
    )
    offset: int = Field(
        default=1,
        ge=1,
        description="Offset for pagination (starts from 1)",
    )
    sort: str = Field(
        default="",
        description="Sort field with optional - prefix (e.g. '-ym:s:visits')",
    )
    lang: str = Field(
        default="",
        description="Language: 'ru', 'en', 'tr'",
    )
    parent_id: str = Field(
        default="",
        description=(
            "Parent ID for drill down variant (JSON array of keys)"
        ),
    )


class CounterCreateParams(BaseModel):
    """Parameters for POST /management/v1/counters — create counter."""

    model_config = ConfigDict(extra="allow")

    name: str = Field(
        ...,
        description="Counter name (e.g. 'My Website')",
    )
    site: str = Field(
        ...,
        description="Website domain (e.g. 'example.com')",
    )
    time_zone_name: str = Field(
        default="Europe/Moscow",
        description="Timezone (e.g. 'Europe/Moscow', 'UTC')",
    )


class CounterUpdateParams(BaseModel):
    """Parameters for PUT /management/v1/counter/{id} — update counter."""

    model_config = ConfigDict(extra="allow")

    name: str = Field(
        default="",
        description="New counter name",
    )
    site: str = Field(
        default="",
        description="New website domain (e.g. 'example.com')",
    )
    time_zone_name: str = Field(
        default="",
        description="New timezone (e.g. 'Europe/Moscow', 'UTC')",
    )


class GoalCreateParams(BaseModel):
    """Parameters for POST /management/v1/counter/{id}/goals — create goal."""

    model_config = ConfigDict(extra="allow")

    name: str = Field(
        ...,
        description="Goal name (e.g. 'Purchase completed')",
    )
    goal_type: str = Field(
        ...,
        description=(
            "Type: url/number/step/action/visit_duration/phone/email"
            "/search/messenger/file/social/chat/payment_system"
        ),
    )
    conditions_json: str = Field(
        default="",
        description=(
            "Conditions as JSON array"
            ' (e.g. \'[{"type":"contain","url":"/thank"}]\')'
        ),
    )
    depth: int = Field(
        default=0,
        description="Page depth (for 'number' type, e.g. 3)",
    )
    duration: int = Field(
        default=0,
        description="Visit duration in seconds (for 'visit_duration' type)",
    )
    default_price: float = Field(
        default=0,
        description="Default goal value (e.g. 100.0)",
    )
    is_favorite: bool = Field(
        default=False,
        description="Mark goal as favorite",
    )


class GoalUpdateParams(BaseModel):
    """Parameters for PUT /management/v1/counter/{id}/goal/{gid} — update goal."""

    model_config = ConfigDict(extra="allow")

    name: str = Field(
        default="",
        description="New goal name",
    )
    goal_type: str = Field(
        default="",
        description=(
            "Type: url/number/step/action/visit_duration/phone/email"
            "/search/messenger/file/social/chat/payment_system"
        ),
    )
    conditions_json: str = Field(
        default="",
        description=(
            "Conditions as JSON array"
            ' (e.g. \'[{"type":"contain","url":"/thank"}]\')'
        ),
    )
    depth: int = Field(
        default=0,
        description="Page depth (for 'number' type)",
    )
    duration: int = Field(
        default=0,
        description="Visit duration in seconds (for 'visit_duration' type)",
    )
    default_price: float = Field(
        default=0,
        description="Default goal value",
    )
    is_favorite: bool = Field(
        default=False,
        description="Mark goal as favorite",
    )


class FilterCreateParams(BaseModel):
    """Parameters for POST /management/v1/counter/{id}/filters — create filter."""

    model_config = ConfigDict(extra="allow")

    attr: str = Field(
        ...,
        description=(
            "Attribute: title/client_ip/url/referer/uniq_id"
        ),
    )
    filter_type: str = Field(
        ...,
        description=(
            "Type: equal/start/contain/interval/me/only_mirrors/regexp"
        ),
    )
    value: str = Field(
        default="",
        description="Filter value (e.g. 'bot' for title contain)",
    )
    action: str = Field(
        default="exclude",
        description="Action: exclude/include",
    )
    status: str = Field(
        default="active",
        description="Status: active/disabled",
    )
    start_ip: str = Field(
        default="",
        description="Start IP address (for 'interval' type, e.g. '192.168.1.1')",
    )
    end_ip: str = Field(
        default="",
        description="End IP address (for 'interval' type, e.g. '192.168.1.255')",
    )


class FilterUpdateParams(BaseModel):
    """Parameters for PUT /management/v1/counter/{id}/filter/{fid} — update filter."""

    model_config = ConfigDict(extra="allow")

    attr: str = Field(
        default="",
        description="Attribute: title/client_ip/url/referer/uniq_id",
    )
    filter_type: str = Field(
        default="",
        description=(
            "Type: equal/start/contain/interval/me/only_mirrors/regexp"
        ),
    )
    value: str = Field(
        default="",
        description="Filter value",
    )
    action: str = Field(
        default="",
        description="Action: exclude/include",
    )
    status: str = Field(
        default="",
        description="Status: active/disabled",
    )
    start_ip: str = Field(
        default="",
        description="Start IP address (for 'interval' type)",
    )
    end_ip: str = Field(
        default="",
        description="End IP address (for 'interval' type)",
    )


class GrantCreateParams(BaseModel):
    """Parameters for POST /management/v1/counter/{id}/grants — create grant."""

    model_config = ConfigDict(extra="allow")

    user_login: str = Field(
        ...,
        description="Yandex login to grant access (e.g. 'john.doe')",
    )
    perm: str = Field(
        ...,
        description="Permission: public_stat/view/edit",
    )
    comment: str = Field(
        default="",
        description="Comment for the grant",
    )


class SegmentCreateParams(BaseModel):
    """Parameters for POST /management/v1/counter/{id}/apisegment/segments — create segment."""

    model_config = ConfigDict(extra="allow")

    name: str = Field(
        ...,
        max_length=255,
        description="Segment name (1-255 chars, e.g. 'Chrome Users')",
    )
    expression: str = Field(
        ...,
        max_length=65535,
        description=(
            "Segment expression"
            " (e.g. \"ym:s:browser=='Chrome'\")"
        ),
    )


class SegmentUpdateParams(BaseModel):
    """Parameters for PUT /management/v1/counter/{id}/apisegment/segment/{sid} — update segment."""

    model_config = ConfigDict(extra="allow")

    name: str = Field(
        default="",
        max_length=255,
        description="New segment name (1-255 chars)",
    )
    expression: str = Field(
        default="",
        max_length=65535,
        description="New segment expression",
    )


class OperationCreateParams(BaseModel):
    """Parameters for POST /management/v1/counter/{id}/operations — create operation."""

    model_config = ConfigDict(extra="allow")

    action: str = Field(
        ...,
        description=(
            "Action: cut_fragment/cut_parameter/cut_all_parameters"
            "/merge_https_and_http/to_lower/replace_domain"
        ),
    )
    attr: str = Field(
        ...,
        description="Attribute: referer/url",
    )
    value: str = Field(
        ...,
        description="Value for the operation (e.g. 'utm_source')",
    )


class OperationUpdateParams(BaseModel):
    """Parameters for PUT /management/v1/counter/{id}/operation/{oid} — update operation."""

    model_config = ConfigDict(extra="allow")

    action: str = Field(
        default="",
        description=(
            "Action: cut_fragment/cut_parameter/cut_all_parameters"
            "/merge_https_and_http/to_lower/replace_domain"
        ),
    )
    attr: str = Field(
        default="",
        description="Attribute: referer/url",
    )
    value: str = Field(
        default="",
        description="Value for the operation",
    )
    status: str = Field(
        default="",
        description="Status: active/disabled",
    )


class LabelCreateParams(BaseModel):
    """Parameters for POST /management/v1/labels — create label."""

    model_config = ConfigDict(extra="allow")

    name: str = Field(
        ...,
        max_length=255,
        description="Label name (e.g. 'Production Sites')",
    )


class AnnotationCreateParams(BaseModel):
    """Parameters for POST /management/v1/counter/{id}/chart_annotations — create annotation."""

    model_config = ConfigDict(extra="allow")

    date: str = Field(
        ...,
        description="Date in YYYY-MM-DD format (e.g. '2024-01-15')",
    )
    title: str = Field(
        ...,
        description="Annotation title (e.g. 'New landing page launched')",
    )
    message: str = Field(
        default="",
        description="Annotation message with additional details",
    )
    group: str = Field(
        default="A",
        description="Group: A/B/C/D/E/HOLIDAY",
    )


class AnnotationUpdateParams(BaseModel):
    """Parameters for PUT /management/v1/counter/{id}/chart_annotation/{aid} — update annotation."""

    model_config = ConfigDict(extra="allow")

    date: str = Field(
        default="",
        description="Date in YYYY-MM-DD format",
    )
    title: str = Field(
        default="",
        description="Annotation title",
    )
    message: str = Field(
        default="",
        description="Annotation message",
    )
    group: str = Field(
        default="",
        description="Group: A/B/C/D/E/HOLIDAY",
    )


class AccessFilterCreateParams(BaseModel):
    """Parameters for POST /management/v1/counter/{id}/access/filters — create access filter."""

    model_config = ConfigDict(extra="allow")

    name: str = Field(
        ...,
        description="Filter name (1-255 chars, e.g. 'Only organic traffic')",
    )
    expression: str = Field(
        ...,
        description=(
            "Filter expression (1-65535 chars,"
            " e.g. \"ym:s:trafficSource=='organic'\")"
        ),
    )
    interface_value: str = Field(
        default="",
        description="Interface value",
    )


class AccessFilterUpdateParams(BaseModel):
    """Parameters for PUT /management/v1/counter/{id}/access/filter/{fid} — update access filter."""

    model_config = ConfigDict(extra="allow")

    name: str = Field(
        default="",
        description="Filter name (1-255 chars)",
    )
    expression: str = Field(
        default="",
        description="Filter expression (1-65535 chars)",
    )
    interface_value: str = Field(
        default="",
        description="Interface value",
    )


class LogRequestCreateParams(BaseModel):
    """Parameters for POST /management/v1/counter/{id}/logrequests — create log request."""

    model_config = ConfigDict(extra="allow")

    date1: str = Field(
        ...,
        description="Start date in YYYY-MM-DD format (e.g. '2024-01-01')",
    )
    date2: str = Field(
        ...,
        description="End date in YYYY-MM-DD format (e.g. '2024-01-31')",
    )
    fields: str = Field(
        ...,
        description=(
            "Fields, comma-separated"
            " (e.g. 'ym:s:date,ym:s:visitID,ym:s:watchIDs')"
        ),
    )
    source: str = Field(
        ...,
        description="Data source: 'hits' or 'visits'",
    )
    attribution: str = Field(
        default="LASTSIGN",
        description=(
            "Attribution model:"
            " FIRST/LAST/LASTSIGN/LAST_YANDEX_DIRECT_CLICK"
        ),
    )


class LogRequestEvaluateParams(BaseModel):
    """Parameters for GET /management/v1/counter/{id}/logrequests/evaluate — evaluate log request."""

    model_config = ConfigDict(extra="allow")

    date1: str = Field(
        ...,
        description="Start date in YYYY-MM-DD format (e.g. '2024-01-01')",
    )
    date2: str = Field(
        ...,
        description="End date in YYYY-MM-DD format (e.g. '2024-01-31')",
    )
    fields: str = Field(
        ...,
        description=(
            "Fields, comma-separated"
            " (e.g. 'ym:s:date,ym:s:visitID,ym:s:watchIDs')"
        ),
    )
    source: str = Field(
        ...,
        description="Data source: 'hits' or 'visits'",
    )


class DelegateAddParams(BaseModel):
    """Parameters for POST /management/v1/delegates — add delegate."""

    model_config = ConfigDict(extra="allow")

    user_login: str = Field(
        ...,
        description="Yandex login (e.g. 'john.doe')",
    )
    comment: str = Field(
        default="",
        description="Comment for the delegate",
    )


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
    # Parameter Models
    "StatDataParams",
    "StatByTimeParams",
    "StatDrilldownParams",
    "StatComparisonParams",
    "CounterCreateParams",
    "CounterUpdateParams",
    "GoalCreateParams",
    "GoalUpdateParams",
    "FilterCreateParams",
    "FilterUpdateParams",
    "GrantCreateParams",
    "SegmentCreateParams",
    "SegmentUpdateParams",
    "OperationCreateParams",
    "OperationUpdateParams",
    "LabelCreateParams",
    "AnnotationCreateParams",
    "AnnotationUpdateParams",
    "AccessFilterCreateParams",
    "AccessFilterUpdateParams",
    "LogRequestCreateParams",
    "LogRequestEvaluateParams",
    "DelegateAddParams",
]
