from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired

class ProblemAlgorithmForm(FlaskForm):
    problem = SelectField("Problema", choices=[
        ('problem_1', 'Problema de clasificación de triángulos'),
    ], validators=[DataRequired()])

    algorithm = SelectField("Algoritmo", choices=[
        ('algorithm_1', 'Algoritmo Genético'),
    ], validators=[DataRequired()])
