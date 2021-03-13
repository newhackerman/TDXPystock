import akshare as ak #api 使用：https://akshare-4gize6tod19f2d2e-1252952517.tcloudbaseapp.com/index.html
import pandas as pd
import time

#A股相关
class akShareUnit():

    #股票列表-A股
    def get_stock_info_a_code_name(self):
        '''
                        code   name
                0     000001   平安银行
         '''
        stock_info_a_code_name_df = ak.stock_info_a_code_name()
        return stock_info_a_code_name_df
    #股票列表-上证
    def get_stock_info_sh_name_code(self,indicator):
        '''
        :param indicator:
        indicator="主板A股"; choice of {"主板A股", "主板B股", "科创板"}

        :return:
        '''
        stock_info_sh_df = ak.stock_info_sh_name_code(indicator="主板A股")
        return stock_info_sh_df

    #股票列表-深证(含基本信息)
    def get_stock_info_sz_name_code(self,indicator):
        '''
        :param indicator: indicator="A股列表"; choice of {"A股列表", "B股列表", "CDR列表", "AB股列表"}

        :return:
        公司代码	str	Y	-
        公司简称	str	Y	-
        公司全称	str	Y	-
        英文名称	str	Y	-
        注册地址	str	Y	-
        A股代码	str	Y	-
        A股简称	str	Y	-
        A股上市日期	str	Y	-
        A股总股本	str	Y	-
        A股流通股本	str	Y	-
        B股代码	str	Y	-
        B股简称	str	Y	-
        B股上市日期	str	Y	-
        B股总股本	str	Y	-
        B股流通股本	str	Y	-
        地区	str	Y	-
        省份	str	Y	-
        城市	str	Y	-
        所属行业	str	Y	-
        公司网址	str	Y	-
        '''
        stock_info_sz_df = ak.stock_info_sz_name_code(indicator="A股列表")
        return stock_info_sz_df


    # 例获取基金排名top20
    def get_Topjijin(self):
        repsponse = ak.fund_em_open_fund_rank()
        print(repsponse.head(21))
        return repsponse.head(21)    #获取基金排名

    # 主要股东
    def get_stock_main_stock_holder(self,stockcode):
        stock_main_stock_holder_df = ak.stock_main_stock_holder(stock=stockcode)
        return stock_main_stock_holder_df
    #机构持股一览表
    def get_stock_institute_hold(self,quarter):
        '''

        :param quarter:
        quarter="20051"; 从 2005 年开始, {"一季报":1, "中报":2 "三季报":3 "年报":4}, e.g., "20191", 其中的 1 表示一季报; "20193", 其中的 3 表示三季报;

        :return:
        证券代码	str	Y	-
        证券简称	str	Y	-
        机构数	float	Y	-
        机构数变化	float	Y	-
        持股比例	float	Y	注意单位: %
        持股比例增幅	float	Y	注意单位: %
        占流通股比例	float	Y	注意单位: %
        占流通股比例增幅	float	Y	注意单位: %
        '''
        stock_institute_hold_df = ak.stock_institute_hold(quarter=quarter)
        return stock_institute_hold_df
    #机构持股详情
    def get_stock_institute_hold_detail(self,stockcode,quarter):
        '''

          :param stockcode:
          stockcode="300003"; 股票代码
          :param quarter:
          quarter="20201"; 从 2005 年开始, {"一季报":1, "中报":2 "三季报":3 "年报":4}, e.g., "20191", 其中的 1 表示一季报; "20193", 其中的 3 表示三季报;

          :return:
            持股机构类型	str	Y	-
            持股机构代码	str	Y	-
            持股机构简称	float	Y	-
            持股机构全称	float	Y	-
            持股数	float	Y	注意单位: 万股
            最新持股数	float	Y	注意单位: 万股
            持股比例	float	Y	注意单位: %
            最新持股比例	float	Y	注意单位: %
            占流通股比例	float	Y	注意单位: %
            最新占流通股比例	float	Y	注意单位: %
            持股比例增幅	float	Y	注意单位: %
            占流通股比例增幅	float	Y	注意单位: %
          '''
        stock_institute_hold_detail_df = ak.stock_institute_hold_detail(stock=stockcode, quarter=quarter)
        return stock_institute_hold_detail_df

    #获取个股实情行情(所有A股)
    def get_CurrentQuoteS(self):
        response=ak.stock_zh_a_spot()
        return response

    #指数实时行情数据(所有指数)
    def get_bank_CurrentQuotes(self):
        stock_df = ak.stock_zh_index_spot()
        return stock_df

    #获取个股历史行情
    def get_stockQuotes(self,stockcode,stardate,enddate):
        if stockcode[0:2]=='60' or stockcode[0:2]=='68':
            stockcode='sh'+stockcode
        else:
            stockcode='sz'+stockcode

        response = ak.stock_zh_a_daily(symbol=stockcode, start_date=stardate, end_date=enddate,
                                                      adjust="qfq")
        return  response

    # 获取指数历史行情
    def stock_zh_index_daily_tx(self,stockcode):
        if stockcode[0:1] == '6' :
            stockcode = 'sh' + stockcode
        else:
            stockcode = 'sz' + stockcode
        stock_zh_index_daily_df = ak.stock_zh_index_daily_tx(symbol=stockcode)
        return stock_zh_index_daily_df

    #获取 1, 5, 15, 30, 60 分钟的数据(所有历史分时行情数据)
    def get_min_stockQuotes(self,stockcode,period,*adjust):
        if stockcode[0:2]=='60' or stockcode[0:2]=='68':
            stockcode='sh'+stockcode
        else:
            stockcode='sz'+stockcode

        if adjust==None:
            stock_zh_a_minute_df = ak.stock_zh_a_minute(symbol=stockcode, period=period, adjust="qfq")
            return stock_zh_a_minute_df
        else:
            stock_zh_a_minute_df = ak.stock_zh_a_minute(symbol=stockcode, period=period, adjust=adjust)
            return stock_zh_a_minute_df

    #某个 A 上市公司的近 2 年历史分笔行情数据
    def get_stock_zh_a_tick_tx(self,stockcode,tradeDate):
        if stockcode[0:2]=='60' or stockcode[0:2]=='68':
            stockcode='sh'+stockcode
        else:
            stockcode='sz'+stockcode

        stock_zh_a_tick_tx_df = ak.stock_zh_a_tick_tx(code=stockcode, trade_date=tradeDate)
        return stock_zh_a_tick_tx_df

    #从新浪财经获取科创板股票数据(所有科创板)
    def get_stock_zh_kcb_spot(self):
        stock_zh_kcb_spot_df = ak.stock_zh_kcb_spot()
        return stock_zh_kcb_spot_df

    #科创板历史行情数据
    def get_stock_zh_kcb_daily(self,stockcode,adjust):
        stockcode='sh'+stockcode
        stock_zh_kcb_daily_df = ak.stock_zh_kcb_daily(symbol=stockcode, adjust="hfq")
        return stock_zh_kcb_daily_df

    #美股实时行情数据(所有美股，数据延迟15分钟)
    def get_stock_us_spot(self):
        us_stock_current_df = ak.stock_us_spot()
        return us_stock_current_df

    #美股历史行情数据
    def get_stock_us_daily(self,stockcode,adjust):
        stock_us_daily_df = ak.stock_us_daily(symbol=stockcode, adjust=adjust)
        return stock_us_daily_df

    #美股基本面数据
    def get_stock_us_fundamental(self,stockcode,sysmbol):
        stock_us_fundamental_df = ak.stock_us_fundamental(stock=stockcode, symbol=sysmbol)
        return stock_us_fundamental_df
        '''
        stock="GOOGL"; 美股 ticker, 可以通过调用 stock_us_fundamental(stock="GOOGL", symbol="info") 获取所有 ticker
        symbol="info"; info, 返回所有美股列表, PE, 返回 PE 数据, PB, 返回 PB 数据
        '''

    #港股实时行情数据（延时15分钟 如果要实时数据可以采用富途的接口，富途需要独立安装网关）
    def get_stock_hk_spot(self):
        current_data_df = ak.stock_hk_spot()
        return current_data_df

    #港股历史行情数据
    def get_stock_hk_daily(self,stockcode,adjust):
        stock_hk_daily_hfq_df = ak.stock_hk_daily(symbol=stockcode, adjust=adjust)
        return stock_hk_daily_hfq_df
    #美港目标价  获取美港电讯-美港目标价数据
    def get_stock_js_price(self,category):
        '''

        :param category:
        category="us"; choice of {"us", "hk"}

        :return:
        id	float	Y	-
        indicator_id	float	Y	-
        latest_rating	str	Y	-
        previous_rating	str	Y	-
        latest_target_price	str	Y	-
        previous_target_price	str	Y	-
        institution	str	Y	-
        pub_time	str	Y	-
        status	float	Y	-
        name	str	Y	-
        us	float	Y	-
        hk	float	Y
        '''
        stock_js_price_df = ak.stock_js_price(category=category)
        return stock_js_price_df

    #机构调研-统计
    def stock_em_jgdy_tj(self):
        stock_em_jgdy_tj_df = ak.stock_em_jgdy_tj()
        return stock_em_jgdy_tj_df

    #机构调研-详细 stock_em_jgdy_detail
    def get_stock_em_jgdy_detail(self):
        stock_em_jgdy_detail_df = ak.stock_em_jgdy_detail()
        return stock_em_jgdy_detail_df

    # 股权质押市场概况
    def get_stock_em_gpzy_profile(self):
        stock_em_gpzy_profile_df = ak.stock_em_gpzy_profile()
        return stock_em_gpzy_profile_df

    # 上市公司质押比例
    def get_stock_em_gpzy_pledge_ratio(self,trade_date):
        stock_em_gpzy_pledge_ratio_df = ak.stock_em_gpzy_pledge_ratio(trade_date=trade_date)  #"2020-08-14"
        return stock_em_gpzy_pledge_ratio_df
    #重要股东股权质押明细
    def get_stock_em_gpzy_pledge_ratio_detail(self):
        stock_em_gpzy_pledge_ratio_detail_df = ak.stock_em_gpzy_pledge_ratio_detail()
        return stock_em_gpzy_pledge_ratio_detail_df

    #股票账户统计月度
    def get_stock_em_account(self):
        stock_em_account_df = ak.stock_em_account()
        return stock_em_account_df
        '''
        输出参数

        名称	类型	默认显示	描述
        数据日期	str	Y	-
        新增投资者-数量	float	Y	注意单位: 万户
        新增投资者-环比	float	Y	-
        新增投资者-同比	float	Y	-
        期末投资者-总量	float	Y	注意单位: 万户
        期末投资者-A股账户	float	Y	注意单位: 万户
        期末投资者-B股账户	float	Y	注意单位: 万户
        上证指数-收盘	float	Y	-
        上证指数-涨跌幅	float	Y	-
        沪深总市值	float	Y	-
        沪深户均市值	float	Y	注意单位: 万
        :return:
        '''
    #个股资金流
    def get_stock_individual_fund_flow(self,stockcode):
        if stockcode[0:2] == '60' or stockcode[0:2] == '68':
            market = 'sh'
        else:
            market = 'sz'
        stock_individual_fund_flow_df = ak.stock_individual_fund_flow(stock=stockcode, market=market)
        return stock_individual_fund_flow_df
        '''
        日期     主力净流入-净额     小单净流入-净额  ... 超大单净流入-净占比   收盘价    涨跌幅
        0    2019-12-05     475688.0    5588835.0  ...      14.38  6.19  -1.12
        1    2019-12-06   49393149.0    1142685.0  ...      35.56  6.30   1.78'''

    #个股资金流排名
    def get_stock_individual_fund_flow_rank(self,indicator): #indicator="今日"; {"今日", "3日", "5日", "10日"}
        stock_individual_fund_flow_rank_df = ak.stock_individual_fund_flow_rank(indicator="今日")
        return stock_individual_fund_flow_rank_df
        '''
        output
        最新价	float	Y	-
        涨跌幅	str	Y	注意单位: %
        代码	str	Y	-
        名称	str	Y	-
        主力净流入-净额	float	Y	-
        主力净流入-净占比	float	Y	注意单位: %
        超大单净流入-净额	float	Y	-
        超大单净流入-净占比	float	Y	注意单位: %
        大单净流入-净额	float	Y	-
        大单净流入-净占比	float	Y	注意单位: %
        中单净流入-净额	float	Y	-
        中单净流入-净占比	float	Y	注意单位: %
        小单净流入-净额	float	Y	-
        小单净流入-净占比	float	Y	注意单位: %
        '''
    #大盘资金流
    def get_stock_market_fund_flow(self):
        stock_market_fund_flow_df = ak.stock_market_fund_flow()
        return stock_market_fund_flow_df
        '''
         日期   上证-收盘价 上证-涨跌幅  ... 中单净流入-净占比        小单净流入-净额 小单净流入-净占比
        0    2020-07-22  3333.16   0.37  ...     -0.51   21186158592.0      1.77
        1    2020-07-23  3325.11  -0.24  ...      0.22   53341659136.0      4.28
        '''
    #板块资金流排名
    def get_stock_sector_fund_flow_rank(self,indicator,sector_type):
        '''
        indicator="5日"; choice of {"今日", "5日", "10日"}
        sector_type="地域资金流"; choice of {"行业资金流": "2", "概念资金流": "3", "地域资金流": "1"}
        :return:
        名称	str	Y	-
        今日涨跌幅	str	Y	注意单位: %
        主力净流入-净额	float	Y	-
        主力净流入-净占比	float	Y	注意单位: %
        超大单净流入-净额	float	Y	-
        超大单净流入-净占比	float	Y	注意单位: %
        大单净流入-净额	float	Y	-
        大单净流入-净占比	float	Y	注意单位: %
        中单净流入-净额	float	Y	-
        中单净流入-净占比	float	Y	注意单位: %
        小单净流入-净额	float	Y	-
        小单净流入-净占比	float	Y	注意单位: %
        主力净流入最大股	float	Y	-
        '''
        stock_sector_fund_flow_rank_df = ak.stock_sector_fund_flow_rank(indicator=indicator, sector_type=sector_type)
        return stock_sector_fund_flow_rank_df

    #流通股东
    def get_stock_circulate_stock_holder(self,stockcode):
        stock_circulate_stock_holder_df = ak.stock_circulate_stock_holder(stock=stockcode)
        return stock_circulate_stock_holder_df
    #龙虎榜-每日详情
    def get_stock_sina_lhb_detail_daily(self,trade_date,symbol):
        '''

        :param trade_date:
        trade_date="20200730"; 交易日
        symbol="涨幅偏离值达7%的证券"; 调用ak.stock_sina_lhb_detail_daily(trade_date="指定交易日",
        symbol="返回当前交易日所有可查询的指标" 返回可以获取的指标

        :return:
        序号	str	Y	股票代码
        股票代码	str	Y	股票简称
        股票名称	str	Y	发布时间
        收盘价	str	Y	注意单位: 元
        对应值	str	Y	注意单位: %
        成交量	str	Y	注意单位: 万股
        成交额	str	Y	注意单位: 万元
        '''
        indicator_name_list = ak.stock_sina_lhb_detail_daily(trade_date=trade_date, symbol=symbol)
        stock_sina_lhb_detail_daily_df = ak.stock_sina_lhb_detail_daily(trade_date=trade_date, symbol=symbol)
        return  indicator_name_list,stock_sina_lhb_detail_daily_df

    #龙虎榜-个股上榜统计
    def get_stock_sina_lhb_ggtj(self,recent_day):
        '''
        recent_day="5"; choice of {"5": 最近 5 天; "10": 最近 10 天; "30": 最近 30 天; "60": 最近 60 天;}

        :param recent_day:
        :return:
        股票代码	str	Y	-
        股票名称	str	Y	-
        上榜次数	str	Y	-
        累积购买额	str	Y	注意单位: 万
        累积卖出额	str	Y	注意单位: 万
        净额	str	Y	注意单位: 万
        买入席位数	str	Y	-
        卖出席位数	str	Y	-
             股票代码  股票名称  上榜次数      累积购买额      累积卖出额         净额  买入席位数  卖出席位数
        0    002415  海康威视     1  301832.02  111932.27  189899.75      5      4
        1    002625  光启技术     3  188974.51  110632.86   78341.65     13     11
        '''
        stock_sina_lhb_ggtj_df = ak.stock_sina_lhb_ggtj(recent_day="5")
        return stock_sina_lhb_ggtj_df

    #龙虎榜-营业上榜统计
    def get_stock_sina_lhb_yytj(self,recent_day):
        '''
        :param recent_day:recent_day="5"; choice of {"5": 最近 5 天; "10": 最近 10 天; "30": 最近 30 天; "60": 最近 60 天;}
         :return:
         营业部名称	str	Y	-
        上榜次数	str	Y	-
        累积购买额	str	Y	注意单位: 万
        买入席位数	str	Y	-
        累积卖出额	str	Y	注意单位: 万
        卖出席位数	str	Y	-
        买入前三股票	str	Y	-
          营业部名称  上榜次数    累积购买额  ...     累积卖出额  卖出席位数          买入前三股票
        0       长城证券股份有限公司资阳娇子大道证券营业部     2  2494.35  ...      0.00      0       展鹏科技,山东威达
        1       上海证券有限责任公司苏州干将西路证券营业部     2  3519.09  ...      0.00      0            展鹏科技
        '''
        stock_sina_lhb_yytj_df = ak.stock_sina_lhb_yytj(recent_day=recent_day)
        return stock_sina_lhb_yytj_df

    #龙虎榜-机构席位成交明细
    def get_stock_sina_lhb_jgmx(self):
        stock_sina_lhb_jgmx_df = ak.stock_sina_lhb_jgmx()
        return stock_sina_lhb_jgmx_df

    #大宗交易-市场统计
    def get_stock_dzjy_sctj(self):
        stock_dzjy_sctj_df = ak.stock_dzjy_sctj()
        return stock_dzjy_sctj_df

    #大宗交易-每日明细
    def get_stock_dzjy_mrmx(self,symbol,start_date,end_date):
        '''
        :param symbol: symbol='债券'; choice of {'A股', 'B股', '债券'}
        :param start_date:start_date='2020-11-23'; 开始日期
        :param end_date:end_date='2020-12-04'; 结束日期
        :return:
        '''
        stock_dzjy_mrmx_df = ak.stock_dzjy_mrmx(symbol=symbol, start_date=start_date, end_date=end_date)
        return stock_dzjy_mrmx_df
    #融资融券汇总
    def get_stock_margin_sse(self,start_date,end_date)  :
        '''
        :param start_date:start_date="20010106"
        :param end_date:end_date="20010106"
        :return:
        信用交易日期	str	Y	-
        融资余额	float	Y	注意单位: 元
        融资买入额	float	Y	注意单位: 元
        融券余量	float	Y	-
        融券余量金额	float	Y	注意单位: 元
        融券卖出量	float	Y	-
        融资融券余额	float	Y	注意单位: 元
        '''
        stock_margin_sse_df = ak.stock_margin_sse(start_date="20010106", end_date="20210208")
        return stock_margin_sse_df
    #融资融券明细
    def get_stock_margin_detail_sse(self,date):
        '''     :param date: date="20210205"
        :return:
        信用交易日期	str	Y	-
        标的证券代码	str	Y	-
        标的证券简称	str	Y	-
        融资余额	float	Y	注意单位: 元
        融资买入额	float	Y	注意单位: 元
        融资偿还额	float	Y	注意单位: 元
        融券余量	float	Y	-
        融券卖出量	float	Y	-
        融券偿还量	float	Y	-
        '''
        stock_margin_detail_sse_df = ak.stock_margin_detail_sse(date="20210201")
        return stock_margin_detail_sse_df

    #研究报告-盈利预测
    def get_stock_profit_forecast(self):
        stock_profit_forecast_df = ak.stock_profit_forecast()
        return stock_profit_forecast_df


