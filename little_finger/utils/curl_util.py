"""
curl util
"""

from little_finger.utils import foreach


def from_http_2_curl(cmd :str) -> str:
    if not cmd:
        raise ValueError('cmd param is None')
    cmd = cmd.strip()
    cmd.splitlines()
    return 'None'
    ...


def from_curl_2_http(cmd :str) -> str:

    ...


if __name__ == '__main__':
    s = """POST http://localhost/v2/mgmt/user/asset/withdrawSuccess
Content-Type: application/json
x-Trace-Id: fix-success-withdraw-001

{
    "body": {
        "userId": 57200254,
        "asset": "XTZ",
        "amount": 1.88,
        "tranId": 608011925,
        "type": 32,
        "info": "withdraw",
        "ensureSuccess": true
    }
}
"""
    foreach(lambda x: print(x + '###'), s.splitlines())

