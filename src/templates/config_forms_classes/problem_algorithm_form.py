"""File containing the ProblemAlgorithmForm class for selecting the problem and algorithm."""
from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired

class ProblemAlgorithmForm(FlaskForm):
    """Form for selecting the problem and algorithm"""
    problem = SelectField(
        id="problem_field",
        label=lazy_gettext('System Under Testing'),
        choices=[
            ('triangles-problem', lazy_gettext('Triangle Classification')),
        ],
        validators=[DataRequired()]
    )

    algorithm = SelectField(
        id="algorithm_field",
        label=lazy_gettext("Algorithm"),
        choices=[
            ('ga', lazy_gettext('Genetic Algorithm')),
        ],
        validators=[DataRequired()]
    )

    apply_button = SubmitField(
        id="initial_config_button",
        label=lazy_gettext('Apply')
    )
