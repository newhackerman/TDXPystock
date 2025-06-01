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

    from app.routes.news_routes import bp as news_bp
    app.register_blueprint(news_bp)

    from app.routes.analysis_routes import bp as analysis_bp
    app.register_blueprint(analysis_bp, url_prefix='/analysis')

    from app.routes.fund_flow_routes import bp as fund_flow_bp # Added fund_flow_bp
    app.register_blueprint(fund_flow_bp, url_prefix='/fund_flow')


    # Placeholder for other blueprints that might not be fully implemented yet
    # from app.routes.auction_routes import bp as auction_bp
    # app.register_blueprint(auction_bp, url_prefix='/auction')

    # from app.routes.strategy_routes import bp as strategy_bp
    # app.register_blueprint(strategy_bp, url_prefix='/strategy')


    from app.models.user_model import Users
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    return app
