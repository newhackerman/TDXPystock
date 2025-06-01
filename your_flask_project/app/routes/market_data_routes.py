from flask import Blueprint, render_template, request
from app.services import data_fetch_svc

bp = Blueprint('market_data', __name__)
DEFAULT_PER_PAGE = 30

# --- Stock Lists ---
@bp.route('/a_shares')
def list_a_shares():
    page = request.args.get('page', 1, type=int)
    stocks_df, total_items, total_pages, current_page = data_fetch_svc.get_a_share_stock_list(page=page, per_page=DEFAULT_PER_PAGE)
    return render_template('market_data/a_shares.html', title='A-Share Stocks', stocks=stocks_df, page=current_page, per_page=DEFAULT_PER_PAGE, total_items=total_items, total_pages=total_pages)

@bp.route('/us_stocks')
def list_us_stocks():
    page = request.args.get('page', 1, type=int)
    stocks_df, total_items, total_pages, current_page = data_fetch_svc.get_us_stock_list(page=page, per_page=DEFAULT_PER_PAGE)
    return render_template('market_data/us_stock_list.html', title='US Stocks', stocks=stocks_df, page=current_page, per_page=DEFAULT_PER_PAGE, total_items=total_items, total_pages=total_pages)

@bp.route('/hk_stocks')
def list_hk_stocks():
    page = request.args.get('page', 1, type=int)
    stocks_df, total_items, total_pages, current_page = data_fetch_svc.get_hk_stock_list(page=page, per_page=DEFAULT_PER_PAGE)
    return render_template('market_data/hk_stock_list.html', title='Hong Kong Stocks', stocks=stocks_df, page=current_page, per_page=DEFAULT_PER_PAGE, total_items=total_items, total_pages=total_pages)

@bp.route('/chinese_concept_stocks')
def list_chinese_concept_stocks():
    page = request.args.get('page', 1, type=int)
    stocks_df, total_items, total_pages, current_page = data_fetch_svc.get_chinese_concept_stock_list(page=page, per_page=DEFAULT_PER_PAGE)
    return render_template('market_data/chinese_concept_stock_list.html', title='Chinese Concept Stocks (US Listed)', stocks=stocks_df, page=current_page, per_page=DEFAULT_PER_PAGE, total_items=total_items, total_pages=total_pages)

@bp.route('/chinext_stocks')
def list_chinext_stocks():
    page = request.args.get('page', 1, type=int)
    stocks_df, total_items, total_pages, current_page = data_fetch_svc.get_chinext_stock_list(page=page, per_page=DEFAULT_PER_PAGE)
    return render_template('market_data/chinext_stock_list.html', title='ChiNext Stocks (创业板)', stocks=stocks_df, page=current_page, per_page=DEFAULT_PER_PAGE, total_items=total_items, total_pages=total_pages)

@bp.route('/sme_stocks')
def list_sme_stocks():
    page = request.args.get('page', 1, type=int)
    stocks_df, total_items, total_pages, current_page = data_fetch_svc.get_sme_stock_list(page=page, per_page=DEFAULT_PER_PAGE)
    return render_template('market_data/sme_stock_list.html', title='SME Stocks (中小板)', stocks=stocks_df, page=current_page, per_page=DEFAULT_PER_PAGE, total_items=total_items, total_pages=total_pages)

@bp.route('/star_market_stocks')
def list_star_market_stocks():
    page = request.args.get('page', 1, type=int)
    stocks_df, total_items, total_pages, current_page = data_fetch_svc.get_star_market_stock_list(page=page, per_page=DEFAULT_PER_PAGE)
    return render_template('market_data/star_market_stock_list.html', title='STAR Market Stocks (科创板)', stocks=stocks_df, page=current_page, per_page=DEFAULT_PER_PAGE, total_items=total_items, total_pages=total_pages)

@bp.route('/bse_stocks')
def list_bse_stocks():
    page = request.args.get('page', 1, type=int)
    stocks_df, total_items, total_pages, current_page = data_fetch_svc.get_bse_stock_list(page=page, per_page=DEFAULT_PER_PAGE)
    return render_template('market_data/bse_stock_list.html', title='Beijing Stock Exchange (BSE) Stocks', stocks=stocks_df, page=current_page, per_page=DEFAULT_PER_PAGE, total_items=total_items, total_pages=total_pages)

