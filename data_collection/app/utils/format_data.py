import re
from typing import Any


def cleanup_json_string(json_str: str) -> str:
    # Remove leading and trailing whitespaces
    json_str = json_str.strip()

    # Remove escaped new lines
    json_str = re.sub(r"\\n", r"\n", json_str)
    json_str = re.sub(r"\n", "", json_str)

    # Replace escaped double quotes with regular double quotes
    json_str = re.sub(r'\\"', r"\"", json_str)
    json_str = re.sub(r"\"", '"', json_str)

    # Remove escaped backslashes
    json_str = re.sub(r"\\\\", "", json_str)

    # Remove unnecessary whitespaces (optional, if you want a more compact JSON)
    json_str = re.sub(r"\s+", " ", json_str)

    json_str = re.sub(r"\\", "", json_str)

    return json_str.replace(",}", "}")
