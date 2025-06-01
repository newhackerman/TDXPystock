from flask import Blueprint, render_template, request
from app.services import data_fetch_svc

bp = Blueprint('monitoring', __name__)
DEFAULT_PER_PAGE = 30

@bp.route('/large_orders')
def list_large_orders():
    page = request.args.get('page', 1, type=int)
    orders_df, total_items, total_pages, current_page = data_fetch_svc.get_large_orders_data(page=page, per_page=DEFAULT_PER_PAGE)
    return render_template(
        'monitoring/large_orders.html',
        title='Large Orders Monitoring (Ranked by Main Fund Flow)',
        orders=orders_df,
        page=current_page,
        per_page=DEFAULT_PER_PAGE,
        total_items=total_items,
        total_pages=total_pages
    )

@bp.route('/leading_stocks')
def list_leading_stocks():
    leading_stocks_data = data_fetch_svc.get_leading_stocks_data()
    is_error_string = isinstance(leading_stocks_data, str)
    return render_template(
        'monitoring/leading_stocks.html',
        title='Leading Stocks Monitor',
        leading_stocks=leading_stocks_data,
        is_error=is_error_string
    )

@bp.route('/sector_monitor') # This is Industry Sector Monitor
def list_sector_monitor():
    page = request.args.get('page', 1, type=int)
    sectors_df, total_items, total_pages, current_page = data_fetch_svc.get_sector_monitor_data(page=page, per_page=DEFAULT_PER_PAGE)
    return render_template(
        'monitoring/sector_monitor.html',
        title='Industry Sector Monitor',
        sectors=sectors_df,
        page=current_page,
        per_page=DEFAULT_PER_PAGE,
        total_items=total_items,
        total_pages=total_pages
    )

@bp.route('/limit_up_stocks')
def list_limit_up_stocks():
    page = request.args.get('page', 1, type=int)
    stocks_df, total_items, total_pages, current_page = data_fetch_svc.get_limit_up_stocks(page=page, per_page=DEFAULT_PER_PAGE)
    return render_template(
        'monitoring/limit_up_stocks.html',
        title='Limit-Up Stocks Pool',
        stocks=stocks_df,
        page=current_page,
        per_page=DEFAULT_PER_PAGE,
        total_items=total_items,
        total_pages=total_pages
    )

@bp.route('/aggregated_large_orders') # New route for "TDX Dadan View"
def list_aggregated_large_orders():
    page = request.args.get('page', 1, type=int)
    # Reusing the same service function as /large_orders
    # The difference will primarily be in the template's title and potentially presentation
    orders_df, total_items, total_pages, current_page = data_fetch_svc.get_large_orders_data(page=page, per_page=DEFAULT_PER_PAGE)
    return render_template(
        'monitoring/aggregated_large_orders.html',
        title='Aggregated Large Orders (TDX Dadan View Style)',
        orders=orders_df, # Using the same variable name 'orders' for template compatibility
        page=current_page,
        per_page=DEFAULT_PER_PAGE,
        total_items=total_items,
        total_pages=total_pages
    )
