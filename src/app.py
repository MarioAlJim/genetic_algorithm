"""This file is for executing the app"""
# Third party imports
from flask import Flask, redirect, url_for

# Local application imports
from routes.about_routes import about_blueprint
from routes.playground_routes import playground_blueprint

def create_app() -> Flask:
    """Create and set up the app"""
    new_app = Flask(__name__)
    new_app.config['SECRET_KEY'] = 'bite'

    new_app.register_blueprint(about_blueprint)
    new_app.register_blueprint(playground_blueprint, url_prefix='/playground')

    @new_app.route('/')
    def home():
        return redirect(url_for('playground_blueprint.show_ga_playground'))

    return new_app

if __name__ == '__main__':
    app = create_app()
    app.run(host='localhost', port=3000, debug=True)
