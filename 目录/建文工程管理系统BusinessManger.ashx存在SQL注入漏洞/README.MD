# 建文工程管理系统 SQL注入漏洞检测工具

## 工具描述

这是一个用于检测建文工程管理系统BusinessManger.ashx接口SQL注入漏洞的Python脚本工具。该工具支持对单个目标或批量目标进行漏洞检测，并使用多线程技术提高扫描效率。

## 功能特性

- 支持单个URL检测和批量文件检测两种模式
- 使用多线程技术提高扫描效率（默认50线程）
- 自动识别HTTP协议并补充URL前缀
- 详细的漏洞检测结果输出
- 自动保存存在漏洞的目标到结果文件

## 安装依赖

```bash
pip install requests urllib3 argparse
```

## 使用方法

### 检测单个目标

```bash
python script.py -u http://example.com
```

### 批量检测目标

```bash
python script.py -f url_list.txt
```

### 帮助信息

```bash
python script.py -h
```

## 参数说明

- `-u/--url`: 指定单个目标URL进行检测
- `-f/--file`: 指定包含多个目标URL的文件路径进行批量检测

## 输入文件格式

批量检测文件应为文本文件，每行包含一个目标URL（可带http/https协议，也可不带）：
```
example.com
http://test.com
https://target.org
```

## 输出结果

- 检测结果会实时显示在控制台
- 存在漏洞的目标会自动保存到`result1.txt`文件中
- 结果文件使用UTF-8编码，避免中文乱码问题

## 注意事项

1. 工具会自动禁用SSL证书验证警告
2. 工具会自动为没有协议前缀的URL添加`http://`前缀
3. 工具使用MD5('1')作为检测payload，值为`c4ca4238a0b923820dcc509a6f75849b`

## 免责声明

本工具仅用于安全检测和教育目的，请勿用于非法用途。使用者需对自身行为负责，与工具作者无关。
