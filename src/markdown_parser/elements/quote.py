"""Quote block parser for markdown."""

import re
from typing import List, Optional, Tuple
from ..models import Quote, BlockElement
from .text import parse_inline_elements


def parse_quote(lines: List[str], start_idx: int) -> Optional[Tuple[Quote, int]]:
    """Parse a quote block starting from the given line index.
    
    Returns the quote element and the index of the next line after the quote.
    """
    if start_idx >= len(lines):
        return None
    
    first_line = lines[start_idx]
    if not first_line.strip().startswith('>'):
        return None
    
    quote_lines = []
    current_idx = start_idx
    
    # Collect all lines that are part of this quote
    while current_idx < len(lines):
        line = lines[current_idx]
        
        # Empty line might end the quote
        if not line.strip():
            # Check if next line continues the quote
            if current_idx + 1 < len(lines) and lines[current_idx + 1].strip().startswith('>'):
                quote_lines.append('')
                current_idx += 1
                continue
            else:
                break
        
        # Check if line is part of quote
        if line.strip().startswith('>'):
            quote_lines.append(line)
            current_idx += 1
        else:
            # Line doesn't start with >, but might be continuation
            # Check if previous line was quote and this is indented
            if quote_lines and len(line) - len(line.lstrip()) >= 2:
                quote_lines.append(line)
                current_idx += 1
            else:
                break
    
    if not quote_lines:
        return None
    
    # Process quote lines to determine level and content
    level = _get_quote_level(quote_lines[0])
    content_lines = []
    
    for line in quote_lines:
        # Remove quote markers
        processed_line = line
        for _ in range(level):
            processed_line = re.sub(r'^\s*>\s?', '', processed_line, count=1)
        content_lines.append(processed_line)
    
    # Parse content recursively (quotes can contain other blocks)
    content = _parse_quote_content('\n'.join(content_lines))
    
    quote = Quote(
        content=content,
        level=level
    )
    
    return quote, current_idx


def _get_quote_level(line: str) -> int:
    """Get the quote nesting level (number of > characters)."""
    level = 0
    temp_line = line.strip()
    
    while temp_line.startswith('>'):
        level += 1
        temp_line = temp_line[1:].strip()
    
    return max(1, level)


def _parse_quote_content(text: str) -> List[BlockElement]:
    """Parse the content inside a quote block.
    
    For now, we'll treat it as inline elements in a paragraph.
    In a full implementation, this would recursively parse all block types.
    """
    # Simple implementation: treat all content as inline elements
    # In a complete parser, this would handle nested blocks
    content = []
    
    lines = text.strip().split('\n')
    current_paragraph_lines = []
    
    for line in lines:
        if not line.strip():
            # Empty line ends paragraph
            if current_paragraph_lines:
                paragraph_text = ' '.join(current_paragraph_lines)
                content.extend(parse_inline_elements(paragraph_text))
                current_paragraph_lines = []
        else:
            current_paragraph_lines.append(line.strip())
    
    # Don't forget the last paragraph
    if current_paragraph_lines:
        paragraph_text = ' '.join(current_paragraph_lines)
        content.extend(parse_inline_elements(paragraph_text))
    
    return content 