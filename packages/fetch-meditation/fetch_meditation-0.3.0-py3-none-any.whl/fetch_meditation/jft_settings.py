from dataclasses import dataclass
from fetch_meditation.jft_language import JftLanguage
from typing import Optional


@dataclass
class JftSettings:
    language: JftLanguage
    time_zone: Optional[str] = None
