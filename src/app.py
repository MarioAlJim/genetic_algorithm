"""This file is for executing the app"""
import os
import logging
import tempfile
import threading
import time
from dotenv import load_dotenv

from flask import Flask, redirect, url_for, request, session, flash
from flask_babel import Babel, gettext

from routes.about_routes import about_blueprint
from routes.playground_routes import playground_blueprint

load_dotenv()


def start_temp_cleanup(directory, interval=600, max_age=3600, logger=None):
    """Start a background thread to clean old files from a directory.

    Args:
        directory (str): Path to the temp directory.
        interval (int): Time between cleanups in seconds (default 10 min).
        max_age (int): Max file age in seconds (default 1 hour).
        logger (Logger): Optional logger to use instead of print.
    """
    if logger is None:
        logger = logging.getLogger("TempCleaner")

    logger.info("Cleaner thread started for directory: %s", directory)

    def cleanup_loop():
        while True:
            now = time.time()
            for filename in os.listdir(directory):
                path = os.path.join(directory, filename)
                try:
                    if os.path.isfile(path) and (now - os.path.getmtime(path)) > max_age:
                        os.remove(path)
                        logger.info(f"[TempCleaner] Removed old file: {path}")
                except Exception as e:
                    logger.warning(f"[TempCleaner] Error deleting {path}: {e}")
            time.sleep(interval)

    thread = threading.Thread(target=cleanup_loop, daemon=True)
    thread.start()

def get_locale():
    """Get the locale from the session or request arguments"""
    if request.args.get("lang"):
        session['lang'] = request.args.get("lang")
    return session.get("lang", "en")

def create_app() -> Flask:
    """Create and set up the app"""
    new_app = Flask(__name__)
    new_app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    new_app.config['BABEL_DEFAULT_LOCALE'] = os.getenv('BABEL_DEFAULT_LOCALE')
    new_app.config['BABEL_TRANSLATION_DIRECTORIES'] = './translations'
    new_app.register_blueprint(about_blueprint)
    new_app.register_blueprint(playground_blueprint, url_prefix='/playground')
    babel_app = Babel(new_app, locale_selector=get_locale)

    TEMP_DIR = os.path.join(tempfile.gettempdir(), "temp_reports")
    os.makedirs(TEMP_DIR, exist_ok=True)
    new_app.config['TEMP_DIR'] = TEMP_DIR

    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    start_temp_cleanup(TEMP_DIR, interval=600, max_age=1800, logger=logger)

    @new_app.route('/')
    def home():
        """Set the home page"""
        return redirect(url_for('playground_blueprint.show_playground'))

    @new_app.route('/setlang')
    def set_lang():
        """Set the language based on the request argument"""
        lang = request.args.get('lang')
        session['lang'] = lang
        return redirect(request.referrer)

    @new_app.context_processor
    def inject_locale():
        """This makes the function available directly, allowing you to call it in the template"""
        return {'get_locale': get_locale}

    @new_app.errorhandler(404)
    def page_not_found(e):
        """Handle 404 errors"""
        return redirect(url_for('home'))

    @new_app.errorhandler(Exception)
    def handle_exception(error):
        """Handle uncaught exceptions globally."""
        logger.exception("Unhandled exception caught: %s", error)
        flash(
            gettext("An unexpected error occurred. Please try again later."),
            category="error"
        )
        return redirect(url_for('home'))

    return new_app

if __name__ == '__main__':
    app = create_app()
    app.run(host='localhost', port=3000, debug=True)
