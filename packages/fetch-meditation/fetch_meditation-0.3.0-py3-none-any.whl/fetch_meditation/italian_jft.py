from typing import Dict, List, Any
import json
from bs4 import BeautifulSoup
from fetch_meditation.utilities.http_utility import HttpUtility
from fetch_meditation.jft_entry import JftEntry


class ItalianJft:
    def __init__(self, settings: Any) -> None:
        self.settings = settings

    def fetch(self) -> "JftEntry":
        url = "https://na-italia.org/get-jft"
        response = HttpUtility.http_get(url)
        data = json.loads(response)[0]
        html_content = data["content"]
        soup = BeautifulSoup(html_content, "html.parser")

        paragraphs = soup.find_all("p")

        initial_result = {
            "quote": "",
            "source": "",
            "thought": "",
            "copyright": "",
            "page": "",
        }

        # Split the title and date parts
        title_parts = data["title"].split(",")
        initial_result["title"] = title_parts[0].strip()
        initial_result["date"] = title_parts[-1].strip()

        # Populate the result dictionary with paragraph content
        for index, paragraph in enumerate(paragraphs):
            key = "quote" if index == 0 else str(index + 1)
            initial_result[key] = paragraph.get_text()

        result = {
            "content": [],
            "thought": "",
            "source": "",
        }

        lastNumericKey = None
        firstNumericKeyWithSource = None

        # Iterate through the initial_result dictionary and categorize content
        for key, value in initial_result.items():
            if value.startswith("--"):
                firstNumericKeyWithSource = key
                result["source"] = value[2:]
            if key.isdigit():
                lastNumericKey = key
                result["content"].append(value)
                result["thought"] = value
            else:
                result[key] = value

        # Remove unnecessary content entries
        result["content"] = result["content"][:-1]

        quote_parts = result["quote"].split("--")
        result["quote"] = quote_parts[0].strip()
        result["source"] = quote_parts[1].strip() if len(quote_parts) > 1 else result["source"]

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
