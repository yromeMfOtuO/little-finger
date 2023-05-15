"""
jinja2 util
use to simplify Template grammar use
"""

from jinja2 import Template

default_loop_tmpl_start = """
{% for datum in data %}"""

default_loop_tmpl_end = """
{% endfor %}
"""

default_loop_line_break = """{{ ", " if not loop.last else ";" }}"""


def build_tmpl(segments: list) -> Template:
    """
    build template with str segments, can refer the segments declared
    :param segments: segments of tmpl str
    :return: jinja2.Template
    """
    tmpl_str = "".join(segments)
    return Template(tmpl_str)


if __name__ == '__main__':
    segments_ = [
        """INSERT IGNORE INTO table_name 
(`field1`, `field2`)
VALUES """,
        default_loop_tmpl_start,
        """('{{datum.field1}}', '{{datum.field2}}'""",
        default_loop_line_break,
        default_loop_tmpl_end
    ]
    tmpl = build_tmpl(segments_)
    print(tmpl)
