"""Playground routes"""
from io import BytesIO
import uuid
from flask import Blueprint, render_template, session, send_file, url_for, flash, redirect
from flask_babel import get_locale, gettext
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
    exec_result = {}
    allow_download = False
    playground_controller = PlaygroundController()

    page = request.args.get("page", default=None, type=int)

    if request.args.get("page") is not None:
        exec_result = playground_controller.get_paginated_results(session["exec_id"], page)
        allow_download = True


    if ga_form.validate_on_submit():
        if os.path.exists(f"routes/{session["exec_id"]}.json"):
            os.remove(f"routes/{session["exec_id"]}.json")

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

@playground_blueprint.route('/download', methods=['GET'])
def download_report():
    """Download the report"""
    controller = PlaygroundController()
    try:
        report = BytesIO(controller.download_report(
            session["exec_id"],
            str(get_locale())
        ))
        return send_file(
            report,
            as_attachment=True,
            download_name=gettext("Execution results") + ".pdf",
            mimetype="application/pdf"
        )
    except FileNotFoundError:
        flash(
            gettext("No report available for download."),
            category="error"
        )
        return redirect(
            url_for(
                endpoint="playground_blueprint.show_playground",
                page=1
            )
        )
