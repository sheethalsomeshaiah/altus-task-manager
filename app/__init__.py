from flask import Flask
from .extensions import db
from .routes import main

# Try loading environment variables from .env, fall back silently if not available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # 'python-dotenv' is not installed. You can set environment variables manually
    # or install it with: pip install python-dotenv
    pass

def create_app():
    # Flask app factory
    app = Flask(__name__)

    # Set secret key for session management and security
    app.config['SECRET_KEY'] = 'secret-key'

    # SQLite database URI (database will be created in instance/ by default)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Altustaskmanagement.db'

    # Disable Flask-SQLAlchemy event system to save resources
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions (SQLAlchemy)
    db.init_app(app)

    # Register main Blueprint containing all routes/views
    app.register_blueprint(main)

    # Create all database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app