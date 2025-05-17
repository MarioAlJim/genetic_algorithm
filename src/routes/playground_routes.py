"""Playground routes"""
import base64
import io
import json
import os
import uuid
import matplotlib.pyplot as plt

from flask import Blueprint, url_for, render_template_string
from flask import render_template, session, redirect, send_file
from pandas import DataFrame

from src.controllers.playground_controller import PlaygroundController
from src.models.evaluations.triangle_classification import TriangleClassification
from src.templates.config_forms.problem_algorithm_form import ProblemAlgorithmForm
from src.templates.config_forms.ga_configurations_form import GAConfigurationsForm


playground_blueprint = Blueprint('playground_blueprint', __name__, template_folder='templates')

@playground_blueprint.route('/', methods=['GET', 'POST'])
def show_ga_playground():
    """Render genetic algorithm playground
    Get and post methods for the playground
    """
    problemAlgorithmForm = ProblemAlgorithmForm()
    configAlgorithmForm = GAConfigurationsForm()

    """TODO"""
    if problemAlgorithmForm.validate_on_submit():
        selected_problem = problemAlgorithmForm.problem.data
        #validar el problema seleccionado para la aplicacion de la configuracion

    if configAlgorithmForm.validate_on_submit():
        population_size = int(configAlgorithmForm.population_size.data)
        generations = int(configAlgorithmForm.generations.data)
        selection_type = configAlgorithmForm.selection_type.data
        selection_rate = float(configAlgorithmForm.selection_rate.data)
        crossover_type = configAlgorithmForm.crossover_type.data
        mutation_type = configAlgorithmForm.mutation_type.data
        mutation_rate = float(configAlgorithmForm.mutation_rate.data)

        playgroundController = PlaygroundController()
        triangle_classification = TriangleClassification()

        conf = {
            "population_size": population_size,
            "generations": generations,
            "selection_type": selection_type,
            "selection_rate": selection_rate,
            "crossover_type": crossover_type,
            "mutation_type": mutation_type,
            "mutation_rate": mutation_rate,
            "expected_solution": "",
        }
        exec_result = []
        for solution in triangle_classification.expected_solutions:
            conf.update({"expected_solution": solution})
            playgroundController.set_algorithm_parameters(conf)
            config, exec_data = playgroundController.start_execution()
            generated_tests = exec_data["Evaluated population"]
            coverage = playgroundController.evaluate_coverage(generated_tests)

            result = {
                "config": config,
                "exec_data": exec_data,
                "coverage_evaluation": coverage
            }
            exec_result.append(result)

        if not "exec_id" in session:
            exec_id = uuid.uuid4()
            session["exec_id"] = exec_id

        with open(f"routes/{session["exec_id"]}.json", "w") as f:
            json.dump(exec_result, f)

        return redirect(url_for("playground_blueprint.show_results_page"))

    return render_template("playground_ga.html", initialConfig=problemAlgorithmForm, gaConfigForm=configAlgorithmForm)

@playground_blueprint.route('/results', methods=['GET', 'POST'])
def show_results_page():
    """Render genetic algorithm results"""
    exec_id = session.get("exec_id")
    try:
        with open(f"routes/{exec_id}.json", "r") as f:
            exec_result = json.load(f)
    except FileNotFoundError:
        return redirect(url_for("playground_blueprint.show_ga_playground"))

    problemAlgorithmForm = ProblemAlgorithmForm()
    configAlgorithmForm = GAConfigurationsForm()
    content = []

    for index_execution, result in enumerate(exec_result):
        config = DataFrame(result["config"]).transpose()
        exec_data = DataFrame(result["exec_data"])
        coverage_evaluation = result["coverage_evaluation"]

        config_html = config.to_html(
            header=False,
            justify='justify-all',
        )
        exec_data_html = exec_data.to_html(
            index=False,
            justify='justify-all',
        )
        generaciones = [d['gen'] for d in coverage_evaluation]
        fitness = [d['fitness'] for d in coverage_evaluation]
        coverage = [d['coverage'] for d in coverage_evaluation]

        # revisar como se grafica
        fig, ax = plt.subplots()
        ax.plot(generaciones, fitness, marker='o', linestyle='-', label='Fitness')
        ax.plot(generaciones, coverage, marker='s', linestyle='--', label='Coverage')
        ax.set_xlabel("Generación")
        ax.set_ylabel("Valor")
        ax.legend()
        ax.grid()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close(fig)

        content.append({
            'iteration': index_execution + 1,
            'config_html': config_html,
            'exec_data_html': exec_data_html,
            'graph': img_base64
        })

        try:
            os.remove(f"routes/{exec_id}.json")
            with open(f"routes/{exec_id}.json", "w") as f:
                json.dump(content, f)
        except FileNotFoundError:
            pass

    return render_template("playground_ga_results.html", initialConfig=problemAlgorithmForm, gaConfigForm=configAlgorithmForm, content=content)

@playground_blueprint.route('/download')
def download_report():
    """Download the report"""
    exec_id = session.get("exec_id")
    try:
        with open(f"routes/{exec_id}.json", "r") as f:
            content = json.load(f)
    except FileNotFoundError:
        return redirect(url_for("playground_blueprint.show_ga_playground"))

    playground_controller = PlaygroundController()
    report = io.BytesIO(playground_controller.create_report((content, exec_id)))

    return send_file(report, as_attachment=True, download_name="reporte.html", mimetype="application/pdf")



