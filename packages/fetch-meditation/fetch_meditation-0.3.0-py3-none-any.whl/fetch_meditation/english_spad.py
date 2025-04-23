from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
from fetch_meditation.utilities.http_utility import HttpUtility
from fetch_meditation.spad_entry import SpadEntry
from datetime import datetime


class EnglishSpad:
    def __init__(self, settings: Any) -> None:
        self.settings = settings

    def fetch(self) -> "SpadEntry":
        # Prepare params if time_zone is set
        params = None
        if hasattr(self.settings, "time_zone") and self.settings.time_zone:
            params = {"timeZone": self.settings.time_zone}

        # Try primary URL first
        try:
            data = HttpUtility.http_get("https://spad.na.org/", params)
        except Exception as e:
            # If primary URL fails, try fallback URL
            try:
                data = HttpUtility.http_get("https://na.org/spadna/", params)
            except Exception as fallback_exception:
                raise Exception(
                    f"Error fetching data from both na.org/spadna and spadna.org. "
                    f"Primary error: {str(e)}"
                )
        soup = BeautifulSoup(data, "html.parser")
        td_elements = soup.find_all("td")
        spad_keys = [
            "date",
            "title",
            "page",
            "quote",
            "source",
            "content",
            "divider",
            "thought",
            "copyright",
        ]
        result: Dict[str, Any] = {}

        for i, td in enumerate(td_elements):
            if spad_keys[i] == "content":
                inner_html = "".join(str(child) for child in td.children)
                result["content"] = [
                    line.strip() for line in inner_html.split("<br/>") if line.strip()
                ]
            else:
                result[spad_keys[i]] = td.text.strip()

        # Handle copyright with fallback
        if "copyright" not in result:
            result["copyright"] = (
                f"Copyright (c) 2007-{datetime.now().year}, NA World Services, Inc. All Rights Reserved"
            )
        else:
            # Clean up existing copyright text
            result["copyright"] = " ".join(result["copyright"].split())

        return SpadEntry(
            result["date"],
            result["title"],
            result["page"],
            result["quote"],
            result["source"],
            result["content"],
            result["thought"],
            result["copyright"],
        )
