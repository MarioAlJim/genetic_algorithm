from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, NumberRange

class GAConfigurationsForm(FlaskForm):
    population_size = IntegerField(
        _("Population size"),
        validators=[DataRequired(), NumberRange(min=1, max=10)],
        default=5,
        id="population_size_field"
    )
    generations = IntegerField(
        _("Number of generations"),
        validators=[DataRequired(), NumberRange(min=1, max=10)],
        default=5,
        id="generations_field"
    )
    selection_type = SelectField(
        _("Selection type"),
        choices=[('random', _('Random')), ('steady-state', _('Steady state'))],
        validators=[DataRequired()],
        id="selection_type_field"
    )
    selection_rate = SelectField(
        _('Selection rate'),
        choices=[(str(round(i / 10, 1)), f"{i * 10}%") for i in range(1, 11)],
        validators=[DataRequired()],
        default="0.5",
        id="selection_rate_field"
    )
    crossover_type = SelectField(
        _('Crossover type'),
        choices=[('one-point', _('One point')), ('two-point', _('Two points')), ('uniform', _('Uniform'))],
        validators=[DataRequired()],
        id="crossover_type_field"
    )
    mutation_type = SelectField(
        _('Mutation type'),
        choices=[('random-resetting', _('Random resetting')),],
        validators=[DataRequired()],
        id="mutation_type_field"
    )
    mutation_rate = SelectField(
        _('Mutation rate'),
        choices=[(str(round(i / 10, 1)), f"{i * 10}%") for i in range(0, 11)],
        validators=[DataRequired()],
        default="0.5",
        id="mutation_rate_field"
    )
    elitism_rate = SelectField(
        _('Elitism rate'),
        choices=[(str(round(i / 10, 1)), f"{i * 10}%") for i in range(0, 11)],
        validators=[DataRequired()],
        default="0.5",
        id="elitism_rate_field"
    )
    execute_algorithm_button = SubmitField(
        _('Execute algorithm'),
        id="execute_algorithm_button"
    )
