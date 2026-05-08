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

    async_flag: Optional[bool] = Field(None, description="Асинхронная загрузка кода счётчика")
    visor: Optional[bool] = Field(None, description="Включён ли Вебвизор")
    clickmap: Optional[bool] = Field(None, description="Включена ли карта кликов")
    ecommerce: Optional[bool] = Field(None, description="Включена ли электронная коммерция")


class Site(MetrikaBaseModel):
    """Сайт счётчика."""

    site: Optional[str] = Field(None, description="Доменное имя сайта")


class CounterBrief(MetrikaBaseModel):
    """Краткая информация о счётчике (из GET /management/v1/counters)."""

    id: int = Field(..., description="Идентификатор счётчика")
    name: Optional[str] = Field(None, description="Название счётчика")
    site: Optional[str] = Field(None, description="Домен сайта")
    site2: Optional[Site] = Field(None, description="Объект сайта с доп. информацией")
    type: Optional[str] = Field(None, description="Тип счётчика (simple/partner)")
    status: Optional[str] = Field(None, description="Статус счётчика (Active/Deleted)")
    owner_login: Optional[str] = Field(None, description="Логин владельца счётчика")
    permission: Optional[str] = Field(None, description="Уровень доступа (own/view/edit)")
    create_time: Optional[str] = Field(None, description="Дата и время создания")
    code_status: Optional[str] = Field(None, description="Статус установки кода (CS_OK/CS_NOT_FOUND и др.)")
    mirrors2: Optional[list[Site]] = Field(None, description="Список зеркал сайта")
    goals_count: Optional[int] = Field(None, description="Количество целей")
    favorite: Optional[bool] = Field(None, description="Добавлен ли в избранное")


class CounterFull(MetrikaBaseModel):
    """Полная информация о счётчике (из GET /management/v1/counter/{id})."""

    id: Optional[int] = Field(None, description="Идентификатор счётчика")
    name: Optional[str] = Field(None, description="Название счётчика")
    site: Optional[str] = Field(None, description="Домен сайта")
    site2: Optional[Site] = Field(None, description="Объект сайта с доп. информацией")
    type: Optional[str] = Field(None, description="Тип счётчика (simple/partner)")
    status: Optional[str] = Field(None, description="Статус счётчика (Active/Deleted)")
    owner_login: Optional[str] = Field(None, description="Логин владельца счётчика")
    permission: Optional[str] = Field(None, description="Уровень доступа (own/view/edit)")
    create_time: Optional[str] = Field(None, description="Дата и время создания")
    code_status: Optional[str] = Field(None, description="Статус установки кода (CS_OK/CS_NOT_FOUND и др.)")
    code_options: Optional[CodeOptions] = Field(None, description="Настройки кода счётчика")
    mirrors2: Optional[list[Site]] = Field(None, description="Список зеркал сайта")
    time_zone_name: Optional[str] = Field(None, description="Часовой пояс (например Europe/Moscow)")
    time_zone_offset: Optional[int] = Field(None, description="Смещение часового пояса в секундах")
    favorite: Optional[bool] = Field(None, description="Добавлен ли в избранное")
    goals: Optional[list] = Field(None, description="Список целей счётчика")
    filters: Optional[list] = Field(None, description="Список фильтров счётчика")
    operations: Optional[list] = Field(None, description="Список операций счётчика")
    grants: Optional[list] = Field(None, description="Список разрешений на доступ")


class CounterRequest(MetrikaBaseModel):
    """Запрос на создание/изменение счётчика."""

    counter: dict = Field(..., description="Данные счётчика для создания или обновления")


class CountersResponse(MetrikaBaseModel):
    """Ответ списка счётчиков."""

    rows: Optional[int] = Field(None, description="Общее количество счётчиков")
    counters: Optional[list[CounterBrief]] = Field(None, description="Список счётчиков")


class CounterResponse(MetrikaBaseModel):
    """Ответ с одним счётчиком."""

    counter: Optional[CounterFull] = Field(None, description="Данные счётчика")


