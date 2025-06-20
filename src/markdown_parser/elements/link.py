"""Link and image parsers for markdown."""

import re
from typing import Optional
from ..models import Link, Image
from ..regex_patterns import (
    LINK_FULL_PATTERN, IMAGE_FULL_PATTERN,
    IMAGE_SIZE_ATTR_PATTERN, IMAGE_CSS_ATTR_PATTERN
)


def parse_link(text: str) -> Optional[Link]:
    """Parse a link from text.
    
    Format: [text](url) or [text](url "title")
    """
    match = LINK_FULL_PATTERN.match(text.strip())
    if not match:
        return None
    
    link_text = match.group(1) or ""
    url = match.group(2) or ""
    title = match.group(3)  # Optional
    
    return Link(content=link_text, url=url, title=title)


def parse_image(text: str) -> Optional[Image]:
    """Parse an image from text.
    
    Format: ![alt](url) or ![alt](url){size=0.5, css="..."}
    """
    match = IMAGE_FULL_PATTERN.match(text.strip())
    if not match:
        return None
    
    alt = match.group(1) or ""
    url = match.group(2) or ""
    attrs = match.group(3)
    
    # Parse extended attributes
    size = None
    css = None
    
    if attrs:
        # Parse size attribute
        size_match = IMAGE_SIZE_ATTR_PATTERN.search(attrs)
        if size_match:
            try:
                size = float(size_match.group(1))
                size = max(0, min(1, size))  # Clamp to 0-1
            except ValueError:
                pass
        
        # Parse css attribute
        css_match = IMAGE_CSS_ATTR_PATTERN.search(attrs)
        if css_match:
            css = css_match.group(1)
    
    return Image(content=alt, url=url, size=size, css=css) 