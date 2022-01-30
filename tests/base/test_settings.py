import pytest
from robozhab.base.settings import get_settings


class TestSettings:
    @pytest.fixture
    def settings_key(self):
        return 'schedule_days'

    @pytest.fixture
    def usual_value(self):
        return 5

    @pytest.fixture
    def override_value(self):
        return 1

    @pytest.fixture
    def temp_override_settings_file(
        self, tmp_path, settings_key, override_value
    ):
        d = tmp_path / "sub"
        d.mkdir()
        f = d / "hello.txt"
        f.write_text(f'{settings_key}={override_value}')
        return f.absolute()

    def test_sanity(self, settings_key, usual_value):
        settings = get_settings()
        assert getattr(settings, settings_key) == usual_value

    def test_file_override(
        self, temp_override_settings_file, settings_key, override_value
    ):
        settings = get_settings(temp_override_settings_file)
        assert getattr(settings, settings_key) == override_value
