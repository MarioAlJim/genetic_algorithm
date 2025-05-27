"""This file is for executing the app"""
# Third party imports
import os
from flask import Flask, redirect, url_for, request, session
from flask_babel import Babel, gettext

# Local application imports
from routes.about_routes import about_blueprint
from routes.playground_routes import playground_blueprint


def clean_temp_files(directory, extensions):
    for filename in os.listdir(directory):
        if any(filename.endswith(ext) for ext in extensions):
            file_path = os.path.join(directory, filename)
            try:
                os.remove(file_path)
                print(f"Residual file removed: {file_path}")
            except Exception as e:
                print(f"Could not be eliminated {file_path}: {e}")
    return

def create_app() -> Flask:
    """Create and set up the app"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'bite'
    app.register_blueprint(about_blueprint)
    app.register_blueprint(playground_blueprint, url_prefix='/playground')

    app.config['BABEL_DEFAULT_LOCALE'] = 'es'
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = './translations'

    def get_locale():
        if 'lang' in request.args:
            lang = request.args.get('lang')
            if lang in ['en', 'es']:
                session['lang'] = lang
                return session['lang']
        elif 'lang' in session:
            return session.get('lang')
        return request.accept_languages.best_match(['en', 'es'])

    babel = Babel(app, locale_selector=get_locale)

    @app.route('/')
    def home():
        return redirect(url_for('playground_blueprint.show_playground'))

    @app.route('/setlang')
    def set_lang():
        lang = request.args.get('lang')
        session['lang'] = lang
        return redirect(url_for('playground_blueprint.show_playground'))

    @app.context_processor
    def inject_locale():
        # This makes the function available directly, allowing you to call it in the template
        return {'get_locale': get_locale}

    return app

if __name__ == '__main__':
    clean_temp_files("routes", [".json"])
    app = create_app()
    app.run(host='localhost', port=3000, debug=True)
