from flask import Flask
from .extensions import db
from .routes import main
import os

# Load .env if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from config import (
    DevelopmentConfig,
    StagingConfig,
    UATConfig,
    ProductionConfig
)

def create_app():
    app = Flask(__name__)

    # Decide environment
    env = os.getenv("FLASK_ENV", "development")

    if env == "production":
        app.config.from_object(ProductionConfig)
    elif env == "staging":
        app.config.from_object(StagingConfig)
    elif env == "uat":
        app.config.from_object(UATConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app