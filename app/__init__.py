from flask import Flask
from app.extensions import db, migrate
from config import Config

from app.routes.users import users_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(users_bp)

    return app