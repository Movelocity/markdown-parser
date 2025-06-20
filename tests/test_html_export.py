"""Test script for HTML export functionality."""

import os
from pathlib import Path
from markdown_parser import parse, export_html


def test_html_export():
    """测试HTML导出功能，读取测试文件并展示原文与HTML对比结果。"""
    # 测试文件路径
    test_files_dir = Path(__file__).parent / "test_files"
    test_files = [
        "basic_syntax.md",
        "extended_syntax.md", 
        "complex_document.md",
        "index.md"
    ]
    
    print("=" * 80)
    print("Markdown to HTML Export Test")
    print("=" * 80)
    
    for test_file in test_files:
        file_path = test_files_dir / test_file
        
        if not file_path.exists():
            print(f"❌ 测试文件不存在: {file_path}")
            continue
            
        print(f"\n{'=' * 60}")
        print(f"测试文件: {test_file}")
        print('=' * 60)
        
        # 读取原始markdown内容
        with open(file_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        print("\n📄 原始Markdown内容:")
        print("-" * 40)
        print(markdown_content)
        
        # 解析markdown
        try:
            document = parse(markdown_content)
            print(f"\n✅ 解析成功！解析出 {len(document.blocks)} 个块级元素")
            
            # 导出为HTML
            html_content = export_html(document, include_extensions=True, title=f"测试文档 - {test_file}")
            
            print("\n🌐 导出的HTML内容:")
            print("-" * 40)
            print(html_content)
            
            # 保存HTML文件以便查看
            output_file = test_files_dir / f"{test_file.replace('.md', '.html')}"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"\n💾 HTML文件已保存至: {output_file}")
            
        except Exception as e:
            print(f"❌ 处理 {test_file} 时出错: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'=' * 80}")
    print("测试完成！")
    print('=' * 80)


def compare_export_modes():
    """比较包含扩展语法和不包含扩展语法的导出差异。"""
    test_file = Path(__file__).parent / "test_files" / "extended_syntax.md"
    
    if not test_file.exists():
        print("❌ 扩展语法测试文件不存在")
        return
    
    with open(test_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    document = parse(markdown_content)
    
    print("\n" + "=" * 60)
    print("扩展语法导出模式对比")
    print("=" * 60)
    
    # 包含扩展语法的HTML导出
    html_with_extensions = export_html(document, include_extensions=True, title="包含扩展语法")
    
    # 不包含扩展语法的HTML导出
    html_without_extensions = export_html(document, include_extensions=False, title="标准语法")
    
    print("\n🔧 包含扩展语法的HTML:")
    print("-" * 30)
    # 只显示body部分，避免输出过长
    body_start = html_with_extensions.find('<body>') + 6
    body_end = html_with_extensions.find('</body>')
    print(html_with_extensions[body_start:body_end].strip())
    
    print("\n📝 标准语法HTML:")
    print("-" * 30)
    body_start = html_without_extensions.find('<body>') + 6
    body_end = html_without_extensions.find('</body>')
    print(html_without_extensions[body_start:body_end].strip())


if __name__ == "__main__":
    test_html_export()
    compare_export_modes() 