"""Controller for the playground"""
import os
import pdfkit
from flask import render_template_string, Flask

from src.controllers.coverage_evaluator import CoverageEvaluator
from src.models.evaluations.triangle_classification import TriangleClassification
from src.models.ga.genetic_algorithm import GeneticAlgorithm

class PlaygroundController:
    """Controller for the playground"""

    def __init__(self):
        """Initialize the controller"""
        self.genetic_algorithm = GeneticAlgorithm()
        pass

    def start_execution(self):
        """Execute the playground"""
        result = self.genetic_algorithm.execute()
        return result

    def set_algorithm_parameters(self, config: dict) -> None:
        """Set the algorithm parameters"""
        self.genetic_algorithm.pop_size = config.get("population_size")
        self.genetic_algorithm.num_generations = config.get("generations")
        self.genetic_algorithm.selection_rate = config.get("selection_rate")
        self.genetic_algorithm.selection_type = config.get("selection_type")
        self.genetic_algorithm.crossover_type = config.get("crossover_type")
        self.genetic_algorithm.mutation_rate = config.get("mutation_rate")
        self.genetic_algorithm.mutation_type = config.get("mutation_type")
        self.genetic_algorithm.expected_solution = config.get("expected_solution")
        return

    @staticmethod
    def evaluate_coverage(test_data: list) -> list:
        """Evaluate the coverage of the test data"""
        evaluation_result = []
        triangle_classification = TriangleClassification()

        for gen_index, gen in enumerate(test_data):
            inputs = [entry[0] for entry in gen]
            fitness_values = [entry[1] for entry in gen]

            coverage_result = CoverageEvaluator.get_coverage(triangle_classification._classify_triangle, inputs)
            average_fitness_value = sum(fitness_values) / len(fitness_values)

            evaluation_result.append({
                'gen': gen_index,
                'fitness': average_fitness_value,
                'coverage': coverage_result["coverage_percent"],
            })

        return evaluation_result

    def download_report(self, report: dict) -> None:
        """Download the report"""
        pass

    @staticmethod
    def create_report(report_data: tuple) -> bytes:
        """Creates a report from the given data"""
        app = Flask(__name__)
        template_html = """
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <title>Reporte</title>
            </head>
            <body>
                <h1>Reporte de Ejecuciones</h1>
                    {% for item in content %}
                        <h2>Iteración {{ item.iteration }}</h2>
                        <div class="graph-conf">
                            <h3>Configuración</h3>
                            {{ item.config_html|safe }}
                            <h3>Gráfico</h3>
                            <img src="data:image/png;base64,{{ item.graph }}" alt="Gráfico Iteración {{ item.iteration }}">
                        </div>
                            <h3>Datos de Ejecución</h3>
                            {{ item.exec_data_html|safe }}
                        <hr>
                    {% endfor %}
            </body>
            </html>
            """

        with app.app_context():
            rendered_html = render_template_string(template_html, content=report_data[0])

        html_to_pdf = os.environ['wkhtmltopdf']
        pdfkit_conf = pdfkit.configuration(wkhtmltopdf=html_to_pdf)
        report = pdfkit.from_string(
            input=rendered_html,
            configuration=pdfkit_conf,
        )

        os.remove(f'routes/{report_data[1]}.json')
        return report
