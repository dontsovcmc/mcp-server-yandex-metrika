<!-- mcp-name: io.github.dontsovcmc/yandex-metrika -->

# mcp-server-yandex-metrika

[![Version](https://img.shields.io/badge/version-0.2.3-blue)](https://github.com/dontsovcmc/mcp-server-yandex-metrika)

MCP-сервер, CLI-утилита и библиотека Pydantic-моделей для [API Яндекс Метрики](https://yandex.com/dev/metrika).

- **MCP-сервер** — интеграция с Claude Code, Claude Desktop и другими MCP-клиентами
- **CLI-утилита** — работа с API из терминала, скрипты и автоматизация
- **Pydantic-модели** — типизированные модели API для использования в своих Python-программах

Все данные остаются на вашем компьютере — токен никуда не передаётся.

## Оглавление

- [Возможности](#возможности)
- [MCP-сервер](#mcp-сервер)
  - [Установка](#установка)
  - [Подключение к Claude Code](#подключение-к-claude-code)
  - [Подключение к Claude Desktop](#подключение-к-claude-desktop)
  - [Подключение через --mcp-config](#подключение-через---mcp-config)
  - [Примеры](#примеры-mcp)
- [CLI-утилита](#cli-утилита)
  - [Установка](#установка-cli)
  - [Использование](#использование-cli)
  - [Примеры команд](#примеры-команд)
- [Pydantic-модели](#pydantic-модели)
  - [Установка](#установка-библиотеки)
  - [Использование в своих программах](#использование-в-своих-программах)
- [Переменные окружения](#переменные-окружения)
- [Лимиты API](#лимиты-api)
- [Разработка](#разработка)
- [Лицензия](#лицензия)

## Возможности

### Отчёты (Reporting API)
| Инструмент | CLI | Описание |
|------------|-----|----------|
| `ym_stat_data` | `stat-data` | Табличный отчёт по метрикам и измерениям |
| `ym_stat_data_bytime` | `stat-bytime` | Отчёт по времени (группировка: час/день/неделя/месяц) |
| `ym_stat_data_drilldown` | `stat-drilldown` | Drill down отчёт с раскрытием уровней |
| `ym_stat_data_comparison` | `stat-comparison` | Сравнение сегментов/периодов |
| `ym_stat_data_comparison_drilldown` | — | Сравнение с drill down |

### Счётчики
| Инструмент | CLI | Описание |
|------------|-----|----------|
| `ym_counters` | `counters` | Список счётчиков (поиск, фильтрация) |
| `ym_counter` | `counter` | Информация о счётчике |
| `ym_counter_create` | `counter-create` | Создать счётчик |
| `ym_counter_update` | `counter-update` | Изменить счётчик |
| `ym_counter_delete` | `counter-delete` | Удалить счётчик |
| `ym_counter_undelete` | `counter-undelete` | Восстановить удалённый |

### Цели
| Инструмент | CLI | Описание |
|------------|-----|----------|
| `ym_goals` | `goals` | Список целей счётчика |
| `ym_goal` | `goal` | Информация о цели |
| `ym_goal_create` | `goal-create` | Создать цель (url/number/step/action/...) |
| `ym_goal_update` | — | Изменить цель |
| `ym_goal_delete` | `goal-delete` | Удалить цель |

### Фильтры
| Инструмент | CLI | Описание |
|------------|-----|----------|
| `ym_filters` | `filters` | Список фильтров |
| `ym_filter` | — | Информация о фильтре |
| `ym_filter_create` | `filter-create` | Создать фильтр (IP, URL, реферер) |
| `ym_filter_update` | — | Изменить фильтр |
| `ym_filter_delete` | `filter-delete` | Удалить фильтр |

### Доступ (Grants)
| Инструмент | CLI | Описание |
|------------|-----|----------|
| `ym_grants` | `grants` | Список разрешений |
| `ym_grant_create` | `grant-create` | Выдать разрешение |
| `ym_grant_update` | — | Изменить разрешение |
| `ym_grant_delete` | `grant-delete` | Удалить разрешение |

### Операции
| Инструмент | CLI | Описание |
|------------|-----|----------|
| `ym_operations` | `operations` | Список операций |
| `ym_operation` | — | Информация об операции |
| `ym_operation_create` | `operation-create` | Создать операцию (cut_parameter, to_lower, ...) |
| `ym_operation_update` | — | Изменить операцию |
| `ym_operation_delete` | `operation-delete` | Удалить операцию |

### Сегменты
| Инструмент | CLI | Описание |
|------------|-----|----------|
| `ym_segments` | `segments` | Список сегментов |
| `ym_segment` | — | Информация о сегменте |
| `ym_segment_create` | `segment-create` | Создать сегмент |
| `ym_segment_update` | — | Изменить сегмент |
| `ym_segment_delete` | `segment-delete` | Удалить сегмент |

### Метки
| Инструмент | CLI | Описание |
|------------|-----|----------|
| `ym_labels` | `labels` | Список меток |
| `ym_label_create` | `label-create` | Создать метку |
| `ym_label_update` | — | Изменить метку |
| `ym_label_delete` | `label-delete` | Удалить метку |
| `ym_counter_label_set` | — | Привязать метку к счётчику |
| `ym_counter_label_unset` | — | Отвязать метку |

### Аккаунты и представители
| Инструмент | CLI | Описание |
|------------|-----|----------|
| `ym_accounts` | `accounts` | Список аккаунтов |
| `ym_account_delete` | — | Удалить аккаунт |
| `ym_delegates` | `delegates` | Список представителей |
| `ym_delegate_add` | `delegate-add` | Добавить представителя |
| `ym_delegate_delete` | `delegate-delete` | Удалить представителя |

### Примечания на графике
| Инструмент | CLI | Описание |
|------------|-----|----------|
| `ym_chart_annotations` | `chart-annotations` | Список примечаний |
| `ym_chart_annotation_create` | `chart-annotation-create` | Создать примечание |
| `ym_chart_annotation_update` | — | Изменить примечание |
| `ym_chart_annotation_delete` | — | Удалить примечание |

### Фильтры доступа
| Инструмент | CLI | Описание |
|------------|-----|----------|
| `ym_access_filters` | — | Список фильтров доступа |
| `ym_access_filter_create` | — | Создать фильтр доступа |
| `ym_access_filter_update` | — | Изменить фильтр доступа |
| `ym_access_filter_delete` | — | Удалить фильтр доступа |

### Logs API
| Инструмент | CLI | Описание |
|------------|-----|----------|
| `ym_log_requests` | `log-requests` | Список запросов логов |
| `ym_log_request` | — | Информация о запросе |
| `ym_log_request_create` | `log-request-create` | Создать запрос (hits/visits) |
| `ym_log_request_evaluate` | `log-request-evaluate` | Оценить возможность запроса |
| `ym_log_request_clean` | — | Очистить обработанные логи |
| `ym_log_request_cancel` | — | Отменить запрос |
| `ym_log_request_download` | `log-download` | Скачать часть лога (TSV) |

### Импорт данных
| Инструмент | CLI | Описание |
|------------|-----|----------|
| `ym_offline_conversions_upload` | `upload-conversions` | Загрузить оффлайн-конверсии |
| `ym_offline_conversions_uploads` | — | Список загрузок конверсий |
| `ym_offline_conversion_upload_info` | — | Инфо о загрузке |
| `ym_calls_upload` | `upload-calls` | Загрузить звонки |
| `ym_calls_uploads` | — | Список загрузок звонков |
| `ym_calls_upload_info` | — | Инфо о загрузке звонков |
| `ym_expenses_upload` | `upload-expenses` | Загрузить расходы |
| `ym_user_params_upload` | — | Загрузить параметры пользователей |

---

## MCP-сервер

### Установка

#### Шаг 1. Получить OAuth-токен Яндекс Метрики

1. Зарегистрируйте приложение на [oauth.yandex.com](https://oauth.yandex.com/client/new)
2. Укажите права: `metrika:read`, `metrika:write`
3. Получите токен: `https://oauth.yandex.com/authorize?response_type=token&client_id=<ваш_client_id>`

#### Шаг 2. Подключить MCP-сервер

### Подключение к Claude Code

**Способ 1: через uvx** (не требует установки пакета)

> Требуется [uv](https://docs.astral.sh/uv/) — если не установлен:
> ```bash
> curl -LsSf https://astral.sh/uv/install.sh | sh
> ```

```bash
claude mcp add yandex-metrika \
  -e YANDEX_METRIKA_TOKEN=ваш_токен \
  -- uvx mcp-server-yandex-metrika
```

**Способ 2: через pip**

```bash
pip install mcp-server-yandex-metrika

claude mcp add yandex-metrika \
  -e YANDEX_METRIKA_TOKEN=ваш_токен \
  -- mcp-server-yandex-metrika
```

Для удаления:
```bash
claude mcp remove yandex-metrika
```

### Подключение к Claude Desktop

Добавьте в конфигурационный файл:

| Клиент | ОС | Путь к файлу |
|--------|----|-------------|
| Claude Code | все | `~/.claude/settings.json` (секция `mcpServers`) |
| Claude Desktop | macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Claude Desktop | Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| Claude Desktop | Linux | `~/.config/Claude/claude_desktop_config.json` |

**Через uvx:**
```json
{
  "mcpServers": {
    "yandex-metrika": {
      "command": "uvx",
      "args": ["mcp-server-yandex-metrika"],
      "env": {
        "YANDEX_METRIKA_TOKEN": "ваш_токен"
      }
    }
  }
}
```

**Через pip** (после `pip install mcp-server-yandex-metrika`):
```json
{
  "mcpServers": {
    "yandex-metrika": {
      "command": "python",
      "args": ["-m", "mcp_server_yandex_metrika"],
      "env": {
        "YANDEX_METRIKA_TOKEN": "ваш_токен"
      }
    }
  }
}
```

### Подключение через --mcp-config

Подключает сервер только на время одной сессии Claude, не сохраняя в настройки. Токен хранится в отдельном `.env.mcp` файле, а не в конфиге Claude.

Из JSON-строки:
```bash
claude --mcp-config '{"yandex-metrika":{"command":"bash","args":["-c","source ~/.env.mcp && exec uvx mcp-server-yandex-metrika"]}}'
```

Из файла:
```bash
claude --mcp-config ~/mcp-servers.json
```

Пример `~/mcp-servers.json`:
```json
{
  "yandex-metrika": {
    "command": "bash",
    "args": ["-c", "source ~/.env.mcp && exec uvx mcp-server-yandex-metrika"]
  }
}
```

Пример `~/.env.mcp`:
```
YANDEX_METRIKA_TOKEN=ваш_токен
```

#### Шаг 3. Проверить

Попросите Claude: *«Покажи список моих счётчиков Яндекс Метрики»* — он вызовет `ym_counters`.

### Примеры (MCP)

- «Покажи статистику по визитам за последнюю неделю для счётчика 12345678» → `ym_stat_data`
- «Создай цель "Покупка" типа url с условием contain "/thank-you"» → `ym_goal_create`
- «Выгрузи логи визитов за январь 2024» → `ym_log_request_create`

---

## CLI-утилита

### Установка (CLI)

```bash
pip install mcp-server-yandex-metrika
```

Переменная окружения `YANDEX_METRIKA_TOKEN` должна быть установлена:

```bash
export YANDEX_METRIKA_TOKEN=ваш_токен
```

Или через файл:

```bash
mcp-server-yandex-metrika --env /path/to/.env counters
```

Формат файла — `KEY=VALUE`, по одной переменной на строку, `#`-комментарии.

### Использование (CLI)

Без аргументов запускается MCP-сервер, с командой — CLI. Все команды выводят JSON.

```bash
# Версия
mcp-server-yandex-metrika --version

# Справка
mcp-server-yandex-metrika --help
mcp-server-yandex-metrika <command> --help
```

### Примеры команд

```bash
# Статистика визитов
mcp-server-yandex-metrika stat-data --ids 12345678 --metrics ym:s:visits,ym:s:users

# Список счётчиков
mcp-server-yandex-metrika counters --search "мой сайт"

# Цели счётчика
mcp-server-yandex-metrika goals 12345678

# Создать запрос логов
mcp-server-yandex-metrika log-request-create 12345678 \
  --date1 2024-01-01 --date2 2024-01-31 \
  --fields "ym:s:date,ym:s:visitID" --source visits
```

---

## Pydantic-модели

Пакет содержит типизированные Pydantic-модели всех объектов API. Модели можно использовать в своих Python-программах для валидации данных и автодополнения в IDE.

### Установка (библиотеки)

```bash
pip install mcp-server-yandex-metrika
```

### Использование в своих программах

```python
from mcp_server_yandex_metrika.models import CounterBrief, Goal

# Валидация данных из API
data = {"id": 12345678, "name": "Мой сайт", "status": "Active"}
counter = CounterBrief.model_validate(data)
print(counter.name)  # type-safe доступ к полям

# Создание объекта
goal = Goal(name="Покупка", type="url")
print(goal.model_dump_json())
```

Все модели используют `extra="allow"` для forward compatibility — неизвестные поля API не вызывают ошибок.

Полный список моделей: [`models.py`](src/mcp_server_yandex_metrika/models.py)

---

## Переменные окружения

| Переменная | Обязательная | По умолчанию | Описание |
|------------|:------------:|:------------:|----------|
| `YANDEX_METRIKA_TOKEN` | да | — | OAuth-токен Яндекс Метрики |
| `METRIKA_TIMEOUT` | нет | `30` | Таймаут HTTP-запросов к API (секунды) |
| `METRIKA_FILE_TIMEOUT` | нет | `60` | Таймаут скачивания файлов (секунды) |

### Загрузка из файла

Вместо передачи переменных через `-e` можно указать файл:

```bash
mcp-server-yandex-metrika --env /path/to/.env
```

Формат файла — `KEY=VALUE`, по одной переменной на строку, `#`-комментарии.

Работает в обоих режимах: MCP-сервер и CLI:

```bash
# MCP-сервер
claude mcp add yandex-metrika -- mcp-server-yandex-metrika --env ~/.config/metrika.env

# CLI
mcp-server-yandex-metrika --env ~/.config/metrika.env counters
```

## Лимиты API

- 30 запросов/секунду на IP
- 5000 запросов/день на пользователя
- 3 параллельных запроса на пользователя
- 200 запросов/5 минут для `/stat/v1/data/`
- HTTP 420 при превышении лимитов

## Разработка

```bash
pip install -e ".[test]"
ruff check src/ tests/
pytest tests/ -v
```

## Лицензия

MIT
