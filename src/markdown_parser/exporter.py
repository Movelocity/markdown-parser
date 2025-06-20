"""Markdown exporter for converting parsed documents back to markdown."""

from typing import List
from .models import (
    Document,
    BlockElement,
    InlineElement,
    Heading,
    Paragraph,
    ListElement,
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
    elif isinstance(block, ListElement):
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


def _export_list(list_elem: ListElement, indent: int = 0) -> str:
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
            if isinstance(element, ListElement):
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


# HTML Export functionality
def export_html(document: Document, include_extensions: bool = True, title: str = "Document") -> str:
    """Export a parsed document to HTML.
    
    Args:
        document: The parsed document
        include_extensions: Whether to include custom extensions
        title: Title for the HTML document
        
    Returns:
        HTML text
    """
    html_parts = []
    
    # HTML document structure
    html_parts.append(f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{_escape_html(title)}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #24292f;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1, h2, h3, h4, h5, h6 {{
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
            line-height: 1.25;
        }}
        h1 {{ font-size: 2em; border-bottom: 1px solid #d0d7de; padding-bottom: 10px; }}
        h2 {{ font-size: 1.5em; border-bottom: 1px solid #d0d7de; padding-bottom: 8px; }}
        h3 {{ font-size: 1.25em; }}
        p {{ margin-bottom: 16px; }}
        ul, ol {{ margin-bottom: 16px; padding-left: 30px; }}
        li {{ margin-bottom: 4px; }}
        blockquote {{
            padding: 0 16px;
            color: #656d76;
            border-left: 4px solid #d0d7de;
            margin: 16px 0;
        }}
        code {{
            background-color: #f6f8fa;
            border-radius: 6px;
            font-size: 85%;
            margin: 0;
            padding: 0.2em 0.4em;
            font-family: ui-monospace, SFMono-Regular, "SF Mono", Monaco, Menlo, monospace;
        }}
        pre {{
            background-color: #f6f8fa;
            border-radius: 6px;
            font-size: 85%;
            line-height: 1.45;
            overflow: auto;
            padding: 16px;
            margin: 16px 0;
        }}
        pre code {{
            background-color: transparent;
            border: 0;
            font-size: 100%;
            margin: 0;
            padding: 0;
        }}
        table {{
            border-collapse: collapse;
            border-spacing: 0;
            width: 100%;
            margin: 16px 0;
        }}
        th, td {{
            border: 1px solid #d0d7de;
            padding: 6px 13px;
        }}
        th {{
            background-color: #f6f8fa;
            font-weight: 600;
        }}
        img {{
            max-width: 100%;
            height: auto;
        }}
        hr {{
            border: none;
            border-top: 1px solid #d0d7de;
            margin: 24px 0;
        }}
        .text-center {{ text-align: center; }}
        .text-left {{ text-align: left; }}
        .text-right {{ text-align: right; }}
    </style>
</head>
<body>""")
    
    # Export blocks
    for block in document.blocks:
        html_content = _export_block_html(block, include_extensions)
        if html_content:
            html_parts.append(html_content)
    
    html_parts.append("</body>\n</html>")
    
    return '\n'.join(html_parts)


def _export_block_html(block: BlockElement, include_extensions: bool) -> str:
    """Export a single block element to HTML."""
    if isinstance(block, Heading):
        return _export_heading_html(block)
    elif isinstance(block, Paragraph):
        return _export_paragraph_html(block)
    elif isinstance(block, ListElement):
        return _export_list_html(block)
    elif isinstance(block, Quote):
        return _export_quote_html(block)
    elif isinstance(block, CodeBlock):
        return _export_code_block_html(block, include_extensions)
    elif isinstance(block, Table):
        return _export_table_html(block)
    elif isinstance(block, HorizontalRule):
        return "<hr>"
    elif isinstance(block, Align):
        return _export_align_html(block, include_extensions)
    else:
        return ""


def _export_heading_html(heading: Heading) -> str:
    """Export a heading to HTML."""
    content = _export_inline_elements_html(heading.content)
    return f"<h{heading.level}>{content}</h{heading.level}>"


def _export_paragraph_html(paragraph: Paragraph) -> str:
    """Export a paragraph to HTML."""
    content = _export_inline_elements_html(paragraph.content)
    return f"<p>{content}</p>"


def _export_list_html(list_elem: ListElement) -> str:
    """Export a list to HTML."""
    tag = "ol" if list_elem.ordered else "ul"
    start_attr = f' start="{list_elem.start_number}"' if list_elem.ordered and list_elem.start_number else ""
    
    items_html = []
    for item in list_elem.items:
        item_content = []
        for element in item.content:
            if isinstance(element, ListElement):
                # Nested list
                item_content.append(_export_list_html(element))
            else:
                # Inline content
                item_content.append(_export_inline_element_html(element))
        
        items_html.append(f"<li>{''.join(item_content)}</li>")
    
    return f"<{tag}{start_attr}>{''.join(items_html)}</{tag}>"


def _export_quote_html(quote: Quote) -> str:
    """Export a quote block to HTML."""
    content = _export_inline_elements_html(quote.content)
    return f"<blockquote>{content}</blockquote>"


def _export_code_block_html(code_block: CodeBlock, include_extensions: bool) -> str:
    """Export a code block to HTML."""
    escaped_code = _escape_html(code_block.code)
    
    if code_block.language:
        title_html = ""
        if include_extensions and code_block.filename:
            title_html = f'<div style="background-color: #f1f3f4; padding: 8px 16px; margin: -16px -16px 16px -16px; border-bottom: 1px solid #d0d7de; font-weight: 600;">{_escape_html(code_block.filename)}</div>'
        
        return f'<pre>{title_html}<code class="language-{code_block.language}">{escaped_code}</code></pre>'
    else:
        return f"<pre><code>{escaped_code}</code></pre>"


def _export_table_html(table: Table) -> str:
    """Export a table to HTML."""
    html_parts = ["<table>"]
    
    # Header
    header_cells = []
    for i, cell in enumerate(table.header.cells):
        alignment = table.alignments[i] if i < len(table.alignments) else None
        style = ""
        if alignment:
            style = f' style="text-align: {alignment};"'
        content = _export_inline_elements_html(cell.content)
        header_cells.append(f"<th{style}>{content}</th>")
    
    html_parts.append(f"<thead><tr>{''.join(header_cells)}</tr></thead>")
    
    # Rows
    if table.rows:
        row_htmls = []
        for row in table.rows:
            cells = []
            for i, cell in enumerate(row.cells):
                alignment = table.alignments[i] if i < len(table.alignments) else None
                style = ""
                if alignment:
                    style = f' style="text-align: {alignment};"'
                content = _export_inline_elements_html(cell.content)
                cells.append(f"<td{style}>{content}</td>")
            row_htmls.append(f"<tr>{''.join(cells)}</tr>")
        
        html_parts.append(f"<tbody>{''.join(row_htmls)}</tbody>")
    
    html_parts.append("</table>")
    return ''.join(html_parts)


def _export_align_html(align: Align, include_extensions: bool) -> str:
    """Export an align element to HTML."""
    if not include_extensions:
        # Just export the content without alignment
        return _export_inline_elements_html(align.content)
    
    css_class = f"text-{align.alignment.value}"
    content = _export_inline_elements_html(align.content)
    return f'<div class="{css_class}">{content}</div>'


def _export_inline_elements_html(elements: List[InlineElement]) -> str:
    """Export a list of inline elements to HTML."""
    return ''.join(_export_inline_element_html(elem) for elem in elements)


def _export_inline_element_html(element: InlineElement) -> str:
    """Export a single inline element to HTML."""
    if isinstance(element, Text):
        return _escape_html(element.content)
    elif isinstance(element, Bold):
        return f"<strong>{_escape_html(element.content)}</strong>"
    elif isinstance(element, Italic):
        return f"<em>{_escape_html(element.content)}</em>"
    elif isinstance(element, Code):
        return f"<code>{_escape_html(element.content)}</code>"
    elif isinstance(element, Link):
        url = _escape_html(element.url)
        content = _escape_html(element.content)
        title_attr = f' title="{_escape_html(element.title)}"' if element.title else ""
        return f'<a href="{url}"{title_attr}>{content}</a>'
    elif isinstance(element, Image):
        url = _escape_html(element.url)
        alt = _escape_html(element.alt)
        title_attr = f' title="{_escape_html(element.title)}"' if element.title else ""
        
        # Handle custom attributes
        style_parts = []
        if element.size is not None:
            style_parts.append(f"width: {element.size * 100}%")
        if element.css:
            style_parts.append(element.css)
        
        style_attr = f' style="{"; ".join(style_parts)}"' if style_parts else ""
        
        return f'<img src="{url}" alt="{alt}"{title_attr}{style_attr}>'
    else:
        return ""


def _escape_html(text: str) -> str:
    """Escape HTML special characters."""
    if not text:
        return ""
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&#x27;")) 