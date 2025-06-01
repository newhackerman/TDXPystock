from flask import Blueprint, render_template, request
from app.services import data_fetch_svc

bp = Blueprint('fund_flow', __name__, url_prefix='/fund_flow')
DEFAULT_PER_PAGE = 20 # Default for top holdings, can be adjusted
NO_PAGINATION = 0 # For service functions that should return all data (or handle pagination differently)

@bp.route('/northbound/daily_flow')
def northbound_daily_flow():
    # Fetching all data, pagination handled in template if needed or shown as chart
    # Service returns: df, total_items, total_pages (will be 1 if NO_PAGINATION), current_page (will be 1)
    flow_df, total_items, _, _ = data_fetch_svc.get_northbound_net_flow(page=1, per_page=NO_PAGINATION)
    # For charting, often the full DataFrame is preferred.
    # If table display is too long, can consider showing last N days or client-side pagination.
    # For now, we pass the full DF and let the template decide how to display.
    return render_template(
        'fund_flow/north_daily_flow.html',
        title='Northbound Daily Net Flow',
        flows=flow_df, # Pass the full DataFrame
        total_days=total_items
    )

@bp.route('/southbound/daily_flow')
def southbound_daily_flow():
    flow_df, total_items, _, _ = data_fetch_svc.get_southbound_net_flow(page=1, per_page=NO_PAGINATION)
    return render_template(
        'fund_flow/south_daily_flow.html',
        title='Southbound Daily Net Flow',
        flows=flow_df,
        total_days=total_items
    )

@bp.route('/northbound/top_holdings')
def northbound_top_holdings():
    page = request.args.get('page', 1, type=int)
    indicator = request.args.get('indicator', "今日排行", type=str)

    holdings_df, total_items, total_pages, current_page = data_fetch_svc.get_northbound_top_holdings(
        page=page, per_page=DEFAULT_PER_PAGE, indicator=indicator
    )

    valid_indicators = ["今日排行", "3日排行", "5日排行", "10日排行"]

    return render_template(
        'fund_flow/north_top_holdings.html',
        title=f'Northbound Top Holdings ({indicator})',
        holdings=holdings_df,
        page=current_page,
        per_page=DEFAULT_PER_PAGE,
        total_items=total_items,
        total_pages=total_pages,
        current_indicator=indicator,
        valid_indicators=valid_indicators
    )

@bp.route('/hgt/top_holdings') # Shanghai-HK Connect (沪股通)
def hgt_top_holdings():
    page = request.args.get('page', 1, type=int)
    indicator = request.args.get('indicator', "今日排行", type=str)
    valid_indicators = ["今日排行", "3日排行", "5日排行", "10日排行"]

    holdings_df, total_items, total_pages, current_page = data_fetch_svc.get_hgt_top_holdings(
        page=page, per_page=DEFAULT_PER_PAGE, indicator=indicator
    )
    return render_template(
        'fund_flow/hgt_top_holdings.html',
        title=f'Shanghai-HK Connect (HGT) Top Holdings ({indicator})',
        holdings=holdings_df,
        page=current_page,
        per_page=DEFAULT_PER_PAGE,
        total_items=total_items,
        total_pages=total_pages,
        current_indicator=indicator,
        valid_indicators=valid_indicators
    )

@bp.route('/sgt/top_holdings') # Shenzhen-HK Connect (深股通)
def sgt_top_holdings():
    page = request.args.get('page', 1, type=int)
    indicator = request.args.get('indicator', "今日排行", type=str)
    valid_indicators = ["今日排行", "3日排行", "5日排行", "10日排行"]

    holdings_df, total_items, total_pages, current_page = data_fetch_svc.get_sgt_top_holdings(
        page=page, per_page=DEFAULT_PER_PAGE, indicator=indicator
    )
    return render_template(
        'fund_flow/sgt_top_holdings.html',
        title=f'Shenzhen-HK Connect (SGT) Top Holdings ({indicator})',
        holdings=holdings_df,
        page=current_page,
        per_page=DEFAULT_PER_PAGE,
        total_items=total_items,
        total_pages=total_pages,
        current_indicator=indicator,
        valid_indicators=valid_indicators
    )
