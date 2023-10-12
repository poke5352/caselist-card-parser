import base64
import jsonlines
import mammoth
import os
import bs4

from bs4 import BeautifulSoup
from io import BytesIO
from typing import List

from settings import CUSTOM_HTML, STYLE_MAP, DEBUG, MINIMUM_WORD_COUNT


def jsonlines_iterator_parser(file: str) -> List[dict]:
    """
    Iterate through all documents in a jsonlines file and parse them into cards
    """
    result: List[dict] = []

    with jsonlines.open(file) as reader:
        for obj in reader:
            parsed_document: List[dict] = parse_document(obj)
            result.extend(parsed_document)

    return result


def folder_parser(folder: str) -> List[dict]:
    """
    Parse all files in a folder and subfolder into cards
    """
    result: List[dict] = []

    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".docx"):
                file_path: str = os.path.join(root, file)
                parsed_document: List[dict] = one_file_parser(file_path)
                result.extend(parsed_document)

    return result


def one_file_parser(file: str) -> List[dict]:
    """
    Parse one file into cards
    """
    with open(file, "rb") as f:
        base64_data: str = base64.b64encode(f.read()).decode("utf-8")

    test_obj: dict = {"base64_file": base64_data,
                      "mime_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                      "file_name": file,
                      "camp": "test",
                      "wiki": "test"
                      }
    
    parsed_document: List[dict] = parse_document(test_obj)
    return parsed_document


def parse_document(document: dict) -> List[dict]:
    """
    Parse document into list of cards

    """
    base64_data: str  = base64.b64decode(document['base64_file'])
    mime_type: str = document['mime_type']

    # Check DOCX mime type
    if mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        # Make a temp file containing base_64 data into docx file

        file: BytesIO = BytesIO(base64_data)

        converted_docx: str = mammoth.convert_to_html(file, style_map=STYLE_MAP)
        
        if DEBUG:
            print("Converted: " + document["file_name"] + " to HTML")

            if converted_docx.messages:
                print(converted_docx.messages)

            with open("output/conversion.html", "w", encoding="utf-8") as file:
                file.write(CUSTOM_HTML + converted_docx.value)

        return card_parser(converted_docx.value, document)
    return []


def card_parser(converted: str, document: dict) -> List[dict]:
    """
    Parse docx into list of cards
    """
    soup: BeautifulSoup = BeautifulSoup(converted, "html.parser")
    cards: List[bs4.Tag] = soup.find_all('h4')

    result: List[dict] = []

    for tag in cards:
        try:
            citation_tag: bs4.Tag = tag.find_next()

            card_tag: bs4.Tag = citation_tag.find_next_sibling()
            card_body: str = ""
            next_card_body: bs4.Tag = card_tag
            
            
            while next_card_body != None and next_card_body.name == "p":
                card_body += str(next_card_body)
                next_card_body = next_card_body.find_next_sibling()

            card_length: int = len(card_body.split())

            if card_length >= MINIMUM_WORD_COUNT and citation_tag.name == "p":
                card_data: dict = {"source": document["wiki"],
                                   "camp": document["camp"],
                                   "document": document["file_name"],
                                   "tag": str(tag),
                                   "cite": str(citation_tag),
                                   "pocket": str(tag.find_previous("h1")),
                                   "hat":  str(tag.find_previous("h2")),
                                   "block":  str(tag.find_previous("h3")),
                                   "cardHTML": str(tag) + str(citation_tag) + card_body,
                                   }
                result.append(card_data)
        except:
            pass

    return result

