# Разработка и диагностика

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
