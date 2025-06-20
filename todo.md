我们正在做一个makdown解析器，将markdown转化为结构化对象，便于后续被其他项目用来解析文档

项目规范: 
- 使用 uv 运行python代码
- 合理模块化
- 测试代码与核心代码分离
- 文档和方案先于代码

# TODOs

基本单行元素
[x] # 标题 - 一级标题
[x] ## 标题 - 二级标题
[x] **粗体** - 粗体文字
[x] *斜体* - 斜体文字
[x] `代码` - 行内代码
[x] [链接](url) - 链接
[x] ![图片](url) - 图片

多行内容发现与解析
[x] - 列表 - 无序列表（按缩进分级）
[x] 1. 列表 - 有序列表（按缩进分级）
[x] > 引用 - 引用块（按缩进分级）
[x] ``` 代码块
[x] 表格行发现 (parse_table.py)
[x] 表格解析

额外内容(markdown语法的超集)
[x] ![图片](url){size=0.5(0~1数字，表示图片宽度/容器),css="border-radius: 6px;"(额外图片容器样式)}
[x] ```python abc.py\nprint(abc)\n```, 将abc.py视为代码块的标题
[x] <Align center>abc</Align> 内容居中，同理还有 <Left></Left> <Right></Right>
[x] export 支持导出不带额外标记内容的纯markdown文档

fix:
[x] <Left></Left> <Right></Right> 需求错误，改为<Align left></Align> <Align right></Align> 

## 额外完成的功能
[x] 水平分割线 (---)
[x] 缩进代码块 (4空格或tab缩进)
[x] 嵌套列表支持
[x] 嵌套引用支持
[x] 完整的模块化架构 (src/markdown_parser/)
[x] 导出时可选择是否包含扩展语法
[x] 链接标题支持 [text](url "title")
[x] 多种对齐标签格式: <Align left/center/right>

[x] 增加几个markdown文件用于测试
[x] 增加基于Document导出 HTML 的功能
[x] 测试时读取预先准备的markdown，调用解析，再调用html导出，然后把原文和转化后的html代码组合输出为结果