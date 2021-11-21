import pytest


@pytest.fixture(autouse=True)
def env_credentials(monkeypatch):
    monkeypatch.setenv('API_ID', '123')
    monkeypatch.setenv('API_HASH', 'hasan')
