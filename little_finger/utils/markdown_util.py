"""
markdown util
"""
from typing import List

import markdown

# 添加CSS样式
DEFAULT_CSS_STYLE = """
<style>
table {
    border-collapse: collapse;
    margin: 20px 0;
}
th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
}
th {
    background-color: #f2f2f2;
}
</style>
"""


def build_table(headers: list, data_rows: List[list]) -> str:
    """拼接Markdown表格数据

    Args:
        headers: list[str] 表头列表
        data_rows: list[list] 数据行二维列表
    Returns:
        str: markdown 表格
    """
    if not headers or not data_rows:
        return ""
    # assert len(headers) == len(data_rows[0])

    table_lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["-----"] * len(headers)) + " |"
    ]

    for row in data_rows:
        table_lines.append("| " + " | ".join(map(str, row)) + " |")

    return "\n".join(table_lines)


def build_unordered_list(items: list) -> str:
    """
    构建无序号列表
    """
    if not items:
        return ""
    return "- " + "\n- ".join(map(str, items))


def to_html(markdown_segments: List[str], css_style: str = DEFAULT_CSS_STYLE) -> str:
    """
    拼接多个markdown片段, 组成整体
    """
    entire_markdown_text = "\n\n".join(markdown_segments)

    # 转换为HTML（可选）
    html_output = markdown.markdown(
        entire_markdown_text,
        extensions=[
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code'
        ]
    )
    return css_style + html_output