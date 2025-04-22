#!/usr/bin/env python3

"""Module providing a function printing python version."""

import sys

from dotenv import load_dotenv
from .model import interact
from .helper import (
    get_question,
    read_file_content,
)

load_dotenv()


def main() -> None:
    """Main function"""

    file_tokens: list[str] = []

    for arg in sys.argv[1:]:
        content = read_file_content(arg)
        if content:
            file_tokens.append(content.strip())

    interact(("\n".join(file_tokens) + "\n" + get_question()).strip())


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
