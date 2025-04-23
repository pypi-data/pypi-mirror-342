from typing import Dict, List, Any
import re
import pytz
from datetime import datetime
from bs4 import BeautifulSoup
from fetch_meditation.utilities.http_utility import HttpUtility
from fetch_meditation.jft_entry import JftEntry


def remove_newlines_from_dict(d: Dict[str, str]) -> None:
    """Remove newlines from all string values in the dictionary."""
    for key, value in d.items():
        if isinstance(value, str):
            d[key] = value.replace("\n", "")


class SpanishJft:
    def __init__(self, settings: Any) -> None:
        self.settings = settings

    def fetch(self) -> "JftEntry":
        timezone = pytz.timezone("America/Mexico_City")
        date = datetime.now(timezone)
        url = "https://fzla.org/wp-content/uploads/meditaciones/" + date.strftime("%m/%d") + ".html"
        data = HttpUtility.http_get(url)
        soup = BeautifulSoup(data, "html.parser")

        # Get content paragraphs
        paragraphs = []
        content_div = soup.find("div", id="content")
        if content_div:
            # Find all paragraphs except those with separa-sxh class
            for p in content_div.find_all("p", class_=lambda x: x != "separa-sxh"):
                text = p.get_text(strip=True)
                # Skip "Sólo por hoy" paragraphs, empty paragraphs, and paragraphs with images
                if not re.match(r"^Sólo por hoy", text, re.I) and text and not p.find("img"):
                    paragraphs.append(text.replace("\n", ""))

        # Get Thought
        extracted_thought = ""
        # Look for paragraph containing strong tag with "Sólo por hoy"
        for p in content_div.find_all("p"):
            strong_tag = p.find("strong")
            if strong_tag and "Sólo por hoy" in strong_tag.get_text():
                thought_text = p.get_text(strip=True)
                if ":" in thought_text:
                    extracted_thought = thought_text.split(":", 1)[1].strip()
                else:
                    extracted_thought = thought_text
                break

        # Extract other elements
        result = {}
        for element in soup.find_all("p"):
            class_name = element.get("class", [])
            if class_name == ["fecha-sxh"]:
                result["date"] = element.get_text()
            elif class_name == ["titulo-sxh"]:
                result["title"] = element.get_text()
            elif class_name == ["descripcion-sxh"]:
                result["quote"] = element.get_text(strip=True).replace("\n", "")
            elif class_name == ["numero-pagina-sxh"]:
                result["source"] = element.get_text()

        # Set content and page
        result["content"] = list(filter(None, paragraphs))
        result["page"] = ""

        # Set copyright
        result["copyright"] = (
            "Servicio del Foro Zonal Latinoamericano, Copyright 2017 NA World Services, Inc. Todos los Derechos Reservados."
        )

        # Handle thought
        if extracted_thought:
            result["thought"] = "Sólo por Hoy: " + extracted_thought.replace("\n", "")
        else:
            result["thought"] = "Sólo por Hoy: "

        remove_newlines_from_dict(result)

        return JftEntry(
            result["date"],
            result["title"],
            result["page"],
            result["quote"],
            result["source"],
            result["content"],
            result["thought"],
            result["copyright"],
        )
