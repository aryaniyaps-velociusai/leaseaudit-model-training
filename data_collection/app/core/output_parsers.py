import json
from typing import Any

from langchain.schema import AIMessage
from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel
from regex import regex

from app.utils.format_data import cleanup_json_string


def parse_json(ai_message: AIMessage) -> dict[Any, Any]:
    """Parse the AI message."""
    text = cleanup_json_string(str(ai_message.content))
    pattern = regex.compile(r"\{(?:[^{}]|(?R))*\}")
    matches = pattern.findall(text)
    print(f"REGEX MATCHES: {matches}")
    if matches:
        return json.loads(matches[0])
    error_message = f"Couldn't find JSON in output: {text}"
    raise OutputParserException(error_message)


def get_json_schema_parser_instructions(pydantic_model: type[BaseModel]) -> str:
    """Get the JSON schema parser instructions."""
    return JsonOutputParser(pydantic_object=pydantic_model).get_format_instructions()
