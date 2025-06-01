from app import db
from sqlalchemy.dialects.mysql import DATE, INTEGER

class HistorySuperAward(db.Model):
    __tablename__ = 'historysuperaward'
    # Composite primary key
    hddate = db.Column(DATE, primary_key=True)
    code = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(20), primary_key=True) # Part of composite PK
    ddlry = db.Column(db.Float, primary_key=True)     # Part of composite PK (Net inflow of super large orders)

    market = db.Column(db.String(2), nullable=True)
    price = db.Column(db.Float, nullable=True)
    zdf = db.Column(db.Float, nullable=True) # Change %
    ddb = db.Column(db.Float, nullable=True) # Proportion of super large orders %

    def __repr__(self):
        return f'<HistorySuperAward {self.code} {self.hddate}>'

class SuperFundHistory(db.Model):
    __tablename__ = 'superfundhistory'
    # Composite primary key
    HDDATE = db.Column(DATE, primary_key=True)
    code = db.Column(db.String(8), primary_key=True)
    superfund = db.Column(db.Float, primary_key=True) # Assuming superfund is part of a unique key constraint

    name = db.Column(db.String(20), nullable=True)
    price = db.Column(db.Float, nullable=True)
    superpect = db.Column(db.Float, nullable=True) # Superfund percentage
    zdf = db.Column(db.Float, nullable=True) # Change %
    bigfund = db.Column(db.Float, nullable=True)
    bigpect = db.Column(db.Float, nullable=True)
    midfund = db.Column(db.Float, nullable=True)
    midpect = db.Column(db.Float, nullable=True)
    minfund = db.Column(db.Float, nullable=True)
    minpect = db.Column(db.Float, nullable=True)
    mainfund = db.Column(db.Float, nullable=True) # Main force net inflow
    mainpect = db.Column(db.Float, nullable=True) # Main force net inflow percentage
    market = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f'<SuperFundHistory {self.code} {self.HDDATE}>'

class Strategys(db.Model):
    __tablename__ = 'strategys'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) # PK from schema
    # Composite unique key (name, datadate, stockcode) handled by db.UniqueConstraint if needed,
    # but SQLAlchemy uses the PK for identity.
    name = db.Column(db.String(50))
    conditions = db.Column(db.String(400), nullable=True)
    datadate = db.Column(DATE, nullable=True) # Date for which the strategy was run or data applies
    stockcode = db.Column(db.String(9))
    stockname = db.Column(db.String(8), nullable=True)
    market = db.Column(db.String(2), nullable=True)
    zdf = db.Column(db.Float, nullable=True) # Change %
    price = db.Column(db.Float, nullable=True)
    dde = db.Column(db.Float, nullable=True) # DDE or similar indicator
    turnover_rate = db.Column(db.Float, nullable=True)
    startdate = db.Column(DATE, nullable=True) # Backtest start date
    maxdate = db.Column(DATE, nullable=True)   # Backtest end date
    maxAnnualYield = db.Column(db.Float, nullable=True)
    maxhaveday = db.Column(db.Integer, nullable=True) # Optimal holding days for max yield
    maxWinRate = db.Column(db.Float, nullable=True)
    maxwinhaveday = db.Column(db.Integer, nullable=True) # Optimal holding days for max win rate
    annualYield = db.Column(db.Integer, nullable=True) # Absolute yield (assuming typo for float)
    averageLossRatio = db.Column(db.Integer, nullable=True) # Profitability (assuming typo for float)
    scount = db.Column(db.Integer, nullable=True) # Trade count
    testdate = db.Column(DATE, nullable=True) # Test date
    maxDrawDown = db.Column(db.Integer, nullable=True) # Max drawdown (assuming typo for float)
    profitVolatility = db.Column(db.Integer, nullable=True) # Stability (assuming typo for float)
    score = db.Column(db.Integer, nullable=True) # Score
    winRate = db.Column(db.Integer, nullable=True) # Win rate (assuming typo for float)

    # Unique constraint as per schema: UNIQUE INDEX sid_name_date_list ON strategys(name,datadate,stockcode)
    __table_args__ = (db.UniqueConstraint('name', 'datadate', 'stockcode', name='uq_strategy_name_date_code'),)


    def __repr__(self):
        return f'<Strategys {self.name} {self.stockcode} {self.datadate}>'

# ... (Keep existing imports: db, DATE, INTEGER)
# ... (Keep existing models: HistorySuperAward, SuperFundHistory, Strategys)

class RpsZycplx(db.Model): # RPS Main Business Product Category
    __tablename__ = 'rpszycplx'
    # Composite primary key
    code = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(20), primary_key=True) # Part of composite PK
    zycplx = db.Column(db.String(50), primary_key=True) # Main product category, part of composite PK

    def __repr__(self):
        return f'<RpsZycplx {self.code} - {self.zycplx}>'

