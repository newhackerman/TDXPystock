from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models.user_model import Users
from app.models.stock_model import Stocks # Needed for watchlist display if joining
from app.models.watchlist_model import Watchlist # Needed for watchlist operations
from .forms import RegistrationForm, LoginForm
from app.services import auth_svc
from app.services import watchlist_svc # Import the new watchlist service

bp = Blueprint('user', __name__)

# User loader is in app/__init__.py

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        success, message = auth_svc.create_user(
            username=form.username.data,
            email=form.email.data,
            phone=form.phone.data,
            password=form.password.data
        )
        if success:
            flash(message, 'success')
            return redirect(url_for('user.login'))
        else:
            flash(message, 'danger')
    return render_template('auth/register.html', title='Register', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = auth_svc.authenticate_user(
            username=form.username.data,
            password=form.password.data
        )
        if user:
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash('Login successful.', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('auth/login.html', title='Login', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@bp.route('/profile')
@login_required
def profile():
    return render_template('user/placeholder.html', title='User Profile')

@bp.route('/watchlist')
@login_required
def display_watchlist():
    # watchlist_items = watchlist_svc.get_watchlist_for_user(current_user.id)
    # The service returns Watchlist objects which have a .stock attribute due to backref or eager loading
    # For simplicity in template, let's ensure we pass items that can be easily iterated to get stock details

    # Using the relationship directly from current_user (if lazy='dynamic' might need .all())
    # items = current_user.watchlist_items # This gives Watchlist objects

    # Using the service which joins and fetches stock details
    items_with_stock_data = watchlist_svc.get_watchlist_for_user(current_user.id)

    return render_template('user/watchlist.html', title='My Watchlist', watchlist_items=items_with_stock_data)

@bp.route('/watchlist/add/<string:stock_code>', methods=['POST']) # Ensure stock_code is string
@login_required
def add_to_watchlist_route(stock_code):
    success, message = watchlist_svc.add_to_watchlist(current_user.id, stock_code)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'danger')
    # Redirect to the page where the add button was clicked, or to watchlist, or stock page
    # For now, redirecting to watchlist. A common pattern is to redirect back to request.referrer
    return redirect(request.referrer or url_for('user.display_watchlist'))

@bp.route('/watchlist/remove/<string:stock_code>', methods=['POST']) # Ensure stock_code is string
@login_required
def remove_from_watchlist_route(stock_code):
    success, message = watchlist_svc.remove_from_watchlist(current_user.id, stock_code)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'danger')
    return redirect(url_for('user.display_watchlist'))
