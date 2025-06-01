from app import db # Import the db instance from app's __init__
from datetime import datetime
# It's good practice to use a library for password hashing, e.g., werkzeug.security
from werkzeug.security import generate_password_hash, check_password_hash

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password_hash = db.Column(db.String(1024), nullable=False) # Store hash, not plain text
    phone = db.Column(db.String(15), nullable=False, unique=True)
    email = db.Column(db.String(25), unique=True, nullable=True)
    idcard = db.Column(db.String(18), nullable=True) # ID card length can vary
    qqid = db.Column(db.String(15), nullable=True)
    wechat = db.Column(db.String(25), nullable=True)
    payid = db.Column(db.String(25), nullable=True)
    registime = db.Column(db.Date, default=datetime.utcnow)
    updatetime = db.Column(db.Date, onupdate=datetime.utcnow)
    level = db.Column(db.Integer, nullable=True)
    availdate = db.Column(db.Integer, nullable=True) # Assuming this means available days
    useddate = db.Column(db.Integer, nullable=True)  # Assuming this means used days
    amount = db.Column(db.Float, nullable=True)
    availbalance = db.Column(db.Float, nullable=True)
    Rechargedate = db.Column(db.Date, nullable=True)
    memo = db.Column(db.String(50), nullable=True)

    # Relationship to Watchlist
    watchlist_items = db.relationship('Watchlist', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
