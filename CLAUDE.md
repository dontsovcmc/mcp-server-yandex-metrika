# CLAUDE.md

## Разработка

**CRITICAL: Все правила разработки описаны в [development.md](development.md). Всегда следовать им при любых изменениях кода, тестов и документации.**

### Запуск из исходников

```bash
pip install -e ".[test]"
```

### Загрузка переменных из файла

```bash
# MCP-сервер с env-файлом
mcp-server-yandex-metrika --env /path/to/.env

# CLI с env-файлом
mcp-server-yandex-metrika --env /path/to/.env counters
```

`--env` загружает переменные через `python-dotenv` до инициализации сервера. Без `--env` — стандартные переменные окружения.

### Запуск тестов

```bash
ruff check src/ tests/
pytest tests/ -v
```

Тесты мокают API Яндекс Метрики — `YANDEX_METRIKA_TOKEN` не нужен. Все тесты проходят локально без доступа к реальному API.

### CI

GitHub Actions: `.github/workflows/test.yml`, `runs-on: self-hosted`. Токен не требуется.

### Структура

```
src/mcp_server_yandex_metrika/
├── __init__.py          # main(), версия
├── __main__.py          # python -m entry point
├── server.py            # FastMCP, все tools
├── metrika_api.py       # HTTP-клиент API Яндекс Метрики
├── models.py            # Pydantic-модели всех объектов API
└── cli.py               # CLI-интерфейс
```

### API Яндекс Метрики

- Документация: https://yandex.com/dev/metrika
- Base URL: `https://api-metrika.yandex.net`
- Авторизация: OAuth 2.0 (Bearer token)

### Переменные окружения

| Переменная | Обязательная | По умолчанию | Описание |
|------------|:------------:|:------------:|----------|
| `YANDEX_METRIKA_TOKEN` | да | — | OAuth-токен Яндекс Метрики |
| `METRIKA_TIMEOUT` | нет | `30` | Таймаут HTTP-запросов (секунды) |
| `METRIKA_FILE_TIMEOUT` | нет | `60` | Таймаут файловых операций (секунды) |

### Обновление MCP-сервера

Когда пользователь просит "обнови mcp yandex-metrika":

1. Определить способ установки:
   ```bash
   which mcp-server-yandex-metrika && pip show mcp-server-yandex-metrika
   ```
2. Обновить пакет:
   - **pip:** `pip install --upgrade mcp-server-yandex-metrika`
   - **uvx:** `uvx --upgrade mcp-server-yandex-metrika`
3. Проверить версию:
   ```bash
   mcp-server-yandex-metrika --version 2>/dev/null || python -c "import mcp_server_yandex_metrika; print(mcp_server_yandex_metrika.__version__)"
   ```
4. Сообщить пользователю новую версию и попросить перезапустить Claude Code (MCP-серверы перезапускаются при рестарте).

### README.md

При изменениях в коде обновлять [README.md](README.md):
- **Новый инструмент** — добавить строку в таблицу «Возможности» (MCP tool + CLI команда + описание).
- **Новая CLI-команда** — добавить в раздел «CLI-режим» → «Команды».
- **Новая переменная окружения** — добавить в таблицу «Переменные окружения».
- **Новый релиз** — обновить версию в бейджике.

### Правила кода

**Полные правила кода — в [development.md](development.md) (раздел "Правила кода").**

### Правила Git и workflow

- **CRITICAL: НИКОГДА не коммить в master!** Все коммиты — только в рабочую ветку.
- **Все изменения — через Pull Request в master.** Создать ветку, закоммитить, сделать rebase на свежий master, запушить, создать PR.
- **ПЕРЕД КОММИТОМ проверить, не слита ли текущая ветка в master.** Если ветка уже слита (merged) — создать новую ветку от свежего master и делать новый PR. Никогда не пушить в уже слитую ветку.
- **MANDATORY BEFORE EVERY `git push`: rebase onto fresh master:**
  ```bash
  git checkout master && git remote update && git pull && git checkout - && git rebase master
  ```
- **NEVER use `git stash`.**
- **NEVER use merge commits. ALWAYS rebase.**
- **CRITICAL: НИКОГДА не читать содержимое `.env` файлов** — запрещено использовать `cat`, `Read`, `grep`, `head`, `tail` и любые другие способы чтения `.env`. Для загрузки переменных использовать **только** `source <path>/.env`. Для проверки наличия файла — только `test -f`. Для проверки наличия переменной — `source .env && test -n "$VAR_NAME"` (без вывода значения).
- **ПЕРЕД КАЖДЫМ КОММИТОМ** проверять все исходные файлы, тесты и документацию на наличие реальных персональных данных (ИНН, номера счетов, имена, адреса, телефоны, email). Заменять на вымышленные.
- **В КАЖДОМ PR** обновлять версию в `pyproject.toml`, `src/mcp_server_yandex_metrika/__init__.py` и `server.json` (patch для фиксов, minor для новых фич).
- **ПЕРЕД публикацией в MCP-реестр** обязательно запускать `mcp-publisher validate` — проверяет `server.json` на соответствие схеме реестра.

### Публикация версии

Валидация, сборка, загрузка в PyPI и публикация в MCP Registry — одной командой:

```bash
mcp-publisher validate && python3 -m build && twine upload dist/* && rm -rf ./dist && mcp-publisher login github && mcp-publisher publish
```
