from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, DecimalField
from wtforms.validators import DataRequired, NumberRange

class GAConfigurationsForm(FlaskForm):
    population_size = IntegerField("Tamaño de la población", validators=[
        DataRequired(), NumberRange(min=1, max=100)], default=50)
    generations = IntegerField("Número de generaciones", validators=[
        DataRequired(), NumberRange(min=1, max=100)], default=100)
    selection_rate = DecimalField("Probabilidad de selección", validators=[
        DataRequired(), NumberRange(min=0, max=1)], places=2, default=0.50)
    selection_type = SelectField("Tipo de selección", choices=[
        ('random', 'Aleatoria'), ('steady-state', 'Estado constante')], validators=[DataRequired()])
    crossover_type = SelectField("Tipo de cruce", choices=[
        ('one-point', 'Punto único'), ('two-point', 'Dos puntos'), ('uniform', 'Uniforme')], validators=[DataRequired()])
    mutation_type = SelectField("Tipo de mutación", choices=[
        ('random-resetting', 'Restablecimiento aleatorio')], validators=[DataRequired()])
    mutation_rate = DecimalField("Probabilidad de mutación", validators=[
        DataRequired(), NumberRange(min=0, max=1)], places=2, default=0.3)
