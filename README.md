<!-- mcp-name: io.github.dontsovcmc/yandex-metrika -->

# mcp-server-yandex-metrika

[![Version](https://img.shields.io/badge/version-0.1.1-blue)](https://github.com/dontsovcmc/mcp-server-yandex-metrika)

MCP-сервер для работы с [API Яндекс Метрики](https://yandex.com/dev/metrika) через Claude Code, Claude Desktop и другие MCP-совместимые клиенты.

Все данные остаются на вашем компьютере — токен никуда не передаётся.

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

## Настройка

### Шаг 1. Получить OAuth-токен Яндекс Метрики

1. Зарегистрируйте приложение на [oauth.yandex.com](https://oauth.yandex.com/client/new)
2. Укажите права: `metrika:read`, `metrika:write`
3. Получите токен: `https://oauth.yandex.com/authorize?response_type=token&client_id=<ваш_client_id>`

### Шаг 2. Подключить MCP-сервер

#### Claude Code (CLI в терминале)

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

#### Claude Desktop

Добавьте в файл конфигурации (`~/Library/Application Support/Claude/claude_desktop_config.json` на macOS):

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

Для удаления:

```bash
claude mcp remove yandex-metrika
```

## Переменные окружения

| Переменная | Обязательная | Описание |
|-----------|-------------|----------|
| `YANDEX_METRIKA_TOKEN` | Да | OAuth-токен Яндекс Метрики |

## Примеры использования

### Через Claude

> «Покажи статистику по визитам за последнюю неделю для счётчика 12345678»

> «Создай цель "Покупка" типа url с условием contain "/thank-you" для счётчика 12345678»

> «Выгрузи логи визитов за январь 2024 для счётчика 12345678»

### CLI

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

## Лимиты API

- 30 запросов/секунду на IP
- 5000 запросов/день на пользователя
- 3 параллельных запроса на пользователя
- 200 запросов/5 минут для `/stat/v1/data/`
- HTTP 420 при превышении лимитов

## Лицензия

MIT