#北向资金相关
class hsgt_north():
    #北向净流入
    def get_stock_em_hsgt_north_net_flow_in(self):
        stock_em_hsgt_north_net_flow_in_df = ak.stock_em_hsgt_north_net_flow_in(indicator="北上") #indicator="沪股通"; 三选一 ("沪股通", "深股通", "北上")
        return stock_em_hsgt_north_net_flow_in_df
    #北向资金余额
    def get_stock_em_hsgt_north_cash(self):
        stock_em_hsgt_north_cash_df = ak.stock_em_hsgt_north_cash(indicator="北上") #indicator="沪股通"; 三选一 ("沪股通", "深股通
        return stock_em_hsgt_north_cash_df
    #北向累计净流入
    def get_stock_em_hsgt_north_acc_flow_in(self):
        stock_em_hsgt_north_acc_flow_in_df = ak.stock_em_hsgt_north_acc_flow_in(indicator="北上") #indicator="沪股通"; 三选一 ("沪股通", "深股通
        return stock_em_hsgt_north_acc_flow_in_df

    #沪深港通持股-行业板块排行
    def get_stock_em_hsgt_board_rank(self,symbol,indicator):
        '''
        symbol="北向资金增持行业板块排行"; choice of {"北向资金增持行业板块排行", "北向资金增持概念板块排行", "北向资金增持地域板块排行"}
        indicator="今日"; choice of {"今日", "3日", "5日", "10日", "1月", "1季", "1年"}
        '''
        stock_em_hsgt_industry_rank_df = ak.stock_em_hsgt_board_rank(symbol=symbol, indicator=indicator)
        return stock_em_hsgt_industry_rank_df
        '''
        序号	int	Y	-
        名称	str	Y	-
        最新涨跌幅	float	Y	注意单位: %
        北向资金今日持股-股票只数	float	Y	-
        北向资金今日持股-市值	float	Y	注意单位: 元
        北向资金今日持股-占板块比	float	Y	-
        北向资金今日持股-占北向资金比	float	Y	-
        北向资金今日增持估计-股票只数	float	Y	-
        北向资金今日增持估计-市值	float	Y	注意单位: 元
        北向资金今日增持估计-市值增幅	float	Y	-
        北向资金今日增持估计-占板块比	float	Y	-
        北向资金今日增持估计-占北向资金比	float	Y	-
        今日增持最大股-市值	float	Y	-
        今日增持最大股-占股本比	float	Y	-
        今日减持最大股-占股本比	float	Y	-
        今日减持最大股-市值	float	Y	-
        '''
    #个股排行
    def get_stock_em_hsgt_hold_stock(self,market,indicator):
        '''market="沪股通"; choice of {"北向", "沪股通", "深股通"}
        indicator="沪股通"; choice of {"今日排行", "3日排行", "5日排行", "10日排行", "月排行", "季排行", "年排行"}
        '''
        stock_em_hsgt_hold_stock_df = ak.stock_em_hsgt_hold_stock(market="北向", indicator="今日排行")
        return stock_em_hsgt_hold_stock_df

