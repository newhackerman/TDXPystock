from flask import Blueprint, render_template, request, flash
from app.services import analysis_svc
from app.services import data_fetch_svc
from .forms import StockCodeForm, FundDataSelectionForm # Added FundDataSelectionForm

bp = Blueprint('analysis', __name__, url_prefix='/analysis')
DEFAULT_PER_PAGE = 20

@bp.route('/risk_scan', methods=['GET', 'POST'])
def risk_scan_page():
    form = StockCodeForm()
    scan_results = None
    stock_code_checked = None
    stock_name_checked = None
    risk_score = None

    if form.validate_on_submit():
        stock_code_input = form.stock_code.data
        try:
            risks, score, name, code_fmt = analysis_svc.get_stock_risk_scan(stock_code_input)
            scan_results = risks
            risk_score = score
            stock_name_checked = name
            stock_code_checked = code_fmt
            if not risks:
                flash(f"Scan for {stock_name_checked} ({stock_code_checked}) completed. Score: {risk_score}. No specific risks listed.", "info")
            elif any("error" in item.lower() or "fail" in item.lower() or "invalid" in item.lower() for item in risks if isinstance(item, str)):
                 flash(f"Scan for {stock_code_input} encountered issues. Score: {risk_score}", "warning")
            else:
                 flash(f"Risk scan for {stock_name_checked} ({stock_code_checked}) completed. Score: {risk_score}", "success" if risk_score > 70 else ("warning" if risk_score > 40 else "danger"))
        except Exception as e:
            flash(f"A critical error occurred during the risk scan: {str(e)}", "danger")
            scan_results = [f"Application error: {str(e)}"]
            risk_score = 0
            stock_code_checked = stock_code_input
            stock_name_checked = stock_code_input

    return render_template(
        'analysis/risk_scan.html',
        title='Stock Risk Scan',
        form=form,
        scan_results=scan_results,
        stock_code_checked=stock_code_checked,
        stock_name_checked=stock_name_checked,
        risk_score=risk_score
    )

@bp.route('/newly_highlighted_stocks')
def list_newly_highlighted_stocks():
    page = request.args.get('page', 1, type=int)
    recent_day_param = request.args.get('days', "5", type=str)

    stocks_df, total_items, total_pages, current_page = data_fetch_svc.get_newly_highlighted_stocks(
        page=page,
        per_page=DEFAULT_PER_PAGE,
        recent_day=recent_day_param
    )
    return render_template(
        'analysis/newly_highlighted_stocks.html',
        title=f'Newly Highlighted Stocks (Last {recent_day_param} Days)',
        stocks=stocks_df,
        page=current_page,
        per_page=DEFAULT_PER_PAGE,
        total_items=total_items,
        total_pages=total_pages,
        current_days_filter=recent_day_param
    )

@bp.route('/fund_data_stock_selection', methods=['GET', 'POST'])
def fund_data_select_page():
    form = FundDataSelectionForm(request.form) # Use request.form for POST data
    stocks_data = None
    total_items = 0
    total_pages = 1
    current_page = 1

    # Keep selected form values to repopulate the form
    selected_indicator = form.indicator.data if form.indicator.data else "今日"
    selected_min_percent = form.min_main_force_percent.data if form.min_main_force_percent.data is not None else None

    if request.method == 'POST' and form.validate_on_submit():
        page = request.args.get('page', 1, type=int) # Get page for results
        stocks_data, total_items, total_pages, current_page = data_fetch_svc.get_fund_data_selected_stocks(
            indicator=selected_indicator,
            min_main_force_percent=selected_min_percent,
            page=page,
            per_page=DEFAULT_PER_PAGE
        )
        if stocks_data.empty:
            flash('No stocks found matching your criteria.', 'info')
    elif request.method == 'GET': # Optionally load default for "今日" on initial GET
        page = request.args.get('page', 1, type=int)
        # To make it cleaner, only fetch if specific parameters are present or a search is initiated.
        # Or, fetch for default "今日" if desired. For now, fetch on POST or if query params exist.
        if 'indicator' in request.args: # If form was submitted via GET links from pagination
             selected_indicator = request.args.get('indicator', "今日")
             min_percent_str = request.args.get('min_main_force_percent', '')
             selected_min_percent = float(min_percent_str) if min_percent_str else None
             form.indicator.data = selected_indicator
             form.min_main_force_percent.data = selected_min_percent

             stocks_data, total_items, total_pages, current_page = data_fetch_svc.get_fund_data_selected_stocks(
                indicator=selected_indicator,
                min_main_force_percent=selected_min_percent,
                page=page,
                per_page=DEFAULT_PER_PAGE
            )


    return render_template(
        'analysis/fund_data_stock_selection.html',
        title='Fund Data Stock Selection',
        form=form,
        stocks=stocks_data,
        page=current_page,
        per_page=DEFAULT_PER_PAGE,
        total_items=total_items,
        total_pages=total_pages,
        selected_indicator=selected_indicator, # Pass current selection back for pagination links
        selected_min_main_force_percent=selected_min_percent
    )
