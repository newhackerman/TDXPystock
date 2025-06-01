## Core Functionalities and Data Sources of 操盘神器

This document outlines the core functionalities and data sources of the "操盘神器" application, based on an analysis of its UI elements in `操盘神器ui.py`.

### I. Main UI Structure

The application is divided into a left main area (`tabWidget_left`) and a right content area (`tabWidget_rightcontent`), along with a main table at the bottom (`tableView_zhangtingdata`) and a menu bar (`menubar`).

### II. Left Main Area (`tabWidget_left`)

This area contains multiple tabs for different market data and analysis.

1.  **监控中心 (Monitoring Center) (`tab_monitorcenter`)**
    *   **Displays:**
        *   大单 (Large Orders): `tableView_superAmount` (Table View) - Likely shows real-time large transaction data.
        *   龙头 (Dragon Stocks/Leading Stocks): `textEdit_drogMoniter` (Text Edit) - Displays information related to leading or trending stocks.
        *   Bank Monitor (Sector/Block Monitoring): `tableView_bankMonitor` (Table View) - Appears to monitor specific sectors or blocks of stocks.
    *   **Labels:**
        *   `label_drogstock`: "龙头"
        *   `label_superAmount`: "大单"
        *   `label_zhangting`: "实时涨停" (Real-time Limit-Up Stocks) - This label is present, but the associated table `tableView_zhangtingdata` is outside this tab.

2.  **行业与概念 (Industry and Concepts) (`tab_bankcenter`)**
    *   **Displays:**
        *   行业板块 (Industry Sectors): `banktabview` (Table View) - Shows data related to industry sectors.
        *   个股行情 (Stock Quotes): `bankstockquote` (Table View) - Displays quotes for individual stocks within a sector/concept.
        *   概念板块 (Concept Sectors): `ganniantabview` (Table View) - Shows data related to concept-based stock categories.
        *   个股资金 (Stock Funds): `bankstock_award` (Table View) - Likely shows fund flow for individual stocks.
    *   **Controls:**
        *   `comboBox_bankgainianflash`: Dropdown for refresh interval settings (e.g., 3s, 5s, 10s).
    *   **Labels:**
        *   `label_flashtimesset`: "刷新间隔设置（s）" (Refresh Interval Setting (s))
        *   `label_ganianbank`: "概念板块"
        *   `label_stockamound`: "个股资金"
        *   `label_hybank`: "行业板块"
        *   `label_stockquotes`: "个股行情"

3.  **指数 (Indices) (`tab_point`)**
    *   **Displays:**
        *   Point Data: `tableView_ponitdata` (Table View) - Shows data for market indices.

4.  **全球指数 (Global Indices) (`tab_2`)**
    *   **Displays:**
        *   Global Point Data: `tableView_globalpoint` (Table View) - Shows data for global market indices.

5.  **ETF行情 (ETF Quotes) (`tab_3`)**
    *   **Displays:**
        *   ETF Data: `tableView_ETF` (Table View) - Shows quotes and data for ETFs.

6.  **可转债 (Convertible Bonds) (`tab`)**
    *   **Displays:**
        *   Convertible Bond Data: `tableView_kzz` (Table View) - Shows data for convertible bonds.

7.  **美股 (US Stocks) (`tab_5`)**
    *   **Displays:**
        *   US Stock Data: `tableView_usa` (Table View) - Shows data for US stocks.

8.  **A 股 (A-Shares) (`tab_4`)**
    *   **Displays:**
        *   A-Share Stock Data: `tableView_allstock` (Table View) - Shows data for all A-share stocks.

9.  **自选股 (My Stocks/Watchlist) (`tab_6`)**
    *   **Displays:**
        *   My Stock Data (Left Panel): `tableView_leftmystock` (Table View) - Displays user's watchlist stocks. This seems to be a secondary watchlist display area.

10. **创业板 (ChiNext/Growth Enterprise Market) (`tab_7`)**
    *   **Displays:**
        *   ChiNext Market Data: `tableView_cyb` (Table View) - Shows data for stocks listed on the ChiNext market.

