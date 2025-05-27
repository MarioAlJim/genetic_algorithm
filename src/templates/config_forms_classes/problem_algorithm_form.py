from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired

class ProblemAlgorithmForm(FlaskForm):
    problem = SelectField(
            _("Problem"),
            choices=[('problem_triangles', _('Triangle classification'))],
            validators=[DataRequired()],
            id="problem_field"
        )

    algorithm = SelectField(
            _("Algorithm"),
            choices=[('algorithm_ga', _('Genetic Algorithm'))],
            validators=[DataRequired()],
            id="algorithm_field"
        )

    initial_config_button = SubmitField(
            _("Apply"),
            id="initial_config_button"
        )