# ── Goal ──────────────────────────────────────────────────────────


class GoalCondition(MetrikaBaseModel):
    """Условие цели."""

    type: Optional[str] = Field(None, description="Тип условия (contain/exact/regexp и др.)")
    url: Optional[str] = Field(None, description="URL или шаблон для сопоставления")


class Goal(MetrikaBaseModel):
    """Цель счётчика."""

    id: Optional[int] = Field(None, description="Идентификатор цели")
    name: Optional[str] = Field(None, description="Название цели")
    type: Optional[str] = Field(None, description="Тип цели (url/number/step/action и др.)")
    default_price: Optional[float] = Field(None, description="Ценность цели по умолчанию")
    is_favorite: Optional[bool] = Field(None, description="Цель в избранном")
    goal_source: Optional[str] = Field(None, description="Источник создания цели")
    conditions: Optional[list[GoalCondition]] = Field(None, description="Список условий цели")
    depth: Optional[int] = Field(None, description="Глубина просмотра (для типа number)")
    duration: Optional[int] = Field(None, description="Длительность визита в секундах (для типа visit_duration)")
    steps: Optional[list] = Field(None, description="Шаги составной цели (для типа step)")
    flag: Optional[str] = Field(None, description="Флаг цели")
    hide_phone_number: Optional[bool] = Field(None, description="Скрывать ли номер телефона")


class GoalRequest(MetrikaBaseModel):
    """Запрос на создание/изменение цели."""

    goal: Goal = Field(..., description="Данные цели для создания или обновления")


class GoalsResponse(MetrikaBaseModel):
    """Ответ списка целей."""

    goals: Optional[list[Goal]] = Field(None, description="Список целей")


class GoalResponse(MetrikaBaseModel):
    """Ответ с одной целью."""

    goal: Optional[Goal] = Field(None, description="Данные цели")


# ── Filter ────────────────────────────────────────────────────────


class FilterE(MetrikaBaseModel):
    """Фильтр счётчика."""

    id: Optional[int] = Field(None, description="Идентификатор фильтра")
    attr: Optional[str] = Field(None, description="Атрибут фильтрации (title/client_ip/url/referer/uniq_id)")
    type: Optional[str] = Field(None, description="Тип фильтра (equal/start/contain/interval/regexp и др.)")
    value: Optional[str] = Field(None, description="Значение фильтра")
    action: Optional[str] = Field(None, description="Действие (exclude/include)")
    status: Optional[str] = Field(None, description="Статус (active/disabled)")
    start_ip: Optional[str] = Field(None, description="Начальный IP-адрес (для типа interval)")
    end_ip: Optional[str] = Field(None, description="Конечный IP-адрес (для типа interval)")
    with_subdomains: Optional[bool] = Field(None, description="Применять ли к поддоменам")


class FilterRequest(MetrikaBaseModel):
    """Запрос на создание/изменение фильтра."""

    filter: FilterE = Field(..., description="Данные фильтра для создания или обновления")


class FiltersResponse(MetrikaBaseModel):
    """Ответ списка фильтров."""

    filters: Optional[list[FilterE]] = Field(None, description="Список фильтров")


class FilterResponse(MetrikaBaseModel):
    """Ответ с одним фильтром."""

    filter: Optional[FilterE] = Field(None, description="Данные фильтра")


# ── Grant ─────────────────────────────────────────────────────────


class Grant(MetrikaBaseModel):
    """Разрешение на доступ к счётчику."""

    user_login: Optional[str] = Field(None, description="Логин пользователя Яндекса")
    user_uid: Optional[int] = Field(None, description="UID пользователя Яндекса")
    perm: Optional[str] = Field(None, description="Уровень доступа (public_stat/view/edit)")
    created_at: Optional[str] = Field(None, description="Дата создания разрешения")
    comment: Optional[str] = Field(None, description="Комментарий к разрешению")
    partner_data_access: Optional[bool] = Field(None, description="Доступ к партнёрским данным")
    access_filters: Optional[list] = Field(None, description="Фильтры доступа для разрешения")