# --- Indices & Bonds ---
@bp.route('/indices')
def list_domestic_indices():
    page = request.args.get('page', 1, type=int)
    indices_df, total_items, total_pages, current_page = data_fetch_svc.get_domestic_indices(page=page, per_page=DEFAULT_PER_PAGE)
    return render_template('market_data/indices.html', title='Domestic Indices', indices=indices_df, page=current_page, per_page=DEFAULT_PER_PAGE, total_items=total_items, total_pages=total_pages)

@bp.route('/global_indices')
def list_global_indices():
    page = request.args.get('page', 1, type=int)
    indices_df, total_items, total_pages, current_page = data_fetch_svc.get_global_indices(page=page, per_page=DEFAULT_PER_PAGE)
    return render_template('market_data/global_indices.html', title='Global Indices', indices=indices_df, page=current_page, per_page=DEFAULT_PER_PAGE, total_items=total_items, total_pages=total_pages)

@bp.route('/global_bonds')
def list_global_bonds():
    page = request.args.get('page', 1, type=int)
    bonds_df, total_items, total_pages, current_page = data_fetch_svc.get_global_bond_list(page=page, per_page=DEFAULT_PER_PAGE)
    return render_template('market_data/global_bond_list.html', title='Global Bond Indices', bonds=bonds_df, page=current_page, per_page=DEFAULT_PER_PAGE, total_items=total_items, total_pages=total_pages)

# --- ETFs & Convertible Bonds ---
@bp.route('/etf')
def list_etf():
    page = request.args.get('page', 1, type=int)
    etf_df, total_items, total_pages, current_page = data_fetch_svc.get_etf_spot_list(page=page, per_page=DEFAULT_PER_PAGE)
    return render_template('market_data/etf_list.html', title='ETF Quotes', etfs=etf_df, page=current_page, per_page=DEFAULT_PER_PAGE, total_items=total_items, total_pages=total_pages)

@bp.route('/convertible_bonds')
def list_convertible_bonds():
    page = request.args.get('page', 1, type=int)
    bonds_df, total_items, total_pages, current_page = data_fetch_svc.get_convertible_bond_list(page=page, per_page=DEFAULT_PER_PAGE)
    return render_template('market_data/convertible_bond_list.html', title='Convertible Bonds', bonds=bonds_df, page=current_page, per_page=DEFAULT_PER_PAGE, total_items=total_items, total_pages=total_pages)

# --- Industry & Concepts ---
@bp.route('/concept_sectors')
def list_concept_sectors():
    page = request.args.get('page', 1, type=int)
    sectors_df, total_items, total_pages, current_page = data_fetch_svc.get_concept_sectors_data(page=page, per_page=DEFAULT_PER_PAGE)
    return render_template('market_data/concept_sectors.html', title='Concept Sectors', sectors=sectors_df, page=current_page, per_page=DEFAULT_PER_PAGE, total_items=total_items, total_pages=total_pages)

@bp.route('/stock_quotes') # General stock quotes page
def stock_quotes_page():
    page = request.args.get('page', 1, type=int)
    # Potentially accept stock_codes via request.args.getlist('codes') if needed
    # For now, calls the general A-share list as per service function's default
    quotes_df, total_items, total_pages, current_page = data_fetch_svc.get_stock_quotes_general(page=page, per_page=DEFAULT_PER_PAGE)
    return render_template('market_data/stock_quotes_page.html', title='Stock Quotes', quotes=quotes_df, page=current_page, per_page=DEFAULT_PER_PAGE, total_items=total_items, total_pages=total_pages)

@bp.route('/stock_fundflow_ranked')
def stock_fundflow_ranked_page():
    page = request.args.get('page', 1, type=int)
    fundflow_df, total_items, total_pages, current_page = data_fetch_svc.get_ranked_stock_fundflow(page=page, per_page=DEFAULT_PER_PAGE)
    return render_template('market_data/stock_fundflow_ranked.html', title='Ranked Stock Fund Flows', fundflows=fundflow_df, page=current_page, per_page=DEFAULT_PER_PAGE, total_items=total_items, total_pages=total_pages)
