from app import db
from sqlalchemy.dialects.mysql import DATE, INTEGER # For specific integer types if needed

class Yjbb(db.Model): # Earnings Per Share Bulletin
    __tablename__ = 'yjbb'
    # Composite primary key
    code = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(20), primary_key=True) # Part of composite PK
    reportdate = db.Column(db.String(10), primary_key=True) # Part of composite PK (e.g., "2023-03-31")
    update_date = db.Column(DATE, primary_key=True) # Part of composite PK

    market = db.Column(db.String(2), nullable=True)
    publishname = db.Column(db.String(50), nullable=True) # Industry/Sector
    basic_eps = db.Column(db.Float, nullable=True)
    deduct_basic_eps = db.Column(db.Float, nullable=True)
    total_operate_income = db.Column(db.Float, nullable=True)
    ystz = db.Column(db.Float, nullable=True) # Operating income YOY %
    yshz = db.Column(db.Float, nullable=True) # Operating income QOQ %
    parent_netprofit = db.Column(db.Float, nullable=True)
    sjltz = db.Column(db.Float, nullable=True) # Net profit YOY %
    sjlhz = db.Column(db.Float, nullable=True) # Net profit QOQ %
    bps = db.Column(db.Float, nullable=True) # Book value per share
    weightavg_roe = db.Column(db.Float, nullable=True) # ROE
    mgjyxjje = db.Column(db.Float, nullable=True) # Operating cash flow per share
    xsmll = db.Column(db.Float, nullable=True) # Gross profit margin %
    assigndscrpt = db.Column(db.String(200), nullable=True) # Dividend description
    zxgxl = db.Column(db.Float, nullable=True) # Dividend yield %
    datatype = db.Column(db.String(50), nullable=True) # Report type (Q1, Mid-year, Q3, Annual)
    datayear = db.Column(db.String(8), nullable=True) # Report year
    datemmdd = db.Column(db.String(8), nullable=True) # Report period (MM-DD for quarters/half-year)
    # reportdate already defined as part of PK
    # update_date already defined as part of PK

    def __repr__(self):
        return f'<Yjbb {self.code} {self.reportdate}>'

class StockFinancial(db.Model):
    __tablename__ = 'stockfinancial'
    # Composite primary key
    code = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(12), primary_key=True) # Part of composite PK
    hddate = db.Column(db.String(12), primary_key=True) # Report date string, e.g., "2023-12-31"

    mgjxjll = db.Column(db.Float, nullable=True) # Net cash flow per share
    mgjyxjl = db.Column(db.Float, nullable=True) # Operating cash flow per share
    mgjzc = db.Column(db.Float, nullable=True) # Net assets per share
    mgsy = db.Column(db.Float, nullable=True) # EPS
    mgsytb = db.Column(db.Float, nullable=True) # Diluted EPS
    mgyylr = db.Column(db.Float, nullable=True) # Operating profit per share
    mgyysr = db.Column(db.Float, nullable=True) # Operating revenue per share
    gsymgssyzdjlr = db.Column(db.Float, nullable=True) # Net profit attributable to parent company
    jlr = db.Column(db.Float, nullable=True) # Net profit
    lrze = db.Column(db.Float, nullable=True) # Total profit
    yylr = db.Column(db.Float, nullable=True) # Operating profit
    yysr = db.Column(db.Float, nullable=True) # Operating revenue
    jll = db.Column(db.Float, nullable=True) # Net profit margin %
    mll = db.Column(db.Float, nullable=True) # Gross profit margin %
    roe = db.Column(db.Float, nullable=True) # ROE %
    yylrl = db.Column(db.Float, nullable=True) # Operating profit margin %
    cwfyl = db.Column(db.Float, nullable=True) # Financial expense ratio %
    glfyl = db.Column(db.Float, nullable=True) # Administrative expense ratio %
    roic = db.Column(db.Float, nullable=True) # ROIC
    xsfyl = db.Column(db.Float, nullable=True) # Sales expense ratio %
    xsqjfyl = db.Column(db.Float, nullable=True) # Period expense ratio % (Sales, G&A, Financial)
    xsqlr = db.Column(db.Float, nullable=True) # EBIT
    cqbl = db.Column(db.Float, nullable=True) # Equity ratio %
    ldbl_r = db.Column(db.Float, nullable=True) # Current ratio
    lxbzbs = db.Column(db.Float, nullable=True) # Interest coverage ratio
    mgjyhdxjllzzl = db.Column(db.Float, nullable=True) # Growth rate of operating cash flow per share %
    qycs = db.Column(db.Float, nullable=True) # Quick ratio (unclear from name, assuming quick ratio)
    sdbl_r = db.Column(db.Float, nullable=True) # Quick ratio
    xjbl = db.Column(db.Float, nullable=True) # Cash ratio %
    xjldfzb = db.Column(db.Float, nullable=True) # Cash to current liabilities ratio
    zcfzl = db.Column(db.Float, nullable=True) # Debt to asset ratio %
    chzzl = db.Column(db.Float, nullable=True) # Inventory turnover rate
    gdzczzl = db.Column(db.Float, nullable=True) # Fixed assets turnover rate
    ldzczzl = db.Column(db.Float, nullable=True) # Current assets turnover rate
    yszkzzl = db.Column(db.Float, nullable=True) # Accounts receivable turnover rate
    zzczzl = db.Column(db.Float, nullable=True) # Total assets turnover rate

    def __repr__(self):
        return f'<StockFinancial {self.code} {self.hddate}>'

