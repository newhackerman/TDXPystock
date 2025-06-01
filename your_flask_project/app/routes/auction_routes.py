from flask import Blueprint, render_template

bp = Blueprint('auction', __name__)

@bp.route('/')
def index():
    return render_template('auction/placeholder.html', title='Auction')
