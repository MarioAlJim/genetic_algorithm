"""Playground routes"""
import io
import uuid

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
    problem_algorithm_form = ProblemAlgorithmForm()

    if problem_algorithm_form.validate_on_submit():
        selected_problem = problem_algorithm_form.problem.data
        selected_algorithm = problem_algorithm_form.algorithm.data

        if selected_algorithm == "algorithm_ga":
            return redirect(url_for("playground_blueprint.show_ga_playground"))

    return render_template("playground.html", initial_config=problem_algorithm_form)

@playground_blueprint.route('/ga', methods=['GET', 'POST'])
def show_ga_playground():
    """Render genetic algorithm playground"""
    problem_algorithm_form = ProblemAlgorithmForm()
    ga_config_form = GAConfigurationsForm()
    if not "exec_id" in session:
        exec_id = uuid.uuid4()
        session["exec_id"] = exec_id
    if ga_config_form.validate_on_submit():
        playground_controller = PlaygroundController()
        conf = {
            "population_size": int(ga_config_form.population_size.data),
            "generations": int(ga_config_form.generations.data),
            "selection_type": ga_config_form.selection_type.data,
            "selection_rate": float(ga_config_form.selection_rate.data),
            "crossover_type": ga_config_form.crossover_type.data,
            "mutation_type": ga_config_form.mutation_type.data,
            "mutation_rate": float(ga_config_form.mutation_rate.data),
            "elitism_rate": float(ga_config_form.elitism_rate.data)
        }
        playground_controller.set_algorithm_parameters(conf)
        exec_result = playground_controller.start_execution(session["exec_id"])
        if exec_result is not None:
            ga_config_form.population_size.data = ga_config_form.population_size.data
            ga_config_form.generations.data = ga_config_form.generations.data
            ga_config_form.selection_type.data = ga_config_form.selection_type.data
            ga_config_form.selection_rate.data = ga_config_form.selection_rate.data
            ga_config_form.crossover_type.data = ga_config_form.crossover_type.data
            ga_config_form.mutation_type.data = ga_config_form.mutation_type.data
            ga_config_form.mutation_rate.data = ga_config_form.mutation_rate.data
            ga_config_form.elitism_rate.data = ga_config_form.elitism_rate.data

            return render_template("playground.html",  initial_config=problem_algorithm_form, config_form="ga_form", ga_config_form=ga_config_form, content=exec_result, allow_download=True)
        else:
            return redirect(url_for("playground_blueprint.show_ga_playground"))
    return render_template("playground.html", initial_config=problem_algorithm_form, config_form="ga_form", ga_config_form=ga_config_form)


@playground_blueprint.route('/download')
def download_report():
    """Download the report"""
    exec_id = session.get("exec_id")
    playground_controller = PlaygroundController()
    report = io.BytesIO(playground_controller.download_report(exec_id))

    return send_file(report, as_attachment=True, download_name="report.html", mimetype="application/pdf")



