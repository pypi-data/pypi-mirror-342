import pytest
from fetch_meditation.spad_language import SpadLanguage
from fetch_meditation.spad_settings import SpadSettings
from fetch_meditation.english_spad import EnglishSpad
from fetch_meditation.spad import Spad


@pytest.fixture(
    params=[
        (EnglishSpad, SpadLanguage.English),
    ]
)
def language_cls(request):
    return request.param


def test_jft_language_property(language_cls):
    spad_cls, language = language_cls
    spad_settings = SpadSettings(language)
    spad_instance = Spad(spad_settings)

    assert spad_instance.language == language


def test_get_instance(language_cls):
    spad_cls, language = language_cls
    spad_settings = SpadSettings(language)
    spad_instance = Spad.get_instance(spad_settings)

    assert isinstance(spad_instance, spad_cls)
