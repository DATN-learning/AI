from app.routes.api import chapter_bp
from app.routes.api import post
from app.routes.api import content
from app.routes.api import ratingss
def register_routes(app):
    app.register_blueprint(chapter_bp, url_prefix='/api')
    app.register_blueprint(post, url_prefix='/api')
    app.register_blueprint(content, url_prefix='/api')
    app.register_blueprint(ratingss, url_prefix='/api')
    