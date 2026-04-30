import os

import pytest

os.environ.setdefault("YANDEX_METRIKA_TOKEN", "test-fake-token")


@pytest.fixture(autouse=True)
def _reset_api_cache():
    """Reset cached MetrikaAPI instance between tests."""
    import mcp_server_yandex_metrika.server as srv
    srv._api = None
    yield
    srv._api = None
