# Markdown Parser

一个将 Markdown 文本转换为结构化 Python 对象的解析器，便于其他项目使用和处理 Markdown 文档。

## 特性

- ✅ 支持标准 Markdown 语法
  - 标题 (1-6 级)
  - 段落
  - 粗体、斜体、行内代码
  - 链接和图片
  - 有序/无序列表（支持嵌套）
  - 引用块
  - 代码块（围栏式和缩进式）
  - 表格
  - 水平分割线

- ✅ 扩展语法支持
  - 图片尺寸和样式：`![alt](url){size=0.5, css="border-radius: 10px;"}`
  - 代码块标题：````python filename.py`
  - 自定义对齐：`<Center>居中内容</Center>`、`<Left>`、`<Right>`、`<Align center>`

- ✅ 导出功能
  - 导出纯 Markdown（不含扩展语法）
  - 保留扩展语法导出

## 安装

```bash
# 克隆项目
git clone <repository-url>
cd markdown-parser

# 使用 uv 安装依赖
uv pip install -e ".[dev]"
```

## 使用示例

```python
from markdown_parser import parse, export_markdown

# 解析 Markdown
markdown_text = """
# 标题

这是一个包含 **粗体** 和 *斜体* 的段落。

- 列表项 1
- 列表项 2

```python
def hello():
    print("Hello, World!")
```
"""

document = parse(markdown_text)

# 访问结构化数据
for block in document.blocks:
    print(type(block).__name__)

# 导出为纯 Markdown
pure_md = export_markdown(document, include_extensions=False)

# 导出包含扩展语法
extended_md = export_markdown(document, include_extensions=True)
```

## 项目结构

```
markdown-parser/
├── src/
│   └── markdown_parser/
│       ├── __init__.py         # 包初始化和 API 导出
│       ├── parser.py           # 主解析器
│       ├── models.py           # 数据模型定义
│       ├── exporter.py         # 导出功能
│       └── elements/           # 元素解析器
│           ├── text.py         # 文本格式解析
│           ├── heading.py      # 标题解析
│           ├── list.py         # 列表解析
│           ├── quote.py        # 引用解析
│           ├── code.py         # 代码块解析
│           ├── table.py        # 表格解析
│           └── custom.py       # 自定义元素解析
├── tests/                      # 测试文件
├── examples/                   # 使用示例
└── docs/                       # 文档
```

## 开发

```bash
# 运行测试
uv run pytest

# 运行示例
uv run python examples/example.py

# 代码格式化
uv run black src tests
uv run ruff src tests
```

## API 文档

### 主要函数

- `parse(markdown_text: str) -> Document`: 解析 Markdown 文本
- `export_markdown(document: Document, include_extensions: bool = True) -> str`: 导出为 Markdown

### 数据模型

- `Document`: 文档对象，包含所有块级元素
- `BlockElement`: 块级元素基类
  - `Heading`: 标题
  - `Paragraph`: 段落
  - `List`: 列表
  - `Quote`: 引用
  - `CodeBlock`: 代码块
  - `Table`: 表格
  - `HorizontalRule`: 水平线
  - `Align`: 对齐块（扩展）
- `InlineElement`: 行内元素基类
  - `Text`: 纯文本
  - `Bold`: 粗体
  - `Italic`: 斜体
  - `Code`: 行内代码
  - `Link`: 链接
  - `Image`: 图片

## 许可证

MIT License
