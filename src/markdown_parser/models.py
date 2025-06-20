"""Data models for markdown elements."""

from typing import List, Optional, Dict, Any, Union
from enum import Enum
from pydantic import BaseModel, Field


class ElementType(str, Enum):
    """Types of markdown elements."""
    # Block elements
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    LIST = "list"
    QUOTE = "quote"
    CODE_BLOCK = "code_block"
    TABLE = "table"
    HORIZONTAL_RULE = "horizontal_rule"
    
    # Inline elements
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    
    # Custom elements
    ALIGN = "align"


class AlignType(str, Enum):
    """Alignment types for custom align element."""
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


class Element(BaseModel):
    """Base class for all markdown elements."""
    type: ElementType
    raw_text: Optional[str] = None
    

class InlineElement(Element):
    """Base class for inline elements."""
    content: str


class Text(InlineElement):
    """Plain text element."""
    type: ElementType = ElementType.TEXT


class Bold(InlineElement):
    """Bold text element."""
    type: ElementType = ElementType.BOLD


class Italic(InlineElement):
    """Italic text element."""
    type: ElementType = ElementType.ITALIC


class Code(InlineElement):
    """Inline code element."""
    type: ElementType = ElementType.CODE


class Link(InlineElement):
    """Link element."""
    type: ElementType = ElementType.LINK
    url: str
    title: Optional[str] = None


class Image(InlineElement):
    """Image element with extended attributes."""
    type: ElementType = ElementType.IMAGE
    content: str  # This will hold the alt text
    url: str
    title: Optional[str] = None
    size: Optional[float] = Field(None, ge=0, le=1)
    css: Optional[str] = None
    
    @property
    def alt(self) -> str:
        """Return content as alt text for backward compatibility."""
        return self.content
    
    @alt.setter
    def alt(self, value: str):
        """Set content when alt is assigned."""
        self.content = value


class BlockElement(Element):
    """Base class for block elements."""
    pass


class Heading(BlockElement):
    """Heading element."""
    type: ElementType = ElementType.HEADING
    level: int = Field(ge=1, le=6)
    content: list[InlineElement]


class Paragraph(BlockElement):
    """Paragraph element."""
    type: ElementType = ElementType.PARAGRAPH
    content: list[InlineElement]


class ListItem(BaseModel):
    """List item."""
    content: list[Union[InlineElement, "ListElement"]]
    indent_level: int = 0


class ListElement(BlockElement):
    """List element (ordered or unordered)."""
    type: ElementType = ElementType.LIST
    ordered: bool
    items: list[ListItem]
    start_number: Optional[int] = None  # For ordered lists


class Quote(BlockElement):
    """Quote block element."""
    type: ElementType = ElementType.QUOTE
    content: list[Union[BlockElement, InlineElement]]
    level: int = Field(default=1, ge=1)


class CodeBlock(BlockElement):
    """Code block element."""
    type: ElementType = ElementType.CODE_BLOCK
    language: Optional[str] = None
    filename: Optional[str] = None  # Extended feature
    code: str


class TableCell(BaseModel):
    """Table cell."""
    content: list[InlineElement]
    alignment: Optional[str] = None  # left, center, right


class TableRow(BaseModel):
    """Table row."""
    cells: list[TableCell]


class Table(BlockElement):
    """Table element."""
    type: ElementType = ElementType.TABLE
    header: TableRow
    alignments: list[Optional[str]]  # Alignment for each column
    rows: list[TableRow]


class HorizontalRule(BlockElement):
    """Horizontal rule element."""
    type: ElementType = ElementType.HORIZONTAL_RULE


class Align(BlockElement):
    """Custom alignment element."""
    type: ElementType = ElementType.ALIGN
    alignment: AlignType
    content: list[Union[BlockElement, InlineElement]]


class Document(BaseModel):
    """The complete markdown document."""
    blocks: list[BlockElement]
    metadata: Dict[str, Any] = Field(default_factory=dict)


# Update forward references
ListItem.model_rebuild()
Quote.model_rebuild()
Align.model_rebuild()

# Aliases for backward compatibility
List = ListElement 