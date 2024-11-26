from flask import Flask
from .extensions import db
from .routes import register_routes


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    # Khởi tạo database và các tiện ích
    db.init_app(app)
    
    # Đăng ký các routes
    register_routes(app)
    return app
