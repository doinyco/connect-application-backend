from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__)

    from .routes import users_bp
    app.register_blueprint(users_bp)

    return app


