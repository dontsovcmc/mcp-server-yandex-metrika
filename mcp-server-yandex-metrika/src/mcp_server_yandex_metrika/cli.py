"""CLI interface for Yandex Metrika tools.

Usage: mcp-server-yandex-metrika <command> [options]
Without arguments starts MCP server (stdio transport).
"""

import argparse
import sys

from . import __version__
from . import server


def main(argv: list[str] | None = None):
    parser = argparse.ArgumentParser(
        prog="mcp-server-yandex-metrika",
        description="Яндекс Метрика: MCP-сервер и CLI",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    sub = parser.add_subparsers(dest="command")

    # ── Reporting ─────────────────────────────────────────────────

    p_stat = sub.add_parser("stat-data", help="Табличный отчёт")
    p_stat.add_argument("--ids", required=True, help="ID счётчиков через запятую")
    p_stat.add_argument("--metrics", required=True, help="Метрики через запятую")
    p_stat.add_argument("--dimensions", default="", help="Измерения через запятую")
    p_stat.add_argument("--date1", default="", help="Дата начала")
    p_stat.add_argument("--date2", default="", help="Дата конца")
    p_stat.add_argument("--filters", default="", help="Фильтр")
    p_stat.add_argument("--limit", type=int, default=100, help="Лимит строк")
    p_stat.add_argument("--sort", default="", help="Сортировка")
    p_stat.add_argument("--preset", default="", help="Пресет отчёта")

    p_bytime = sub.add_parser("stat-bytime", help="Отчёт по времени")
    p_bytime.add_argument("--ids", required=True, help="ID счётчиков")
    p_bytime.add_argument("--metrics", required=True, help="Метрики")
    p_bytime.add_argument("--dimensions", default="", help="Измерения")
    p_bytime.add_argument("--date1", default="", help="Дата начала")
    p_bytime.add_argument("--date2", default="", help="Дата конца")
    p_bytime.add_argument("--group", default="day", help="Группировка: day/week/month/hour")
    p_bytime.add_argument("--limit", type=int, default=100, help="Лимит")
    p_bytime.add_argument("--sort", default="", help="Сортировка")

    p_drill = sub.add_parser("stat-drilldown", help="Drill down отчёт")
    p_drill.add_argument("--ids", required=True, help="ID счётчиков")
    p_drill.add_argument("--metrics", required=True, help="Метрики")
    p_drill.add_argument("--dimensions", default="", help="Измерения")
    p_drill.add_argument("--date1", default="", help="Дата начала")
    p_drill.add_argument("--date2", default="", help="Дата конца")
    p_drill.add_argument("--parent-id", default="", help="Parent ID")
    p_drill.add_argument("--limit", type=int, default=100, help="Лимит")

    p_comp = sub.add_parser("stat-comparison", help="Сравнение сегментов")
    p_comp.add_argument("--ids", required=True, help="ID счётчиков")
    p_comp.add_argument("--metrics", required=True, help="Метрики")
    p_comp.add_argument("--dimensions", default="", help="Измерения")
    p_comp.add_argument("--date1-a", default="", help="Дата начала A")
    p_comp.add_argument("--date2-a", default="", help="Дата конца A")
    p_comp.add_argument("--date1-b", default="", help="Дата начала B")
    p_comp.add_argument("--date2-b", default="", help="Дата конца B")
    p_comp.add_argument("--limit", type=int, default=100, help="Лимит")

    # ── Counters ──────────────────────────────────────────────────

    p_counters = sub.add_parser("counters", help="Список счётчиков")
    p_counters.add_argument("--search", default="", help="Поиск по названию")
    p_counters.add_argument("--permission", default="", help="Фильтр: own/view/edit")
    p_counters.add_argument("--status", default="", help="Фильтр: Active/Deleted")
    p_counters.add_argument("--per-page", type=int, default=100, help="На страницу")

    p_counter = sub.add_parser("counter", help="Информация о счётчике")
    p_counter.add_argument("counter_id", type=int, help="ID счётчика")
    p_counter.add_argument("--field", default="", help="Доп. поля")

    p_ccreate = sub.add_parser("counter-create", help="Создать счётчик")
    p_ccreate.add_argument("--name", required=True, help="Название")
    p_ccreate.add_argument("--site", required=True, help="Домен сайта")
    p_ccreate.add_argument("--timezone", default="Europe/Moscow", help="Часовой пояс")

    p_cupdate = sub.add_parser("counter-update", help="Изменить счётчик")
    p_cupdate.add_argument("counter_id", type=int, help="ID счётчика")
    p_cupdate.add_argument("--name", default="", help="Новое название")
    p_cupdate.add_argument("--site", default="", help="Новый домен")

    p_cdelete = sub.add_parser("counter-delete", help="Удалить счётчик")
    p_cdelete.add_argument("counter_id", type=int, help="ID счётчика")

    p_cundelete = sub.add_parser("counter-undelete", help="Восстановить счётчик")
    p_cundelete.add_argument("counter_id", type=int, help="ID счётчика")

    # ── Goals ─────────────────────────────────────────────────────

    p_goals = sub.add_parser("goals", help="Список целей")
    p_goals.add_argument("counter_id", type=int, help="ID счётчика")

    p_goal = sub.add_parser("goal", help="Информация о цели")
    p_goal.add_argument("counter_id", type=int, help="ID счётчика")
    p_goal.add_argument("goal_id", type=int, help="ID цели")

    p_gcreate = sub.add_parser("goal-create", help="Создать цель")
    p_gcreate.add_argument("counter_id", type=int, help="ID счётчика")
    p_gcreate.add_argument("--name", required=True, help="Название цели")
    p_gcreate.add_argument("--type", required=True, dest="goal_type", help="Тип цели")
    p_gcreate.add_argument("--conditions", default="", help="Условия (JSON)")

    p_gdelete = sub.add_parser("goal-delete", help="Удалить цель")
    p_gdelete.add_argument("counter_id", type=int, help="ID счётчика")
    p_gdelete.add_argument("goal_id", type=int, help="ID цели")

    # ── Filters ───────────────────────────────────────────────────

    p_filters = sub.add_parser("filters", help="Список фильтров")
    p_filters.add_argument("counter_id", type=int, help="ID счётчика")

    p_fcreate = sub.add_parser("filter-create", help="Создать фильтр")
    p_fcreate.add_argument("counter_id", type=int, help="ID счётчика")
    p_fcreate.add_argument("--attr", required=True, help="Атрибут")
    p_fcreate.add_argument("--type", required=True, dest="filter_type", help="Тип")
    p_fcreate.add_argument("--value", default="", help="Значение")
    p_fcreate.add_argument("--action", default="exclude", help="Действие")

    p_fdelete = sub.add_parser("filter-delete", help="Удалить фильтр")
    p_fdelete.add_argument("counter_id", type=int, help="ID счётчика")
    p_fdelete.add_argument("filter_id", type=int, help="ID фильтра")

    # ── Grants ────────────────────────────────────────────────────

    p_grants = sub.add_parser("grants", help="Список разрешений")
    p_grants.add_argument("counter_id", type=int, help="ID счётчика")

    p_grcreate = sub.add_parser("grant-create", help="Выдать разрешение")
    p_grcreate.add_argument("counter_id", type=int, help="ID счётчика")
    p_grcreate.add_argument("--login", required=True, help="Логин Яндекс")
    p_grcreate.add_argument("--perm", required=True, help="Разрешение: view/edit")

    p_grdelete = sub.add_parser("grant-delete", help="Удалить разрешение")
    p_grdelete.add_argument("counter_id", type=int, help="ID счётчика")
    p_grdelete.add_argument("--login", required=True, help="Логин Яндекс")

    # ── Segments ──────────────────────────────────────────────────

    p_segments = sub.add_parser("segments", help="Список сегментов")
    p_segments.add_argument("counter_id", type=int, help="ID счётчика")

    p_segcreate = sub.add_parser("segment-create", help="Создать сегмент")
    p_segcreate.add_argument("counter_id", type=int, help="ID счётчика")
    p_segcreate.add_argument("--name", required=True, help="Название")
    p_segcreate.add_argument("--expression", required=True, help="Выражение")

    p_segdelete = sub.add_parser("segment-delete", help="Удалить сегмент")
    p_segdelete.add_argument("counter_id", type=int, help="ID счётчика")
    p_segdelete.add_argument("segment_id", type=int, help="ID сегмента")

    # ── Labels ────────────────────────────────────────────────────

    sub.add_parser("labels", help="Список меток")

    p_lcreate = sub.add_parser("label-create", help="Создать метку")
    p_lcreate.add_argument("--name", required=True, help="Название метки")

    p_ldelete = sub.add_parser("label-delete", help="Удалить метку")
    p_ldelete.add_argument("label_id", type=int, help="ID метки")

    # ── Operations ────────────────────────────────────────────────

    p_operations = sub.add_parser("operations", help="Список операций")
    p_operations.add_argument("counter_id", type=int, help="ID счётчика")

    p_opcreate = sub.add_parser("operation-create", help="Создать операцию")
    p_opcreate.add_argument("counter_id", type=int, help="ID счётчика")
    p_opcreate.add_argument("--action", required=True, help="Действие")
    p_opcreate.add_argument("--attr", required=True, help="Атрибут: referer/url")
    p_opcreate.add_argument("--value", required=True, help="Значение")

    p_opdelete = sub.add_parser("operation-delete", help="Удалить операцию")
    p_opdelete.add_argument("counter_id", type=int, help="ID счётчика")
    p_opdelete.add_argument("operation_id", type=int, help="ID операции")

    # ── Accounts ──────────────────────────────────────────────────

    sub.add_parser("accounts", help="Список аккаунтов")

    # ── Delegates ─────────────────────────────────────────────────

    sub.add_parser("delegates", help="Список представителей")

    p_dadd = sub.add_parser("delegate-add", help="Добавить представителя")
    p_dadd.add_argument("--login", required=True, help="Логин Яндекс")

    p_ddel = sub.add_parser("delegate-delete", help="Удалить представителя")
    p_ddel.add_argument("--login", required=True, help="Логин Яндекс")

    # ── Chart Annotations ─────────────────────────────────────────

    p_anns = sub.add_parser("chart-annotations", help="Примечания на графике")
    p_anns.add_argument("counter_id", type=int, help="ID счётчика")

    p_anncreate = sub.add_parser("chart-annotation-create", help="Создать примечание")
    p_anncreate.add_argument("counter_id", type=int, help="ID счётчика")
    p_anncreate.add_argument("--date", required=True, help="Дата (YYYY-MM-DD)")
    p_anncreate.add_argument("--title", required=True, help="Заголовок")
    p_anncreate.add_argument("--message", default="", help="Текст")
    p_anncreate.add_argument("--group", default="A", help="Группа: A/B/C/D/E/HOLIDAY")

    # ── Logs API ──────────────────────────────────────────────────

    p_logrequests = sub.add_parser("log-requests", help="Список запросов логов")
    p_logrequests.add_argument("counter_id", type=int, help="ID счётчика")

    p_logcreate = sub.add_parser("log-request-create", help="Создать запрос логов")
    p_logcreate.add_argument("counter_id", type=int, help="ID счётчика")
    p_logcreate.add_argument("--date1", required=True, help="Дата начала")
    p_logcreate.add_argument("--date2", required=True, help="Дата конца")
    p_logcreate.add_argument("--fields", required=True, help="Поля через запятую")
    p_logcreate.add_argument("--source", required=True, help="hits или visits")
    p_logcreate.add_argument("--attribution", default="LASTSIGN", help="Атрибуция")

    p_logeval = sub.add_parser("log-request-evaluate", help="Оценить запрос логов")
    p_logeval.add_argument("counter_id", type=int, help="ID счётчика")
    p_logeval.add_argument("--date1", required=True, help="Дата начала")
    p_logeval.add_argument("--date2", required=True, help="Дата конца")
    p_logeval.add_argument("--fields", required=True, help="Поля через запятую")
    p_logeval.add_argument("--source", required=True, help="hits или visits")

    p_logdownload = sub.add_parser("log-download", help="Скачать часть лога")
    p_logdownload.add_argument("counter_id", type=int, help="ID счётчика")
    p_logdownload.add_argument("request_id", type=int, help="ID запроса")
    p_logdownload.add_argument("part_number", type=int, help="Номер части")
    p_logdownload.add_argument("--output", required=True, help="Путь к файлу")

    # ── Upload ────────────────────────────────────────────────────

    p_upload_conv = sub.add_parser("upload-conversions", help="Загрузить конверсии")
    p_upload_conv.add_argument("counter_id", type=int, help="ID счётчика")
    p_upload_conv.add_argument("--file", required=True, help="Путь к CSV")

    p_upload_calls = sub.add_parser("upload-calls", help="Загрузить звонки")
    p_upload_calls.add_argument("counter_id", type=int, help="ID счётчика")
    p_upload_calls.add_argument("--file", required=True, help="Путь к CSV")

    p_upload_exp = sub.add_parser("upload-expenses", help="Загрузить расходы")
    p_upload_exp.add_argument("counter_id", type=int, help="ID счётчика")
    p_upload_exp.add_argument("--file", required=True, help="Путь к CSV")
    p_upload_exp.add_argument("--comment", default="", help="Комментарий")
    p_upload_exp.add_argument("--provider", default="", help="Провайдер")

    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        sys.exit(1)

    handlers = {
        # Reporting
        "stat-data": lambda: server.ym_stat_data(
            ids=args.ids, metrics=args.metrics, dimensions=args.dimensions,
            date1=args.date1, date2=args.date2, filters=args.filters,
            limit=args.limit, sort=args.sort, preset=args.preset,
        ),
        "stat-bytime": lambda: server.ym_stat_data_bytime(
            ids=args.ids, metrics=args.metrics, dimensions=args.dimensions,
            date1=args.date1, date2=args.date2, group=args.group,
            limit=args.limit, sort=args.sort,
        ),
        "stat-drilldown": lambda: server.ym_stat_data_drilldown(
            ids=args.ids, metrics=args.metrics, dimensions=args.dimensions,
            date1=args.date1, date2=args.date2, parent_id=args.parent_id,
            limit=args.limit,
        ),
        "stat-comparison": lambda: server.ym_stat_data_comparison(
            ids=args.ids, metrics=args.metrics, dimensions=args.dimensions,
            date1_a=args.date1_a, date2_a=args.date2_a,
            date1_b=args.date1_b, date2_b=args.date2_b,
            limit=args.limit,
        ),
        # Counters
        "counters": lambda: server.ym_counters(
            search_string=args.search, permission=args.permission,
            status=args.status, per_page=args.per_page,
        ),
        "counter": lambda: server.ym_counter(args.counter_id, args.field),
        "counter-create": lambda: server.ym_counter_create(args.name, args.site, args.timezone),
        "counter-update": lambda: server.ym_counter_update(args.counter_id, args.name, args.site),
        "counter-delete": lambda: server.ym_counter_delete(args.counter_id),
        "counter-undelete": lambda: server.ym_counter_undelete(args.counter_id),
        # Goals
        "goals": lambda: server.ym_goals(args.counter_id),
        "goal": lambda: server.ym_goal(args.counter_id, args.goal_id),
        "goal-create": lambda: server.ym_goal_create(args.counter_id, args.name, args.goal_type, args.conditions),
        "goal-delete": lambda: server.ym_goal_delete(args.counter_id, args.goal_id),
        # Filters
        "filters": lambda: server.ym_filters(args.counter_id),
        "filter-create": lambda: server.ym_filter_create(
            args.counter_id, args.attr, args.filter_type, args.value, args.action,
        ),
        "filter-delete": lambda: server.ym_filter_delete(args.counter_id, args.filter_id),
        # Grants
        "grants": lambda: server.ym_grants(args.counter_id),
        "grant-create": lambda: server.ym_grant_create(args.counter_id, args.login, args.perm),
        "grant-delete": lambda: server.ym_grant_delete(args.counter_id, args.login),
        # Segments
        "segments": lambda: server.ym_segments(args.counter_id),
        "segment-create": lambda: server.ym_segment_create(args.counter_id, args.name, args.expression),
        "segment-delete": lambda: server.ym_segment_delete(args.counter_id, args.segment_id),
        # Labels
        "labels": lambda: server.ym_labels(),
        "label-create": lambda: server.ym_label_create(args.name),
        "label-delete": lambda: server.ym_label_delete(args.label_id),
        # Operations
        "operations": lambda: server.ym_operations(args.counter_id),
        "operation-create": lambda: server.ym_operation_create(args.counter_id, args.action, args.attr, args.value),
        "operation-delete": lambda: server.ym_operation_delete(args.counter_id, args.operation_id),
        # Accounts
        "accounts": lambda: server.ym_accounts(),
        # Delegates
        "delegates": lambda: server.ym_delegates(),
        "delegate-add": lambda: server.ym_delegate_add(args.login),
        "delegate-delete": lambda: server.ym_delegate_delete(args.login),
        # Chart annotations
        "chart-annotations": lambda: server.ym_chart_annotations(args.counter_id),
        "chart-annotation-create": lambda: server.ym_chart_annotation_create(
            args.counter_id, args.date, args.title, args.message, args.group,
        ),
        # Logs API
        "log-requests": lambda: server.ym_log_requests(args.counter_id),
        "log-request-create": lambda: server.ym_log_request_create(
            args.counter_id, args.date1, args.date2, args.fields, args.source, args.attribution,
        ),
        "log-request-evaluate": lambda: server.ym_log_request_evaluate(
            args.counter_id, args.date1, args.date2, args.fields, args.source,
        ),
        "log-download": lambda: server.ym_log_request_download(
            args.counter_id, args.request_id, args.part_number, args.output,
        ),
        # Upload
        "upload-conversions": lambda: server.ym_offline_conversions_upload(args.counter_id, args.file),
        "upload-calls": lambda: server.ym_calls_upload(args.counter_id, args.file),
        "upload-expenses": lambda: server.ym_expenses_upload(
            args.counter_id, args.file, args.comment, args.provider,
        ),
    }

    handler = handlers[args.command]
    print(handler())
