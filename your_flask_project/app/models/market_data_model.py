from app import db
from sqlalchemy.dialects.mysql import DATE # For DATE type

class StockOpenData(db.Model):
    __tablename__ = 'stockopendata'
    # Assuming a composite primary key based on the UNIQUE index
    code = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(12), primary_key=True) # Part of composite PK
    date = db.Column(DATE, primary_key=True)          # Part of composite PK

    zhangfu = db.Column(db.Float, nullable=True)
    liangbi = db.Column(db.Float, nullable=True)
    kaipan = db.Column(db.Float, nullable=True)      # Opening change %
    huanshuonu = db.Column(db.Float, nullable=True)  # Turnover rate %
    kaipanjine = db.Column(db.Float, nullable=True)  # Opening amount
    zongjine = db.Column(db.Float, nullable=True)    # Total amount
    liutongguyi = db.Column(db.String(15), nullable=True) # Tradable shares (in 100 millions)
    liutongsizhi = db.Column(db.String(15), nullable=True)# Tradable market cap
    lianzhangtiansu = db.Column(db.Integer, nullable=True)# Consecutive up days
    shanrizhangfu = db.Column(db.Float, nullable=True)   # 3-day change %
    ershirizhangfu = db.Column(db.Float, nullable=True)  # 20-day change %
    liushirizhangfu = db.Column(db.Float, nullable=True) # 60-day change %

    def __repr__(self):
        return f'<StockOpenData {self.code} {self.date}>'

class JinjiaData(db.Model):
    __tablename__ = 'jinjiadata'
    # Composite primary key based on UNIQUE index
    HDDATE = db.Column(DATE, primary_key=True)
    code = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(20), primary_key=True) # Part of composite PK
    market = db.Column(db.String(4), primary_key=True) # Part of composite PK

    vol = db.Column(db.Integer, nullable=True)
    price = db.Column(db.Float, nullable=True)
    amount = db.Column(db.Float, nullable=True)
    drict = db.Column(db.String(4), nullable=True) # Direction

    def __repr__(self):
        return f'<JinjiaData {self.code} {self.HDDATE}>'

class StockFirstMinData(db.Model):
    __tablename__ = 'stockfirstmindata'
    # Composite primary key
    HDDATE = db.Column(DATE, primary_key=True)
    htime = db.Column(db.String(10), primary_key=True)
    code = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(20), primary_key=True) # Part of composite PK

    vol = db.Column(db.Integer, nullable=True)
    price = db.Column(db.Float, nullable=True)
    amount = db.Column(db.Float, nullable=True)
    drict = db.Column(db.String(4), nullable=True)
    market = db.Column(db.Integer, nullable=True) # Assuming market is an int identifier
    buycount = db.Column(db.Integer, nullable=True)
    sellcount = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f'<StockFirstMinData {self.code} {self.HDDATE} {self.htime}>'

class StockKline(db.Model):
    __tablename__ = 'stockkline'
    # Composite primary key
    hdate = db.Column(DATE, primary_key=True)
    code = db.Column(db.String(8), primary_key=True)

    name = db.Column(db.String(20), nullable=True)
    zdf = db.Column(db.Float, nullable=True)      # Change percentage
    close = db.Column(db.Float, nullable=True)
    open = db.Column(db.Float, nullable=True)
    low = db.Column(db.Float, nullable=True)
    high = db.Column(db.Float, nullable=True)
    chg = db.Column(db.Float, nullable=True)      # Change amount
    vol = db.Column(db.Integer, nullable=True)    # Volume
    hsl = db.Column(db.Float, nullable=True)      # Turnover rate
    amount = db.Column(db.Float, nullable=True)   # Trading amount
    market = db.Column(db.Integer, nullable=True) # Assuming market is an int identifier

    def __repr__(self):
        return f'<StockKline {self.code} {self.hdate}>'

class DateList(db.Model):
    __tablename__ = 'datelist'
    date = db.Column(DATE, primary_key=True)
    isopen = db.Column(db.Integer, nullable=True) # 1 for open, 0 for closed

    def __repr__(self):
        return f'<DateList {self.date} IsOpen: {self.isopen}>'
