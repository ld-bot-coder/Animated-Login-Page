from flask import Flask
from config import Config
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configure Logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Register Blueprints
    from app.routing import api_bp, web_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(web_bp)

    return app
