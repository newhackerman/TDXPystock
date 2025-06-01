from app import db
from datetime import datetime

class Watchlist(db.Model):
    __tablename__ = 'watchlist'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    stock_code = db.Column(db.String(8), db.ForeignKey('stocks.code'), nullable=False)
    added_on = db.Column(db.DateTime, default=datetime.utcnow)

    # Define relationships (optional here, but good for ORM use)
    # user = db.relationship('Users', back_populates='watchlist_items') # See user_model.py modification
    # stock = db.relationship('Stocks', back_populates='watched_by') # See stock_model.py modification

    __table_args__ = (db.UniqueConstraint('user_id', 'stock_code', name='uq_user_stock'),)

    def __repr__(self):
        return f'<Watchlist UserID:{self.user_id} StockCode:{self.stock_code}>'
