from typing import Dict, List, Any
from bs4 import BeautifulSoup
from fetch_meditation.utilities.http_utility import HttpUtility
from fetch_meditation.jft_entry import JftEntry


class GermanJft:
    def __init__(self, settings: Any) -> None:
        self.settings = settings

    def fetch(self) -> "JftEntry":
        url = "https://narcotics-anonymous.de/artikel/nur-fuer-heute/"
        data = HttpUtility.http_get(url)
        soup = BeautifulSoup(data, "html.parser")
        container = soup.find("div", {"id": "jft-container"})
        result: Dict[str, Any] = {}

        for node in container.children:
            if node.name is not None:
                id = node.get("id")
                if id == "jft-content":
                    content_list = []
                    for contentNode in node.find_all("p"):
                        if contentNode.get("id") != "jft-content-1":
                            content_list.append(contentNode.get_text(strip=True).replace("\n", " "))
                    result[id] = content_list
                else:
                    result[id] = node.get_text(strip=True).replace("\n", "")
        result["page"] = ""
        result["copyright"] = ""
        result["jft-content"] = list(filter(None, result["jft-content"]))

        return JftEntry(
            result["jft-date"],
            result["jft-title"],
            result["page"],
            result["jft-quote"],
            result["jft-quote-source"],
            result["jft-content"],
            result["jft-thought"],
            result["copyright"],
        )
