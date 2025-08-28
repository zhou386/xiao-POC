# 科荣AIO任意文件读取漏洞检测工具

## 工具概述

这是一个用于检测科荣AIO系统是否存在任意文件读取漏洞的Python脚本。该脚本支持对单个URL或批量URL列表进行漏洞检测，并使用多线程技术提高检测效率。

## 漏洞描述

科荣AIO系统的ReportServlet接口存在任意文件读取漏洞，攻击者可以通过构造特定的请求参数读取服务器上的敏感文件，如`/DISKC/Windows/Win.ini`等。

## 功能特点

- 支持单个URL检测和批量URL检测
- 使用多线程技术，提高检测效率（默认50线程）
- 自动识别并标记存在漏洞的URL
- 将存在漏洞的URL自动保存到`result1.txt`文件中
- 忽略SSL证书验证警告

## 安装依赖

```bash
pip install requests urllib3 argparse
```

## 使用方法

### 检测单个URL

```bash
python script_name.py -u http://example.com
```

### 批量检测URL

```bash
python script_name.py -f url_list.txt
```

### 查看帮助信息

```bash
python script_name.py -h
```

## 参数说明

- `-u/--url`: 指定要检测的单个URL地址
- `-f/--file`: 指定包含多个URL的文本文件路径
- `-h/--help`: 显示帮助信息

## 文件格式

批量检测时使用的URL列表文件应为纯文本格式，每行一个URL，例如：

```
http://example1.com
http://example2.com
https://example3.com
```

## 输出结果

- 检测到存在漏洞的URL会显示`[+]`前缀并保存到`result1.txt`文件中
- 不存在漏洞的URL会显示`[-]`前缀
- 无法访问或存在其他问题的URL会显示`[*]`前缀

## 注意事项

1. 该工具仅用于安全检测目的，请勿用于非法用途
2. 使用前请确保已获得相关系统的测试授权
3. 工具会自动为URL添加`http://`前缀（如果未指定协议）
4. 检测结果会实时显示并保存到`result1.txt`文件中

## 免责声明

本工具仅面向合法授权的安全测试活动，任何未经授权的使用行为均与开发者无关。使用本工具即表示您同意承担所有相关风险和责任。
