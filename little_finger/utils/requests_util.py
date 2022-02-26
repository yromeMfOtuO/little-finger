"""
convert curl to python requests
"""

import argparse
from http.cookies import SimpleCookie
from shlex import split
from urllib.parse import urlparse

import requests
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
    headers = {}
    cookies = {}
    for header in args.headers or ():
        name, val = header.split(':', 1)
        name = name.strip()
        val = val.strip()
        if name.title() == 'Cookie':
            for name, morsel in SimpleCookie(val).items():
                cookies[name] = morsel.value
        else:
            headers[name] = val
    if args.auth:
        user, password = args.auth.split(':', 1)
        headers['Authorization'] = basic_auth_header(user, password)
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
    args = args_from_curl(curl)

    def req():
        if not args or not args['method'] or not args['url']:
            raise Exception('参数错误')
        if args['method'] == 'GET':
            # 注意默认requests无超时时间，会导致阻塞
            return requests.get(url=args['url'], cookies=args['cookies'], headers=args['headers'], timeout=2)
        elif args['method'] == 'POST':
            return requests.post(url=args['url'], cookies=args['cookies'], headers=args['headers'], timeout=2)
        else:
            raise Exception('请求方法错误')
    return req

if __name__ == '__main__':
    curl = """curl 'https://mp.weixin.qq.com/mp/appmsgreport?action=page_time_5s&__biz=MzIxNTQ3NDMzMw==&uin=&key=&pass_ticket=&wxtoken=777&devicetype=&clientversion=&__biz=MzIxNTQ3NDMzMw%3D%3D&appmsg_token=&x5=0&f=json' \
  -H 'authority: mp.weixin.qq.com' \
  -H 'sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"' \
  -H 'content-type: application/x-www-form-urlencoded; charset=UTF-8' \
  -H 'x-requested-with: XMLHttpRequest' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36' \
  -H 'sec-ch-ua-platform: "Windows"' \
  -H 'accept: */*' \
  -H 'origin: https://mp.weixin.qq.com' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-dest: empty' \
  -H 'referer: https://mp.weixin.qq.com/s/_DqBnZlD3Ucgdc8Gi2Mo8Q' \
  -H 'accept-language: zh-CN,zh;q=0.9' \
  -H 'cookie: rewardsn=; wxtokenkey=777' \
  --data-raw 'report_bizuin=MzIxNTQ3NDMzMw%3D%3D&title=%E5%85%B3%E4%BA%8E%E4%BA%8B%E5%8A%A1%E5%92%8C%E9%94%81%E7%9A%84%E4%B8%80%E4%BA%9B%E7%BB%86%E8%8A%82&mid=2247484347&idx=1&subscene=10000&sessionid=svr_37d3f1e83b4&enterid=1645882556&read_cnt=0&old_like_cnt=0&like_cnt=0&screen_width=1205&screen_height=321&screen_num=22&idkey=64469_15_1%3B27613_31_270&copyright_stat=1&ori_article_type=%E7%A7%91%E6%8A%80%E4%BA%92%E8%81%94%E7%BD%91&video_cnt=0&read_screen_num=1&is_finished_read=0&scene=&content_len=1195556&start_time=1645882556091&end_time=1645882562405&handup_time=0&total_height=7000&exit_height=321&img_640_cnt=0&img_0_cnt=0&img_300_cnt=0&wtime=1505&ftime=293&ptime=682&onload_time=1505&reward_heads_total=0&reward_heads_fail=0&outer_pic=0&publish_time=1573777860&item_show_type=0&page_req_info=%7B%22startGetAppmsgExtTime%22%3A1645882556604%2C%22startGetAppmsgAdTime%22%3A1645882556695%2C%22receiveGetAppmsgExt%22%3A%22200%7C1645882556910%22%2C%22receiveGetAppmsgAd%22%3A%22200%7C1645882556925%22%2C%22domCompleteTime%22%3A1645882556297%7D&is_darkmode=1&search_click_id=0&webp_total=1&webp_lossy=1&webp_lossless=1&webp_alpha=1&webp_animation=1&download_cdn_webp_img_cnt=0&download_img_cnt=0&download_cdn_img_cnt=0&img_cnt=1&report_time=1645882562&source=&req_id=2621edxlIQ9Yqher5RgogEv3&recommend_version=&class_id=&ascene=-1&hotspotjson=%7B%22hotspotinfolist%22%3A%5B%5D%7D&is_pay_subscribe=0&is_paid=0&preview_percent=0&is_finished_preview=0&fee=&pay_cnt=undefined&worthy_cnt=undefined&exptype=&expsessionid=' \
  --compressed"""
    r = args_from_curl(curl)
    print(r)
    req = closure_from_curl(curl)
    resp = req()
    print(resp)
