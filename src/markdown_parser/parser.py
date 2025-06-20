"""Main markdown parser."""

import re
from typing import List, Optional
from .models import Document, BlockElement, Paragraph, HorizontalRule
from .elements import (
    parse_heading,
    parse_list,
    parse_quote,
    parse_code_block,
    parse_table,
    parse_align,
    parse_inline_elements,
)


def parse(markdown_text: str) -> Document:
    """Parse markdown text into a structured document.
    
    Args:
        markdown_text: The markdown text to parse
        
    Returns:
        A Document object containing the parsed structure
    """
    lines = markdown_text.split('\n')
    blocks = _parse_blocks(lines)
    
    return Document(blocks=blocks)


def _parse_blocks(lines: List[str]) -> List[BlockElement]:
    """Parse lines into block elements."""
    blocks = []
    i = 0
    
    while i < len(lines):
        # Skip empty lines between blocks
        if not lines[i].strip():
            i += 1
            continue
        
        # Try to parse as various block types
        block = None
        next_i = i + 1
        
        # Custom align tags
        if not block:
            align_result = parse_align(lines, i)
            if align_result:
                block, next_i = align_result
        
        # Code block
        if not block:
            code_result = parse_code_block(lines, i)
            if code_result:
                block, next_i = code_result
        
        # Heading
        if not block:
            heading = parse_heading(lines[i])
            if heading:
                block = heading
                next_i = i + 1
        
        # Horizontal rule
        if not block:
            if _is_horizontal_rule(lines[i]):
                block = HorizontalRule()
                next_i = i + 1
        
        # Table
        if not block:
            table_result = parse_table(lines, i)
            if table_result:
                block, next_i = table_result
        
        # List
        if not block:
            list_result = parse_list(lines, i)
            if list_result:
                block, next_i = list_result
        
        # Quote
        if not block:
            quote_result = parse_quote(lines, i)
            if quote_result:
                block, next_i = quote_result
        
        # Paragraph (default)
        if not block:
            paragraph, next_i = _parse_paragraph(lines, i)
            if paragraph:
                block = paragraph
            else:
                # If no paragraph was parsed, advance at least one line to avoid infinite loop
                next_i = i + 1
        
        if block:
            blocks.append(block)
        
        i = next_i
    
    return blocks


def _parse_paragraph(lines: List[str], start_idx: int) -> tuple[Optional[Paragraph], int]:
    """Parse a paragraph starting from the given line index."""
    if start_idx >= len(lines):
        return None, start_idx
    
    paragraph_lines = []
    i = start_idx
    
    while i < len(lines):
        line = lines[i]
        
        # Empty line ends paragraph
        if not line.strip():
            break
        
        # Check if line starts a different block type
        if (_is_horizontal_rule(line) or
            parse_heading(line) or
            line.strip().startswith('>') or
            line.strip().startswith('```') or
            re.match(r'^(    |\t)', line) or
            re.match(r'^<(Align|Left|Center|Right)', line, re.IGNORECASE) or
            _could_be_list_item(line) or
            _could_be_table_start(lines, i)):
            break
        
        paragraph_lines.append(line)
        i += 1
    
    if not paragraph_lines:
        return None, start_idx
    
    # Join lines and parse inline elements
    text = ' '.join(line.strip() for line in paragraph_lines)
    content = parse_inline_elements(text)
    
    paragraph = Paragraph(content=content)
    return paragraph, i


def _is_horizontal_rule(line: str) -> bool:
    """Check if a line is a horizontal rule."""
    line = line.strip()
    
    # Return False for empty lines or lines that are too short
    if len(line) < 3:
        return False
    
    # Simple and fast checks for horizontal rules
    # Three or more consecutive -, *, or _
    if line.replace('-', '') == '' and len(line) >= 3:
        return True
    if line.replace('*', '') == '' and len(line) >= 3:
        return True
    if line.replace('_', '') == '' and len(line) >= 3:
        return True
    
    # Check for spaced patterns (limit complexity)
    # Remove all spaces and check if remaining chars are all the same
    no_spaces = line.replace(' ', '')
    if len(no_spaces) >= 3:
        if (no_spaces.replace('-', '') == '' or 
            no_spaces.replace('*', '') == '' or 
            no_spaces.replace('_', '') == ''):
            return True
    
    return False


def _could_be_list_item(line: str) -> bool:
    """Check if a line could be the start of a list."""
    # Unordered list markers
    if re.match(r'^\s*[-*+]\s+', line):
        return True
    
    # Ordered list markers
    if re.match(r'^\s*\d+[.)]\s+', line):
        return True
    
    return False


def _could_be_table_start(lines: List[str], idx: int) -> bool:
    """Check if the current position could be the start of a table."""
    if idx >= len(lines):
        return False
    
    # Check if current line has pipes
    if '|' not in lines[idx]:
        return False
    
    # Check if next line could be separator
    if idx + 1 < len(lines):
        next_line = lines[idx + 1].strip()
        if '|' in next_line and '-' in next_line:
            return True
    
    return False 