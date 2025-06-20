"""List parser for markdown."""

import re
from typing import List, Optional, Tuple
from ..models import ListElement, ListItem
from .text import parse_inline_elements


def parse_list(lines: List[str], start_idx: int) -> Optional[Tuple[ListElement, int]]:
    """Parse a list starting from the given line index.
    
    Returns the list element and the index of the next line after the list.
    """
    if start_idx >= len(lines):
        return None
    
    first_line = lines[start_idx]
    list_match = _match_list_item(first_line)
    
    if not list_match:
        return None
    
    ordered = list_match['ordered']
    items = []
    current_idx = start_idx
    
    while current_idx < len(lines):
        line = lines[current_idx]
        
        # Check if this is a list item
        item_match = _match_list_item(line)
        if not item_match:
            # Check if it's a continuation of the previous item (indented)
            if line.strip() and len(line) - len(line.lstrip()) >= 2:
                # This is a continuation, will be handled by the item parser
                current_idx += 1
                continue
            else:
                # End of list
                break
        
        # Check if it's the same type of list
        if item_match['ordered'] != ordered:
            break
        
        # Parse this list item and any sub-items
        item, next_idx = _parse_list_item(lines, current_idx)
        if item:
            items.append(item)
        current_idx = next_idx
    
    if not items:
        return None
    
    list_element = ListElement(
        ordered=ordered,
        items=items,
        start_number=list_match.get('number') if ordered else None
    )
    
    return list_element, current_idx


def _match_list_item(line: str) -> Optional[dict]:
    """Match a list item and return its properties."""
    # Unordered list: -, *, or +
    unordered_match = re.match(r'^(\s*)([-*+])\s+(.*)$', line)
    if unordered_match:
        return {
            'ordered': False,
            'indent': len(unordered_match.group(1)),
            'marker': unordered_match.group(2),
            'content': unordered_match.group(3)
        }
    
    # Ordered list: 1. or 1)
    ordered_match = re.match(r'^(\s*)(\d+)([.)])\s+(.*)$', line)
    if ordered_match:
        return {
            'ordered': True,
            'indent': len(ordered_match.group(1)),
            'number': int(ordered_match.group(2)),
            'marker': ordered_match.group(3),
            'content': ordered_match.group(4)
        }
    
    return None


def _parse_list_item(lines: List[str], start_idx: int) -> Tuple[Optional[ListItem], int]:
    """Parse a single list item, including any nested content."""
    if start_idx >= len(lines):
        return None, start_idx
    
    item_match = _match_list_item(lines[start_idx])
    if not item_match:
        return None, start_idx
    
    indent_level = item_match['indent'] // 2  # Convert spaces to levels
    content_lines = [item_match['content']]
    current_idx = start_idx + 1
    
    # Collect continuation lines
    base_indent = item_match['indent']
    while current_idx < len(lines):
        line = lines[current_idx]
        
        # Empty line might be part of the item
        if not line.strip():
            # Check if next line is still part of this item
            if current_idx + 1 < len(lines):
                next_line = lines[current_idx + 1]
                next_indent = len(next_line) - len(next_line.lstrip())
                if next_indent > base_indent:
                    content_lines.append('')
                    current_idx += 1
                    continue
            break
        
        # Check indentation
        line_indent = len(line) - len(line.lstrip())
        
        # If it's a new list item at the same or lower level, stop
        if _match_list_item(line) and line_indent <= base_indent:
            break
        
        # If it's indented more than the base, it's part of this item
        if line_indent > base_indent:
            # Remove the base indentation
            content_lines.append(line[base_indent + 2:])  # +2 for the marker space
            current_idx += 1
        else:
            break
    
    # Parse the content
    content_text = '\n'.join(content_lines).strip()
    
    # Check if the content contains a nested list
    content = []
    if '\n' in content_text and any(_match_list_item(line) for line in content_text.split('\n')):
        # Parse nested list
        nested_lines = content_text.split('\n')
        nested_idx = 0
        
        while nested_idx < len(nested_lines):
            line = nested_lines[nested_idx]
            
            # Try to parse as nested list
            nested_list_match = _match_list_item(line)
            if nested_list_match:
                nested_list, next_nested_idx = parse_list(nested_lines, nested_idx)
                if nested_list:
                    content.append(nested_list)
                    nested_idx = next_nested_idx
                    continue
            
            # Otherwise, parse as inline elements
            if line.strip():
                content.extend(parse_inline_elements(line))
            nested_idx += 1
    else:
        # Simple content, just parse inline elements
        content = parse_inline_elements(content_text)
    
    item = ListItem(
        content=content,
        indent_level=indent_level
    )
    
    return item, current_idx 