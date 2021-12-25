"""Initialize Flask app."""
from flask import Flask
from dash import Dash
from flask_cors import CORS

def init_app(debug=False, page=None):
    """
    Construct core Flask application with embedded Dash app.
    hard-write .config call to either ProdConfig or DevConfig 
    """
    if debug == False:
        app = Flask(__name__, instance_relative_config=False)
        CORS(app)
        app.config.from_object('config.ProdConfig')
        

        with app.app_context():
            

            # Import parts of our core Flask app
            from . import routes

            # Import Dash applications
            from .dashboard.dashboard import init_dashboard
            app = init_dashboard(app)

    else:
        app = Dash(__name__)
        from .dashboard.dashboard import init_dashboard
        app = init_dashboard(app, debug=True)
        
    return app
