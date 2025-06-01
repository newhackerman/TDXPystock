from flask import Blueprint, render_template

bp = Blueprint('analysis', __name__)

@bp.route('/')
def index():
    return render_template('analysis/placeholder.html', title='Analysis')
