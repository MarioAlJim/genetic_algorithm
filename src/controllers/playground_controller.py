"""Controller for the playground"""
import ast
import os

from pandas import DataFrame
import pdfkit

from src.controllers.coverage_evaluator import get_coverage
from src.problems.triangle_classifier import classify_triangle
from src.models.ga.genetic_algorithm import GeneticAlgorithm

class PlaygroundController:
    """Controller for the playground"""

    def __init__(self):
        """Initialize the controller"""
        self.genetic_algorithm = GeneticAlgorithm()
        pass

    def start_execution(self):
        """Execute the playground"""
        self.genetic_algorithm.init_pop()
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
        return

    @staticmethod
    def evaluate_coverage(test_data: list) -> list:
        """Evaluate the coverage of the test data"""
        result = []
        generations = [[ast.literal_eval(line) for line in cadena.split('\n')] for cadena in test_data]

        for gen_index, gen in enumerate(generations):
            inputs = [entry[0] for entry in gen]
            fitness_values = [entry[1] for entry in gen]

            coverage_result = get_coverage(classify_triangle, inputs)
            average_fitness_value = sum(fitness_values) / len(fitness_values)

            result.append({
                'gen': gen_index,
                'fitness': average_fitness_value,
                'coverage': coverage_result["coverage_percent"],
            })

        return result

    def download_report(self, report: dict) -> None:
        """Download the report"""
        pass

    def create_report(self, report_data: tuple) -> None:
        """Creates a report from the given data"""
        config = DataFrame(report_data[0]).transpose()
        exec_data = DataFrame(report_data[1])

        config_html = config.to_html(
            header=False,
            justify='justify-all',
        )
        exec_data_html = exec_data.to_html(
            index=False,
            justify='justify-all',
        )

        html_content = (
            '<!DOCTYPE html>'
            '<html>'
            '<head>'
            '<meta charset="UTF-8">'
            '<title>Report</title>'
            '</head>'
            '<body>'
            '<h1>Execution Report</h1>'
            '<h2>Configuration</h2>'
            f'{config_html}'
            '<h2>Execution Data</h2>'
            f'{exec_data_html}'
            '<h2>Execution Graph</h2>'
            '</body>'
            '</html>'
        )

        wkhtml_to_pdf = os.environ['wkhtmltopdf']
        pdfkit_conf = pdfkit.configuration(wkhtmltopdf=wkhtml_to_pdf)
        pdfkit.from_string(
            input=html_content,
            output_path='playground_report.pdf',
            configuration=pdfkit_conf,
        )
