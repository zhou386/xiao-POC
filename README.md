# H3C 网管系统文件读取漏洞检测脚本

## 简介
该脚本用于检测H3C网管系统是否存在文件读取漏洞。通过构造特定请求，判断目标系统是否允许未授权读取敏感文件（如`/etc/passwd`），适用于批量检测或单个目标验证场景。


## 漏洞原理
H3C网管系统的`/webui/?file_name=xxx&g=sys_dia_data_down`接口存在路径遍历漏洞，攻击者可通过构造包含`../../../../../`的路径，读取服务器上的任意敏感文件（如`/etc/passwd`）。脚本通过检测该接口是否能成功读取`/etc/passwd`中的特征内容（如`root::0:0:root:/:/bin/sh`）来判断漏洞是否存在。


## 环境要求
- Python 3.x
- 依赖库：`requests`

安装依赖：
```bash
pip install requests
```


## 使用方法

### 1. 命令参数说明
| 参数 | 作用 | 示例 |
|------|------|------|
| `-u`/`--url` | 检测单个目标URL | `python script.py -u http://192.168.1.1` |
| `-f`/`--file` | 批量检测文件中的URL列表 | `python script.py -f urls.txt` |
| `-h`/`--help` | 显示帮助信息 | `python script.py -h` |


### 2. 单个目标检测
```bash
python script.py -u http://target-ip:port
```
- 若漏洞存在，输出：`[+]http://target-ip:port 存在任意读取漏洞`，并记录到`result1.txt`。
- 若漏洞不存在，输出：`[-]该http://target-ip:port 不存在任意读取漏洞`。
- 若目标访问异常，输出：`[*]该http://target-ip:port 存在问题,请手工测试`。


### 3. 批量目标检测
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
2. 检测过程中会忽略SSL证书验证（`verify=False`），适用于内部网络或自签名证书场景。
3. 请在合法授权范围内使用本脚本，禁止未授权检测他人系统。
4. 若目标系统的`/etc/passwd`内容与脚本匹配特征（`root::0:0:root:/:/bin/sh`）不符，可能导致误判，建议结合手工验证。


## 结果文件
检测到的漏洞目标会保存至当前目录的`result1.txt`，可用于后续处理或报告生成。
