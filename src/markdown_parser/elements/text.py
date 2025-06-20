"""Text format parsers for inline elements."""

import re
from typing import List, Tuple, Optional
from ..models import InlineElement, Text, Bold, Italic, Code, Link, Image


def parse_inline_elements(text: str) -> List[InlineElement]:
    """Parse inline elements from text.
    
    Handles: bold, italic, inline code, links, and images.
    """
    if not text:
        return []
    
    elements = []
    position = 0
    
    # Patterns for inline elements
    patterns = [
        # Image: ![alt](url) or ![alt](url){size=0.5, css="..."}
        (r'!\[([^\]]*)\]\(([^)]+)\)(\{[^}]+\})?', 'image'),
        # Link: [text](url) or [text](url "title")
        (r'\[([^\]]+)\]\(([^)]+?)(?:\s+"([^"]+)")?\)', 'link'),
        # Bold: **text** or __text__
        (r'(\*\*|__)([^*_]+?)\1', 'bold'),
        # Italic: *text* or _text_ (but not ** or __)
        (r'(?<!\*)\*(?!\*)([^*]+?)(?<!\*)\*(?!\*)|(?<!_)_(?!_)([^_]+?)(?<!_)_(?!_)', 'italic'),
        # Inline code: `code`
        (r'`([^`]+)`', 'code'),
    ]
    
    combined_pattern = '|'.join(f'({pattern})' for pattern, _ in patterns)
    
    for match in re.finditer(combined_pattern, text):
        # Add any plain text before the match
        if match.start() > position:
            elements.append(Text(content=text[position:match.start()]))
        
        # Determine which pattern matched
        matched_text = match.group(0)
        
        if matched_text.startswith('!['):
            # Image
            elements.append(_parse_image_match(match))
        elif matched_text.startswith('['):
            # Link
            elements.append(_parse_link_match(match))
        elif matched_text.startswith('**') or matched_text.startswith('__'):
            # Bold
            content = match.group(2) if match.group(2) else match.group(0).strip('*_')
            elements.append(Bold(content=content))
        elif matched_text.startswith('*') or matched_text.startswith('_'):
            # Italic
            # Find the actual content group
            for i in range(1, len(match.groups()) + 1):
                if match.group(i) and match.group(i) in matched_text:
                    content = match.group(i)
                    if content and not content.startswith(('*', '_')):
                        elements.append(Italic(content=content))
                        break
        elif matched_text.startswith('`'):
            # Code
            content = matched_text.strip('`')
            elements.append(Code(content=content))
        
        position = match.end()
    
    # Add any remaining plain text
    if position < len(text):
        elements.append(Text(content=text[position:]))
    
    return elements


def _parse_image_match(match: re.Match) -> Image:
    """Parse image from regex match."""
    full_match = match.group(0)
    
    # Extract basic image parts
    img_match = re.match(r'!\[([^\]]*)\]\(([^)]+)\)(\{[^}]+\})?', full_match)
    if not img_match:
        return Image(content="", url="")
    
    alt = img_match.group(1) or ""
    url = img_match.group(2) or ""
    attrs = img_match.group(3)
    
    # Parse extended attributes if present
    size = None
    css = None
    
    if attrs:
        # Parse size attribute
        size_match = re.search(r'size\s*=\s*([0-9.]+)', attrs)
        if size_match:
            try:
                size = float(size_match.group(1))
                size = max(0, min(1, size))  # Clamp to 0-1
            except ValueError:
                pass
        
        # Parse css attribute
        css_match = re.search(r'css\s*=\s*"([^"]+)"', attrs)
        if css_match:
            css = css_match.group(1)
    
    return Image(content=alt, url=url, size=size, css=css)


def _parse_link_match(match: re.Match) -> Link:
    """Parse link from regex match."""
    full_match = match.group(0)
    
    # Extract link parts
    link_match = re.match(r'\[([^\]]+)\]\(([^)]+?)(?:\s+"([^"]+)")?\)', full_match)
    if not link_match:
        return Link(content="", url="")
    
    text = link_match.group(1) or ""
    url = link_match.group(2) or ""
    title = link_match.group(3)  # Optional title
    
    return Link(content=text, url=url, title=title) 