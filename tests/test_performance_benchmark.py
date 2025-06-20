"""Performance benchmark tests for regex optimization."""

import time
import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from markdown_parser import parse


# Sample markdown content for benchmarking
SAMPLE_MARKDOWN = """
# Heading 1

This is a **bold** text with *italic* and `inline code`.

## Heading 2 

Here's a [link](http://example.com "title") and an ![image](image.jpg){size=0.5}.

### Lists

- Item 1 with **bold** text
- Item 2 with *italic* text  
- Item 3 with `code`

1. Ordered item 1
2. Ordered item 2 with [link](http://test.com)
3. Ordered item 3

### Code Block

```python
def hello_world():
    print("Hello, World!")
    return True
```

### Quote

> This is a quote with **bold** and *italic* text.
> It spans multiple lines.

### Table

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| **Bold** | *Italic* | `Code`   |
| [Link](http://example.com) | ![Image](img.jpg) | Normal text |

---

Final paragraph with mixed **bold**, *italic*, `code`, [links](http://example.com), and ![images](test.jpg).
"""


def test_parsing_performance():
    """Benchmark markdown parsing performance."""
    iterations = 100
    
    start_time = time.time()
    for _ in range(iterations):
        document = parse(SAMPLE_MARKDOWN)
        assert document is not None
    end_time = time.time()
    
    total_time = end_time - start_time
    avg_time = total_time / iterations
    
    print(f"\nPerformance Benchmark:")
    print(f"Total time for {iterations} iterations: {total_time:.4f}s")
    print(f"Average time per parse: {avg_time:.6f}s")
    print(f"Throughput: {iterations/total_time:.1f} parses/second")
    
    # Performance assertion - should parse within reasonable time
    assert avg_time < 0.01, f"Parsing too slow: {avg_time:.6f}s per document"


def test_regex_heavy_content():
    """Test performance with regex-heavy content."""
    regex_heavy = """
This text has **many** *different* `inline` **formatting** *elements* `scattered` **throughout** *the* `text`.

[Link1](url1) and ![img1](img1.jpg) and [Link2](url2) and ![img2](img2.jpg).

**Bold1** *italic1* `code1` **bold2** *italic2* `code2` **bold3** *italic3* `code3`.

Multiple [links](http://example.com "title") with ![images](test.jpg){size=0.8} everywhere.
"""
    
    iterations = 50
    start_time = time.time()
    
    for _ in range(iterations):
        document = parse(regex_heavy)
        assert document is not None
        
    end_time = time.time()
    avg_time = (end_time - start_time) / iterations
    
    print(f"\nRegex-heavy content benchmark:")
    print(f"Average time per parse: {avg_time:.6f}s")
    
    # Should handle regex-heavy content efficiently
    assert avg_time < 0.005, f"Regex-heavy parsing too slow: {avg_time:.6f}s"


if __name__ == "__main__":
    test_parsing_performance()
    test_regex_heavy_content()
    print("\n✅ All performance benchmarks passed!") 