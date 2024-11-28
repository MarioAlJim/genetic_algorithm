'''Playground routes'''
from flask import Blueprint
from flask import render_template

playground_blueprint = Blueprint('playground_blueprint', __name__, template_folder='templates')

@playground_blueprint.route('/ga')
def show_ga_playground():
    '''Render genetic algorithm playground'''
    return render_template('playground_ga.html')
