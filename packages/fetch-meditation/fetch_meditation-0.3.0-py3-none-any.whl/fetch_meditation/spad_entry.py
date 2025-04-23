import json
from typing import Any, Dict, List
from dataclasses import dataclass
from bs4 import BeautifulSoup


@dataclass
class SpadEntry:
    date: str
    title: str
    page: str
    quote: str
    source: str
    content: List[str]
    thought: str
    copyright: str

    def _to_dict(self) -> Dict[str, Any]:
        return {
            "date": self.date,
            "title": self.title,
            "page": self.page,
            "quote": self.quote,
            "source": self.source,
            "content": self.content,
            "thought": self.thought,
            "copyright": self.copyright,
        }

    def to_json(self) -> str:
        return json.dumps(self._to_dict())

    def without_tags(self) -> Dict[str, Any]:
        def strip_tags(item: str) -> str:
            if isinstance(item, list):
                return [strip_tags(sub_item) for sub_item in item]
            else:
                soup = BeautifulSoup(item, "html.parser")
                return soup.text

        return {key: strip_tags(value) for key, value in self._to_dict().items()}
