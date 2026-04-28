# CLAUDE.md

## Разработка

**CRITICAL: Все правила разработки описаны в [development.md](development.md). Всегда следовать им при любых изменениях кода, тестов и документации.**

### Запуск из исходников

```bash
pip install -e ".[test]"
```

### Запуск тестов

```bash
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
4. Сообщить пользователю новую версию и попросить перезапустить Claude Code.

### Правила

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
- Не хардкодить токены и секреты в коде.
- stdout в MCP сервере занят JSON-RPC — для логов использовать только stderr.
- **ПЕРЕД КАЖДЫМ КОММИТОМ** проверять все исходные файлы, тесты и документацию на наличие реальных персональных данных (ИНН, номера счетов, имена, адреса, телефоны, email). Заменять на вымышленные.
- **В КАЖДОМ PR** обновлять версию в `pyproject.toml` и `src/mcp_server_yandex_metrika/__init__.py` (patch для фиксов, minor для новых фич).
