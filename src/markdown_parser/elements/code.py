"""Code block parser for markdown."""

import re
from typing import List, Optional, Tuple
from ..models import CodeBlock
from ..regex_patterns import (
    CODE_FENCE_START_PATTERN, CODE_FENCE_END_PATTERN,
    CODE_INDENT_PATTERN, CODE_INDENT_CAPTURE_PATTERN
)


def parse_code_block(lines: List[str], start_idx: int) -> Optional[Tuple[CodeBlock, int]]:
    """Parse a code block starting from the given line index.
    
    Supports both fenced code blocks (```) and indented code blocks.
    Returns the code block element and the index of the next line after the block.
    """
    if start_idx >= len(lines):
        return None
    
    first_line = lines[start_idx]
    
    # Check for fenced code block
    fence_match = CODE_FENCE_START_PATTERN.match(first_line)
    if fence_match:
        return _parse_fenced_code_block(lines, start_idx, fence_match)
    
    # Check for indented code block (4 spaces or 1 tab)
    if CODE_INDENT_PATTERN.match(first_line):
        return _parse_indented_code_block(lines, start_idx)
    
    return None


def _parse_fenced_code_block(lines: List[str], start_idx: int, fence_match: re.Match) -> Optional[Tuple[CodeBlock, int]]:
    """Parse a fenced code block (```)."""
    language = fence_match.group(1)
    filename = fence_match.group(2).strip() if fence_match.group(2) else None
    
    # If filename looks like a language identifier, treat it as such
    if filename and not language and not ('.' in filename or '/' in filename):
        language = filename
        filename = None
    
    code_lines = []
    current_idx = start_idx + 1
    
    # Collect lines until closing fence
    while current_idx < len(lines):
        line = lines[current_idx]
        
        # Check for closing fence
        if CODE_FENCE_END_PATTERN.match(line):
            current_idx += 1
            break
        
        code_lines.append(line.rstrip())
        current_idx += 1
    
    # Join code lines
    code = '\n'.join(code_lines)
    
    code_block = CodeBlock(
        language=language,
        filename=filename,
        code=code
    )
    
    return code_block, current_idx


def _parse_indented_code_block(lines: List[str], start_idx: int) -> Optional[Tuple[CodeBlock, int]]:
    """Parse an indented code block (4 spaces or tab)."""
    code_lines = []
    current_idx = start_idx
    
    while current_idx < len(lines):
        line = lines[current_idx]
        
        # Empty line might be part of the code block
        if not line.strip():
            # Check if next line is still indented
            if current_idx + 1 < len(lines):
                next_line = lines[current_idx + 1]
                if CODE_INDENT_PATTERN.match(next_line):
                    code_lines.append('')
                    current_idx += 1
                    continue
            break
        
        # Check if line is indented
        indent_match = CODE_INDENT_CAPTURE_PATTERN.match(line)
        if indent_match:
            # Remove the indentation
            code_lines.append(indent_match.group(2).rstrip())
            current_idx += 1
        else:
            break
    
    if not code_lines:
        return None
    
    # Join code lines
    code = '\n'.join(code_lines)
    
    code_block = CodeBlock(
        language=None,
        filename=None,
        code=code
    )
    
    return code_block, current_idx 