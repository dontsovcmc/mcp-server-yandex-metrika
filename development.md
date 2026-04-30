# Разработка и диагностика

## Правила кода

### Безопасность

- **Пути для записи/чтения файлов** — валидировать через `_safe_output_path()`. Никогда не принимать произвольные пути от LLM без проверки. Функция кроссплатформенная (Windows/Linux/macOS):
  - Разрешены только домашняя директория и системный temp (`tempfile.gettempdir()`, `/tmp`).
  - Запись в dotfiles/dotdirs под home запрещена (`~/.ssh`, `~/.bashrc`, `~/.config/...`) — проверка через `os.sep + "." in relative_path`.
  - Пути разворачиваются через `os.path.realpath()` (защита от `..` и симлинков).
- **Парсинг JSON от пользователя** — всегда через `_parse_json(text, label)`, не через голый `json.loads()`. Пользователь должен получить понятное сообщение об ошибке, а не стектрейс `JSONDecodeError`.
- **Секреты** — только через переменные окружения (`os.getenv`). Не хардкодить токены в коде или тестах. В тестах использовать `test-fake-token`.
- **stdout зарезервирован** для JSON-RPC. Весь логгинг — только через `logging` в stderr.
- **HTTP-ответы в исключениях** — НИКОГДА не включать `resp.text` в `RuntimeError`. Тело ответа API может содержать персональные данные, которые утекут в логи Claude, MCP-ответ или скриншоты. В исключение — только метод, путь и статус-код: `raise RuntimeError(f"GET {path} -> {resp.status_code}")`. Полный ответ логировать только на уровне `log.debug()`.

### Обработка ошибок

- **Никогда не глотать исключения молча.** `except Exception:` без логирования запрещён. Всегда логировать через `log.warning()` или `log.error()` с контекстом (что делали, для какого объекта).
- **HTTP-ошибки** — `metrika_api.py` бросает `RuntimeError` с методом, путём и статус-кодом (без тела ответа). Не перехватывать эти ошибки в tool-функциях — FastMCP сам вернёт ошибку клиенту.
- **Ошибки валидации** — бросать `RuntimeError` с понятным сообщением. Пример: `raise RuntimeError(f"Invalid conditions_json: {e}")`.

### Стиль кода

- **Именование** — функции-хелперы с префиксом `_`. Имена должны быть читаемыми: `_to_json`, `_parse_json`, `_safe_output_path`, а не `_j`, `_p`, `_s`.
- **Дублирование** — каждая tool-функция самодостаточна (вызывает `_get_api()`). Это допустимое повторение, а не дублирование. Не выносить в декораторы/контекстные менеджеры.
- **Типы** — аннотировать параметры и возвращаемые значения. `dict`, `list`, `str` — не `Dict`, `List`, `Str` (используем встроенные типы Python 3.10+).
- **Импорты** — стандартная библиотека → сторонние пакеты → локальные модули, разделённые пустой строкой. Не импортировать неиспользуемые имена.
- **Модели** — Pydantic-модели в `models.py`. `extra="allow"` для forward compatibility с API.
- **Линтер** — `ruff check src/ tests/` должен проходить без ошибок. Максимальная длина строки — 120 символов.

### API-клиент (metrika_api.py)

- **Сессия** — `MetrikaAPI` кэшируется в `server._api` (один экземпляр на процесс). Не создавать новый `MetrikaAPI` на каждый вызов.
- **HTTP-хелперы** — `_get()`, `_post()`, `_put()`, `_delete()`, `_post_file()`, `_get_raw()`. Не писать ручные `session.get()`.
- **Таймаут** — 30 секунд на обычные запросы, 60 секунд на файловые операции.

### Тесты

- **Мокаем `MetrikaAPI`** на уровне класса: `@patch("mcp_server_yandex_metrika.server.MetrikaAPI")`. Кэш API сбрасывается через фикстуру в `conftest.py`.
- **Тестовые данные** — вымышленные. Никаких реальных персональных данных (ИНН, телефоны, email).

## Как Claude запускает MCP-сервер

Claude Code запускает MCP-сервер как **дочерний процесс** (subprocess) и общается с ним по **stdin/stdout** через JSON-RPC 2.0:

```
Claude Code                          MCP-сервер
    │                                    │
    │── spawn subprocess ──────────────►│  (command + args из конфига)
    │                                    │
    │── stdin: {"method":"initialize"} ─►│  handshake (таймаут 10 сек)
    │◄─ stdout: {"capabilities":...} ───│
    │                                    │
    │── stdin: {"method":"tools/list"} ─►│  получить список инструментов
    │◄─ stdout: [tools...] ─────────────│
    │                                    │
    │        ✓ Connected                 │
```

**Важно:**
- Сервер **не запускается в login shell** — `~/.bashrc`, `~/.zshrc` не выполняются
- **PATH может быть урезан** — команда может не находиться, хотя в обычном терминале работает
- **stdout зарезервирован** для протокола — любой `print()` в stdout ломает соединение (используйте stderr)

## `✗ Failed to connect` — что делать

**1. Запустить сервер вручную** — самый быстрый способ увидеть ошибку:

```bash
# Если ставили через uvx:
uvx mcp-server-yandex-metrika

# Если ставили через pip:
mcp-server-yandex-metrika
```

**2. Проверить что команда доступна:**

```bash
which mcp-server-yandex-metrika   # или: which uvx
```

Если `not found` — пакет не установлен или не в PATH.

**3. Использовать абсолютный путь** (если PATH урезан):

```bash
# Узнать полный путь:
which mcp-server-yandex-metrika
# Например: /Users/me/.local/bin/mcp-server-yandex-metrika

# Использовать его в конфиге:
claude mcp remove yandex-metrika
claude mcp add yandex-metrika \
  -e YANDEX_METRIKA_TOKEN=ваш_токен \
  -- /полный/путь/к/mcp-server-yandex-metrika
```

**4. Посмотреть логи Claude Code:**

```bash
# macOS:
ls ~/Library/Logs/Claude/
tail -f ~/Library/Logs/Claude/mcp*.log

# Windows:
dir %APPDATA%\Claude\logs\

# Linux:
ls ~/.config/Claude/logs/
```

**5. Включить debug-режим:**

```bash
claude --mcp-debug          # отладка протокола MCP
claude --verbose             # подробный вывод
CLAUDE_DEBUG=1 claude        # максимум логов
```

## Частые проблемы

| Симптом | Причина | Решение |
|---------|---------|---------|
| `command not found` | Пакет не установлен или не в PATH | `pip install mcp-server-yandex-metrika` или используйте абсолютный путь |
| `Failed to connect` без ошибки | Claude не может найти команду из-за урезанного PATH | Используйте абсолютный путь к команде |
| Сервер запускается вручную, но не в Claude | PATH в Claude отличается от PATH в терминале | Используйте абсолютный путь |
| `No module named mcp_server_yandex_metrika` | pip установил в другой Python | Используйте entry point `mcp-server-yandex-metrika` вместо `python -m` |
| `401 Unauthorized` | Неверный OAuth токен | Проверьте токен, получите новый на oauth.yandex.com |
| Таймаут при подключении | Сервер не ответил за 10 секунд | Проверьте сеть и токен |
