"""Playground routes"""
from io import BytesIO
import uuid
from flask import Blueprint, render_template, session, send_file, url_for, flash, redirect
from flask_babel import get_locale, gettext
from src.controllers.playground_controller import PlaygroundController
from src.templates.config_forms_classes.problem_algorithm_form import ProblemAlgorithmForm
from src.templates.config_forms_classes.ga_configurations_form import GAConfigurationsForm

playground_blueprint = Blueprint('playground_blueprint', __name__, template_folder='templates')

def init_session() -> None:
    """Initialize session variables if not already set"""
    if "exec_id" not in session:
        session["exec_id"] = str(uuid.uuid4())
    if "context" not in session:
        session["context"] = {
            "problem": "triangle-classification",
            "algorithm": "ga"
        }
    if "param" not in session:
        session["param"] = {}
    if "allow_download" not in session:
        session["allow_download"] = False

def init_forms(context_form, config_form) -> tuple:
    """Initialize forms values from session"""
    algorithm = session["context"]["algorithm"]

    context_form.problem.data = session["context"]["problem"]
    context_form.algorithm.data = algorithm
    if algorithm == "ga":
        config_form = GAConfigurationsForm(data=session["param"])

    return context_form, config_form

@playground_blueprint.route('/', defaults={'page': 1}, methods=['GET', 'POST'])
@playground_blueprint.route('/<int:page>', methods=['GET', 'POST'])
def show_playground(page: int):
    """Render playground
    Get and post methods for the playground
    """
    controller = PlaygroundController()
    context_form = ProblemAlgorithmForm()
    config_form = None
    config_form_template = None

    init_session()

    if context_form.validate_on_submit():
        # Update session parameters
        session["context"] = {
            "problem": context_form.problem.data,
            "algorithm": context_form.algorithm.data
        }
        session["allow_download"] = False

    # Initialize the algorithm form based on the selected algorithm
    if session["context"]["algorithm"] == "ga":
        config_form = GAConfigurationsForm()
        config_form_template = "ga_form_template.html"

    if config_form and config_form.validate_on_submit():
        controller.set_algorithm_parameters({
            "algorithm": session["context"]["algorithm"],
            "sut": session["context"]["problem"],
            "param": config_form.data
        })
        controller.start_execution(session["exec_id"])

        # Update session parameters and reset page
        session["param"] = config_form.data
        session["allow_download"] = True
        page = 1

    try:
        exec_result = controller.update_page_data(
            session["exec_id"],
            page
        )
    except FileNotFoundError:
        exec_result = {}
        session["allow_download"] = False

    context_form, config_form = init_forms(context_form,config_form)

    return render_template(
        template_name_or_list="playground.html",
        context=context_form,
        config_form=config_form,
        config_form_template=config_form_template,
        content=exec_result,
        allow_download=session["allow_download"],
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