#南向相关
class  hsgt_south():

    #南向净流入
    def get_stock_em_hsgt_south_net_flow_in(self):
        stock_em_hsgt_south_net_flow_in_df = ak.stock_em_hsgt_south_net_flow_in(indicator="南下")  #indicator="沪股通"; choice of {"沪股通", "深股通", "南下"}
        return stock_em_hsgt_south_net_flow_in_df

    #南向资金余额
    def get_stock_em_hsgt_south_cash(self):
        stock_em_hsgt_south_cash_df = ak.stock_em_hsgt_south_cash(indicator="南下")
        return stock_em_hsgt_south_cash_df
    #南向累计净流入
    def get_stock_em_hsgt_south_acc_flow_in(self):
        stock_em_hsgt_south_acc_flow_in_df = ak.stock_em_hsgt_south_acc_flow_in(indicator="南下")
        return stock_em_hsgt_south_acc_flow_in_df
#期货相关
class futures():
    #日线行情K线
    def get_get_futures_daily(self,start_date,end_date,market):
        '''
        :param start_date: start_date="20190107"
        :param end_date:end_date="20190108"
        :param market: 可以添为四个交易所的简称, 即 “DCE” 代表大商所; “INE” 代表能源所; “SHFE” 代表上期所; “CZCE” 代表郑商所,
        :return:
        '''
        futures_daily_df = ak.get_futures_daily(start_date=start_date, end_date=end_date, market=market,index_bar=True)
        return futures_daily_df
    #期货行情数据-实时行情数据
    def get_futures_zh_spot(self,subscribe_list,market,adjust):
        '''
        :param subscribe_list: 需要订阅的合约代码; e.g., 按照示例获取
        :param market:market="CF"; market="CF": 商品期货, market="FF": 金融期货
        :param adjust:adjust=False; adjust=True: 返回合约、交易所和最小变动单位的实时数据, 返回数据会变慢
        :return:
            symbol	str	Y	品种
            time	float	Y	时间, e.g., 144050表示下午14点40分50秒
            open	float	Y	开盘
            high	float	Y	高
            low	float	Y	低
            current_price	str	Y	当前价格(买价)
            bid_price	str	Y	买
            ask_price	str	Y	卖价
            buy_vol	float	Y	买量
            sell_vol	float	Y	卖量
            hold	float	Y	持仓量
            volume	str	Y	成交量
            avg_price	float	Y	均价
            last_close	float	Y	上一个交易日的收盘价
            last_settle_price	str	Y	上一个交易日的结算价
        '''
        dce_text = ak.match_main_contract(exchange="dce")
        czce_text = ak.match_main_contract(exchange="czce")
        shfe_text = ak.match_main_contract(exchange="shfe")
        while True:   #实时订阅
            time.sleep(3)
            data = ak.futures_zh_spot(
                subscribe_list=",".join([dce_text, czce_text, shfe_text]),
                market=market,
                adjust=adjust)
            print(data)
            return data

    #期货历史行情数据
    def get_futures_daily(self,start_date,end_date,market,index_bar):
        '''
        名称	类型	必选	描述
        start_date	str	Y	start_date="20200701"
        end_date	str	Y	end_date="20200716"
        market	str	Y	market="DCE"; choice of {"CFFEX", "INE", "CZCE", "DCE", "SHFE"}
        index_bar	str	Y	index_bar=False; 是否合成指数
        out
        名称	类型	默认显示	描述
        symbol	str	Y	合约
        date	str	Y	交易日
        open	float	Y	开盘价
        high	float	Y	最高价
        low	float	Y	最低价
        close	str	Y	收盘价
        volume	str	Y	成交量
        open_interest	str	Y	持仓量
        turnover	float	Y	成交额
        settle	float	Y	结算价
        pre_settle	float	Y	前结算价
        variety	str	Y	品种
        '''
        futures_daily_df = ak.get_futures_daily(start_date=start_date, end_date=end_date, market=market,
                                                    index_bar=index_bar)
        return futures_daily_df

#恐慌指数
def get_index_vix(start_date,end_date):
    '''

    :param start_date:start_date="2020-06-11"
    :param end_date:end_date="2020-06-11"
    :return:
    开盘价    当前价    涨跌    涨跌幅
    2020-03-20 00:00  76.45  76.68  0.23   0.30
    2020-03-20 00:01  76.45  76.79  0.34   0.44
    '''
    index_vix_df = ak.index_vix(start_date=start_date, end_date=end_date)  # 只能获取当前交易日近一个月内的数据
    return  index_vix_df

if __name__ == '__main__':
    aks=akShareUnit()
    stockcurrent=aks.get_CurrentQuoteS()

    bankcurrent=aks.get_bank_CurrentQuotes()

    print(stockcurrent.head(20))

