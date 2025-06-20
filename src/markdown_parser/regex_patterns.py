"""Centralized regex patterns for markdown parsing.

All regex patterns are pre-compiled for better performance and to eliminate duplication.
"""

import re

# ============================================================================
# INLINE ELEMENTS
# ============================================================================

# Images
IMAGE_PATTERN = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)(\{[^}]+\})?')
IMAGE_FULL_PATTERN = re.compile(r'^!\[([^\]]*)\]\(([^)]+)\)(\{[^}]+\})?$')

# Links  
LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+?)(?:\s+"([^"]+)")?\)')
LINK_FULL_PATTERN = re.compile(r'^\[([^\]]+)\]\(([^)]+?)(?:\s+"([^"]+)")?\)$')

# Text formatting
BOLD_PATTERN = re.compile(r'(\*\*|__)([^*_]+?)\1')
ITALIC_ASTERISK_PATTERN = re.compile(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)')
ITALIC_UNDERSCORE_PATTERN = re.compile(r'(?<!_)_(?!_)([^_]+?)(?<!_)_(?!_)')
INLINE_CODE_PATTERN = re.compile(r'`([^`]+)`')

# Image attributes
IMAGE_SIZE_ATTR_PATTERN = re.compile(r'size\s*=\s*([0-9.]+)')
IMAGE_CSS_ATTR_PATTERN = re.compile(r'css\s*=\s*"([^"]+)"')

# ============================================================================
# BLOCK ELEMENTS
# ============================================================================

# Headings
HEADING_PATTERN = re.compile(r'^(#{1,6})\s+(.+)$')
HEADING_TRAILING_HASH_PATTERN = re.compile(r'\s*#+\s*$')

# Code blocks
CODE_FENCE_START_PATTERN = re.compile(r'^```(\w+)?\s*(.*)$')
CODE_FENCE_END_PATTERN = re.compile(r'^```\s*$')
CODE_INDENT_PATTERN = re.compile(r'^(    |\t)')
CODE_INDENT_CAPTURE_PATTERN = re.compile(r'^(    |\t)(.*)$')

# Lists
UNORDERED_LIST_PATTERN = re.compile(r'^(\s*)([-*+])\s+(.*)$')
ORDERED_LIST_PATTERN = re.compile(r'^(\s*)(\d+)([.)])\s+(.*)$')

# Lists (simple matching)
UNORDERED_LIST_SIMPLE_PATTERN = re.compile(r'^\s*[-*+]\s+')
ORDERED_LIST_SIMPLE_PATTERN = re.compile(r'^\s*\d+[.)]\s+')

# Quotes
QUOTE_PREFIX_PATTERN = re.compile(r'^\s*>\s?')

# Tables
TABLE_SEPARATOR_PATTERN = re.compile(r'^:?-{3,}:?$')

# Custom elements
ALIGN_TAG_PATTERN = re.compile(r'^<Align\s+(left|center|right)>(.*)$', re.IGNORECASE)
CUSTOM_TAG_PATTERN = re.compile(r'^<(Align|Left|Center|Right)', re.IGNORECASE)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def is_indented_line(line: str) -> bool:
    """Check if a line is indented (4 spaces or 1 tab)."""
    return CODE_INDENT_PATTERN.match(line) is not None

def is_list_item(line: str) -> bool:
    """Check if a line is a list item."""
    return (UNORDERED_LIST_SIMPLE_PATTERN.match(line) is not None or 
            ORDERED_LIST_SIMPLE_PATTERN.match(line) is not None)

def is_custom_tag(line: str) -> bool:
    """Check if a line starts with a custom tag."""
    return CUSTOM_TAG_PATTERN.match(line) is not None

def remove_quote_prefix(line: str, count: int = 1) -> str:
    """Remove quote prefix from a line."""
    return QUOTE_PREFIX_PATTERN.sub('', line, count=count) 