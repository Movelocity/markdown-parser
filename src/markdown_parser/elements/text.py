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
    
    while position < len(text):
        # Look for the next inline element starting from current position
        remaining_text = text[position:]
        
        # Find all possible matches
        all_matches = []
        
        for pattern_func in [_try_image, _try_link, _try_bold, _try_italic, _try_code]:
            matches = pattern_func(remaining_text)
            for match_pos, element, match_length in matches:
                all_matches.append((match_pos, element, match_length, pattern_func.__name__))
        
        if all_matches:
            # Filter out overlapping matches, keeping the outermost/longest ones
            filtered_matches = _filter_nested_matches(all_matches)
            
            if filtered_matches:
                # Sort by position
                filtered_matches.sort(key=lambda x: x[0])
                
                # Take the first match
                match_pos, element, match_length, pattern_name = filtered_matches[0]
                
                # Add any plain text before the match
                if match_pos > 0:
                    text_content = remaining_text[:match_pos]
                    if elements and isinstance(elements[-1], Text):
                        # Merge with previous text element
                        elements[-1].content += text_content
                    else:
                        elements.append(Text(content=text_content))
                
                # Add the matched element
                elements.append(element)
                position += match_pos + match_length
            else:
                # No valid matches, add the rest as plain text
                remaining_content = remaining_text
                if elements and isinstance(elements[-1], Text):
                    # Merge with previous text element
                    elements[-1].content += remaining_content
                else:
                    elements.append(Text(content=remaining_content))
                break
        else:
            # No matches found, add the rest as plain text
            remaining_content = remaining_text
            if elements and isinstance(elements[-1], Text):
                # Merge with previous text element
                elements[-1].content += remaining_content
            else:
                elements.append(Text(content=remaining_content))
            break
    
    # Post-process: merge short punctuation-only Text elements with previous elements
    merged_elements = []
    for i, element in enumerate(elements):
        if (isinstance(element, Text) and 
            element.content.strip() == '.' and
            merged_elements and 
            isinstance(merged_elements[-1], Text)):
            # Merge single period with previous text element
            merged_elements[-1].content += element.content
        else:
            merged_elements.append(element)
    
    return merged_elements


def _filter_nested_matches(matches):
    """Filter out nested matches, keeping only the outermost ones."""
    if not matches:
        return []
    
    # Sort by start position, then by length (longer first)
    matches.sort(key=lambda x: (x[0], -x[2]))
    
    filtered = []
    
    for match in matches:
        match_start, element, match_length, pattern_name = match
        match_end = match_start + match_length
        
        # Check if this match overlaps with any already accepted match
        overlaps = False
        for existing_start, existing_element, existing_length, existing_pattern in filtered:
            existing_end = existing_start + existing_length
            
            # Check for overlap
            if (match_start < existing_end and match_end > existing_start):
                overlaps = True
                break
        
        if not overlaps:
            filtered.append(match)
    
    return filtered


def _try_image(text: str) -> List[Tuple[int, InlineElement, int]]:
    """Try to find all images in text."""
    matches = []
    for match in re.finditer(r'!\[([^\]]*)\]\(([^)]+)\)(\{[^}]+\})?', text):
        element = _parse_image_from_match(match)
        matches.append((match.start(), element, match.end() - match.start()))
    return matches


def _try_link(text: str) -> List[Tuple[int, InlineElement, int]]:
    """Try to find all links in text."""
    matches = []
    for match in re.finditer(r'\[([^\]]+)\]\(([^)]+?)(?:\s+"([^"]+)")?\)', text):
        element = _parse_link_from_match(match)
        matches.append((match.start(), element, match.end() - match.start()))
    return matches


def _try_bold(text: str) -> List[Tuple[int, InlineElement, int]]:
    """Try to find all bold text in text."""
    matches = []
    for match in re.finditer(r'(\*\*|__)([^*_]+?)\1', text):
        content = match.group(2)
        matches.append((match.start(), Bold(content=content), match.end() - match.start()))
    return matches


def _try_italic(text: str) -> List[Tuple[int, InlineElement, int]]:
    """Try to find all italic text in text."""
    matches = []
    
    # Single asterisk pattern - allow any content except isolated asterisks at boundaries
    for match in re.finditer(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', text):
        content = match.group(1)
        # Make sure the content doesn't end or start with ** (which would be bold)
        if not (content.startswith('*') or content.endswith('*')):
            matches.append((match.start(), Italic(content=content), match.end() - match.start()))
    
    # Single underscore pattern
    for match in re.finditer(r'(?<!_)_(?!_)([^_]+?)(?<!_)_(?!_)', text):
        content = match.group(1)
        matches.append((match.start(), Italic(content=content), match.end() - match.start()))
    
    return matches


def _try_code(text: str) -> List[Tuple[int, InlineElement, int]]:
    """Try to find all inline code in text."""
    matches = []
    for match in re.finditer(r'`([^`]+)`', text):
        content = match.group(1)
        matches.append((match.start(), Code(content=content), match.end() - match.start()))
    return matches


def _parse_image_from_match(match: re.Match) -> Image:
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


def _parse_link_from_match(match: re.Match) -> Link:
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