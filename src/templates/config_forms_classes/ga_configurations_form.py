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
            NumberRange(min=1, max=50)
        ],
        default=5
    )

    generations = IntegerField(
        id="generations_field",
        label=lazy_gettext('Number of generations'),
        validators=[
            DataRequired(),
            NumberRange(min=1, max=100)
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
        choices=[(round(i / 10, 1), f"{i * 10}%") for i in range(1, 11)],
        validators=[DataRequired()],
        default=0.5
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
        choices=[(round(i / 10, 1), f"{i * 10}%") for i in range(0, 11)],
        validators=[DataRequired()],
        default=0.5
    )

    elite_pop_rate = SelectField(
        id="elite_pop_rate_field",
        label=lazy_gettext('Elite population rate'),
        choices=[(round(i / 10, 1), f"{i * 10}%") for i in range(0, 11)],
        validators=[DataRequired()],
        default=0.5
    )

    execute_algorithm_button = SubmitField(
        id="execute_algorithm_button",
        label=lazy_gettext('Execute')
    )

    @property
    def modals(self):
        return [
            {
                "modal_id": "modal_population-size",
                "modal_title": lazy_gettext("Population size"),
                "help_items": [
                    {"title": lazy_gettext("Definition"),
                     "description": lazy_gettext("Number of individuals in each generation.")},
                    {"title": lazy_gettext("Impact"), "description": lazy_gettext(
                        "A larger size can improve diversity but increases computational cost.")}
                ]
            },
            {
                "modal_id": "modal_generations",
                "modal_title": lazy_gettext("Number of generations"),
                "help_items": [
                    {"title": lazy_gettext("Definition"),
                     "description": lazy_gettext("Total number of iterations for the genetic algorithm.")},
                    {"title": lazy_gettext("Impact"),
                     "description": lazy_gettext("More generations may improve results but increase execution time.")}
                ]
            },
            {
                "modal_id": "modal_selection_type",
                "modal_title": lazy_gettext("Selection type"),
                "help_items": [
                    {"title": lazy_gettext("Definition"),
                     "description": lazy_gettext("Method used to select individuals for reproduction.")},
                    {"title": lazy_gettext("Impact"),
                     "description": lazy_gettext("Affects convergence speed and genetic diversity.")},
                    {"title": lazy_gettext("Random"), "description": lazy_gettext(
                        "Selects individuals randomly, promoting diversity but possibly reducing convergence speed.")},
                    {"title": lazy_gettext("Steady state"), "description": lazy_gettext(
                        "Maintains a stable population by replacing only a few individuals at a time. Helps preserve good solutions.")}
                ]
            },
            {
                "modal_id": "modal_selection_rate",
                "modal_title": lazy_gettext("Selection rate"),
                "help_items": [
                    {"title": lazy_gettext("Definition"),
                     "description": lazy_gettext("Proportion of population selected for reproduction.")},
                    {"title": lazy_gettext("Impact"), "description": lazy_gettext(
                        "Higher rates increase selective pressure, but too high may cause premature convergence.")}
                ]
            },
            {
                "modal_id": "modal_crossover_type",
                "modal_title": lazy_gettext("Crossover type"),
                "help_items": [
                    {"title": lazy_gettext("Definition"),
                     "description": lazy_gettext("Method used to combine two parents to produce offspring.")},
                    {"title": lazy_gettext("Impact"),
                     "description": lazy_gettext("Determines how genetic material is mixed, influencing diversity.")},
                    {"title": lazy_gettext("One point"), "description": lazy_gettext(
                        "Swaps genetic material at a single crossover point. Simple and fast.")},
                    {"title": lazy_gettext("Two point"), "description": lazy_gettext(
                        "Swaps two segments of genes between parents. Allows more variability.")},
                    {"title": lazy_gettext("Uniform"), "description": lazy_gettext(
                        "Mixes genes randomly from both parents at each gene position. Maximizes diversity.")}
                ]
            },
            {
                "modal_id": "modal_mutation_type",
                "modal_title": lazy_gettext("Mutation type"),
                "help_items": [
                    {"title": lazy_gettext("Definition"),
                     "description": lazy_gettext("Method used to introduce random variations in individuals.")},
                    {"title": lazy_gettext("Impact"),
                     "description": lazy_gettext("Prevents premature convergence by exploring new solutions.")},
                    {"title": lazy_gettext("Random resetting"), "description": lazy_gettext(
                        "Changes the value of one or more genes to a random value within its domain.")}
                ]
            },
            {
                "modal_id": "modal_mutation_rate",
                "modal_title": lazy_gettext("Mutation rate"),
                "help_items": [
                    {"title": lazy_gettext("Definition"),
                     "description": lazy_gettext("Probability of applying mutation to individuals.")},
                    {"title": lazy_gettext("Impact"),
                     "description": lazy_gettext("Higher rates explore more, but can destabilize the population.")}
                ]
            },
            {
                "modal_id": "modal_elite_pop_rate",
                "modal_title": lazy_gettext("Elite population rate"),
                "help_items": [
                    {"title": lazy_gettext("Definition"), "description": lazy_gettext(
                        "Proportion of the best individuals preserved to the next generation.")},
                    {"title": lazy_gettext("Impact"),
                     "description": lazy_gettext("Helps retain strong solutions but too high may reduce diversity.")}
                ]
            }
        ]
