from typing import Dict, List, Any
from bs4 import BeautifulSoup
from datetime import datetime
from fetch_meditation.utilities.http_utility import HttpUtility
from fetch_meditation.jft_entry import JftEntry


class SwedishJft:
    def __init__(self, settings: Any) -> None:
        self.settings = settings

    def fetch(self) -> "JftEntry":
        url = "https://www.nasverige.org/dagens-text/"
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

        # Extract the date
        date_element = soup.find("div", class_="border-bottom mb-4").find("p", class_="h3")
        if date_element:
            result["date"] = date_element.text.strip()

        # Extract the title
        title_element = soup.find("div", class_="border-bottom mb-4").find("h2")
        if title_element:
            result["title"] = title_element.text.strip()

        # Extract the quote and source
        quote_element = soup.find("p", class_="bg-lightBlue p-4 preamble")
        if quote_element:
            result["quote"] = quote_element.text.strip()
            result["quote"] = " ".join(result["quote"].split())
            quote_parts = result["quote"].split("/")
            result["quote"] = quote_parts[0].strip()
            result["source"] = quote_parts[-1].strip()

        # Extract the thought
        thought_element = soup.find("div", class_="col-12 col-md-8 col-lg-6 pt-5").find_all("p")[1]
        if thought_element:
            result["thought"] = thought_element.text.strip()

        # Extract the content
        content_element = soup.find("div", class_="col-12 col-md-8 col-lg-6 pt-5").find_all("p")[0]
        if content_element:
            items = [item.strip() for item in content_element.text.strip().split("\n")]
            result["content"] = list(filter(None, items))

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
