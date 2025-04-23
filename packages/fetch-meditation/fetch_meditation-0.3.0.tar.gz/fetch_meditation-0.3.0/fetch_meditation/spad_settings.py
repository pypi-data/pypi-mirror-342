from dataclasses import dataclass
from fetch_meditation.spad_language import SpadLanguage
from typing import Optional


@dataclass
class SpadSettings:
    language: SpadLanguage
    time_zone: Optional[str] = None
