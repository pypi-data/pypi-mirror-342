from dataclasses import dataclass
from typing import Any, Union
from fetch_meditation.jft_language import JftLanguage
from fetch_meditation.english_jft import EnglishJft
from fetch_meditation.french_jft import FrenchJft
from fetch_meditation.german_jft import GermanJft
from fetch_meditation.italian_jft import ItalianJft
from fetch_meditation.japanese_jft import JapaneseJft
from fetch_meditation.portuguese_jft import PortugueseJft
from fetch_meditation.russian_jft import RussianJft
from fetch_meditation.spanish_jft import SpanishJft
from fetch_meditation.swedish_jft import SwedishJft


@dataclass
class Jft:
    settings: Any

    @property
    def language(self) -> JftLanguage:
        return self.settings.language

    @staticmethod
    def get_instance(
        settings: Any,
    ) -> Union[
        EnglishJft,
        FrenchJft,
        GermanJft,
        ItalianJft,
        JapaneseJft,
        PortugueseJft,
        RussianJft,
        SpanishJft,
        SwedishJft,
    ]:
        return {
            JftLanguage.English: EnglishJft,
            JftLanguage.French: FrenchJft,
            JftLanguage.German: GermanJft,
            JftLanguage.Italian: ItalianJft,
            JftLanguage.Japanese: JapaneseJft,
            JftLanguage.Portuguese: PortugueseJft,
            JftLanguage.Russian: RussianJft,
            JftLanguage.Spanish: SpanishJft,
            JftLanguage.Swedish: SwedishJft,
        }[settings.language](settings)
