"""Playground routes"""
import io
import os
from flask import Blueprint, url_for
from flask import render_template, session, redirect, send_file
from src.controllers.playground_controller import PlaygroundController
from src.templates.config_forms_classes.problem_algorithm_form import ProblemAlgorithmForm
from src.templates.config_forms_classes.ga_configurations_form import GAConfigurationsForm


playground_blueprint = Blueprint('playground_blueprint', __name__, template_folder='templates')

@playground_blueprint.route('/', methods=['GET', 'POST'])
def show_playground():
    """Render playground
    Get and post methods for the playground
    """
    context_form = ProblemAlgorithmForm()
    if context_form.validate_on_submit():
        selected_problem = context_form.problem.data
        selected_algorithm = context_form.algorithm.data

        if selected_algorithm == "ga":
            return redirect(url_for("playground_blueprint.show_ga_playground"))

    return render_template(
        template_name_or_list="playground.html",
        context=context_form
    )

@playground_blueprint.route('/ga', methods=['GET', 'POST'])
def show_ga_playground():
    """Render genetic algorithm playground"""
    context_form = ProblemAlgorithmForm()
    ga_form = GAConfigurationsForm()
    exec_result = None
    allow_download = False

    if ga_form.validate_on_submit():
        playground_controller = PlaygroundController()
        playground_controller.set_algorithm_parameters({
            "algorithm": "ga",
            "population_size": int(ga_form.population_size.data),
            "generations": int(ga_form.generations.data),
            "selection_type": ga_form.selection_type.data,
            "selection_rate": float(ga_form.selection_rate.data),
            "crossover_type": ga_form.crossover_type.data,
            "mutation_type": ga_form.mutation_type.data,
            "mutation_rate": float(ga_form.mutation_rate.data),
            "elite_pop_rate": float(ga_form.elite_pop_rate.data)
        })

        exec_result = playground_controller.start_execution(session["exec_id"])
        allow_download = True

    return render_template(
        template_name_or_list="playground.html",
        context=context_form,
        config_form="ga_form",
        ga_config_form=ga_form,
        content=exec_result,
        allow_download=allow_download
    )

@playground_blueprint.route('/download')
def download_report():
    """Download the report"""
    exec_id = session.get("exec_id")
    playground_controller = PlaygroundController()
    report = io.BytesIO(playground_controller.download_report(exec_id))

    return send_file(report, as_attachment=True, download_name="report.html", mimetype="application/pdf")