11. **中小板 (SME Board) (`tab_8`)**
    *   **Displays:**
        *   SME Board Data: `tableView_zxb` (Table View) - Shows data for stocks listed on the Small and Medium Enterprise Board.

12. **科创板 (STAR Market/Sci-Tech Innovation Board) (`tab_9`)**
    *   **Displays:**
        *   STAR Market Data: `tableView_kcb` (Table View) - Shows data for stocks listed on the STAR Market.

13. **京交所 (Beijing Stock Exchange) (`tab_10`)**
    *   **Displays:**
        *   Beijing Stock Exchange Data: `tableView_jjs` (Table View) - Shows data for stocks listed on the Beijing Stock Exchange.

14. **中概股 (Chinese Concept Stocks/US-listed Chinese Stocks) (`tab_11`)**
    *   **Displays:**
        *   Chinese Concept Stock Data: `tableView_zgg` (Table View) - Shows data for US-listed Chinese companies.

15. **港股 (Hong Kong Stocks) (`tab_12`)**
    *   **Displays:**
        *   Hong Kong Stock Data: `tableView_hk` (Table View) - Shows data for Hong Kong stocks.

16. **全球债券 (Global Bonds) (`tab_13`)**
    *   **Displays:**
        *   Global Bond Data: `tableView_qqzq` (Table View) - Shows data for global bonds.

### III. Right Content Area (`tabWidget_rightcontent`)

This area provides supplementary information and tools.

1.  **自选股 (My Stocks/Watchlist) (`MYSTOCK`)**
    *   **Displays:**
        *   My Stock Data: `tableView_mystock` (Table View) - Primary display for user's watchlist stocks.
    *   **Actions (Buttons):**
        *   `pushButtonaddmysocks`: "添加" (Add) - Add stocks to watchlist.
        *   `pushButtondelmystocks`: "删除" (Delete) - Remove stocks from watchlist.
        *   `pushButtonflushquotestart`: "刷新已开" (Refresh On) - Toggle auto-refresh for watchlist.
        *   `pushButtonvoiceremainder`: "语音已开" (Voice Reminder On) - Toggle voice alerts.

2.  **财联社新闻 (CLS News) (`clsnews`)**
    *   **Displays:**
        *   News View: `textEdit_clxnewsView` (Text Edit) - Displays news from CaiLianShe (CLS).

3.  **新入围 (Newly Selected/Filtered) (`tab_14`)**
    *   **Displays:**
        *   Newly Selected Stocks: `tableView_bankstocktop2` (Table View) - Likely shows stocks that recently met certain criteria or were newly added to a list (e.g. "newly shortlisted bank stocks").

4.  **实时资金 (Real-time Funds) (`realfund`)**
    *   **Displays:**
        *   Real-time Fund Flow: `tableView_realfund` (Table View) - Shows real-time fund flow data.
    *   **Controls:**
        *   `lineEdit_realfundtime`: Text input for refresh interval (default "20" seconds).
        *   `pushButton_flushfundsort`: "刷新已开" (Refresh On) - Toggle auto-refresh for fund data.
    *   **Labels:**
        *   `label_realfundflushtime`: "刷新间隔（秒）：" (Refresh Interval (seconds):)

5.  **通达信大单 (TongDaXin Large Orders) (`tdxdd`)**
    *   **Displays:**
        *   TDX Large Order View: `textEdit_tdxdadanView` (Text Edit) - Displays large order information, possibly from TongDaXin data source.

6.  **扫雷 (Risk Scan/Mine Sweeper) (`stockcheckhealth`)**
    *   **Displays:**
        *   Risk List: `textEdit_fengxianlist` (Text Edit) - Displays risk assessment or warnings for a stock.
    *   **Controls:**
        *   `lineEdit_inputstock`: Text input to enter a stock code for checking.
        *   `pushButton_checkhealth`: "检 查" (Check) - Button to initiate the risk scan.

### IV. Bottom Main Table

