"""This file is for executing the app"""
import os
from flask import Flask, redirect, url_for, request, session
from flask_babel import Babel
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

def get_locale():
    """Get the locale from the session or request arguments"""
    if request.args.get("lang"):
        session['lang'] = request.args.get("lang")
    return session.get("lang", "en")

def create_app() -> Flask:
    """Create and set up the app"""
    new_app = Flask(__name__)
    new_app.config['SECRET_KEY'] = 'bite'
    new_app.config['BABEL_DEFAULT_LOCALE'] = 'es'
    new_app.config['BABEL_TRANSLATION_DIRECTORIES'] = './translations'
    new_app.register_blueprint(about_blueprint)
    new_app.register_blueprint(playground_blueprint, url_prefix='/playground')
    babel_app = Babel(new_app, locale_selector=get_locale)

    @new_app.route('/')
    def home():
        return redirect(url_for('playground_blueprint.show_playground'))

    @new_app.route('/setlang')
    def set_lang():
        lang = request.args.get('lang')
        session['lang'] = lang
        return redirect(request.referrer)

    @new_app.context_processor
    def inject_locale():
        # This makes the function available directly, allowing you to call it in the template
        return {'get_locale': get_locale}

    return new_app

if __name__ == '__main__':
    clean_temp_files("routes", [".json"])
    app = create_app()
    app.run(host='localhost', port=3000, debug=True)
