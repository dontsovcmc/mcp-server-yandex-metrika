"""CLI interface for Yandex Metrika tools.

Usage: mcp-server-yandex-metrika <command> [options]
Without arguments starts MCP server (stdio transport).
"""

import argparse
import asyncio
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
    p_stat.add_argument("--ids", required=True)
    p_stat.add_argument("--metrics", required=True)
    p_stat.add_argument("--dimensions", default="")
    p_stat.add_argument("--date1", default="")
    p_stat.add_argument("--date2", default="")
    p_stat.add_argument("--filters", default="")
    p_stat.add_argument("--limit", type=int, default=100)
    p_stat.add_argument("--sort", default="")
    p_stat.add_argument("--preset", default="")

    p_bytime = sub.add_parser("stat-bytime", help="Отчёт по времени")
    p_bytime.add_argument("--ids", required=True)
    p_bytime.add_argument("--metrics", required=True)
    p_bytime.add_argument("--dimensions", default="")
    p_bytime.add_argument("--date1", default="")
    p_bytime.add_argument("--date2", default="")
    p_bytime.add_argument("--group", default="day")
    p_bytime.add_argument("--limit", type=int, default=100)

    # ── Counters ──────────────────────────────────────────────────
    p_counters = sub.add_parser("counters", help="Список счётчиков")
    p_counters.add_argument("--search", default="")
    p_counters.add_argument("--permission", default="")
    p_counters.add_argument("--status", default="")
    p_counters.add_argument("--per-page", type=int, default=100)

    p_counter = sub.add_parser("counter", help="Информация о счётчике")
    p_counter.add_argument("counter_id", type=int)
    p_counter.add_argument("--field", default="")

    # ── Goals ─────────────────────────────────────────────────────
    p_goals = sub.add_parser("goals", help="Список целей")
    p_goals.add_argument("counter_id", type=int)

    # ── Search / Execute ──────────────────────────────────────────
    p_search = sub.add_parser("search", help="Поиск действий")
    p_search.add_argument("query")
    p_search.add_argument("--domain", default="")

    p_exec = sub.add_parser("execute", help="Выполнить действие")
    p_exec.add_argument("action")
    p_exec.add_argument("--params", default="{}")

    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        sys.exit(1)

    handlers = {
        "stat-data": lambda: server.ym_stat_data(
            ids=args.ids, metrics=args.metrics, dimensions=args.dimensions,
            date1=args.date1, date2=args.date2, filters=args.filters,
            limit=args.limit, sort=args.sort, preset=args.preset,
        ),
        "stat-bytime": lambda: server.ym_stat_data_bytime(
            ids=args.ids, metrics=args.metrics, dimensions=args.dimensions,
            date1=args.date1, date2=args.date2, group=args.group,
            limit=args.limit,
        ),
        "counters": lambda: server.ym_counters(
            search_string=args.search, permission=args.permission,
            status=args.status, per_page=args.per_page,
        ),
        "counter": lambda: server.ym_counter(args.counter_id, args.field),
        "goals": lambda: server.ym_goals(args.counter_id),
        "search": lambda: server.ym_search(args.query, args.domain),
        "execute": lambda: server.ym_execute(args.action, args.params),
    }

    handler = handlers[args.command]
    print(asyncio.run(handler()))
