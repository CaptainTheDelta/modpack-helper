import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask("Modpack Helper")
    app.config.from_object("app.config.Config")

    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    from app.routes import bp as routes_bp
    from app.api import bp as api_bp

    app.register_blueprint(routes_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    return app