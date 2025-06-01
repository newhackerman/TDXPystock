import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'user.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register blueprints
    from app.routes.main_routes import bp as main_bp
    app.register_blueprint(main_bp)

    from app.routes.user_routes import bp as user_bp
    app.register_blueprint(user_bp, url_prefix='/user')

    from app.routes.monitoring_routes import bp as monitoring_bp
    app.register_blueprint(monitoring_bp, url_prefix='/monitoring')

    from app.routes.market_data_routes import bp as market_data_bp
    app.register_blueprint(market_data_bp, url_prefix='/market_data')

    # fund_flow_routes, auction_routes, analysis_routes, strategy_routes were created as placeholders
    # but not fully implemented with __init__.py content or actual routes.
    # For now, we assume they are not breaking the app if not fully defined.
    # If they were meant to be used, they would need proper setup.
    # from app.routes.fund_flow_routes import bp as fund_flow_bp
    # app.register_blueprint(fund_flow_bp, url_prefix='/fund_flow')

    # from app.routes.auction_routes import bp as auction_bp
    # app.register_blueprint(auction_bp, url_prefix='/auction')

    # from app.routes.analysis_routes import bp as analysis_bp
    # app.register_blueprint(analysis_bp, url_prefix='/analysis')

    # from app.routes.strategy_routes import bp as strategy_bp
    # app.register_blueprint(strategy_bp, url_prefix='/strategy')

    from .routes.news_routes import bp as news_bp # Added news_bp
    app.register_blueprint(news_bp) # Default prefix is /news as defined in news_routes.py


    from app.models.user_model import Users
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    return app
