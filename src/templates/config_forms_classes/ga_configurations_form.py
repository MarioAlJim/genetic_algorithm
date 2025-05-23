from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, NumberRange

class GAConfigurationsForm(FlaskForm):
    population_size = IntegerField(
        "Tamaño de la población",
        validators=[DataRequired(), NumberRange(min=1, max=10)],
        default=5,
        id="population_size_field"
    )
    generations = IntegerField(
        "Número de generaciones",
        validators=[DataRequired(), NumberRange(min=1, max=10)],
        default=5,
        id="generations_field"
    )
    selection_type = SelectField(
        "Tipo de selección",
        choices=[('random', 'Aleatoria'), ('steady-state', 'Estado uniforme')],
        validators=[DataRequired()],
        id="selection_type_field"
    )
    selection_rate = SelectField(
        "Probabilidad de selección",
        choices=[(str(round(i / 10, 1)), f"{i * 10}%") for i in range(1, 11)],
        validators=[DataRequired()],
        default="0.5",
        id="selection_rate_field"
    )
    crossover_type = SelectField(
        "Tipo de cruce",
        choices=[('one-point', 'Punto único'), ('two-point', 'Dos puntos'), ('uniform', 'Uniforme')],
        validators=[DataRequired()],
        id="crossover_type_field"
    )
    mutation_type = SelectField(
        "Tipo de mutación",
        choices=[('random-resetting', 'Restablecimiento aleatorio')],
        validators=[DataRequired()],
        id="mutation_type_field"
    )
    mutation_rate = SelectField(
        "Probabilidad de mutación",
        choices=[(str(round(i / 10, 1)), f"{i * 10}%") for i in range(0, 11)],
        validators=[DataRequired()],
        default="0.5",
        id="mutation_rate_field"
    )
    elitism_rate = SelectField(
        "Probabilidad de elitismo",
        choices=[(str(round(i / 10, 1)), f"{i * 10}%") for i in range(0, 11)],
        validators=[DataRequired()],
        default="0.5",
        id="elitism_rate_field"
    )
    execute_algorithm_button = SubmitField(
        "Ejecutar algoritmo",
        id="execute_algorithm_button"
    )
