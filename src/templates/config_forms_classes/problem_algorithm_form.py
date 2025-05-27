"""File containing the ProblemAlgorithmForm class for selecting the problem and algorithm."""
from flask_babel import gettext
from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired

class ProblemAlgorithmForm(FlaskForm):
    """Form for selecting the problem and algorithm"""
    problem = SelectField(
        label="problem",
        choices=[
            ('triangles-problem', gettext('Triangle Classification')),
        ],
        validators=[DataRequired()]
    )

    algorithm = SelectField(
        label="algorithm",
        choices=[
            ('ga', gettext('Genetic Algorithm')),
        ],
        validators=[DataRequired()]
    )

    apply_button = SubmitField(gettext('Apply'))
