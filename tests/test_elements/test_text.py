"""Tests for text format parsing."""

from markdown_parser.elements.text import parse_inline_elements
from markdown_parser import Text, Bold, Italic, Code, Link, Image


class TestTextParsing:
    """Test inline text element parsing."""
    
    def test_parse_plain_text(self):
        """Test parsing plain text."""
        elements = parse_inline_elements("Just plain text")
        assert len(elements) == 1
        assert isinstance(elements[0], Text)
        assert elements[0].content == "Just plain text"
    
    def test_parse_bold(self):
        """Test parsing bold text."""
        # Double asterisk
        elements = parse_inline_elements("**bold text**")
        assert len(elements) == 1
        assert isinstance(elements[0], Bold)
        assert elements[0].content == "bold text"
        
        # Double underscore
        elements = parse_inline_elements("__bold text__")
        assert len(elements) == 1
        assert isinstance(elements[0], Bold)
        assert elements[0].content == "bold text"
    
    def test_parse_italic(self):
        """Test parsing italic text."""
        # Single asterisk
        elements = parse_inline_elements("*italic text*")
        assert len(elements) == 1
        assert isinstance(elements[0], Italic)
        assert elements[0].content == "italic text"
        
        # Single underscore
        elements = parse_inline_elements("_italic text_")
        assert len(elements) == 1
        assert isinstance(elements[0], Italic)
        assert elements[0].content == "italic text"
    
    def test_parse_code(self):
        """Test parsing inline code."""
        elements = parse_inline_elements("`code snippet`")
        assert len(elements) == 1
        assert isinstance(elements[0], Code)
        assert elements[0].content == "code snippet"
    
    def test_parse_link(self):
        """Test parsing links."""
        # Simple link
        elements = parse_inline_elements("[link text](https://example.com)")
        assert len(elements) == 1
        assert isinstance(elements[0], Link)
        assert elements[0].content == "link text"
        assert elements[0].url == "https://example.com"
        assert elements[0].title is None
        
        # Link with title
        elements = parse_inline_elements('[link text](https://example.com "Title")')
        assert len(elements) == 1
        assert isinstance(elements[0], Link)
        assert elements[0].content == "link text"
        assert elements[0].url == "https://example.com"
        assert elements[0].title == "Title"
    
    def test_parse_image(self):
        """Test parsing images."""
        # Simple image
        elements = parse_inline_elements("![alt text](image.png)")
        assert len(elements) == 1
        assert isinstance(elements[0], Image)
        assert elements[0].alt == "alt text"
        assert elements[0].url == "image.png"
        assert elements[0].size is None
        assert elements[0].css is None
        
        # Image with size
        elements = parse_inline_elements("![alt text](image.png){size=0.5}")
        assert len(elements) == 1
        assert isinstance(elements[0], Image)
        assert elements[0].alt == "alt text"
        assert elements[0].url == "image.png"
        assert elements[0].size == 0.5
        
        # Image with css
        elements = parse_inline_elements('![alt text](image.png){css="border: 1px solid;"}')
        assert len(elements) == 1
        assert isinstance(elements[0], Image)
        assert elements[0].css == "border: 1px solid;"
        
        # Image with both
        elements = parse_inline_elements('![alt text](image.png){size=0.75, css="rounded"}')
        assert len(elements) == 1
        assert isinstance(elements[0], Image)
        assert elements[0].size == 0.75
        assert elements[0].css == "rounded"
    
    def test_parse_mixed_elements(self):
        """Test parsing mixed inline elements."""
        text = "This has **bold**, *italic*, `code`, and [a link](url)."
        elements = parse_inline_elements(text)
        
        assert len(elements) == 8
        assert isinstance(elements[0], Text)
        assert elements[0].content == "This has "
        
        assert isinstance(elements[1], Bold)
        assert elements[1].content == "bold"
        
        assert isinstance(elements[2], Text)
        assert elements[2].content == ", "
        
        assert isinstance(elements[3], Italic)
        assert elements[3].content == "italic"
        
        assert isinstance(elements[4], Text)
        assert elements[4].content == ", "
        
        assert isinstance(elements[5], Code)
        assert elements[5].content == "code"
        
        assert isinstance(elements[6], Text)
        assert elements[6].content == ", and "
        
        assert isinstance(elements[7], Link)
        assert elements[7].content == "a link"
        assert elements[7].url == "url"
    
    def test_nested_formatting(self):
        """Test that nested formatting is not parsed (markdown doesn't support it)."""
        # Bold inside italic - should only parse the outer element
        elements = parse_inline_elements("*italic with **bold** inside*")
        assert len(elements) == 1
        assert isinstance(elements[0], Italic)
        assert elements[0].content == "italic with **bold** inside" 