import pytest
from fetch_meditation.jft_settings import JftSettings
from fetch_meditation.jft_language import JftLanguage


def test_constructor():
    settings = JftSettings(JftLanguage.English)
    assert settings.language == JftLanguage.English
    assert settings.time_zone is None


def test_constructor_with_timezone():
    settings = JftSettings(JftLanguage.English, time_zone="America/New_York")
    assert settings.language == JftLanguage.English
    assert settings.time_zone == "America/New_York"