class GrantRequest(MetrikaBaseModel):
    """Запрос на создание/изменение разрешения."""

    grant: Grant = Field(..., description="Данные разрешения для создания или обновления")


class GrantsResponse(MetrikaBaseModel):
    """Ответ списка разрешений."""

    grants: Optional[list[Grant]] = Field(None, description="Список разрешений")


class GrantResponse(MetrikaBaseModel):
    """Ответ с одним разрешением."""

    grant: Optional[Grant] = Field(None, description="Данные разрешения")


# ── Operation ─────────────────────────────────────────────────────


class OperationE(MetrikaBaseModel):
    """Операция над данными счётчика."""

    id: Optional[int] = Field(None, description="Идентификатор операции")
    action: Optional[str] = Field(None, description="Действие (cut_fragment/cut_parameter/replace_domain и др.)")
    attr: Optional[str] = Field(None, description="Атрибут (referer/url)")
    value: Optional[str] = Field(None, description="Значение операции")
    status: Optional[str] = Field(None, description="Статус (active/disabled)")


class OperationRequest(MetrikaBaseModel):
    """Запрос на создание/изменение операции."""

    operation: OperationE = Field(..., description="Данные операции для создания или обновления")


class OperationsResponse(MetrikaBaseModel):
    """Ответ списка операций."""

    operations: Optional[list[OperationE]] = Field(None, description="Список операций")


class OperationResponse(MetrikaBaseModel):
    """Ответ с одной операцией."""

    operation: Optional[OperationE] = Field(None, description="Данные операции")


# ── Segment ───────────────────────────────────────────────────────


class Segment(MetrikaBaseModel):
    """API-сегмент."""

    segment_id: Optional[int] = Field(None, description="Идентификатор сегмента")
    counter_id: Optional[int] = Field(None, description="Идентификатор счётчика")
    name: Optional[str] = Field(None, description="Название сегмента")
    expression: Optional[str] = Field(None, description="Выражение сегмента")
    status: Optional[str] = Field(None, description="Статус сегмента (active/deleted)")
    segment_source: Optional[str] = Field(None, description="Источник создания сегмента")
    create_time: Optional[str] = Field(None, description="Дата и время создания")


class SegmentRequest(MetrikaBaseModel):
    """Запрос на создание/изменение сегмента."""

    segment: Segment = Field(..., description="Данные сегмента для создания или обновления")


class SegmentsResponse(MetrikaBaseModel):
    """Ответ списка сегментов."""

    segments: Optional[list[Segment]] = Field(None, description="Список сегментов")


class SegmentResponse(MetrikaBaseModel):
    """Ответ с одним сегментом."""

    segment: Optional[Segment] = Field(None, description="Данные сегмента")


# ── Label ─────────────────────────────────────────────────────────


class Label(MetrikaBaseModel):
    """Метка для счётчиков."""

    id: Optional[int] = Field(None, description="Идентификатор метки")
    name: Optional[str] = Field(None, description="Название метки")


class LabelRequest(MetrikaBaseModel):
    """Запрос на создание/изменение метки."""

    label: Label = Field(..., description="Данные метки для создания или обновления")


class LabelsResponse(MetrikaBaseModel):
    """Ответ списка меток."""

    labels: Optional[list[Label]] = Field(None, description="Список меток")


class LabelResponse(MetrikaBaseModel):
    """Ответ с одной меткой."""

    label: Optional[Label] = Field(None, description="Данные метки")


# ── Account ───────────────────────────────────────────────────────


class Account(MetrikaBaseModel):
    """Аккаунт."""

    user_login: Optional[str] = Field(None, description="Логин пользователя Яндекса")
    created_at: Optional[str] = Field(None, description="Дата создания аккаунта")


class AccountsResponse(MetrikaBaseModel):
    """Ответ списка аккаунтов."""

    accounts: Optional[list[Account]] = Field(None, description="Список аккаунтов")


# ── Delegate ──────────────────────────────────────────────────────


