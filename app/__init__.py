from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'routes.login'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret_key123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.routes import routes as routes_blueprint
    app.register_blueprint(routes_blueprint)

    with app.app_context():
        from app.models import User

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(user_id)  # ✅ no int() — works with username

        db.create_all()

    return app




