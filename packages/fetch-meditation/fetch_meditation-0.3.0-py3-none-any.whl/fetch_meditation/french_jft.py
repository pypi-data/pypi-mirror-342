from typing import Dict, List, Any
from datetime import datetime
from bs4 import BeautifulSoup
from fetch_meditation.utilities.http_utility import HttpUtility
from fetch_meditation.jft_entry import JftEntry


class FrenchJft:
    def __init__(self, settings: Any) -> None:
        self.settings = settings

    def fetch(self) -> "JftEntry":
        url = "https://jpa.narcotiquesanonymes.org/"
        data = HttpUtility.http_get(url)
        soup = BeautifulSoup(data, "html.parser")

        result = {
            "date": "",
            "quote": "",
            "source": "",
            "thought": "",
            "content": [],
            "title": "",
            "page": "",
            "copyright": f"Copyright (c) {datetime.now().year}, NA World Service, Inc. All Rights Reserved",
        }

        # Extract the title
        title_element = soup.find("div", class_="cartouche").find("h1")
        if title_element:
            result["title"] = title_element.text.strip()

        # Extract the date
        date_element = soup.find("p", class_="info-publi")
        if date_element:
            result["date"] = date_element.text.strip()

        # Extract the quote and source
        quote_div = soup.find("div", class_="chapo")
        if quote_div:
            quote_text = quote_div.text.strip()
            # Split the text into quote and source
            parts = quote_text.split("Texte de base")
            if len(parts) >= 2:
                result["quote"] = parts[0].strip()
                result["source"] = "Texte de base" + parts[1].strip()

        # Extract the thought
        thought_element = soup.find("h2", class_="spip")
        if thought_element:
            result["thought"] = thought_element.text.strip()

        # Extract the content
        text_div = soup.find("div", class_="texte")
        if text_div:
            p_tags = text_div.find_all("p")
            for p_tag in p_tags:
                # Skip if it's the thought (already captured)
                if p_tag.text.strip() == result["thought"]:
                    continue
                result["content"].append(p_tag.text.strip())

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