*   **实时涨停数据 (Real-time Limit-Up Data): `tableView_zhangtingdata` (Table View)**
    *   Located at the bottom of the main window, this table likely displays stocks that have hit their upper price limit in real-time.

### V. Menu Bar (`menubar`) Functionalities

The menu bar provides access to a wide range of features and data analysis tools.

1.  **超级资金监控 (Super Funds Monitoring) (`SupperAmtmenu`)**
    *   Actions:
        *   `actionSuperRealQuote`: "开启实时监控" (Start Real-time Monitoring)
        *   `actionSuperstop`: "停止实时监控" (Stop Real-time Monitoring)
        *   `actionsuperordersendmsg`: "开启微信通知" (Enable WeChat Notifications)
        *   `actioncloseSendmsg`: "关闭微信通知" (Disable WeChat Notifications)
        *   `actionMonitorlistAddstock`: "监控列表添加" (Add to Monitoring List)
        *   `actionxlwanshoudan`: "万手单(XL)" (10k+ Share Orders XL)
        *   `actionstockhistoryawardselect`: "个股历史资金查询" (Query Stock Historical Fund Data)
    *   Sub-menus:
        *   `levelset` ("监控档位设置" - Monitoring Level Settings): `actionvol10000` (>10000手), `actionvol5000` (>5000手), `actionvol2000` (>2000手), `actionvol1000` (>1000手)
        *   `menu_dadanDataOutput` ("数据导出" - Data Export): Export large order data to TXT, CSV, HTML.
        *   `menu_dadananaly` ("大单统计分析" - Large Order Statistical Analysis): Analyze large orders for individual stocks, today, specific day, last 5 days, and trends (`actionddcjcs`).

2.  **板块资金监控 (Sector Funds Monitoring) (`bankmenu`)**
    *   Actions:
        *   `actionbankstartnmonitor`: "开启板块监控" (Start Sector Monitoring)
        *   `actionbanknmonitorStop`: "停止监控" (Stop Monitoring)
        *   `actionbankyidong`: "板块异动" (Sector Unusual Movements)
    *   Sub-menus:
        *   `menu_intervalset` ("监控间隔设置" - Monitoring Interval Settings): 10s, 20s, 30s, 60s, 5m, 10m.

3.  **龙头盯盘 (Leading Stock Monitoring) (`menuMaxstockmonitor`)**
    *   Actions:
        *   `actiondrogstartmonitor`: "开启龙头盯盘" (Start Leading Stock Monitoring)
        *   `actiondrogmonitorstop`: "停止盯盘" (Stop Monitoring)
        *   `actionpankouyidong`: "盘口异动" (Order Book Unusual Movements)
        *   `actionjiguopankoudata`: "机构盘口**" (Institutional Order Book Data) - Name seems truncated.

4.  **涨 停 (Limit-Up) (`menuzhangting`)**
    *   Actions:
        *   `actionintimezhangtingstart`: "涨停监控开启" (Start Limit-Up Monitoring)
        *   `actionintimezhangtingstop`: "涨停监控停止" (Stop Limit-Up Monitoring)
        *   `actionToddayzhangting`: "选股宝涨停盯盘" (Xuangubao Limit-Up Monitoring)
        *   `action_lhborder`: "龙虎榜单" (Dragon Tiger List / Longhu Bang)
        *   `actionfanxinxia`: "方新侠" (Fang Xin Xia - likely a specific strategy or data source)
        *   `actionthslhb`: "同花顺龙虎榜" (THS Dragon Tiger List)
        *   `actiondabankanban`: "打板看盘" (Limit-Up Chase Monitoring)
        *   `actionzhangtingdataoutput`: "涨停数据导出" (Export Limit-Up Data)
        *   `actiondfcfqsgc`: "东财强势股池" (Eastmoney Strong Stock Pool)

