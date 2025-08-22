# 金和OA viewConTemplate.action 远程命令执行漏洞检测工具 README

## 工具简介
本工具用于检测**金和OA系统**的 `/jc6/platform/portalwb/portalwb-con-template!viewConTemplate.action` 接口是否存在**远程命令执行（RCE）漏洞**。该漏洞利用Freemarker模板注入，通过构造恶意请求参数执行系统命令（工具默认执行`ipconfig`命令），并通过响应中是否包含`root`（Linux系统特征）判断漏洞是否存在。

工具支持**单URL精准检测**与**多URL批量检测**，采用多线程（默认100线程）提升批量检测效率，最终将存在漏洞的目标自动保存至`result.txt`文件。


## 漏洞背景
### 核心信息
- **漏洞接口**：`/jc6/platform/portalwb/portalwb-con-template!viewConTemplate.action`
- **漏洞类型**：Freemarker模板注入导致的远程命令执行（RCE）
- **漏洞原理**：接口的`code`参数未对Freemarker表达式进行过滤，攻击者可传入恶意模板语法（如`${"freemarker.template.utility.Execute"?new()("命令")}`），触发命令执行
- **检测逻辑**：向目标接口发送包含`ipconfig`命令的恶意请求，若响应中出现`root`（Linux系统用户特征，适配多数服务器环境），则判定漏洞存在


## 环境依赖
| 依赖项         | 版本要求       | 说明                     |
|----------------|----------------|--------------------------|
| Python         | 3.6 及以上     | 工具基于Python 3开发     |
| requests       | 任意稳定版本   | 用于发送HTTP/HTTPS请求   |
| urllib3        | 任意稳定版本   | 处理HTTPS证书警告        |
| multiprocessing | 内置模块       | 实现多线程批量检测       |

### 依赖安装命令
若未安装`requests`库，执行以下命令安装：
```bash
pip install requests urllib3
```


## 工具使用说明
### 1. 命令行参数说明
工具通过命令行参数指定检测模式，参数含义如下：

| 参数         | 简写 | 功能描述                     | 示例                          |
|--------------|------|------------------------------|-------------------------------|
| `--url`      | `-u` | 指定单个检测目标URL          | `-u http://192.168.1.10:8080` |
| `--file`     | `-f` | 指定包含多个URL的列表文件路径 | `-f target_urls.txt`          |
| `--help`     | `-h` | 查看工具使用帮助             | `-h`                          |

### 2. 具体使用场景
#### 场景1：单URL检测
检测单个金和OA目标是否存在漏洞，命令格式：
```bash
python 工具文件名.py -u 目标URL
```
**示例**：
```bash
python jinhe_oa_rce.py -u http://10.0.0.5:8080
```
- 若目标URL未带`http://`或`https://`，工具会自动补全`http://`（如输入`10.0.0.5`，处理为`http://10.0.0.5`）


#### 场景2：多URL批量检测
批量排查多个目标（需将URL按行存入文本文件），步骤如下：
1. **准备URL列表文件**：创建`targets.txt`，内容格式示例：
   ```txt
   http://192.168.1.10:8080
   https://oa.example.com
   192.168.1.11:80  # 自动补全http://
   ```
2. **执行批量检测命令**：
   ```bash
   python jinhe_oa_rce.py -f targets.txt
   ```
- 批量检测默认开启**100线程**，可修改代码中`Pool(100)`的数值调整线程数（如`Pool(50)`降低并发压力，避免目标服务器拒绝服务）


#### 场景3：查看帮助
执行以下命令获取参数说明：
```bash
python jinhe_oa_rce.py -h
```
**预期输出**：
```
usage: jinhe_oa_rce.py [-h] [-u URL] [-f FILE]

金和OA viewConTemplate.action存在远程命令执行漏洞

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     please input your link
  -f FILE, --file FILE  please input your file path
```


## 输出结果说明
工具实时在控制台输出检测状态，不同标识对应不同结果：

| 输出标识 | 结果含义                                                                 | 示例输出                                  |
|----------|--------------------------------------------------------------------------|-------------------------------------------|
| `[+]`    | 目标存在远程命令执行漏洞（已写入`result.txt`）                           | `[+] http://192.168.1.10:8080 存在远程命令执行` |
| `[-]`    | 目标不存在该漏洞（参数过滤正常或已修复）                                 | `[-] http://192.168.1.11 不存在远程命令执行` |
| `[*]`    | 目标访问异常（HTTP状态码非200，需手工验证）                              | `[*] http://192.168.1.12 访问有问题，请手工检查` |
| 无输出    | 目标连接失败（网络不通、超时、端口未开放等，工具捕获异常后跳过）         | -                                         |


## 结果文件说明
工具会在运行目录自动生成/追加`result.txt`文件，仅保存**存在漏洞的目标URL**，格式为“每行1个URL”，便于后续漏洞验证或修复跟踪。

**示例`result.txt`内容**：
```txt
http://192.168.1.10:8080
https://oa.example.com
```


## 注意事项
1. **合法性声明**：本工具仅用于**合法授权的安全测试**（如企业内部资产自查、经甲方允许的渗透测试），禁止用于未授权攻击，使用者需承担法律责任。
2. **线程数调整建议**：
   - 生产环境目标：建议将线程数降至`20-30`，避免高并发导致服务器宕机；
   - 测试环境目标：可提高至`50-80`以提升效率。
3. **HTTPS支持**：工具已禁用HTTPS证书验证（`verify=False`），可直接检测HTTPS目标，无需额外配置。
4. **命令与检测条件优化**：
   - 若目标为Windows服务器，可将`data`中的`ipconfig`改为`whoami`，并将检测条件`'root' in res2.text`改为`'NT AUTHORITY' in res2.text`；
   - 若需执行其他命令（如`id`、`dir`），直接修改`data`参数中`"ipconfig"`的内容即可。
5. **超时与异常处理**：工具默认请求超时时间为`5秒`，可修改`requests.get()`中的`timeout=5`调整；若需排查失败原因，可在`except`块中添加日志输出（如`except Exception as e: print(f"[!] {target} 异常: {str(e)}")`）。


## 漏洞修复建议（参考）
若检测到漏洞，建议采取以下修复措施：
1. **参数过滤**：对`code`参数严格过滤Freemarker敏感语法（如`${`、`?new()`、`Execute`等），禁止模板注入；
2. **权限控制**：降低Web服务进程权限（如Linux使用非root用户、Windows使用普通用户），限制命令执行范围；
3. **禁用危险类**：在Freemarker配置中禁用`freemarker.template.utility.Execute`等危险工具类；
4. **升级补丁**：联系金和OA厂商获取漏洞修复补丁，及时更新系统至安全版本。
