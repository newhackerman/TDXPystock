import requests as req

import json,re


class checkStock():

    @staticmethod
    def baolei(stockcode) ->str:
        url = 'http://page3.tdx.com.cn:7615/site/pcwebcall_static/bxb/json/%s.js'
        fxlist=[]
        sum=100  #股票评分，默认100分，如果出现风险项则减出相应的分数
        # self.stockcode=stockcode
        url1=url %stockcode
        try:
            response=req.get(url1)
        except BaseException as B:
            print(B)
            print('查询异常！！！！')
            return None
        reg='g_sdata=(.*)'
        # print(response.text)
        catalog=re.findall(reg,response.text,re.M)[0]
        # print(catalog)
        checksum=json.loads(catalog)['total']  #检查风险项数
        checkname=json.loads(catalog)['name']  #股票名称
        isfengxiantotal=int(json.loads(catalog)['num']) #存在风险项
        if isfengxiantotal ==0:
            print('未查出风险 ! 代码：%s 名称：%s   评分为：%s ' % (str(stockcode), checkname, str(sum)))
            return fxlist,sum
        else:
            fxdata=json.loads(catalog)['data']
            cwfx=fxdata[0]['rows']    #财务类风险
            scfx = fxdata[1]['rows']  #市场类风险
            jyfx = fxdata[2]['rows']  #交易类风险
            tsfx = fxdata[3]['rows']  #退市类风险

            for data in cwfx:
                trig=data['trig']
                if trig==1:
                    fx=data['lx']
                    fxscore = data['fs']  # 风险分数
                    sum = sum - fxscore
                    trigtext=data['trigyy']
                    fxlist.append('财务类风险：'+fx+'\t 风险详情：'+trigtext)

            for data in scfx:
                trig=data['trig']
                if trig==1:
                    fx=data['lx']
                    fxscore = data['fs']  # 风险分数
                    sum = sum - fxscore
                    trigtext=data['trigyy']
                    fxlist.append('市场类风险：'+fx+'\t 风险详情：'+trigtext)

            for data in jyfx:
                trig=data['trig']
                if trig==1:
                    fx=data['lx']
                    fxscore = data['fs']  # 风险分数
                    sum = sum - fxscore
                    trigtext=data['trigyy']
                    fxlist.append('交易类风险：'+fx+'\t 风险详情：'+trigtext)

            for data in tsfx:
                trig=data['trig']
                if trig==1:   #trig==1 表示存在风险
                    fx=data['lx']  #风险名称
                    fxscore=data['fs']   #风险风数
                    sum=sum-fxscore
                    trigtext=data['trigyy']  #风险描述
                    fxlist.append('交易类风险：'+fx+'\t 风险详情：'+trigtext)
            print('代码：%s  名称：%s   评分为：%s '%(str(stockcode),checkname,str(sum)))
            print('分险项为：')
            for data in fxlist:
                print(data)

            return fxlist,fxscore
if __name__ == '__main__':
    process=checkStock()
    process.baolei('600120')



