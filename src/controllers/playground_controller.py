"""Controller for the playground"""
import ast

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pandas import DataFrame

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
        config = DataFrame(report_data[0])
        exec_data = DataFrame(report_data[1])

        with PdfPages('playground_report.pdf') as pdf:
            fig, ax = plt.subplots()
            ax.axis('off')
            ax.set_title('Execution report')
            table = ax.table(
                cellText=exec_data.values,
                colLabels=exec_data.columns,
                loc='center',
                cellLoc='left',
            )
            table.auto_set_font_size(False)
            table.set_fontsize(3)
            fig.tight_layout()
            plt.show()
            #pdf.savefig()
