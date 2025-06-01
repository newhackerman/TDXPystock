from flask import Blueprint, render_template

bp = Blueprint('strategy', __name__)

@bp.route('/')
def index():
    return render_template('strategy/placeholder.html', title='Strategy')
