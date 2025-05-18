from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired

class ProblemAlgorithmForm(FlaskForm):
    problem = SelectField("Problema", choices=[
        ('problem_triangles', 'Problema de clasificación de triángulos'),
    ], validators=[DataRequired()])

    algorithm = SelectField("Algoritmo", choices=[
        ('algorithm_ga', 'Algoritmo Genético'),
    ], validators=[DataRequired()])
    execute_button = SubmitField("Aplicar")