5.  **竞 价 (Auction/Bidding) (`menu_jingjia`)**
    *   Actions:
        *   `actionjingjiadataAnalyies`: "打开分析工具" (Open Analysis Tool)
        *   `actionjingjiawriteToTDX`: "竞价数据写通达信" (Write Auction Data to TDX)
        *   `actionjingjiadataExport`: "竞价数据导出" (Export Auction Data)

6.  **南向资金 (Southbound Funds) (`southAmtmenu`)**
    *   Actions for analyzing and tracking Southbound fund flows (funds from mainland China to Hong Kong).
        *   `actionsouthDatainserttoDB`: "数据更新入库" (Update Data to DB)
        *   `actionsouthTop20Select`: "净买入前20查询" (Query Top 20 Net Buys)
        *   `actionsouthbuy`: "今日开始净买查询" (Query Net Buys Starting Today)
        *   `actionsouthDataforone`: "个股南资数据查询" (Query Individual Stock Southbound Data)
        *   `actionsouthbusinessTop20`: "个股经纪商查询" (Query Individual Stock Brokers)
        *   `actionSouthmoreFunction`: "打开南向资金分析工具" (Open Southbound Funds Analysis Tool)

7.  **北资分析 (Northbound Funds Analysis) (`NorthAmtmenu`)**
    *   Actions for analyzing and tracking Northbound fund flows (funds from Hong Kong/international to mainland China).
        *   `action_opennorthanalyiesForm`: "更多功能（打开）" (More Functions (Open))
        *   `actionsuportjust30dayNorthData`: "补齐近30日数据" (Complete Last 30 Days Data)
        *   `actionnorthTop20Select`: "净买入前20查询" (Query Top 20 Net Buys)
        *   `actionnorthbuyup`: "今日开始净买查询" (Query Net Buys Starting Today)
        *   `actionnorthDataforone`: "个股北资查询" (Query Individual Stock Northbound Data)
        *   `actionnorthFindstockF10`: "F10查询" (Query F10 Info)
        *   `actionnorthdataWriteToTDX`: "北资写入通达信" (Write Northbound Data to TDX)
        *   `actionNorthfundview`: "南北资概览" (North-South Funds Overview)

8.  **领先企业获取 (Leading Companies Retrieval) (`topStockgetmenu`)**
    *   Actions:
        *   `actionAlist`: "A股市场领先企业" (A-Share Market Leading Companies)
        *   `actionHKlist`: "港股市场领先企业" (HK Stock Market Leading Companies)
        *   `actionUSAlist`: "美股市场领先企业" (US Stock Market Leading Companies)
        *   `actionStocklistOutput`: "数据导出" (Data Export)

