import urllib.request
import urllib.parse
import json
#利用有道翻译
def youdao():

    url='http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    method='post'
    timeout=30
    data={}
    data['i']='I hate play game'  #翻译的语句
    #data['from']='AUTO'
    ##data['to']='AUTO'
    #data['smartresult']='dict'
    #data['client']='fanyideskweb'
    #data['salt']='16069947030391'
    #data['sign']='e2c5e6b040eabb08533fd085a4a3653a'
    #data['lts']='1606994703039'
    #data['bv']='8269b35cc1594b7635631cdd3a301112'
    data['doctype']='json'
    data['version']='2.1'
    data['keyfrom']='fanyi.web'
    data['action']='FY_BY_REALTlME'
    data=urllib.parse.urlencode(data).encode('utf-8')   #对发送的数据进行编码
    print(data)
    header={}
    header['Host']='fanyi.youdao.com'
    header['Connection']='keep-alive'
    header['Content-Length']='253'
    header['Accept']='application/json, text/javascript, */*; q=0.01'
    header['X-Requested-With']='XMLHttpRequest'
    header['User-Agent']='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
    header['Content-Type']='application/x-www-form-urlencoded; charset=UTF-8'
    header['Origin']='http://fanyi.youdao.com'
    header['Referer']='http://fanyi.youdao.com/'
    header['Accept-Encoding']='gzip, deflate'
    header['Accept-Language']='zh-CN,zh;q=0.9'
    header['Cookie']='OUTFOX_SEARCH_USER_ID_NCOO=542034614.5390359; OUTFOX_SEARCH_USER_ID="-1214737004@10.108.160.18"; _ga=GA1.2.1787642428.1597494551; P_INFO=null; UM_distinctid=174fd4eee0d1b7-0d7e6fe07a1b39-f7d1d38-144000-174fd4eee0e5d8; JSESSIONID=aaa05Orb8ZeHodOPkwOyx; ___rl__test__cookies=1606994703035'
    header=urllib.parse.urlencode(header).encode('utf-8')
    req=urllib.request.Request(url,data)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36')
    req.add_header('Cookie','OUTFOX_SEARCH_USER_ID_NCOO=542034614.5390359; OUTFOX_SEARCH_USER_ID="-1214737004@10.108.160.18"; _ga=GA1.2.1787642428.1597494551; P_INFO=null; UM_distinctid=174fd4eee0d1b7-0d7e6fe07a1b39-f7d1d38-144000-174fd4eee0e5d8; JSESSIONID=aaa05Orb8ZeHodOPkwOyx; ___rl__test__cookies=1606994703035')
    response1=urllib.request.urlopen(req)
    html=response1.read().decode('utf-8')
    text=json.loads(html)
    if response1.getcode()=='200':
        print('success!')
    else:
        print(text['errorCode'])

#使用代理
def proxytest():
    url='http://www.baidu.com/'
    proxy_support=urllib.request.ProxyHandler({'http':'120.24.227.230:8080'})
    opener=urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)
    response=urllib.request.urlopen(url)
    html=response.read().decode('utf-8')
    print(html)

if __name__ == '__main__':
    proxytest()
