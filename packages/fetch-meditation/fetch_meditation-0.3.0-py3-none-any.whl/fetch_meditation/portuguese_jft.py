from typing import Dict, List, Any
from bs4 import BeautifulSoup
from fetch_meditation.utilities.http_utility import HttpUtility
from fetch_meditation.jft_entry import JftEntry


class PortugueseJft:
    def __init__(self, settings: Any) -> None:
        self.settings = settings

    def fetch(self) -> "JftEntry":
        url = "https://www.na.org.br/meditacao/"
        data = HttpUtility.http_get(url)
        soup = BeautifulSoup(data, "html.parser")

        # Extract paragraphs
        paragraph_div = soup.find("div", id="sep-i")
        paragraph_content = paragraph_div.next_element
        filtered_content = ""
        while True:
            if paragraph_content.name == "div":
                break
            filtered_content += str(paragraph_content)
            paragraph_content = paragraph_content.next_element
        paragraphs = [t.strip() for t in filtered_content.split("<br/>") if t.strip()]

        # Extract other elements
        result = {}
        for element in soup.find_all("p"):
            class_attr = element.get("class")[0] if element.get("class") else None
            text = element.get_text(strip=True)
            if class_attr == "dat":
                result["date"] = text
            elif class_attr == "cit":
                result["source"] = text
            elif class_attr == "ef":
                result["quote"] = text
            elif class_attr == "sph":
                result["thought"] = " ".join(text.split())
            elif class_attr == "ct":
                result["copyright"] = " ".join(text.replace("\n", "").split())

        # Extract the title
        title_element = soup.find("h1", class_="tit")
        result["title"] = title_element.get_text(strip=True) if title_element else ""

        # Create the final result dictionary
        result["page"] = ""
        result["content"] = paragraphs

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
