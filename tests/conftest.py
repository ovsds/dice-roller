import pytest

import tests.settings as tests_settings


@pytest.fixture(name="settings")
def settings_fixture():
    return tests_settings.PytestSettings()
