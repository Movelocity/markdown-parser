"""Custom element parsers for markdown extensions."""

import re
from typing import List, Optional, Tuple
from ..models import Align, AlignType, BlockElement, InlineElement
from .text import parse_inline_elements


def parse_align(lines: List[str], start_idx: int) -> Optional[Tuple[Align, int]]:
    """Parse custom alignment tags.
    
    Formats:
    - <Align center>content</Align>
    - <Left>content</Left>
    - <Center>content</Center>
    - <Right>content</Right>
    """
    if start_idx >= len(lines):
        return None
    
    first_line = lines[start_idx]
    
    # Check for align tag
    align_match = re.match(r'^<(Align|Left|Center|Right)(?:\s+(left|center|right))?>(.*)$', 
                          first_line.strip(), re.IGNORECASE)
    
    if not align_match:
        return None
    
    tag_name = align_match.group(1).lower()
    align_attr = align_match.group(2)
    remaining_content = align_match.group(3)
    
    # Determine alignment
    if tag_name == 'left':
        alignment = AlignType.LEFT
    elif tag_name == 'center':
        alignment = AlignType.CENTER
    elif tag_name == 'right':
        alignment = AlignType.RIGHT
    elif tag_name == 'align' and align_attr:
        alignment = AlignType(align_attr.lower())
    else:
        return None
    
    # Check if closing tag is on the same line
    closing_pattern = f'</{tag_name}>'
    if closing_pattern.lower() in remaining_content.lower():
        # Single line align
        content_match = re.search(f'^(.*?){re.escape(closing_pattern)}', 
                                 remaining_content, re.IGNORECASE)
        if content_match:
            content_text = content_match.group(1)
            content = parse_inline_elements(content_text)
            
            align = Align(
                alignment=alignment,
                content=content
            )
            
            return align, start_idx + 1
    
    # Multi-line align
    content_lines = [remaining_content] if remaining_content else []
    current_idx = start_idx + 1
    
    while current_idx < len(lines):
        line = lines[current_idx]
        
        # Check for closing tag
        if re.search(f'{closing_pattern}', line, re.IGNORECASE):
            # Extract content before closing tag
            content_match = re.search(f'^(.*?){re.escape(closing_pattern)}', 
                                     line, re.IGNORECASE)
            if content_match:
                content_lines.append(content_match.group(1))
            
            # Parse all content
            content_text = '\n'.join(content_lines).strip()
            content = _parse_align_content(content_text)
            
            align = Align(
                alignment=alignment,
                content=content
            )
            
            return align, current_idx + 1
        
        content_lines.append(line.rstrip())
        current_idx += 1
    
    # No closing tag found
    return None


def _parse_align_content(text: str) -> List[InlineElement]:
    """Parse content inside align tags.
    
    For now, treats everything as inline elements.
    Could be extended to support block elements.
    """
    return parse_inline_elements(text) 