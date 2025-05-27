"""File containing the GAConfigurationsForm class for configuring the genetic algorithm."""
from flask_babel import gettext
from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, NumberRange

class GAConfigurationsForm(FlaskForm):
    """Form for configuring the genetic algorithm"""
    population_size = IntegerField(
        label=gettext('Population size'),
        validators=[
            DataRequired(),
            NumberRange(min=1, max=10)
        ],
        default=5
    )

    generations = IntegerField(
        gettext('Number of generations'),
        validators=[
            DataRequired(),
            NumberRange(min=1, max=10)
        ],
        default=5
    )

    selection_type = SelectField(
        label=gettext('Selection type'),
        choices=[
            ('random', gettext('Random')),
            ('steady-state', gettext('Steady state')),
        ],
        validators=[DataRequired()]
    )

    selection_rate = SelectField(
        label=gettext('Selection rate'),
        choices=[(str(round(i / 10, 1)), f"{i * 10}%") for i in range(1, 11)],
        validators=[DataRequired()],
        default="0.5"
    )

    crossover_type = SelectField(
        label=gettext('Crossover type'),
        choices=[
            ('one-point', gettext('One point')),
            ('two-point', gettext('Two point')),
            ('uniform', gettext('Uniform')),
        ],
        validators=[DataRequired()]
    )

    mutation_type = SelectField(
        label=gettext('Mutation type'),
        choices=[
            ('random-resetting', gettext('Random resetting')),
        ],
        validators=[DataRequired()]
    )

    mutation_rate = SelectField(
        label=gettext('Mutation rate'),
        choices=[(str(round(i / 10, 1)), f"{i * 10}%") for i in range(0, 11)],
        validators=[DataRequired()],
        default="0.5"
    )

    elite_pop_rate = SelectField(
        label=gettext('Elite population rate'),
        choices=[(str(round(i / 10, 1)), f"{i * 10}%") for i in range(0, 11)],
        validators=[DataRequired()],
        default="0.5"
    )

    execute_button = SubmitField(gettext('Execute'))
