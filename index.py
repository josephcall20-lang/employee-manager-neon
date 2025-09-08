import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
cors = CORS()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    cors.init_app(app, supports_credentials=True)

    # Import blueprints from modules in your repo root
    from admin import admin_bp
    from candidate import candidate_bp
    from files import files_bp
    from indeed import indeed_bp

    app.register_blueprint(admin_bp, url_prefix='/api')
    app.register_blueprint(candidate_bp, url_prefix='/api')
    app.register_blueprint(files_bp, url_prefix='/api')
    app.register_blueprint(indeed_bp, url_prefix='/api/indeed')

    @app.get("/api/health")
    def health_check():
        return jsonify({"ok": True})

    # TEMP: one‑time DB initialization
    @app.post("/api/admin/init-db")
    def init_db_once():
        if os.getenv("ALLOW_INIT_DB") != "true":
            return ("forbidden", 403)
        with app.app_context():
            db.create_all()
        return jsonify({"ok": True})

    return app

app = create_app()
