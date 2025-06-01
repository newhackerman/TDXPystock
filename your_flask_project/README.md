# Flask Stock Application

This is a Flask web application converted from an original PyQt desktop application (`操盘神器ui.py`).

## Features Implemented
*   User Authentication (Login, Registration)
*   Watchlist Management (Display, Add, Remove - DB interaction pending successful migrations)
*   Extensive Market Data Views (A-Shares, US, HK, ChiNext, SME, STAR, BSE, Domestic & Global Indices, ETFs, Convertible Bonds, Global Bonds etc.) with pagination.
*   Monitoring Tools (Large Orders, Aggregated Large Orders, Leading Stocks, Industry Sector Monitor, Limit-Up Stocks, Market Fundflow Overview) with pagination.
*   News Display (CLS Telegraph News) with pagination.
*   Analysis Tools:
    *   Stock Risk Scan (扫雷)
    *   Newly Highlighted Stocks (龙虎榜)
    *   Fund Data Stock Selection
*   Data Export (CSV for Large Orders).

## Setup (General)
1.  Create a Python virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Set up a MySQL database:
    *   Ensure MySQL server is running.
    *   Create a database named `stock`.
    *   Create a user `stock` with password `!!` and grant permissions on the `stock` database.
    *   Alternatively, update the `SQLALCHEMY_DATABASE_URI` in `config.py` to your database credentials.
4.  Initialize Flask environment variables:
    *   `export FLASK_APP=run.py` (Linux/macOS) or `set FLASK_APP=run.py` (Windows)
    *   `export FLASK_DEBUG=1` (Linux/macOS) or `set FLASK_DEBUG=1` (Windows) - for development mode
5.  Run database migrations (once MySQL is accessible and configured):
    *   `flask db init` (Run this only once if the `migrations` folder doesn't exist)
    *   `flask db migrate -m "Initial schema setup"` (Or a more descriptive message for subsequent migrations)
    *   `flask db upgrade` (To apply the migrations to the database)
6.  Run the application:
    ```bash
    flask run
    ```
    Or:
    ```bash
    python run.py
    ```
    The application will typically be available at `http://127.0.0.1:5000/`.

## Database Connectivity
The application requires a running MySQL server for full functionality, including user accounts, watchlists, and any features that persist data. Many data display features fetch live data from external APIs and will work without a database connection, but will use dummy data if API calls fail.

If you encounter database connection issues during migrations or application startup:
*   Verify your MySQL server is running.
*   Check that the database `stock` exists.
*   Ensure the user `stock` with password `!!` has the necessary privileges on the `stock` database.
*   Confirm that the `SQLALCHEMY_DATABASE_URI` in `config.py` correctly points to your MySQL instance. The default is `mysql+pymysql://stock:!!@127.0.0.1/stock`.

## Project Structure
*   `app/`: Main application package.
    *   `models/`: SQLAlchemy database models.
    *   `routes/`: Flask blueprints and route definitions.
    *   `services/`: Business logic and data fetching/processing services.
    *   `static/`: Static assets (CSS, JavaScript, images).
    *   `templates/`: Jinja2 HTML templates.
*   `migrations/`: Flask-Migrate database migration scripts.
*   `original_codebase_references/`: Contains references or parts of the original PyQt application for conversion context.
*   `config.py`: Application configuration.
*   `run.py`: Script to run the Flask development server.
*   `wsgi.py`: WSGI entry point for production deployment.
```
