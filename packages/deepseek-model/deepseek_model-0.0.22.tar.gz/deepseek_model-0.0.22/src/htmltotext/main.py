#!/usr/bin/env python

"""HTML to text"""

import sys
from markdownify import markdownify as md


def main():
    """Main"""
    html_content = sys.stdin.read()
    print(md(html_content).strip())


if __name__ == "__main__":
    main()
