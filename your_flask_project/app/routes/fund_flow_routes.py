from flask import Blueprint, render_template

bp = Blueprint('fund_flow', __name__)

@bp.route('/')
def index():
    return render_template('fund_flow/placeholder.html', title='Fund Flow')