class StockShareholder(db.Model):
    __tablename__ = 'stockshareholder'
    # Composite primary key
    code = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(12), primary_key=True) # Part of composite PK
    hddate = db.Column(db.String(12), primary_key=True) # Date of data

    total_share = db.Column(INTEGER, nullable=True) # Using INTEGER for potentially large numbers
    total_market_value = db.Column(db.Float, nullable=True)
    circulating_share = db.Column(db.Float, nullable=True)
    circulating_market_value = db.Column(db.Float, nullable=True)
    circulating_ratio = db.Column(db.Float, nullable=True)
    top10_share_holders = db.Column(db.Float, nullable=True) # Market value held by top 10
    top10_share_sum = db.Column(db.Float, nullable=True) # Shares held by top 10
    top10_share_ratio = db.Column(db.Float, nullable=True) # Holding ratio of top 10 %
    free_circulation_marke_value = db.Column(db.Float, nullable=True)
    free_circulation_share = db.Column(db.Float, nullable=True)
    top10_share_name = db.Column(db.String(500), nullable=True)
    persons = db.Column(db.Float, nullable=True) # Number of shareholders
    personshare_sum = db.Column(db.Float, nullable=True) # Avg holding value per person

    def __repr__(self):
        return f'<StockShareholder {self.code} {self.hddate}>'

class StockZycplIncome(db.Model): # Main Business Product Category Income
    __tablename__ = 'stock_zycpfl_income'
    # Composite primary key
    hddate = db.Column(db.String(12), primary_key=True)
    code = db.Column(db.String(8), primary_key=True)
    MAINOP_TYPE = db.Column(db.Integer, primary_key=True) # Product category type
    RANK = db.Column(db.Integer, primary_key=True) # Income rank

    name = db.Column(db.String(12), nullable=True) # Stock name
    ITEM_NAME = db.Column(db.String(50), nullable=True) # Category item name
    MAIN_BUSINESS_INCOME = db.Column(db.Float, nullable=True)
    MBI_RATIO = db.Column(db.Float, nullable=True) # Income ratio %
    MAIN_BUSINESS_COST = db.Column(db.Float, nullable=True)
    MBC_RATIO = db.Column(db.Float, nullable=True) # Cost ratio %
    MAIN_BUSINESS_RPOFIT = db.Column(db.Float, nullable=True) # Profit
    MBR_RATIO = db.Column(db.Float, nullable=True) # Profit ratio %
    GROSS_RPOFIT_RATIO = db.Column(db.Float, nullable=True) # Gross profit margin %

    def __repr__(self):
        return f'<StockZycplIncome {self.code} {self.hddate} Item: {self.ITEM_NAME}>'
