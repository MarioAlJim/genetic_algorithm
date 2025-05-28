"""File containing the GAConfigurationsForm class for configuring the genetic algorithm."""
from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, NumberRange

class GAConfigurationsForm(FlaskForm):
    """Form for configuring the genetic algorithm"""
    population_size = IntegerField(
        id="population_size_field",
        label=lazy_gettext('Population size'),
        validators=[
            DataRequired(),
            NumberRange(min=1, max=10)
        ],
        default=5
    )

    generations = IntegerField(
        id="generations_field",
        label=lazy_gettext('Number of generations'),
        validators=[
            DataRequired(),
            NumberRange(min=1, max=10)
        ],
        default=5
    )

    selection_type = SelectField(
        id="selection_type_field",
        label=lazy_gettext('Selection type'),
        choices=[
            ('random', lazy_gettext('Random')),
            ('steady-state', lazy_gettext('Steady state')),
        ],
        validators=[DataRequired()]
    )

    selection_rate = SelectField(
        id="selection_rate_field",
        label=lazy_gettext('Selection rate'),
        choices=[(str(round(i / 10, 1)), f"{i * 10}%") for i in range(1, 11)],
        validators=[DataRequired()],
        default="0.5"
    )

    crossover_type = SelectField(
        id="crossover_type_field",
        label=lazy_gettext('Crossover type'),
        choices=[
            ('one-point', lazy_gettext('One point')),
            ('two-point', lazy_gettext('Two point')),
            ('uniform', lazy_gettext('Uniform')),
        ],
        validators=[DataRequired()]
    )

    mutation_type = SelectField(
        id="mutation_type_field",
        label=lazy_gettext('Mutation type'),
        choices=[
            ('random-resetting', lazy_gettext('Random resetting')),
        ],
        validators=[DataRequired()]
    )

    mutation_rate = SelectField(
        id="mutation_rate_field",
        label=lazy_gettext('Mutation rate'),
        choices=[(str(round(i / 10, 1)), f"{i * 10}%") for i in range(0, 11)],
        validators=[DataRequired()],
        default="0.5"
    )

    elite_pop_rate = SelectField(
        id="elite_pop_rate_field",
        label=lazy_gettext('Elite population rate'),
        choices=[(str(round(i / 10, 1)), f"{i * 10}%") for i in range(0, 11)],
        validators=[DataRequired()],
        default="0.5"
    )

    execute_algorithm_button = SubmitField(
        id="execute_algorithm_button",
        label=lazy_gettext('Execute')
    )