class RpsXfhy(db.Model): # RPS Sub-industry
    __tablename__ = 'rpsxfhy'
    # Composite primary key
    code = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(20), primary_key=True) # Part of composite PK
    SJFL = db.Column(db.String(50), primary_key=True) # Level 4 classification, part of composite PK

    xfhy = db.Column(db.String(50), nullable=True) # THS custom industry
    SWEJFL = db.Column(db.String(50), nullable=True) # Shenwan Level 2 classification

    def __repr__(self):
        return f'<RpsXfhy {self.code} - {self.SJFL}>'

class BankRps(db.Model): # Sector RPS
    __tablename__ = 'bankrps'
    # Composite primary key
    bankname = db.Column(db.String(30), primary_key=True)
    hddate = db.Column(db.String(15), primary_key=True) # Date string
    bk3zf = db.Column(db.Float, primary_key=True) # Assuming bk3zf is part of a unique key ensuring record uniqueness

    bkvol = db.Column(db.Float, nullable=True)
    bkamount = db.Column(db.Float, nullable=True)
    bkzf = db.Column(db.Float, nullable=True)
    # bk3zf is PK
    bk5zf = db.Column(db.Float, nullable=True)
    bk10zf = db.Column(db.Float, nullable=True)
    bk20zf = db.Column(db.Float, nullable=True)
    bk60zf = db.Column(db.Float, nullable=True)
    bk120zf = db.Column(db.Float, nullable=True)
    bk250zf = db.Column(db.Float, nullable=True)
    bkzfrt = db.Column(db.Float, nullable=True) # Rank for bkzf
    bk3zfrt = db.Column(db.Float, nullable=True)
    bk5zfrt = db.Column(db.Float, nullable=True)
    bk10zfrt = db.Column(db.Float, nullable=True)
    bk20zfrt = db.Column(db.Float, nullable=True)
    bk60zfrt = db.Column(db.Float, nullable=True)
    bk120zfrt = db.Column(db.Float, nullable=True)
    bk250zfrt = db.Column(db.Float, nullable=True)
    bkrps = db.Column(db.Float, nullable=True)
    bk3rps = db.Column(db.Float, nullable=True)
    bk5rps = db.Column(db.Float, nullable=True)
    bk10rps = db.Column(db.Float, nullable=True)
    bk20rps = db.Column(db.Float, nullable=True)
    bk60rps = db.Column(db.Float, nullable=True)
    bk120rps = db.Column(db.Float, nullable=True)
    bk250rps = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f'<BankRps {self.bankname} {self.hddate}>'

class StockRps(db.Model):
    __tablename__ = 'stockrps'
    # Composite primary key
    hddate = db.Column(db.String(15), primary_key=True) # Date string
    code = db.Column(db.String(8), primary_key=True)
    zf3 = db.Column(db.Float, primary_key=True) # Assuming zf3 is part of a unique key

    name = db.Column(db.String(12), nullable=True)
    swejfl = db.Column(db.String(50), nullable=True) # Shenwan Level 2 classification
    sjfl = db.Column(db.String(50), nullable=True) # Level 4 classification
    vol = db.Column(db.Float, nullable=True)
    amount = db.Column(db.Float, nullable=True)
    zf = db.Column(db.Float, nullable=True)
    # zf3 is PK
    zf5 = db.Column(db.Float, nullable=True)
    zf10 = db.Column(db.Float, nullable=True)
    zf20 = db.Column(db.Float, nullable=True)
    zf60 = db.Column(db.Float, nullable=True)
    zf120 = db.Column(db.Float, nullable=True)
    zf250 = db.Column(db.Float, nullable=True)
    zfrt = db.Column(db.Float, nullable=True) # Rank for zf
    zf3rt = db.Column(db.Float, nullable=True)
    zf5rt = db.Column(db.Float, nullable=True)
    zf10rt = db.Column(db.Float, nullable=True)
    zf20rt = db.Column(db.Float, nullable=True)
    zf60rt = db.Column(db.Float, nullable=True)
    zf120rt = db.Column(db.Float, nullable=True)
    zf250rt = db.Column(db.Float, nullable=True)
    rps = db.Column(db.Float, nullable=True)
    rps3 = db.Column(db.Float, nullable=True)
    rps5 = db.Column(db.Float, nullable=True)
    rps10 = db.Column(db.Float, nullable=True)
    rps20 = db.Column(db.Float, nullable=True)
    rps60 = db.Column(db.Float, nullable=True)
    rps120 = db.Column(db.Float, nullable=True)
    rps250 = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f'<StockRps {self.code} {self.hddate}>'

class StockScore(db.Model):
    __tablename__ = 'stockscore'
    # Composite primary key
    code = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(12), primary_key=True) # Part of composite PK
    hddate = db.Column(db.String(12), primary_key=True) # Date string
    zhdf = db.Column(db.Float, primary_key=True) # Overall score, part of composite PK

    jsdf = db.Column(db.Float, nullable=True)  # Technical score
    zjdf = db.Column(db.Float, nullable=True)  # Fund score
    xxdf = db.Column(db.Float, nullable=True)  # News score
    hydf = db.Column(db.Float, nullable=True)  # Industry score
    jbmdf = db.Column(db.Float, nullable=True) # Fundamental score

    def __repr__(self):
        return f'<StockScore {self.code} {self.hddate}>'

