import re

def is_separator_line(line, expected_columns=None):
    line_stripped = line.strip()
    if not line_stripped:
        return False
    
    parts = line_stripped.split('|')
    # 去除首尾可能存在的空字符串
    if parts and not parts[0].strip():
        parts = parts[1:]
    if parts and not parts[-1].strip():
        parts = parts[:-1]
    
    n_cols = len(parts)
    # 检查列数是否匹配期望值
    if expected_columns is not None and n_cols != expected_columns:
        return False
    # 需要至少两列才有意义
    if n_cols < 1:
        return False
    
    # 验证每部分是否只包含分隔符规则字符
    for part in parts:
        clean_part = part.strip().replace(' ', '')
        if not re.match(r'^:?-{3,}:?$', clean_part):
            return False
    return True

def locate_markdown_tables(lines):
    tables = []  # 存储表格位置 (start, end)
    state = "outside"  # 状态机：outside, header, inside
    current_start = None
    current_cols = None
    n = len(lines)
    i = 0

    while i < n:
        line = lines[i].rstrip('\n')
        line_stripped = line.strip()

        if state == "outside":
            if not line_stripped:  # 跳过空行
                i += 1
                continue
            
            if '|' in line:
                # 检查是否为分隔行（避免误判单独的分隔行）
                if is_separator_line(line):
                    i += 1
                    continue
                
                # 解析表头行获取列数
                parts = line_stripped.split('|')
                if parts and not parts[0].strip():
                    parts = parts[1:]
                if parts and not parts[-1].strip():
                    parts = parts[:-1]
                n_cols = len(parts)
                
                if n_cols < 1:  # 无效表头
                    i += 1
                    continue
                
                # 进入表头检测状态
                current_start = i
                current_cols = n_cols
                state = "header"
                i += 1  # 移动到下一行检测分隔线
            else:
                i += 1  # 无竖线则跳过

        elif state == "header":
            if not line_stripped:  # 空行中断表格
                state = "outside"
                i += 1
                continue
            
            # 验证是否为有效的分隔行
            if is_separator_line(line, current_cols):
                state = "inside"  # 进入表格数据区
                i += 1  # 检查下一行数据
            else:
                # 当前行不是分隔线，重置状态并重新检测当前行
                state = "outside"
                continue  # 不移动i，以outside状态重新处理此行

        elif state == "inside":
            if not line_stripped:  # 空行结束表格
                tables.append((current_start, i - 1))
                state = "outside"
                i += 1
                continue
            
            # 检测表格行：列数必须匹配
            parts = line_stripped.split('|')
            if parts and not parts[0].strip():
                parts = parts[1:]
            if parts and not parts[-1].strip():
                parts = parts[:-1]
            n_cols = len(parts)
            
            if n_cols == current_cols:  # 列数匹配则继续
                i += 1
            else:  # 列数不匹配结束表格
                tables.append((current_start, i - 1))
                state = "outside"
                continue  # 重新处理当前行
    
    # 文件末尾仍在表格内
    if state == "inside":
        tables.append((current_start, n - 1))
    
    return tables

# 使用示例
if __name__ == "__main__":
    markdown_content = """
This is regular text.

| Header1 | Header2 | Header3 |
|---------|:-------:|--------:|
| Row11   | Row12   | Row13   |
| Row21   | Row22   | Row23   |

Another table without outer pipes:
Header1 | Header2 | Header3
--------|---------|--------
A1 | B1 | C1
A2 | B2 | C2

End document.
""".splitlines(keepends=True)

    tables = locate_markdown_tables(markdown_content)
    for start, end in tables:
        print(f"Table found from line {start} to {end}")
        print("Table content:")
        for j in range(start, end + 1):
            print(markdown_content[j].rstrip())
        print()  # 空行分隔
