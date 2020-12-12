import urllib.request as rqs
import urllib.parse
import json
import os
import re
import urllib.error as urlerror
import random,time


#利用有道翻译
def youdao():

    url='http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    method='post'
    timeout=30
    data={}
    data['i']='I hate play game'  #翻译的语句
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
#获取代理服务器的代理地址列表 ,随机返回一个
#free-proxy=http://31f.cn/http-proxy/
def getproxy(url):
    proxyurls=[]
    response=rqs.urlopen(url)
    context=response.read().decode('utf-8')
    #要匹配的格式如下，且有换行符
    '''<td>18</td>
    <td>111.11.227.114</td>
    <td>80</td>'''
    #p=r'(?:(?:[0,1]?\d\d|2[0-4]\d|25[0-5])\.){3}(?:[0,1]?\d\d|2[0-4]\d|25[0-5])' #匹配IP地址
    pattern = re.compile(r'<td>((?:(?:[0,1]?\d\d|2[0-4]\d|25[0-5])\.){3}(?:[0,1]?\d\d|2[0-4]\d|25[0-5])</td>[\s\S]<td>(?:\d{1,4}))</td>',re.S)
    ips=re.findall(pattern,context)
    #print(ips)
    for tempip in ips:
        #print(tempip)
        ip=str(tempip).replace('</td>','',-1).replace('\n<td>',':',-1)
        #print('ip :',ip)
        proxyurls.append(ip)
    #print(proxyurls)
    proxy=random.choice(proxyurls)
    #print(proxy)
    return proxy
#使用代理
def proxytest():
    dricturl='http://jandan.net/'
    #req = rqs.Request(dricturl)
    #req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36')
    proxy=getproxy(url='http://31f.cn/http-proxy/') #获取一个代理地址
    print('use proxy: ',proxy)
    proxy_support=urllib.request.ProxyHandler({'http':proxy})
    opener=urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)
    try:
        response=urllib.request.urlopen(dricturl)
        html=response.read()
        print(html)
    except urllib.error.URLError as urler:
        print('地址错误',urler)
    except urllib.error.ContentTooShortError as cr:
        print('连接错误',cr)
        proxytest()
    except urllib.error.HTTPError as httper:
        print('访问出现错误，尝试中...')
        proxytest()

#w创建子目录
def mkdir(subpath):
    os.chdir(savepath)
    if not os.path.exists(subpath):
        #os.chdir(picture)
        os.mkdir(subpath)

    else:
        pass

#获取子类页面分类
def get_page(url):
    urllist=[]
    req=rqs.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36')
    response=rqs.urlopen(url)
    html=response.read().decode('GB2312',errors = 'ignore').replace('\r','',-1).replace(' ','',-1).replace('\n','',-1)  #由于访问的页面是GB2312
    #print(html)
    sub=re.findall('screeningListTop.*全部</a>.*href="(.*)餐饮美食</a>',html,re.S)
    str1=sub[0]
    urllist1=str1.split('</a>')  #以</a>分割成不同的串
    for line in urllist1:
        #print(line)
        dir1=line.split('/')[2]   #再次分割取第3个值为文件夹名称也是URL的一部分
        #print(dir1)
        mkdir(dir1)
        urllist.append(dir1)
    return urllist
#要匹配的内容
'''<div class="screeningListTop clearfix">
				 <a href="/" class="active">全部</a>
                 <a href="/tuku/renwutupian/">人物图片</a>
				 <a href="/tuku/fengjingtupian/">风景图片</a>
                 <a href="/tuku/huadetupian/">花的图片</a>
                 <a href="/tuku/dongwutupian/">动物图片</a>
                 <a href="/tuku/construction/">环境家居</a>
                 <a href="/tuku/culture/">文化艺术</a>
                 <a href="/tuku/technology/">现代科技</a>
                 <a href="/tuku/life/">生活百科</a>
                 <a href="/tuku/illustration/">漫画插画</a>
                 <a href="/tuku/business/">商务金融</a>
                 <a href="/tuku/background/">背景花边</a>
                 <a href="/tuku/dining/">餐饮美食</a>
                    </div>'''
#获取子类页面中图片地址
def find_images(suburl):
    #print('suburl: ',suburl)
    imglist=[]
    html = suburl
    res = rqs.urlopen(suburl).read().decode('GB2312',errors = 'ignore') # 有了网站地址后向服务器发出请求
    ''' < div    class ="list_1Pic" > < img src="https://pic03.scbao.com/201017/1081972-20101F1255119-lp.jpg" alt="唯美原生态瀑布" > < / div >'''

    p=r'<div class="list_1Pic"><img src="([^"]+\.jpg)"' # 匹配除“号后的所有包括.jpg的内容
    #print('bs ',bs)
    tempimages =re.findall(p,res)  #

    for image in tempimages:  # 在列表中循环
        #print(image)
        imglist.append(image)
    #print('imglist: ',imglist)
    return imglist

#保存图片到指定的目录下
def savepicture(savepath,classlist,imgurl):
    response=rqs.urlopen(imgurl)
    picture=response.read()
    imgname=imgurl.split('/')[-1]    #截取后面的文件名
    img=savepath+'/'+classlist+'/'+imgname
    print('img is :',img)
    try:
        with open(img,'wb') as fw:  #保存在对应的子类下面
            fw.write(picture)
    except FileExistsError as fer:
        print('文件已存在')

#下载图片
def downloadmm(savepath,pages=10):
    #mkdir('picture',savepath)
    url='https://www.taopic.com/tuku/'
    subimgs=get_page(url)      #获取图片分类
    len1=len(subimgs)
    for i in range(0,pages,1):
        if i>=len1-1:
            break
        suburl=url+subimgs[i]   #将获的分类拼装成URL
        imgaddress=find_images(suburl) #访问拼装的URL（此页面中包括该类的图片地址，N多图片）
        time.sleep(random.randrange(1, 10, 1)) #随机生成1~10的随机数
        for img in imgaddress:
            picture=savepicture(savepath,subimgs[i],img)

if __name__ == '__main__':
    savepath = 'D:/pythonTtest/TDXPystock/other/picture'
    #downloadmm(savepath,pages=10)  #爬取图片
    #getproxy(url='http://31f.cn/http-proxy/')
    proxytest() #使用代理  （代理不稳定）