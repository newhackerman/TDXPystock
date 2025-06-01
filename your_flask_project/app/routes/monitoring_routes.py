from flask import Blueprint, render_template, request, Response, flash, redirect, url_for
from flask_login import login_required # Assuming exports should be protected
from app.services import data_fetch_svc
from datetime import datetime

bp = Blueprint('monitoring', __name__)
DEFAULT_PER_PAGE = 30
DEFAULT_FUNDFLOW_OVERVIEW_PER_PAGE = 50

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

@bp.route('/sector_monitor')
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

@bp.route('/aggregated_large_orders')
def list_aggregated_large_orders():
    page = request.args.get('page', 1, type=int)
    orders_df, total_items, total_pages, current_page = data_fetch_svc.get_large_orders_data(page=page, per_page=DEFAULT_PER_PAGE)
    return render_template(
        'monitoring/aggregated_large_orders.html',
        title='Aggregated Large Orders (TDX Dadan View Style)',
        orders=orders_df,
        page=current_page,
        per_page=DEFAULT_PER_PAGE,
        total_items=total_items,
        total_pages=total_pages
    )

@bp.route('/market_fundflow_overview')
def market_fundflow_overview_page():
    page = request.args.get('page', 1, type=int)
    fundflow_df, total_items, total_pages, current_page = data_fetch_svc.get_market_fundflow_overview(page=page, per_page=DEFAULT_FUNDFLOW_OVERVIEW_PER_PAGE)
    return render_template(
        'monitoring/market_fundflow_overview.html',
        title='Market Fundflow Overview',
        fundflows=fundflow_df,
        page=current_page,
        per_page=DEFAULT_FUNDFLOW_OVERVIEW_PER_PAGE,
        total_items=total_items,
        total_pages=total_pages
    )

@bp.route('/export/large_orders_csv')
@login_required # Assuming exports should also be protected if the page is
def export_large_orders_csv():
    # Call service function with per_page=0 to get all data
    df, total_items, _, _ = data_fetch_svc.get_large_orders_data(page=1, per_page=0)

    if df is None or df.empty:
        flash('No data available to export for Large Orders.', 'warning')
        return redirect(url_for('monitoring.list_large_orders'))

    try:
        current_date = datetime.now().strftime("%Y-%m-%d")
        filename = f"large_orders_export_{current_date}.csv"

        # Use utf-8-sig for better Excel compatibility with UTF-8 characters
        csv_data = df.to_csv(index=False, encoding='utf-8-sig')

        return Response(
            csv_data,
            mimetype="text/csv",
            headers={"Content-Disposition": f"attachment;filename={filename}"}
        )
    except Exception as e:
        flash(f'Error exporting Large Orders data: {str(e)}', 'danger')
        return redirect(url_for('monitoring.list_large_orders'))
