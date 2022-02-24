"""
convert curl to python requests
"""

import argparse
from http.cookies import SimpleCookie
from shlex import split
from urllib.parse import urlparse

from w3lib.http import basic_auth_header

parser = argparse.ArgumentParser()
parser.add_argument('url')
parser.add_argument('-H', '--header', dest='headers', action='append')
parser.add_argument('-X', '--request', dest='method', default='get')
parser.add_argument('-d', '--data', dest='data')
parser.add_argument('-u', '--user', dest='auth')

safe_to_ignore_arguments = [
    ['--compressed'],
    # `--compressed` argument is not safe to ignore, but it's included here
    # because the `HttpCompressionMiddleware` is enabled by default
    ['-s', '--silent'],
    ['-v', '--verbose'],
    ['-#', '--progress-bar']
]
for argument in safe_to_ignore_arguments:
    parser.add_argument(*argument, action='store_true')


def args_from_curl(curl: str):
    """
    转换 curl 为 requests 参数
    :param curl: curl 命令
    :return: 返回参数 dict
    """
    print(curl)

    command_args = split(curl)
    if command_args[0] != 'curl':
        raise Exception('a curl command must start whith "curl"')
    args = parser.parse_known_args(command_args[1:])[0]
    print(args)
    url = args.url
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = 'http://' + url
    result = {'method': args.method.upper(), 'url': url}
    headers = []
    cookies = {}
    for header in args.headers or ():
        name, val = header.split(':', 1)
        name = name.strip()
        val = val.strip()
        if name.title() == 'Cookie':
            for name, morsel in SimpleCookie(val).items():
                cookies[name] = morsel.value
        else:
            headers.append((name, val))
    if args.auth:
        user, password = args.auth.split(':', 1)
        headers.append(('Authorization', basic_auth_header(user, password)))
    if headers:
        result['headers'] = headers
    if cookies:
        result['cookies'] = cookies
    if args.data:
        result['data'] = args.data
    return result


def closure_from_curl(curl: str):
    """
    convert curl to python requests closure
    :param curl: curl命令
    :return: python requests closure
    """

    ...

if __name__ == '__main__':
    r = args_from_curl("""curl 'https://dwci.aihaisi.com/job/CI_supervision-api/build?delay=0sec' \
      -H 'authority: dwci.aihaisi.com' \
      -H 'cache-control: max-age=0' \
      -H 'sec-ch-ua: " Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"' \
      -H 'sec-ch-ua-mobile: ?0' \
      -H 'sec-ch-ua-platform: "macOS"' \
      -H 'upgrade-insecure-requests: 1' \
      -H 'origin: https://dwci.aihaisi.com' \
      -H 'content-type: application/x-www-form-urlencoded' \
      -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36' \
      -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
      -H 'sec-fetch-site: same-origin' \
      -H 'sec-fetch-mode: navigate' \
      -H 'sec-fetch-user: ?1' \
      -H 'sec-fetch-dest: document' \
      -H 'referer: https://dwci.aihaisi.com/job/CI_supervision-api/build?delay=0sec' \
      -H 'accept-language: zh-CN,zh;q=0.9' \
      -H 'cookie: jenkins-timestamper-offset=-28800000; JSESSIONID.903ef379=node017r79jv0x6wbs11fskht9rzmwj16593.node0; JSESSIONID.bdccae7f=node01n0dwjwr8rcir1sja7qo5ketu3267.node0; JSESSIONID.771445df=node09kkz0ped68cm1cmdp6zf0khh2370.node0; JSESSIONID.91669e47=node01b1utukfnd5u857ahqwxk0nji2495.node0; JSESSIONID.1957dbe9=node015hzy8w9aztcioyy6qfzee73y489.node0; JSESSIONID.66d06f01=node01th58dzovwh6e1m05fpx2xke4r14676.node0; JSESSIONID.002cf490=node0fyvbd6xy13ns13bi5bq5gz2xq446.node0; JSESSIONID.b72fef8c=node01prkv51oqyuo2y2gi4cdsclt626.node0; JSESSIONID.ed4dc631=node010co59q0frx6g19oer0fubtx4f2760.node0; JSESSIONID.6c62b03e=node0cp5syx1cfvon1ptuvivje5onu1360.node0; ADMIN_SESSION=8b21c708a960de9e56f4a6d6769d284da80850d3-partnerCode=&userId=5872; experimentation_subject_id=ImVmYzU5MjY5LTVjYmEtNGJhMC1iMGY2LTgxM2VhNjZmNTAxOSI%3D--d067ed262cc28e5d35b84e197192a7ebfd906e30; JSESSIONID.2c352043=node0yltxbvi7gt8zygd8uprhjmim842.node0; JSESSIONID.8479b1df=node0r1s2z5jvkvkvw86eb1n5fl4w2009.node0; JSESSIONID.7a89bdd9=node01x0okhka04zvh14rtwjd563kam184.node0; _ga=GA1.2.92600959.1597117503; JSESSIONID.3ab5a7ef=node0kq7300daq1o71o505uqo62qhm1586.node0; JSESSIONID.c77bffac=node016owf3qlm6da1yyvh6s5ecmvi1063.node0; _gcl_au=1.1.848091483.1641539925; _rdt_uuid=1641539926551.8b79cae9-6958-425c-a858-6e7d1388dda6; screenResolution=1440x900; hudson_auto_refresh=true; JSESSIONID.1fa093a2=node01g2q69k7ebej8u7wd2hy00a1h17715.node0' \
      --data-raw 'name=branchName&value=master&name=ciId&value=&statusCode=303&redirectTo=.&json=%7B%22parameter%22%3A+%5B%7B%22name%22%3A+%22branchName%22%2C+%22value%22%3A+%22master%22%7D%2C+%7B%22name%22%3A+%22ciId%22%2C+%22value%22%3A+%22%22%7D%5D%2C+%22statusCode%22%3A+%22303%22%2C+%22redirectTo%22%3A+%22.%22%7D&Submit=%E5%BC%80%E5%A7%8B%E6%9E%84%E5%BB%BA' \
      --compressed""")
    print(r)
