from app import db

class Stocks(db.Model):
    __tablename__ = 'stocks'
    code = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(12))
    area = db.Column(db.String(12), nullable=True)
    market = db.Column(db.String(2), nullable=True) # e.g., SH, SZ
    industry = db.Column(db.String(12), nullable=True)
    ltgb = db.Column(db.Float, nullable=True) # 流通股本

    # Relationship to Watchlist
    watched_by_users = db.relationship('Watchlist', backref='stock', lazy='dynamic')

    def __repr__(self):
        return f'<Stock {self.code} - {self.name}>'

class StockInfo(db.Model):
    __tablename__ = 'stockinfo'
    # Assuming 'code' is the primary key, though not explicitly defined as such in SQL
    # For a one-to-one relationship with Stocks, it should be a primary key and foreign key.
    code = db.Column(db.String(6), db.ForeignKey('stocks.code'), primary_key=True)
    name = db.Column(db.String(10)) # Likely redundant if linked to Stocks table
    market = db.Column(db.String(6), nullable=True) # Also potentially redundant
    bank = db.Column(db.String(300), nullable=True)  # 板块 (Sectors)
    gainan = db.Column(db.String(300), nullable=True) # 概念 (Concepts)
    gsld = db.Column(db.String(300), nullable=True)   # 公司亮点 (Company Highlights)
    zyfw = db.Column(db.String(300), nullable=True)   # 经营范围 (Business Scope)
    kbgs = db.Column(db.String(300), nullable=True)   # 可比公司 (Comparable Companies)
    zycpmc = db.Column(db.String(300), nullable=True) # 主营产品名称 (Main Product Names)
    url = db.Column(db.String(300), nullable=True)    # 公司URL (Company URL)

    # Relationship (if code in StockInfo is a FK to Stocks.code)
    # stock_details = db.relationship('Stocks', backref=db.backref('info', uselist=False))
    # Renamed 'stock' to 'stock_details' to avoid conflict if 'stock' is used by Watchlist backref on Stocks model


    def __repr__(self):
        return f'<StockInfo {self.code} - {self.name}>'
