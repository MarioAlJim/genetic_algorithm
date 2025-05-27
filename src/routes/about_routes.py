"""About routes"""
from flask import Blueprint
from flask import render_template
from flask_babel import get_locale

about_blueprint = Blueprint('about_blueprint', __name__, template_folder='templates')

@about_blueprint.route('/about', methods=['GET', 'POST'])
def show_about():
    """Render about template"""
    return render_template(
        'about.html'
    )
