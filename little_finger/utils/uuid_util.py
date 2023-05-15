"""
uuid util
"""

import uuid


def next_id() -> str:
    return str(uuid.uuid4())


if __name__ == '__main__':
    print(next_id())