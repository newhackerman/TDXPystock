from app import db
from sqlalchemy.dialects.mysql import DATE

class SouthDataAnaly(db.Model):
    __tablename__ = 'southdataanly'
    # Composite primary key
    SCODE = db.Column(db.String(8), primary_key=True)
    SNAME = db.Column(db.String(20), primary_key=True) # Part of composite PK
    HDDATE = db.Column(DATE, primary_key=True)        # Part of composite PK
    SHARESRATE = db.Column(db.Float, primary_key=True)# Part of composite PK

    SHAREHOLDSUM = db.Column(db.Float, nullable=True)
    CLOSEPRICE = db.Column(db.Float, nullable=True)
    ZDF = db.Column(db.Float, nullable=True)          # Change percentage
    SHAREHOLDPRICE = db.Column(db.Float, nullable=True)
    SHAREHOLDPRICEONE = db.Column(db.Float, nullable=True)
    SHAREHOLDPRICEFIVE = db.Column(db.Float, nullable=True)
    SHAREHOLDPRICETEN = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f'<SouthDataAnaly {self.SCODE} {self.HDDATE}>'

class NorthDataAnaly(db.Model):
    __tablename__ = 'northdataAnaly'
    # Composite primary key
    SCODE = db.Column(db.String(8), primary_key=True)
    SNAME = db.Column(db.String(20), primary_key=True) # Part of composite PK
    HDDATE = db.Column(DATE, primary_key=True)        # Part of composite PK
    SHARESRATE = db.Column(db.Float, primary_key=True)# Part of composite PK

    SHAREHOLDSUM = db.Column(db.Float, nullable=True)
    CLOSEPRICE = db.Column(db.Float, nullable=True)
    ZDF = db.Column(db.Float, nullable=True)
    SHAREHOLDPRICE = db.Column(db.Float, nullable=True)
    SHAREHOLDPRICEONE = db.Column(db.Float, nullable=True)
    SHAREHOLDPRICEFIVE = db.Column(db.Float, nullable=True)
    SHAREHOLDPRICETEN = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f'<NorthDataAnaly {self.SCODE} {self.HDDATE}>'
