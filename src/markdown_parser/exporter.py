"""Markdown exporter for converting parsed documents back to markdown."""

from typing import List
from .models import (
    Document,
    BlockElement,
    InlineElement,
    Heading,
    Paragraph,
    List,
    ListItem,
    Quote,
    CodeBlock,
    Table,
    HorizontalRule,
    Text,
    Bold,
    Italic,
    Code,
    Link,
    Image,
    Align,
    ElementType,
)


def export_markdown(document: Document, include_extensions: bool = True) -> str:
    """Export a parsed document back to markdown.
    
    Args:
        document: The parsed document
        include_extensions: Whether to include custom extensions
        
    Returns:
        Markdown text
    """
    lines = []
    
    for i, block in enumerate(document.blocks):
        # Add spacing between blocks
        if i > 0 and not isinstance(document.blocks[i-1], HorizontalRule):
            lines.append("")
        
        block_text = _export_block(block, include_extensions)
        if block_text:
            lines.append(block_text)
    
    return '\n'.join(lines)


def _export_block(block: BlockElement, include_extensions: bool) -> str:
    """Export a single block element."""
    if isinstance(block, Heading):
        return _export_heading(block)
    elif isinstance(block, Paragraph):
        return _export_paragraph(block)
    elif isinstance(block, List):
        return _export_list(block)
    elif isinstance(block, Quote):
        return _export_quote(block)
    elif isinstance(block, CodeBlock):
        return _export_code_block(block, include_extensions)
    elif isinstance(block, Table):
        return _export_table(block)
    elif isinstance(block, HorizontalRule):
        return "---"
    elif isinstance(block, Align):
        return _export_align(block, include_extensions)
    else:
        return ""


def _export_heading(heading: Heading) -> str:
    """Export a heading."""
    prefix = '#' * heading.level
    content = _export_inline_elements(heading.content)
    return f"{prefix} {content}"


def _export_paragraph(paragraph: Paragraph) -> str:
    """Export a paragraph."""
    return _export_inline_elements(paragraph.content)


def _export_list(list_elem: List, indent: int = 0) -> str:
    """Export a list."""
    lines = []
    
    for i, item in enumerate(list_elem.items):
        # Determine marker
        if list_elem.ordered:
            number = list_elem.start_number + i if list_elem.start_number else i + 1
            marker = f"{number}."
        else:
            marker = "-"
        
        # Add indentation
        prefix = "  " * (indent + item.indent_level) + marker + " "
        
        # Export item content
        item_lines = []
        for element in item.content:
            if isinstance(element, List):
                # Nested list
                nested_text = _export_list(element, indent + item.indent_level + 1)
                item_lines.extend(nested_text.split('\n'))
            else:
                # Inline content
                text = _export_inline_element(element)
                if text:
                    item_lines.append(text)
        
        # Format the item
        if item_lines:
            lines.append(prefix + item_lines[0])
            for line in item_lines[1:]:
                lines.append("  " * (indent + item.indent_level + 1) + line)
    
    return '\n'.join(lines)


def _export_quote(quote: Quote) -> str:
    """Export a quote block."""
    prefix = '>' * quote.level + ' '
    
    # For now, treat content as inline elements
    content = _export_inline_elements(quote.content)
    
    # Add prefix to each line
    lines = content.split('\n')
    return '\n'.join(prefix + line for line in lines)


def _export_code_block(code_block: CodeBlock, include_extensions: bool) -> str:
    """Export a code block."""
    if code_block.language or code_block.filename:
        # Fenced code block
        info = code_block.language or ""
        if include_extensions and code_block.filename:
            info += f" {code_block.filename}"
        
        lines = ["```" + info]
        lines.extend(code_block.code.split('\n'))
        lines.append("```")
        return '\n'.join(lines)
    else:
        # Indented code block
        lines = []
        for line in code_block.code.split('\n'):
            lines.append("    " + line)
        return '\n'.join(lines)


def _export_table(table: Table) -> str:
    """Export a table."""
    lines = []
    
    # Header
    header_cells = [_export_inline_elements(cell.content) for cell in table.header.cells]
    lines.append("| " + " | ".join(header_cells) + " |")
    
    # Separator
    separators = []
    for i, alignment in enumerate(table.alignments):
        if alignment == 'left':
            separators.append(":---")
        elif alignment == 'center':
            separators.append(":---:")
        elif alignment == 'right':
            separators.append("---:")
        else:
            separators.append("---")
    lines.append("| " + " | ".join(separators) + " |")
    
    # Data rows
    for row in table.rows:
        cells = [_export_inline_elements(cell.content) for cell in row.cells]
        lines.append("| " + " | ".join(cells) + " |")
    
    return '\n'.join(lines)


def _export_align(align: Align, include_extensions: bool) -> str:
    """Export an align element."""
    if not include_extensions:
        # Just export the content without alignment
        return _export_inline_elements(align.content)
    
    # Determine tag name
    tag_map = {
        'left': 'Left',
        'center': 'Center',
        'right': 'Right',
    }
    tag = tag_map.get(align.alignment.value, 'Align')
    
    content = _export_inline_elements(align.content)
    
    if tag == 'Align':
        return f"<Align {align.alignment.value}>{content}</Align>"
    else:
        return f"<{tag}>{content}</{tag}>"


def _export_inline_elements(elements: List[InlineElement]) -> str:
    """Export a list of inline elements."""
    return ''.join(_export_inline_element(elem) for elem in elements)


def _export_inline_element(element: InlineElement) -> str:
    """Export a single inline element."""
    if isinstance(element, Text):
        return element.content
    elif isinstance(element, Bold):
        return f"**{element.content}**"
    elif isinstance(element, Italic):
        return f"*{element.content}*"
    elif isinstance(element, Code):
        return f"`{element.content}`"
    elif isinstance(element, Link):
        text = f"[{element.content}]({element.url}"
        if element.title:
            text += f' "{element.title}"'
        text += ")"
        return text
    elif isinstance(element, Image):
        text = f"![{element.alt}]({element.url})"
        if element.size is not None or element.css:
            attrs = []
            if element.size is not None:
                attrs.append(f"size={element.size}")
            if element.css:
                attrs.append(f'css="{element.css}"')
            text += "{" + ", ".join(attrs) + "}"
        return text
    else:
        return "" 