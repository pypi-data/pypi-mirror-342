import pytest
from fetch_meditation.jft_language import JftLanguage
from fetch_meditation.jft_settings import JftSettings
from fetch_meditation.english_jft import EnglishJft
from fetch_meditation.french_jft import FrenchJft
from fetch_meditation.german_jft import GermanJft
from fetch_meditation.italian_jft import ItalianJft
from fetch_meditation.portuguese_jft import PortugueseJft
from fetch_meditation.japanese_jft import JapaneseJft
from fetch_meditation.russian_jft import RussianJft
from fetch_meditation.spanish_jft import SpanishJft
from fetch_meditation.swedish_jft import SwedishJft
from fetch_meditation.jft import Jft


@pytest.fixture(
    params=[
        (EnglishJft, JftLanguage.English),
        (FrenchJft, JftLanguage.French),
        (GermanJft, JftLanguage.German),
        (ItalianJft, JftLanguage.Italian),
        (PortugueseJft, JftLanguage.Portuguese),
        (JapaneseJft, JftLanguage.Japanese),
        (RussianJft, JftLanguage.Russian),
        (SpanishJft, JftLanguage.Spanish),
        (SwedishJft, JftLanguage.Swedish),
    ]
)
def language_cls(request):
    return request.param


def test_jft_language_property(language_cls):
    jft_cls, language = language_cls
    jft_settings = JftSettings(language)
    jft_instance = Jft(jft_settings)

    assert jft_instance.language == language


def test_get_instance(language_cls):
    jft_cls, language = language_cls
    jft_settings = JftSettings(language)
    jft_instance = Jft.get_instance(jft_settings)

    assert isinstance(jft_instance, jft_cls)
