from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired

class ProblemAlgorithmForm(FlaskForm):
    problem = SelectField(
        "Problema",
        choices=[('problem_triangles', 'Problema de clasificación de triángulos')],
        validators=[DataRequired()],
        id="problem_field"
        )

    algorithm = SelectField(
        "Algoritmo",
        choices=[('algorithm_ga', 'Algoritmo Genético')],
        validators=[DataRequired()],
        id="algorithm_field"
    )
    initial_config_button = SubmitField(
        "Aplicar",
        id="initial_config_button"
    )
