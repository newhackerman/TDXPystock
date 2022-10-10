# 从同花顺获取竞价数据
    def getstockNowjinjiaFromTHS(self,tradedate):
        tradedate1=str(tradedate)[0:4]+'年'+str(tradedate)[5:7]+'月'+str(tradedate)[8:10]+'日'
        tradedate2=str(tradedate)[0:4]+str(tradedate)[5:7]+str(tradedate)[8:10]
        dateText=str(tradedate)+'日'
        datenow = datetime.datetime.now().strftime('%H%M%S')
        now = tradeday.getlastTradeday()
        istraday = tradeday.isTradeDay()
        if datenow < '092500' and istraday:
            now = tradeday.getlastNtradeday(2)
        filename = u'./outdata/竞价数据/竞价数据_' + str(tradedate) + '_' + str(self.pageid) + '.csv'
        if os.path.exists(filename):
            pddata = pd.read_csv(filename)
            self.insertNowdata(pddata)
            return pddata
        content = ''
        jinjiadatainfos = []
        url = f'http://www.iwencai.com/gateway/urp/v7/landing/getDataList'
        header={
            'Host':'ai.iwencai.com',
                'Connection':'keep-alive',
                'Content-Length':'880',
                'Accept':'application/json',
                'User-Agent':'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1',
                'Content-Type':'application/x-www-form-urlencoded',
                'Origin':'http://wap.iwencai.com',
                'Referer':'http://wap.iwencai.com/',
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8'}
           start=(int(self.pageid)-1)*self.step
        end=(int(self.pageid))*self.step+1
        for i in range(start+1,end):
            postdata={
                'query': self.tradedate+'日集合竞价额',
                'urp_sort_index': '',
                'urp_sort_way': 'desc',
                'condition': '[{"dateText":"'+dateText+'","indexName":"竞价金额","indexProperties":["交易日期 '+tradedate2+'"],"dateUnit":"日","source":"new_parser","type":"index","indexPropertiesMap":{"交易日期":"'+dateText+'"},"reportType":"TRADE_DAILY","dateType":"交易日期","chunkedResult":"'+dateText+'集合竞价额","valueType":"_浮点型数值(元)","domain":"abs_股票领域","uiText":"'+tradedate1+'的竞价金额","sonSize":0,"queryText":"'+tradedate1+'的竞价金额","relatedSize":0,"tag":"['+tradedate+']竞价金额"}]',
                'codelist': '',
                'is_cache': '1',
                'perpage': 100,
                'page': str(i),
                'logid': '',
                'ret': 'json_all',
                'sessionid':'',
                'iwc_token': '',
                'urp_use_sort': '1',
                'user_id': '234319860',
                'uuids[0]': '24087',
                'query_type': 'stock',
                'comp_id':iwencai_comp_id,
                'business_cat': 'soniu',
                'uuid': '24087'
            }
            try:
                content = req.post(url=url,headers=header, data=postdata,timeout=6).json()
                # print('收到的内容为：', content)
            except BaseException as b:
                print('获取竞价数据请求异常',b)
                time.sleep(3)
                count = 0
                while count < 5:
                    try:
                        content = req.post(url=url,headers=header, data=postdata,timeout=15).json()
                    except BaseException as b:
                        time.sleep(2)
                        continue
                    if content != '':
                        break

            if content['status_code']!='0':
                continue
            jsondata = content['answer']['components'][0]['data']['datas']
            if jsondata is None:
                continue
            HDDATE =tradedate
            # print(jsondata)
            if jsondata is None:
                continue
            for jsondata1 in jsondata:
                # print(jsondata1)
                try:
                    # print(jsondata1)
                    code=jsondata1['code']
                    name = jsondata1['股票简称']
                    vol =''
                    try:
                        price = jsondata1['最新价']
                    except BaseException as b:
                        price=''
                    jjje=str('竞价金额['+self.tradedate+']')
                    # print(jjje)
                    amount=''
                    try:
                        amount =jsondata1[jjje]
                    except BaseException as b:
                        jjje = str('竞价金额[' +tradedate2 + ']')
                        amount = jsondata1[jjje]
                    drict =''
                    market=jsondata1['股票代码'][7:9]
                    marketcode='1'
                    if market=='SZ':
                        marketcode='0'
                    tmpdict = {'HDDATE': HDDATE, 'code': code, 'name': name, 'vol': vol, 'price': price,
                               'amount': amount, 'drict': drict, 'market': marketcode}
                    # print(tmpdict)
                    jinjiadatainfos.append(tmpdict)
                    # print('第%d 页数据为:,%s' %(i,jinjiadatainfos))

                except BaseException as b:
                    continue
        self.insertNowdata(pd.DataFrame(jinjiadatainfos))
