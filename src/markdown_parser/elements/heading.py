"""Heading parser for markdown."""

import re
from typing import Optional
from ..models import Heading
from .text import parse_inline_elements
from ..regex_patterns import HEADING_PATTERN, HEADING_TRAILING_HASH_PATTERN


def parse_heading(line: str) -> Optional[Heading]:
    """Parse a heading from a line.
    
    Supports ATX-style headings (# Heading).
    """
    # Match heading pattern: 1-6 # followed by space and content
    match = HEADING_PATTERN.match(line.strip())
    
    if not match:
        return None
    
    level = len(match.group(1))
    content_text = match.group(2).strip()
    
    # Remove trailing # if present (optional in markdown)
    content_text = HEADING_TRAILING_HASH_PATTERN.sub('', content_text)
    
    # Parse inline elements in the heading
    content = parse_inline_elements(content_text)
    
    return Heading(
        level=level,
        content=content,
        raw_text=line
    ) 