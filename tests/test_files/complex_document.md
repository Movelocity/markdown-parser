# 复杂文档示例

这是一个复杂的markdown文档，包含各种元素的组合。

## 项目介绍

**Markdown Parser** 是一个强大的解析工具，支持：

1. 标准markdown语法
2. 扩展语法功能
3. HTML导出功能

---

## 技术文档

### 安装指南

使用以下命令安装：

```bash install.sh
# 使用uv安装依赖
uv sync

# 运行测试
uv run python -m pytest
```

### API参考

| 函数名 | 参数 | 返回值 | 描述 |
|--------|------|--------|------|
| `parse()` | `text: str` | `Document` | 解析markdown文本 |
| `export_markdown()` | `doc: Document` | `str` | 导出为markdown |
| `export_html()` | `doc: Document` | `str` | 导出为HTML |

### 使用示例

```python example.py
from markdown_parser import parse, export_html

# 解析文档
doc = parse("# Hello **World**!")

# 导出为HTML
html = export_html(doc)
print(html)
```

## 特性展示

### 图片处理

支持不同尺寸的图片：

![小图片](bee.jpeg){size=0.3, css="float: left; margin-right: 10px;"}

![大图片](bee.jpeg){size=0.9}

### 文本对齐

<Align center>
**居中的重要声明**

这是一个居中显示的重要内容。
</Align>

<Align right>
*右对齐的注释*
</Align>

### 引用和代码的组合

> **重要提示：**
> 
> 在使用解析器时，请注意以下几点：
> 
> 1. 确保输入文本编码正确
> 2. 处理大文件时注意内存使用
> 
> ```python
> # 推荐的使用方式
> with open('large_file.md', 'r', encoding='utf-8') as f:
>     content = f.read()
>     doc = parse(content)
> ```

## 结论

这个解析器功能完整，支持各种复杂的markdown结构。

---

*文档更新时间：2024年* 