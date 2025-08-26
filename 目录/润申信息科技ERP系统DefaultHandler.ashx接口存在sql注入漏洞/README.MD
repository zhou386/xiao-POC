润申ERP系统SQL注入漏洞检测工具

工具概述

这是一个用于检测润申信息科技ERP系统中DefaultHandler.ashx接口SQL注入漏洞的Python脚本工具。该漏洞存在于系统的特定接口，可能允许攻击者执行恶意SQL查询。

功能特点

• 支持单个URL检测和批量URL检测

• 使用多线程技术提高批量检测效率

• 自动识别HTTP响应中的MD5哈希值判断漏洞存在

• 简洁的命令行界面，易于使用

安装要求

• Python 3.x

• 需要安装的Python库：

  • argparse (Python标准库)

  • requests

  • urllib3

可以使用以下命令安装依赖：

pip install requests urllib3


使用方法

检测单个目标


python script_name.py -u http://example.com


批量检测目标


python script_name.py -f url_list.txt


参数说明

• -u/--url: 指定单个目标URL进行检测

• -f/--file: 指定包含多个URL的文件路径进行批量检测

• -h/--help: 显示帮助信息

输出结果

• 检测到漏洞的目标URL会被保存到result1.txt文件中

• 控制台会显示每个目标的检测状态：

  • [+] 表示存在漏洞

  • [-] 表示不存在漏洞

  • [*] 表示需要手工验证

注意事项

1. 该工具仅用于授权下的安全测试，请勿用于非法用途
2. 使用前请确保已获得目标系统的测试授权
3. 工具会自动为URL添加http://前缀（如果未提供协议头）
4. 工具会忽略SSL证书验证警告

免责声明

本工具仅面向合法授权的安全测试活动。使用者应自行承担因使用该工具而可能带来的法律后果，开发者不对任何误用或损害承担责任。