class StockLimitUp(db.Model):
    __tablename__ = 'stocklimitup'
    # Composite primary key
    code = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(12), primary_key=True) # Part of composite PK
    hddate = db.Column(db.String(12), primary_key=True) # Date string

    price = db.Column(db.Float, nullable=True)
    zdf = db.Column(db.Float, nullable=True) # Change %
    limituptime = db.Column(db.Float, nullable=True) # Time of limit up (float might represent HHMM.SS or similar)
    updays = db.Column(db.Float, nullable=True) # Consecutive limit-up days
    openlimits = db.Column(db.Float, nullable=True) # Times limit was broken and re-sealed
    gainan = db.Column(db.String(20), nullable=True) # Associated concept
    reason = db.Column(db.String(200), nullable=True) # Reason for limit up

    def __repr__(self):
        return f'<StockLimitUp {self.code} {self.hddate}>'

class StockHoldersChg(db.Model):
    __tablename__ = 'stock_holderschg'
    # Composite primary key
    code = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(12), primary_key=True) # Part of composite PK
    hddate = db.Column(db.String(12), primary_key=True) # Date string

    HOLDER_TOTAL_NUM = db.Column(db.Integer, nullable=True)
    TOTAL_NUM_RATIO = db.Column(db.Float, nullable=True) # Change in number of shareholders %
    AVG_FREE_SHARES = db.Column(db.Integer, nullable=True) # Avg tradable shares per holder
    AVG_FREESHARES_RATIO = db.Column(db.Float, nullable=True) # Change in avg tradable shares %
    HOLD_FOCUS = db.Column(db.String(12), nullable=True) # Chip concentration status
    AVG_HOLD_AMT = db.Column(db.Float, nullable=True) # Avg holding value per person
    HOLD_RATIO_TOTAL = db.Column(db.Float, nullable=True) # Top 10 holders total ratio %
    FREEHOLD_RATIO_TOTAL = db.Column(db.Float, nullable=True) # Top 10 tradable holders total ratio %
    holder_point = db.Column(db.Float, nullable=True) # Retail investor index

    def __repr__(self):
        return f'<StockHoldersChg {self.code} {self.hddate}>'

class StockFundInOutResult(db.Model):
    __tablename__ = 'stockfundinoutresult'
    # Composite primary key
    code = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(12), primary_key=True) # Part of composite PK
    hddate = db.Column(db.String(12), primary_key=True) # Date string

    fundin = db.Column(db.Float, nullable=True)
    fundout = db.Column(db.Float, nullable=True)
    inflow = db.Column(db.Float, nullable=True) # Net inflow
    inflowpect = db.Column(db.Float, nullable=True) # Net inflow percentage
    zdf = db.Column(db.Float, nullable=True) # Change %

    def __repr__(self):
        return f'<StockFundInOutResult {self.code} {self.hddate}>'

class BankZfTop(db.Model):
    __tablename__ = 'bankzftop'
    # Composite primary key
    hddate = db.Column(db.String(12), primary_key=True)
    bankname = db.Column(db.String(30), primary_key=True)
    stockname = db.Column(db.String(12), primary_key=True)

    bankcode = db.Column(db.String(8), nullable=True)
    bankzdf = db.Column(db.Float, nullable=True)
    stockcode = db.Column(db.String(8), nullable=True)
    stockzdf = db.Column(db.Float, nullable=True)
    rank = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f'<BankZfTop {self.bankname} {self.stockname} {self.hddate}>'

class StockPerTradeAnaly(db.Model):
    __tablename__ = 'stockpertradeanaly'
    # Composite primary key
    code = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(12), primary_key=True) # Part of composite PK
    hddate = db.Column(db.String(12), primary_key=True) # Date string
    htime = db.Column(db.String(12), primary_key=True) # Time string

    price = db.Column(db.Float, nullable=True)
    vol = db.Column(db.Float, nullable=True)
    amount = db.Column(db.Float, nullable=True)
    drict = db.Column(db.String(4), nullable=True) # Direction (e.g., buy/sell)
    daybuy = db.Column(db.Float, nullable=True) # Daily net buy/sell
    daybuy3 = db.Column(db.Float, nullable=True) # 3-day net buy/sell
    daybuy5 = db.Column(db.Float, nullable=True)
    daybuy10 = db.Column(db.Float, nullable=True)
    daybuy20 = db.Column(db.Float, nullable=True)
    daybuy30 = db.Column(db.Float, nullable=True)
    daybuy60 = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f'<StockPerTradeAnaly {self.code} {self.hddate} {self.htime}>'
