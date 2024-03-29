from flask import Flask, render_template, url_for
import secrets

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'wei0829'
    
    # import blueprint
    from .views import views
    
    app.register_blueprint(views, url_prefix='/')
    
    @app.errorhandler(404)
    def invalid_route(e):
        return render_template("404.html"), 404
    
    
    return app