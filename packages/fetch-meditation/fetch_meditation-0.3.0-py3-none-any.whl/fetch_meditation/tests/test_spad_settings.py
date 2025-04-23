import pytest
from fetch_meditation.spad_settings import SpadSettings
from fetch_meditation.spad_language import SpadLanguage


def test_constructor():
    settings = SpadSettings(SpadLanguage.English)
    assert settings.language == SpadLanguage.English
    assert settings.time_zone is None


def test_constructor_with_timezone():
    settings = SpadSettings(SpadLanguage.English, time_zone="Australia/Sydney")
    assert settings.language == SpadLanguage.English
    assert settings.time_zone == "Australia/Sydney"