class Delegate(MetrikaBaseModel):
    """Представитель."""

    user_login: Optional[str] = Field(None, description="Логин представителя")
    created_at: Optional[str] = Field(None, description="Дата добавления представителя")
    comment: Optional[str] = Field(None, description="Комментарий")


class DelegateRequest(MetrikaBaseModel):
    """Запрос на добавление представителя."""

    delegate: Delegate = Field(..., description="Данные представителя для добавления")


class DelegatesResponse(MetrikaBaseModel):
    """Ответ списка представителей."""

    delegates: Optional[list[Delegate]] = Field(None, description="Список представителей")


# ── Chart Annotation ──────────────────────────────────────────────


class ChartAnnotation(MetrikaBaseModel):
    """Примечание на графике."""

    id: Optional[int] = Field(None, description="Идентификатор примечания")
    date: Optional[str] = Field(None, description="Дата примечания (YYYY-MM-DD)")
    time: Optional[str] = Field(None, description="Время примечания")
    title: Optional[str] = Field(None, description="Заголовок примечания")
    message: Optional[str] = Field(None, description="Текст примечания")
    group: Optional[str] = Field(None, description="Группа (A/B/C/D/E/HOLIDAY)")


class ChartAnnotationRequest(MetrikaBaseModel):
    """Запрос на создание/изменение примечания."""

    chart_annotation: ChartAnnotation = Field(..., description="Данные примечания для создания или обновления")


class ChartAnnotationsResponse(MetrikaBaseModel):
    """Ответ списка примечаний."""

    chart_annotations: Optional[list[ChartAnnotation]] = Field(None, description="Список примечаний")


class ChartAnnotationResponse(MetrikaBaseModel):
    """Ответ с одним примечанием."""

    chart_annotation: Optional[ChartAnnotation] = Field(None, description="Данные примечания")


# ── Access Filter ─────────────────────────────────────────────────


class AccessFilter(MetrikaBaseModel):
    """Фильтр доступа."""

    id: Optional[int] = Field(None, description="Идентификатор фильтра доступа")
    name: Optional[str] = Field(None, description="Название фильтра доступа")
    expression: Optional[str] = Field(None, description="Выражение фильтра доступа")
    interface_value: Optional[str] = Field(None, description="Значение для интерфейса")


class AccessFilterRequest(MetrikaBaseModel):
    """Запрос на создание/изменение фильтра доступа."""

    access_filter: AccessFilter = Field(..., description="Данные фильтра доступа для создания или обновления")


class AccessFiltersResponse(MetrikaBaseModel):
    """Ответ списка фильтров доступа."""

    access_filters: Optional[list[AccessFilter]] = Field(None, description="Список фильтров доступа")


class AccessFilterResponse(MetrikaBaseModel):
    """Ответ с одним фильтром доступа."""

    access_filter: Optional[AccessFilter] = Field(None, description="Данные фильтра доступа")


# ── Log Request ───────────────────────────────────────────────────


class LogRequest(MetrikaBaseModel):
    """Запрос логов (Logs API)."""

    request_id: Optional[int] = Field(None, description="Идентификатор запроса логов")
    counter_id: Optional[int] = Field(None, description="Идентификатор счётчика")
    source: Optional[str] = Field(None, description="Источник данных (hits/visits)")
    date1: Optional[str] = Field(None, description="Начальная дата (YYYY-MM-DD)")
    date2: Optional[str] = Field(None, description="Конечная дата (YYYY-MM-DD)")
    fields: Optional[list[str]] = Field(None, description="Список запрошенных полей")
    status: Optional[str] = Field(None, description="Статус запроса (created/processed/cleaned_by_user и др.)")
    size: Optional[int] = Field(None, description="Размер данных в байтах")
    attribution: Optional[str] = Field(None, description="Модель атрибуции (FIRST/LAST/LASTSIGN и др.)")
    parts: Optional[list] = Field(None, description="Список частей для скачивания")


class LogRequestResponse(MetrikaBaseModel):
    """Ответ с информацией о запросе логов."""

    log_request: Optional[LogRequest] = Field(None, description="Данные запроса логов")


