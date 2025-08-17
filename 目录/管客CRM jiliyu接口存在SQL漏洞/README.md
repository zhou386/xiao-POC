# 管客CRM jiliyu接口SQL注入漏洞检测脚本

## 简介
该脚本用于检测管客CRM系统的`jiliyu`接口是否存在SQL注入漏洞。通过构造特定的SQL注入 payload，判断目标系统是否存在漏洞，支持单个目标检测和批量检测模式。


## 漏洞原理
管客CRM系统的`/index.php/jiliyu`接口在处理`xu`参数时，未对用户输入进行严格过滤，导致存在SQL注入漏洞。攻击者可通过构造恶意SQL语句，获取数据库敏感信息或执行未授权操作。

脚本通过向目标接口发送包含`updatexml`函数的注入 payload，检测响应中是否包含`md5(1)`的特征值（`c4ca4238a0b923820dcc509a6f75849`）来判断漏洞是否存在。


## 环境要求
- Python 3.x
- 依赖库：`requests`

安装依赖：
```bash
pip install requests
```


## 使用方法

### 命令参数说明
| 参数 | 作用 | 示例 |
|------|------|------|
| `-u`/`--url` | 检测单个目标URL | `python script.py -u http://192.168.1.1` |
| `-f`/`--file` | 批量检测文件中的URL列表 | `python script.py -f urls.txt` |
| `-h`/`--help` | 显示帮助信息 | `python script.py -h` |


### 单个目标检测
```bash
python script.py -u http://target-ip:port
```
- 若漏洞存在，输出：`[+]http://target-ip:port 存在sql漏洞`，并记录到`result1.txt`。
- 若漏洞不存在，输出：`[-]该http://target-ip:port 不存在sql漏洞`。
- 若目标访问异常，输出：`[*]该http://target-ip:port 存在问题,请手工测试`。


### 批量目标检测
1. 准备URL列表文件（如`urls.txt`），每行一个目标URL，格式示例：
   ```
   http://192.168.1.100
   http://10.0.0.5:8080
   ```
2. 执行批量检测命令：
   ```bash
   python script.py -f urls.txt
   ```
3. 结果会自动保存到`result1.txt`，包含所有存在漏洞的目标URL。


## 注意事项
1. 脚本默认使用50个进程进行批量检测，可根据网络环境修改`Pool(50)`中的数值调整并发数。
2. 脚本会自动为缺少协议头（`http://`或`https://`）的目标添加`http://`协议。
3. 请在合法授权范围内使用本脚本，禁止对未授权目标进行检测。
4. 部分系统可能存在WAF或过滤机制，可能导致检测结果不准确，建议结合手工验证。


## 结果文件
检测到的漏洞目标会保存至当前目录的`result1.txt`文件中，方便后续处理和分析。
##仅供学习使用

