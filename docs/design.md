# Markdown Parser 设计文档

## 项目概述

本项目是一个 Markdown 解析器，将 Markdown 文本转换为结构化的 Python 对象，便于其他项目使用和处理。

## 架构设计

### 1. 核心组件

#### 1.1 Parser（解析器）
- 负责整体解析流程的协调
- 管理各种元素解析器
- 处理文档级别的结构

#### 1.2 Element Parsers（元素解析器）
每种 Markdown 元素都有独立的解析器：
- HeadingParser: 解析标题（# ## ### 等）
- TextParser: 解析文本格式（粗体、斜体、行内代码）
- LinkParser: 解析链接和图片
- ListParser: 解析有序和无序列表
- QuoteParser: 解析引用块
- CodeBlockParser: 解析代码块
- TableParser: 解析表格
- CustomParser: 解析自定义扩展元素

#### 1.3 Models（数据模型）
使用 Pydantic 定义结构化的数据模型：
- Document: 文档对象
- Block: 块级元素基类
- Inline: 行内元素基类
- 各种具体元素类

#### 1.4 Exporter（导出器）
- 支持导出纯 Markdown（不含扩展语法）
- 可扩展支持其他格式

### 2. 解析流程

1. **预处理**: 将文本分割成行
2. **块级解析**: 识别和解析块级元素
3. **行内解析**: 在块级元素内部解析行内元素
4. **后处理**: 构建完整的文档树

### 3. 扩展功能

#### 3.1 图片扩展
```markdown
![alt](url){size=0.5, css="border-radius: 6px;"}
```

#### 3.2 代码块标题
```markdown
```python filename.py
code here
```

#### 3.3 对齐标签
```markdown
<Align center>内容</Align>
<Left>左对齐</Left>
<Right>右对齐</Right>
```

### 4. 设计原则

1. **模块化**: 每个解析器独立，易于维护和扩展
2. **类型安全**: 使用 Pydantic 确保数据结构的正确性
3. **可扩展**: 易于添加新的元素类型
4. **性能**: 单次遍历，避免重复解析

### 5. API 设计

```python
from markdown_parser import parse, export_markdown

# 解析 Markdown
document = parse(markdown_text)

# 访问结构化数据
for block in document.blocks:
    if isinstance(block, Heading):
        print(f"标题级别 {block.level}: {block.content}")

# 导出纯 Markdown
pure_markdown = export_markdown(document, include_extensions=False)
``` 