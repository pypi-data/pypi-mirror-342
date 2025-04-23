#!/usr/bin/env python3

"""Main module for the append script"""

import sys
from enum import Enum
from typing import List
from pydantic import BaseModel, ValidationError
import yaml


class LiteralStr(str):
    """Custom string class to trigger the literal block style in YAML"""


def literal_str_representer(dumper, data):
    """Represent LiteralStr as a YAML literal block"""
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")


yaml.add_representer(LiteralStr, literal_str_representer)


class Role(str, Enum):
    """Enum for roles in the conversation"""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(BaseModel):  # pylint: disable=too-few-public-methods
    """Message class for conversation data"""

    role: Role
    content: str


class MessageList(BaseModel):  # pylint: disable=too-few-public-methods
    """Model for validating a list of messages"""

    RootModel: List[Message]


def get_any(content: str) -> List[dict] | None:
    """Parse and validate YAML content, returning a list of messages or a fallback"""

    try:
        messages = []
        parsed = yaml.safe_load_all(content)

        for item in parsed:
            if isinstance(item, list):
                result = MessageList(**{"RootModel": item})
                for message in result.RootModel:
                    messages.append(
                        {
                            "role": message.role.value,
                            "content": LiteralStr(message.content),
                        }
                    )
            elif isinstance(item, dict):
                message = Message(**item)
                messages.append(
                    {
                        "role": message.role.value,
                        "content": LiteralStr(message.content),
                    }
                )
            elif isinstance(item, str):
                messages.append(
                    {
                        "role": Role.USER.value,
                        "content": LiteralStr(content),
                    }
                )

        return messages

    except (yaml.YAMLError, ValidationError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return None


def main() -> None:
    """Main function"""

    data = get_any(sys.stdin.read())

    if data:
        yaml.dump(data, sys.stdout)


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
