"""Playground routes"""
from flask import Blueprint, jsonify
from flask import render_template, request

from src.templates.config_forms.problem_algorithm_form import ProblemAlgorithmForm
from src.templates.config_forms.ga_configurations_form import GAConfigurationsForm
from src.controllers.playground_controller import PlaygroundController

playground_blueprint = Blueprint('playground_blueprint', __name__, template_folder='templates')

@playground_blueprint.route('/ga', methods=['GET'])
def show_ga_playground():
    """Render genetic algorithm playground"""
    problemAlgorithmForm = ProblemAlgorithmForm()
    configAlgorithmForm = GAConfigurationsForm()

    if problemAlgorithmForm.validate_on_submit():
        selected_problem = problemAlgorithmForm.problem.data #para funciones futuras

    return render_template("playground_ga.html", initialConfig=problemAlgorithmForm, gaConfigForm=configAlgorithmForm)


@playground_blueprint.route('/ga/execute', methods=['POST'])
def execute_ga_algorithm():
    """Execute the genetic algorithm with the given parameters"""
    data = request.json  # Obtenido desde fetch()

    # Obtener los datos del formulario
    population_size = int(data.get("population_size", 10))
    generations = int(data.get("generations", 10))
    selection_type = data.get("selection_type")
    selection_rate = float(data.get("selection_rate", 0.5))
    crossover_type = data.get("crossover_type")
    mutation_type = data.get("mutation_type")
    mutation_rate = float(data.get("mutation_rate", 0.3))

    print ("Datos recibidos:", data)

    playgroundController = PlaygroundController()
    conf = {
        "population_size": population_size,
        "generations": generations,
        "selection_type": selection_type,
        "selection_rate": selection_rate,
        "crossover_type": crossover_type,
        "mutation_type": mutation_type,
        "mutation_rate": mutation_rate
    }
    playgroundController.set_algorithm_parameters(conf)

    controller = PlaygroundController()
    controller.set_algorithm_parameters(conf)
    config, exec_data = controller.start_execution()

    generated_tests = exec_data["Evaluated population"]
    coverage = controller.evaluate_coverage(generated_tests)

    result = {
        "config": config,
        "exec_data": exec_data,
        "coverage_evaluation": coverage
    }

    return jsonify(result)



