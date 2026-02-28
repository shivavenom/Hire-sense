import json
import re
from typing import Any


# ----------------------------------------
# JSON Utilities
# ----------------------------------------

def strip_markdown_fences(text: str) -> str:
    """
    Removes ```json ``` fences if LLM returns them.
    """
    text = text.strip()

    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*", "", text)
        text = text.replace("```", "")

    return text.strip()


def safe_json_loads(text: str) -> Any:
    """
    Safely parse JSON from LLM output.
    Raises ValueError if invalid.
    """
    cleaned = strip_markdown_fences(text)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON from LLM: {str(e)}")


# ----------------------------------------
# Text Utilities
# ----------------------------------------

def normalize_text(text: str) -> str:
    """
    Lowercase and normalize whitespace.
    """
    return re.sub(r"\s+", " ", text.lower()).strip()


def contains_keyword(text: str, keyword: str) -> bool:
    """
    Case-insensitive keyword check.
    """
    return keyword.lower() in text.lower()