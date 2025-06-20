"""Example usage of the markdown parser."""

from markdown_parser import parse, export_markdown
from markdown_parser import Heading, Paragraph, ListElement, CodeBlock, Table


def main():
    # Example markdown text
    markdown_text = """# Welcome to Markdown Parser

This is a **bold** text and this is *italic*. Here's some `inline code`.

## Features

- Parse markdown to structured objects
- Support for standard markdown elements
- Extended syntax support
  - Nested lists work too!
  - With multiple levels

### Links and Images

Check out [this link](https://example.com "Example Site").

![Example Image](https://example.com/image.png){size=0.5, css="border-radius: 10px;"}

### Code Blocks

```python example.py
def hello_world():
    print("Hello, World!")
```

### Tables

| Header 1 | Header 2 | Header 3 |
|----------|:--------:|---------:|
| Left     | Center   | Right    |
| Data 1   | Data 2   | Data 3   |

### Quotes

> This is a quote
> It can span multiple lines

### Custom Alignment

<Center>This text is centered</Center>

<Align right>This text is right-aligned</Align>
"""

    # Parse the markdown
    print("Parsing markdown...")
    document = parse(markdown_text)
    
    # Display document structure
    print("\nDocument structure:")
    for i, block in enumerate(document.blocks):
        print(f"{i+1}. {type(block).__name__}")
        
        if isinstance(block, Heading):
            content_text = ''.join(elem.content for elem in block.content if hasattr(elem, 'content'))
            print(f"   Level {block.level}: {content_text}")
        elif isinstance(block, ListElement):
            print(f"   {'Ordered' if block.ordered else 'Unordered'} list with {len(block.items)} items")
        elif isinstance(block, CodeBlock):
            print(f"   Language: {block.language or 'none'}")
            if block.filename:
                print(f"   Filename: {block.filename}")
        elif isinstance(block, Table):
            print(f"   {len(block.header.cells)} columns, {len(block.rows)} data rows")
    
    # Export back to markdown
    print("\n\nExporting to pure markdown (without extensions)...")
    pure_markdown = export_markdown(document, include_extensions=False)
    print("\nPure markdown:")
    print("-" * 50)
    print(pure_markdown)
    
    print("\n\nExporting with extensions...")
    extended_markdown = export_markdown(document, include_extensions=True)
    print("\nExtended markdown:")
    print("-" * 50)
    print(extended_markdown)


if __name__ == "__main__":
    main() 