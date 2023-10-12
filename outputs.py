import json

from settings import CUSTOM_HTML
from typing import List


def save_html_data(data: List[dict]) -> None:
    """
    Save HTML data to file
    """
    with open("output/output.html", "w", encoding="utf-8") as file:
        file.write(CUSTOM_HTML)
        for card in data:
            file.write(card["cardHTML"] + "<br><br>")


def save_json_data(data: List[dict]) -> None:
    """
    Save JSON data to file
    """
    with open("output/output.jsonl", "w", encoding="utf-8") as f:
        for card in data:
            f.write(json.dumps(card) + "\n")