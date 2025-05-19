from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, NumberRange

class GAConfigurationsForm(FlaskForm):
    population_size = IntegerField("Tamaño de la población", validators=[
        DataRequired(), NumberRange(min=1, max=10)], default=5)
    generations = IntegerField("Número de generaciones", validators=[
        DataRequired(), NumberRange(min=1, max=10)], default=5)
    selection_type = SelectField("Tipo de selección", choices=[
        ('random', 'Aleatoria'), ('steady-state', 'Estado uniforme')], validators=[DataRequired()])
    selection_rate = SelectField(
        "Probabilidad de selección",
        choices=[(str(round(i / 10, 1)), f"{i * 10}%") for i in range(1, 11)],
        validators=[DataRequired()],
        default="0.5"
    )
    crossover_type = SelectField("Tipo de cruce", choices=[
        ('one-point', 'Punto único'), ('two-point', 'Dos puntos'), ('uniform', 'Uniforme')], validators=[DataRequired()])
    mutation_type = SelectField("Tipo de mutación", choices=[
        ('random-resetting', 'Restablecimiento aleatorio')], validators=[DataRequired()])
    mutation_rate = SelectField(
        "Probabilidad de mutación",
        choices=[(str(round(i / 10, 1)), f"{i * 10}%") for i in range(0, 11)],
        validators=[DataRequired()],
        default="0.5"
    )
    elitism_rate = SelectField(
        "Probabilidad de elitismo",
        choices=[(str(round(i / 10, 1)), f"{i * 10}%") for i in range(0, 11)],
        validators=[DataRequired()],
        default="0.5"
    )
    execute_button = SubmitField("Ejecutar algoritmo")
