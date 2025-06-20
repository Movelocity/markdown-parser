 #!/usr/bin/env python3
"""
Markdown Parser Demo
演示markdown解析器的完整功能
"""

from markdown_parser import parse, export_markdown, export_html
from pathlib import Path


def demo_basic_parsing():
    """演示基本解析功能"""
    print("=" * 60)
    print("基本解析功能演示")
    print("=" * 60)
    
    markdown_text = """# Hello World

这是一个**粗体**和*斜体*的示例。

## 列表示例
- 第一项
- 第二项
  - 嵌套项目

```python
def hello():
    print("Hello, World!")
```

> 这是一个引用块
> 包含多行内容

[链接示例](https://example.com "链接标题")
"""
    
    print("📝 原始Markdown:")
    print(markdown_text)
    
    # 解析
    document = parse(markdown_text)
    
    print(f"\n✅ 解析结果: {len(document.blocks)} 个块级元素")
    for i, block in enumerate(document.blocks, 1):
        print(f"  {i}. {type(block).__name__}")
    
    return document


def demo_extended_syntax():
    """演示扩展语法功能"""
    print("\n" + "=" * 60)
    print("扩展语法功能演示")
    print("=" * 60)
    
    extended_text = """# 扩展语法演示

## 带标题的代码块
```python app.py
from markdown_parser import parse

doc = parse("# Hello")
```

## 图片扩展
![示例图片](https://example.com/img.png){size=0.8, css="border-radius: 10px;"}

## 文本对齐
<Center>这段文字居中显示</Center>
<Align right>这段文字右对齐</Align>

## 表格
| 功能 | 状态 |
|------|:----:|
| 解析 | ✅ |
| 导出 | ✅ |
"""
    
    print("📝 扩展语法Markdown:")
    print(extended_text)
    
    document = parse(extended_text)
    
    print(f"\n✅ 解析结果: {len(document.blocks)} 个块级元素")
    for i, block in enumerate(document.blocks, 1):
        print(f"  {i}. {type(block).__name__}")
    
    return document


def demo_export_functionality():
    """演示导出功能"""
    print("\n" + "=" * 60)
    print("导出功能演示")
    print("=" * 60)
    
    # 使用扩展语法示例
    sample_text = """# Markdown Parser Demo

这是一个功能完整的markdown解析器。

## 特性
- **标准语法**支持
- *扩展语法*支持
- `HTML导出`功能

```python demo.py
print("Hello, World!")
```

![Logo](https://example.com/logo.png){size=0.5}

<Center>**项目完成！**</Center>
"""
    
    document = parse(sample_text)
    
    # 导出为markdown（标准语法）
    print("📄 导出为标准Markdown:")
    standard_md = export_markdown(document, include_extensions=False)
    print(standard_md)
    
    print("\n" + "-" * 40)
    
    # 导出为markdown（包含扩展）
    print("🔧 导出为扩展Markdown:")
    extended_md = export_markdown(document, include_extensions=True)
    print(extended_md)
    
    print("\n" + "-" * 40)
    
    # 导出为HTML
    print("🌐 导出为HTML:")
    html_content = export_html(document, include_extensions=True, title="Demo Page")
    
    # 只显示body部分，避免输出过长
    body_start = html_content.find('<body>') + 6
    body_end = html_content.find('</body>')
    body_content = html_content[body_start:body_end].strip()
    
    print(body_content)
    
    # 保存完整HTML文件
    output_file = Path("demo_output.html")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"\n💾 完整HTML已保存至: {output_file}")


def demo_file_processing():
    """演示文件处理功能"""
    print("\n" + "=" * 60)
    print("文件处理演示")
    print("=" * 60)
    
    test_files = [
        "tests/test_files/basic_syntax.md",
        "tests/test_files/extended_syntax.md",
        "tests/test_files/complex_document.md"
    ]
    
    for file_path in test_files:
        path = Path(file_path)
        if not path.exists():
            print(f"❌ 文件不存在: {file_path}")
            continue
        
        print(f"\n📁 处理文件: {path.name}")
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        document = parse(content)
        print(f"   解析出 {len(document.blocks)} 个块级元素")
        
        # 生成HTML文件
        html_content = export_html(document, title=f"解析结果 - {path.name}")
        html_output = path.with_suffix('.demo.html')
        
        with open(html_output, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"   ✅ HTML已生成: {html_output}")


def main():
    """主演示函数"""
    print("🚀 Markdown Parser 功能演示")
    print("开发工具: uv + Python")
    print("项目特色: 完整的markdown解析和HTML导出功能")
    
    try:
        # 基本功能演示
        demo_basic_parsing()
        
        # 扩展语法演示
        demo_extended_syntax()
        
        # 导出功能演示
        demo_export_functionality()
        
        # 文件处理演示
        demo_file_processing()
        
        print("\n" + "=" * 60)
        print("✨ 演示完成！所有功能正常工作")
        print("=" * 60)
        
        print("\n📚 使用说明:")
        print("from markdown_parser import parse, export_markdown, export_html")
        print("document = parse(markdown_text)")
        print("html = export_html(document)")
        
    except Exception as e:
        print(f"\n❌ 演示过程中出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()