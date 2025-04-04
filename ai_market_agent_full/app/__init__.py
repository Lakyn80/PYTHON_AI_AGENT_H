from flask import Flask
from app.db import init_db
from app.routes.search_routes import search_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:205800@localhost:5432/hyalchondro'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    init_db(app)
    
    with app.app_context():
        # Vytvoření tabulek pokud neexistují
        from app.models import ProductEntry
        from app.db import db
        db.create_all()

    return app
