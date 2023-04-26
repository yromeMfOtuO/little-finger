"""
jinja2 util
use to simplify Template grammar use
"""

from jinja2 import Template

loop_tmpl_start = """
{% for datum in data %}"""

loop_tmpl_end = """
{% endfor %}
"""

loop_line_break = """{{ ", " if not loop.last else ";" }}"""


def build_tmpl(segments: list) -> Template:
    """
    build template with str segments, can refer the segments declared
    :param segments: segments of tmpl str
    :return: jinja2.Template
    """
    tmpl_str = "".join(segments)
    return Template(tmpl_str)


if __name__ == '__main__':
    segments = [
        """INSERT IGNORE INTO table_name 
(`field1`, `field2`)
VALUES """,
        loop_tmpl_start,
        """('{{datum.field1}}', '{{datum.field2}}'""",
        loop_line_break,
        loop_tmpl_end
    ]
    tmpl = build_tmpl(segments)
    print(tmpl)
