from app import db
from app.models.watchlist_model import Watchlist
from app.models.stock_model import Stocks
# It's good to also import Users if you need to validate user_id, though Flask-Login usually handles user existence.

def get_watchlist_for_user(user_id):
    """
    Fetches stocks favorited by the user, joined with stock details.
    Returns a list of Watchlist objects, each having a .stock attribute.
    Or could return a list of Stock objects directly if preferred.
    """
    # This query joins Watchlist with Stocks and filters by user_id
    # It eagerly loads the related 'stock' object for each watchlist item
    # to avoid N+1 queries if accessing stock details later in the template.
    watchlist_items_with_stock_data = db.session.query(Watchlist).join(Stocks, Watchlist.stock_code == Stocks.code).filter(Watchlist.user_id == user_id).all()

    # Alternatively, to return a list of Stock objects directly:
    # stocks = Stocks.query.join(Watchlist, Stocks.code == Watchlist.stock_code).filter(Watchlist.user_id == user_id).all()
    # return stocks

    return watchlist_items_with_stock_data


def add_to_watchlist(user_id, stock_code):
    """
    Adds a stock to the user's watchlist.
    Returns (True, "Stock added to watchlist.") on success,
            (False, "Error message") on failure.
    """
    # Check if stock exists (optional, depends on how stock_code is obtained)
    stock = Stocks.query.get(stock_code)
    if not stock:
        return False, "Stock code not found."

    # Check if it's already in the watchlist
    existing_item = Watchlist.query.filter_by(user_id=user_id, stock_code=stock_code).first()
    if existing_item:
        return False, "Stock already in watchlist."

    new_item = Watchlist(user_id=user_id, stock_code=stock_code)
    try:
        db.session.add(new_item)
        db.session.commit()
        return True, "Stock added to watchlist."
    except Exception as e:
        db.session.rollback()
        # Log error e
        return False, f"Could not add stock to watchlist: {str(e)}"


def remove_from_watchlist(user_id, stock_code):
    """
    Removes a stock from the user's watchlist.
    Returns (True, "Stock removed from watchlist.") on success,
            (False, "Error message") on failure.
    """
    item = Watchlist.query.filter_by(user_id=user_id, stock_code=stock_code).first()
    if not item:
        return False, "Stock not found in watchlist."

    try:
        db.session.delete(item)
        db.session.commit()
        return True, "Stock removed from watchlist."
    except Exception as e:
        db.session.rollback()
        # Log error e
        return False, f"Could not remove stock from watchlist: {str(e)}"