9.  **开/复盘 (Market Open/Review) (`menu_MarketOoenAndclose`)**
    *   Actions:
        *   `actionzhaopanfx`: "打开早盘竞价分析" (Open Early Session Auction Analysis)
        *   `actionMarketCloseView`: "每日盘面分析(TDX)" (Daily Market Analysis (TDX))
        *   `actionkaipanlaFP`: "开盘啦复盘" (Kaipanla Review)
        *   `actionxilimaofp`: "犀利猫复盘" (Xilimao Review)
        *   `actionsuperfundintoflow`: "超级资金流入流出情况" (Super Fund Inflow/Outflow Status)
        *   `actiontodayklineToDB`: "更新当日kline" (Update Today's K-line to DB)
        *   `actionhistoryklinetoDB`: "更新历史kline" (Update Historical K-line to DB)

10. **选 股 (Stock Selection) (`menu_stock_select`)**
    *   Various actions for stock selection strategies:
        *   `actioniwencaixg`: "爱问财选股" (iFinD Stock Selection)
        *   `actiondfcfxg`: "东财选股" (Eastmoney Stock Selection)
        *   `actiontdxSelectStock`: "通达信策略选股" (TDX Strategy Stock Selection)
        *   `actionSmartselectstock`: "智能条件选股" (Smart Conditional Stock Selection)
        *   `actionactionrelationglgsld`: "概念公司亮点选股" (Concept/Company Highlights Stock Selection)
        *   `actionmainbussnesskeyselect`: "主营业务选股" (Main Business Stock Selection)
        *   `actionSelectStockByPm`: "尾盘策略选股" (End-of-Day Strategy Stock Selection)
        *   `actionSelectStockByAm`: "早盘策略选股" (Early Session Strategy Stock Selection)
        *   `actionSelectlowlinestock`: "再上450" (Cross 450 Again - specific strategy)
        *   `actionpc_zjlx_xg`: "资金数据选股" (Fund Data Stock Selection)
        *   `actionfincalhislowvalueZT`: "历史低估区域近期涨停" (Historically Undervalued Area Recent Limit-Up)
        *   `actionzhaohonglicaodi`: "赵红力抄底(市场全面大跌尾声)" (Zhao Hongli Bottom Fishing)
        *   `actionopen3mafterselectstock`: "开盘3分钟后选股" (Select Stocks 3 Mins After Open)
        *   `actionzhangtinguplimit`: "涨停不破" (Limit-Up Not Broken)
        *   `actioncross_pressurese`: "压力突破选股" (Resistance Breakthrough Stock Selection)
        *   `actionupdate_tracert_longtime_stock`: "长期跟踪股更新" (Update Long-term Tracked Stocks)
        *   `actionupdate_Amarket_longprofitstock`: "A股长期赢利风格股池更新" (Update A-Share Long-term Profit Style Stock Pool)

11. **我的面板 (My Panel) (`menu_myblank`)**
    *   Collection of various tools and data views:
        *   `actionhgldx`: "宏观数据-流动性" (Macro Data - Liquidity)
        *   `actionfunddirector`: "资金动向" (Fund Direction)
        *   `actionpertradeview`: "逐笔追踪" (Tick-by-Tick Tracking)
        *   `actiontradeingcount`: "盘中统计" (Intraday Statistics)
        *   `actionluobotuoyan`: "萝卜投研" (Luobo Touyan - research platform)
        *   `actiontopichottop`: "题材龙头" (Theme Leaders)
        *   `actionCompanies_PerformanceForecast`: "业绩预告" (Earnings Forecast)
        *   `actionaiwencai`: "爱问财" (iFinD)
        *   `pc_tcld_bkzqb`: "近期热点回顾" (Recent Hotspots Review)
        *   `actionjinqihiuyi`: "近期会议" (Recent Meetings)
        *   `actionAhistoryPEAndPB`: "A股历史PE与PB" (A-Share Historical PE & PB)
        *   `actionupdatesuperfunddata`: "更新超级净流入数据" (Update Super Net Inflow Data)
        *   `actionopen_Fundamentalanalysis`: "打开基本面分析" (Open Fundamental Analysis)
        *   `actionopenrpsanaly`: "开打RPS分析" (Open RPS Analysis)
        *   `actionopenquotecenter`: "行情中心" (Quote Center)
        *   `actionopenstrategyManager`: "打开策略管理" (Open Strategy Manager)
        *   `actionopentradeterminetor`: "打开交易终端" (Open Trading Terminal)
        *   `actionsmallsotcksuperfundmonitor`: "个股分类资金监控" (Stock Category Fund Monitoring)
        *   `action_stocks_judge_trend`: "金牛抄底判断大盘底" (Golden Bull Bottom Fishing - Market Bottom 판단)
        *   `actionstockfundinflow_calc`: "个股资金流入自定义计算" (Custom Calculation of Stock Fund Inflow)


12. **数据中心 (Data Center) (`menu_TDXdatascenter`)**
    *   Access to various TDX (TongDaXin) data categories like investment calendar, new stock calendar, Dragon Tiger list, margin trading, shareholding changes, etc. (e.g., `tdxsj_tzrl_tzrl`, `tdxsj_xgzx_xgzx`, `tdxsj_lhbd`).

13. **AI助手 (AI Assistant) (`menuAI`)**
    *   Actions:
        *   `actionOpenBot`: "打开机器人助手" (Open Robot Assistant)
        *   `actionaiwencaitools`: "爱问财助手" (iFinD Assistant)

14. **外挂工具 (External Tools) (`menu_2`)**
    *   Tools like "操盘手学习" (Trader Learning), "同花顺涨停分析工具" (THS Limit-Up Analysis Tool), "股价预测" (Stock Price Prediction), "空间密码" (Space Password - unclear), "龙头复盘" (Leading Stock Review), "外部数据更新" (External Data Update).

15. **资 讯 (Information/News) (`menu_zixun`)**
    *   Actions:
        *   `actionmarketNews`: "沪深港美资讯" (Shanghai, Shenzhen, HK, US News)
        *   `action_zsyj`: "招商研究" (China Merchants Securities Research)

16. **样式 (Style) (`menu`)**
    *   Actions to change the UI theme/style (e.g., `actiondark_amber`, `actionlight_blue`).

### VI. Overall Functionalities Summary

Based on the UI elements, the "操盘神器" application appears to be a comprehensive stock trading and analysis platform with the following core functionalities:

1.  **Real-time Market Monitoring:**
    *   Stock quotes (A-shares, HK, US, Global, ETFs, Convertible Bonds).
    *   Index tracking (Domestic and Global).
    *   Large order monitoring (`tableView_superAmount`, `textEdit_tdxdadanView`).
    *   Limit-up stock tracking (`tableView_zhangtingdata`, `menuzhangting`).
    *   Sector and concept tracking (`tab_bankcenter`).
    *   Leading stock (龙头) monitoring (`textEdit_drogMoniter`, `menuMaxstockmonitor`).

2.  **Data Analysis:**
    *   Northbound and Southbound fund flow analysis (`NorthAmtmenu`, `southAmtmenu`).
    *   Fund flow analysis for individual stocks and sectors (`tableView_realfund`, `bankstock_award`).
    *   Large order analysis (`menu_dadananaly`).
    *   Auction data analysis (`menu_jingjia`).
    *   Market review and replay (`menu_MarketOoenAndclose`).
    *   Risk scanning/health checks for stocks (`stockcheckhealth`).
    *   Fundamental analysis and PE/PB data (`actionopen_Fundamentalanalysis`, `actionAhistoryPEAndPB`).
    *   RPS (Relative Strength Price) analysis (`actionopenrpsanaly`).

3.  **News and Information:**
    *   Financial news (CLS News: `textEdit_clxnewsView`).
    *   Various other news and research sources from the menu (`menu_zixun`, `menu_TDXdatascenter`).

4.  **Portfolio/Watchlist Management:**
    *   Managing personal stock watchlists (`tableView_mystock`, `pushButtonaddmysocks`, `pushButtondelmystocks`).

5.  **Stock Selection & Strategy:**
    *   Multiple tools and strategies for stock selection (`menu_stock_select`).
    *   Strategy management (`actionopenstrategyManager`).

6.  **Trading Support (Implied):**
    *   "Open Trading Terminal" (`actionopentradeterminetor`) suggests integration with trading execution.
    *   Voice reminders and WeChat notifications.

7.  **Customization:**
    *   UI theme customization (`menu`).
    *   Configurable refresh intervals for various data views.

### VII. Key Data Sources (Inferred)

*   **TongDaXin (TDX):** Explicitly mentioned for large orders, daily market analysis, and data center.
*   **CaiLianShe (CLS):** For news.
*   **Xuangubao:** For limit-up monitoring.
*   **iFinD (爱问财):** For stock selection and AI assistant.
*   **Eastmoney (东财):** For stock selection and strong stock pool.
*   **THS (同花顺):** For Dragon Tiger List and limit-up analysis.
*   **Kaipanla, Xilimao, Luobo Touyan:** External platforms for market review and research.
*   **China Merchants Securities Research (招商研究):** For research reports.
*   Direct market data feeds for quotes, indices, fund flows.
*   Database for storing historical data, user preferences, and analysis results (implied by "数据更新入库" actions).

This analysis provides a comprehensive overview of the application's capabilities as reflected in its user interface.
