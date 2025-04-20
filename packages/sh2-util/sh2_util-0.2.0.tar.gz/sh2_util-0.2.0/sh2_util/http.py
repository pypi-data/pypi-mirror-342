#!/Users/tuze/.pyenv/shims/python

import json

import requests
from colorama import Fore, Style, init

# 初始化 colorama
init(autoreset=True)

# 发送HTTP POST请求
def send_post_request(url, headers, data):
    """ 发送 POST 请求并返回响应 """
    print_request(url, headers, data)
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print_response(response)
    return response

# 打印响应
def print_response(response):
    """ 打印请求的状态码、头部信息和响应体 """
    
        # 获取 HTTP 协议版本
    if response.raw.version == 10:
        http_version = 'HTTP/1.0'
    elif response.raw.version == 11:
        http_version = 'HTTP/1.1'
    elif response.raw.version == 20:
        http_version = 'HTTP/2'
    else:
        http_version = 'Unknown'
    
    # 打印状态码
    if response.status_code == 200:
        print(Fore.GREEN+f"响应Code\n{http_version} {response.status_code} {response.reason}\n")
    else:
        print(Fore.RED+f"{http_version} {response.status_code} {response.reason}\n")

    print(Fore.CYAN+f"响应Headers\n{json.dumps(dict(response.headers), ensure_ascii=False,indent=4)}\n")
    
    # 打印响应体
    try:
        data = json.dumps(response.json(), indent=4, ensure_ascii=False)
        print(Fore.YELLOW+f"响应Body\n{data} \n")
    except:
        print(Fore.YELLOW+f"响应Body\n{response.text} \n")

# 打印请求
def print_request(url, headers, data):
    """ 打印请求的状态码、头部信息和响应体 """
    # 打印url
    print(Fore.GREEN+f"请求URL\n{url}\n")


    # 打印请求Headers
    print(Fore.CYAN+f"请求Headers\n{json.dumps(headers, ensure_ascii=False,indent=4)}\n")

    # 打印请求body
    print(Fore.YELLOW+f"请求Body\n{json.dumps(data, ensure_ascii=False,indent=4)}\n")
