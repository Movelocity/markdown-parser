"""Tests for the main parser."""

from markdown_parser import parse, Document
from markdown_parser import Heading, Paragraph, ListElement, Quote, CodeBlock, Table, HorizontalRule


class TestParser:
    """Test the main parser functionality."""
    
    def test_parse_empty_document(self):
        """Test parsing an empty document."""
        doc = parse("")
        assert isinstance(doc, Document)
        assert len(doc.blocks) == 0
    
    def test_parse_heading(self):
        """Test parsing headings."""
        markdown = """# Heading 1
## Heading 2
### Heading 3"""
        
        doc = parse(markdown)
        assert len(doc.blocks) == 3
        
        assert isinstance(doc.blocks[0], Heading)
        assert doc.blocks[0].level == 1
        
        assert isinstance(doc.blocks[1], Heading)
        assert doc.blocks[1].level == 2
        
        assert isinstance(doc.blocks[2], Heading)
        assert doc.blocks[2].level == 3
    
    def test_parse_paragraph(self):
        """Test parsing paragraphs."""
        markdown = """This is a paragraph.

This is another paragraph with **bold** and *italic* text."""
        
        doc = parse(markdown)
        assert len(doc.blocks) == 2
        
        assert isinstance(doc.blocks[0], Paragraph)
        assert isinstance(doc.blocks[1], Paragraph)
    
    def test_parse_list(self):
        """Test parsing lists."""
        markdown = """- Item 1
- Item 2
- Item 3

1. First
2. Second
3. Third"""
        
        doc = parse(markdown)
        assert len(doc.blocks) == 2
        
        assert isinstance(doc.blocks[0], ListElement)
        assert not doc.blocks[0].ordered
        assert len(doc.blocks[0].items) == 3
        
        assert isinstance(doc.blocks[1], ListElement)
        assert doc.blocks[1].ordered
        assert len(doc.blocks[1].items) == 3
    
    def test_parse_code_block(self):
        """Test parsing code blocks."""
        markdown = '''```python
def hello():
    print("Hello")
```

    indented code
    block'''
        
        doc = parse(markdown)
        assert len(doc.blocks) == 2
        
        assert isinstance(doc.blocks[0], CodeBlock)
        assert doc.blocks[0].language == "python"
        
        assert isinstance(doc.blocks[1], CodeBlock)
        assert doc.blocks[1].language is None
    
    def test_parse_quote(self):
        """Test parsing quotes."""
        markdown = """> This is a quote
> It spans multiple lines"""
        
        doc = parse(markdown)
        assert len(doc.blocks) == 1
        
        assert isinstance(doc.blocks[0], Quote)
        assert doc.blocks[0].level == 1
    
    def test_parse_table(self):
        """Test parsing tables."""
        markdown = """| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |"""
        
        doc = parse(markdown)
        assert len(doc.blocks) == 1
        
        assert isinstance(doc.blocks[0], Table)
        assert len(doc.blocks[0].header.cells) == 2
        assert len(doc.blocks[0].rows) == 1
    
    def test_parse_horizontal_rule(self):
        """Test parsing horizontal rules."""
        markdown = """Text before

---

Text after"""
        
        doc = parse(markdown)
        assert len(doc.blocks) == 3
        
        assert isinstance(doc.blocks[0], Paragraph)
        assert isinstance(doc.blocks[1], HorizontalRule)
        assert isinstance(doc.blocks[2], Paragraph)
    
    def test_parse_mixed_document(self):
        """Test parsing a document with mixed elements."""
        markdown = """# Title

This is a paragraph with **bold** text.

## Section

- List item 1
- List item 2

```python
code block
```

> Quote text

---

End of document."""
        
        doc = parse(markdown)
        
        # Verify we have the expected number and types of blocks
        assert len(doc.blocks) == 8
        assert isinstance(doc.blocks[0], Heading)
        assert isinstance(doc.blocks[1], Paragraph)
        assert isinstance(doc.blocks[2], Heading)
        assert isinstance(doc.blocks[3], ListElement)
        assert isinstance(doc.blocks[4], CodeBlock)
        assert isinstance(doc.blocks[5], Quote)
        assert isinstance(doc.blocks[6], HorizontalRule)
        assert isinstance(doc.blocks[7], Paragraph) 