class LogRequestsResponse(MetrikaBaseModel):
    """Ответ списка запросов логов."""

    requests: Optional[list[LogRequest]] = Field(None, description="Список запросов логов")


class LogRequestEvaluation(MetrikaBaseModel):
    """Оценка возможности запроса логов."""

    possible: Optional[bool] = Field(None, description="Возможен ли запрос логов")
    max_possible_day_quantity: Optional[int] = Field(None, description="Максимальное количество дней для запроса")


class LogRequestEvaluationResponse(MetrikaBaseModel):
    """Ответ оценки запроса логов."""

    log_request_evaluation: Optional[LogRequestEvaluation] = Field(None, description="Результат оценки запроса логов")


# ── Report Data ───────────────────────────────────────────────────


class ReportQuery(MetrikaBaseModel):
    """Параметры запроса отчёта."""

    ids: Optional[list[int]] = Field(None, description="Идентификаторы счётчиков")
    dimensions: Optional[list[str]] = Field(None, description="Список измерений")
    metrics: Optional[list[str]] = Field(None, description="Список метрик")
    sort: Optional[list[str]] = Field(None, description="Список полей сортировки")
    date1: Optional[str] = Field(None, description="Начальная дата")
    date2: Optional[str] = Field(None, description="Конечная дата")
    limit: Optional[int] = Field(None, description="Максимальное количество строк")
    offset: Optional[int] = Field(None, description="Смещение для пагинации")
    filters: Optional[str] = Field(None, description="Выражение фильтра")
    preset: Optional[str] = Field(None, description="Название пресета отчёта")


class StatRow(MetrikaBaseModel):
    """Строка табличного отчёта."""

    dimensions: Optional[list[dict]] = Field(None, description="Значения измерений строки")
    metrics: Optional[list[float]] = Field(None, description="Значения метрик строки")


class ReportResponse(MetrikaBaseModel):
    """Ответ табличного отчёта."""

    query: Optional[ReportQuery] = Field(None, description="Параметры выполненного запроса")
    data: Optional[list[StatRow]] = Field(None, description="Строки данных отчёта")
    total_rows: Optional[int] = Field(None, description="Общее количество строк")
    total_rows_rounded: Optional[bool] = Field(None, description="Округлено ли количество строк")
    sampled: Optional[bool] = Field(None, description="Использовалась ли выборка")
    sample_share: Optional[float] = Field(None, description="Доля выборки (0.0-1.0)")
    sample_size: Optional[int] = Field(None, description="Размер выборки")
    sample_space: Optional[int] = Field(None, description="Общий объём данных")
    data_lag: Optional[int] = Field(None, description="Задержка данных в секундах")
    totals: Optional[list[float]] = Field(None, description="Итоговые значения метрик")
    min: Optional[list[float]] = Field(None, description="Минимальные значения метрик")
    max: Optional[list[float]] = Field(None, description="Максимальные значения метрик")


class DrillDownRow(MetrikaBaseModel):
    """Строка drill down отчёта."""

    dimension: Optional[dict] = Field(None, description="Значение измерения строки")
    metrics: Optional[list[float]] = Field(None, description="Значения метрик строки")
    expand: Optional[bool] = Field(None, description="Можно ли раскрыть строку глубже")


class DrillDownReportResponse(MetrikaBaseModel):
    """Ответ drill down отчёта."""

    query: Optional[ReportQuery] = Field(None, description="Параметры выполненного запроса")
    data: Optional[list[DrillDownRow]] = Field(None, description="Строки данных отчёта")
    total_rows: Optional[int] = Field(None, description="Общее количество строк")
    totals: Optional[list[float]] = Field(None, description="Итоговые значения метрик")
    min: Optional[list[float]] = Field(None, description="Минимальные значения метрик")
    max: Optional[list[float]] = Field(None, description="Максимальные значения метрик")
    sampled: Optional[bool] = Field(None, description="Использовалась ли выборка")
    sample_share: Optional[float] = Field(None, description="Доля выборки (0.0-1.0)")
    sample_size: Optional[int] = Field(None, description="Размер выборки")
    sample_space: Optional[int] = Field(None, description="Общий объём данных")
    data_lag: Optional[int] = Field(None, description="Задержка данных в секундах")


