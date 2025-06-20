# 扩展语法测试

这个文档测试项目支持的扩展语法功能。

## 带标题的代码块

```python hello.py
def greet(name):
    """问候函数"""
    return f"Hello, {name}!"

if __name__ == "__main__":
    print(greet("World"))
```

```javascript app.js
const message = "Hello from JavaScript!";
console.log(message);
```

## 扩展图片语法

![普通图片](bee.jpeg)

![调整大小的图片](bee.jpeg){size=0.5}

![带样式的图片](bee.jpeg){size=0.8, css="border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"}

## 对齐标签

<Center>这段文字居中对齐</Center>

<Align left>这段文字左对齐</Align>

<Align right>这段文字右对齐</Align>

## 表格

| 项目 | 描述 | 状态 |
|------|:----:|-----:|
| 解析器 | Markdown解析功能 | ✅ 完成 |
| 导出器 | 导出为markdown | ✅ 完成 |
| HTML导出 | 导出为HTML | 🚧 开发中 |

## 复杂嵌套

> ### 引用中的标题
> 
> 这是引用块中的内容，包含：
> - **粗体列表项**
> - *斜体列表项*
> - `代码列表项`
> 
> ```bash
> # 引用中的代码块
> echo "Hello from quote!"
> ```

---

最后一段普通文字。 