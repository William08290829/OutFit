from flask import Flask, render_template, url_for
import secrets

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secrets.token_hex(16)
    
    # import blueprint
    from .routes import views
    
    app.register_blueprint(routes, url_prefix='/')
    
    @app.errorhandler(404)
    def invalid_route(e):
        return render_template("404.html"), 404
    
    
    return app