class ComparisonRow(MetrikaBaseModel):
    """Строка сравнительного отчёта."""

    dimensions: Optional[list[dict]] = Field(None, description="Значения измерений строки")
    metrics: Optional[dict] = Field(None, description="Значения метрик по сегментам (a/b)")


class ComparisonReportResponse(MetrikaBaseModel):
    """Ответ сравнительного отчёта."""

    query: Optional[ReportQuery] = Field(None, description="Параметры выполненного запроса")
    data: Optional[list[ComparisonRow]] = Field(None, description="Строки данных отчёта")
    total_rows: Optional[int] = Field(None, description="Общее количество строк")
    totals: Optional[dict] = Field(None, description="Итоговые значения метрик по сегментам")
    sampled: Optional[bool] = Field(None, description="Использовалась ли выборка")
    sample_share: Optional[float] = Field(None, description="Доля выборки (0.0-1.0)")
    sample_size: Optional[int] = Field(None, description="Размер выборки")
    sample_space: Optional[int] = Field(None, description="Общий объём данных")
    data_lag: Optional[int] = Field(None, description="Задержка данных в секундах")


class ByTimeRow(MetrikaBaseModel):
    """Строка отчёта по времени."""

    dimensions: Optional[list[dict]] = Field(None, description="Значения измерений строки")
    metrics: Optional[list[list[float]]] = Field(None, description="Временные ряды значений метрик")


class ByTimeReportResponse(MetrikaBaseModel):
    """Ответ отчёта по времени."""

    query: Optional[ReportQuery] = Field(None, description="Параметры выполненного запроса")
    data: Optional[list[ByTimeRow]] = Field(None, description="Строки данных отчёта")
    total_rows: Optional[int] = Field(None, description="Общее количество строк")
    totals: Optional[list[list[float]]] = Field(None, description="Итоговые временные ряды метрик")
    sampled: Optional[bool] = Field(None, description="Использовалась ли выборка")
    sample_share: Optional[float] = Field(None, description="Доля выборки (0.0-1.0)")
    sample_size: Optional[int] = Field(None, description="Размер выборки")
    sample_space: Optional[int] = Field(None, description="Общий объём данных")
    data_lag: Optional[int] = Field(None, description="Задержка данных в секундах")


# ── Upload Responses ──────────────────────────────────────────────


class UploadInfo(MetrikaBaseModel):
    """Информация о загрузке данных."""

    id: Optional[int] = Field(None, description="Идентификатор загрузки")
    create_time: Optional[str] = Field(None, description="Дата и время создания загрузки")
    source_quantity: Optional[int] = Field(None, description="Количество записей в источнике")
    line_quantity: Optional[int] = Field(None, description="Количество обработанных строк")
    provider: Optional[str] = Field(None, description="Провайдер данных")
    comment: Optional[str] = Field(None, description="Комментарий к загрузке")
    type: Optional[str] = Field(None, description="Тип загрузки")
    status: Optional[str] = Field(None, description="Статус загрузки")
    content_id_type: Optional[str] = Field(None, description="Тип идентификатора контента")
    action: Optional[str] = Field(None, description="Действие загрузки")


class UploadResponse(MetrikaBaseModel):
    """Ответ загрузки данных."""

    uploading: Optional[UploadInfo] = Field(None, description="Данные загрузки")


class UploadListResponse(MetrikaBaseModel):
    """Ответ списка загрузок."""

    uploadings: Optional[list[UploadInfo]] = Field(None, description="Список загрузок")


# ── Success Response ──────────────────────────────────────────────


class SuccessResponse(MetrikaBaseModel):
    """Стандартный ответ успешной операции."""

    success: Optional[bool] = Field(None, description="Признак успешного выполнения операции")


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
