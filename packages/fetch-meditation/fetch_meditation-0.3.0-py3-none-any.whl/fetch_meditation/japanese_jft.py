from datetime import datetime
from typing import Dict, List, Any
from bs4 import BeautifulSoup
from fetch_meditation.utilities.http_utility import HttpUtility
from fetch_meditation.jft_entry import JftEntry


class JapaneseJft:
    def __init__(self, settings: Any) -> None:
        self.settings = settings

    def fetch(self) -> "JftEntry":
        url = "https://najapan.org/just_for_today/"
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

        # Extract the date and title
        h2_element = soup.find("h2")
        if h2_element:
            date_parts = h2_element.text.split("　")
            result["date"] = date_parts[0].strip()
            result["title"] = date_parts[-1].strip()

        # Extract quote
        p0_element = soup.find("p")
        if p0_element:
            result["quote"] = p0_element.next_element.get_text(strip=True).replace("\n", "")

        # Extract the source and page
        p1_element = soup.find_all("p")[1]
        if p1_element:
            result["source"] = p1_element.text.strip()

        p_tags = soup.find_all("p")
        p_tag_count = len(p_tags)

        # Extract the thought
        if p_tag_count >= 2:
            thought_p_tag = p_tags[-2]
            result["thought"] = thought_p_tag.text.strip()

        # Extract the copyright
        center_tags = soup.find_all("center")
        if center_tags:
            result["copyright"] = center_tags[0].text.strip()

        # Extract the content
        right_aligned_p = soup.find("p", style="text-align:right")
        paragraph_content = right_aligned_p.next_element.next_element.next_element
        filtered_content = []
        while True:
            if paragraph_content.name == "b":
                break
            if paragraph_content.name is None:
                filtered_content.append(paragraph_content.strip())
            paragraph_content = paragraph_content.next_element
        result["content"] = [i for i in filtered_content if i]

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
