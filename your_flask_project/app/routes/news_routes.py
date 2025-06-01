from flask import Blueprint, render_template, request # Added request for pagination later if needed
from app.services import data_fetch_svc

bp = Blueprint('news', __name__, url_prefix='/news')
DEFAULT_PER_PAGE_NEWS = 25 # Can be different from other pages

@bp.route('/cls')
def cls_news_page():
    page = request.args.get('page', 1, type=int)
    # get_cls_news will return: paginated_data, total_items, total_pages, current_page
    news_data, total_items, total_pages, current_page = data_fetch_svc.get_cls_news(page=page, per_page=DEFAULT_PER_PAGE_NEWS)

    return render_template(
        'news/cls_news.html',
        news_items=news_data,
        title="CLS Telegraph News",
        page=current_page,
        per_page=DEFAULT_PER_PAGE_NEWS,
        total_items=total_items,
        total_pages=total_pages
    )
