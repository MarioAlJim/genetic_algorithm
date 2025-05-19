"""This file is for executing the app"""
# Third party imports
import os
from flask import Flask, redirect, url_for

# Local application imports
from routes.about_routes import about_blueprint
from routes.playground_routes import playground_blueprint

def clean_temp_files(directory, extensions):
    for filename in os.listdir(directory):
        if any(filename.endswith(ext) for ext in extensions):
            file_path = os.path.join(directory, filename)
            try:
                os.remove(file_path)
                print(f"Archivo eliminado: {file_path}")
            except Exception as e:
                print(f"No se pudo eliminar {file_path}: {e}")


def create_app() -> Flask:
    """Create and set up the app"""
    new_app = Flask(__name__)
    new_app.config['SECRET_KEY'] = 'bite'

    new_app.register_blueprint(about_blueprint)
    new_app.register_blueprint(playground_blueprint, url_prefix='/playground')

    @new_app.route('/')
    def home():
        return redirect(url_for('playground_blueprint.show_playground'))

    return new_app

if __name__ == '__main__':
    clean_temp_files("routes", [".json"])
    app = create_app()
    app.run(host='localhost', port=3000, debug=True)
