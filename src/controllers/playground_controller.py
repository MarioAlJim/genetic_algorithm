"""Controller for the playground"""
import base64
import io
import json
import os
import pdfkit
from flask import render_template_string, Flask, session
from matplotlib import pyplot as plt
from pandas import DataFrame

from src.models.ga.genetic_algorithm import GeneticAlgorithm

class PlaygroundController:
    """Controller for the playground"""

    def __init__(self):
        """Initialize the controller"""
        self.genetic_algorithm = GeneticAlgorithm()
        pass

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
        self.genetic_algorithm.elite_pop_rate = config.get("elitism_rate")
        return

    def start_execution(self, exec_id: str) -> list:
        """Execute the experiment"""
        config, exec_data = self.genetic_algorithm.execute()
        content = self.generate_execution_report(config, exec_data)
        with open(f"routes/{exec_id}.json", "w") as file:
            file.truncate(0)
            json.dump(content, file)
        return content

    @staticmethod
    def generate_execution_report(config, exec_data) -> list:
        """Generate the execution report"""
        config = DataFrame(config)
        exec_data = DataFrame(exec_data)
        config_html = config.transpose().to_html(header=False)
        exec_data_html = exec_data.to_html(index=False, justify="center")
        num_generations = exec_data["Generation"]
        data_generations = exec_data["Evaluated population"]
        fitness = []
        for generation in data_generations:
            fitness.append([chromo_fitness[1] for chromo_fitness in generation])
        average_fitness = [sum(pop) / len(pop) for pop in fitness]

        plt.plot(num_generations, average_fitness, marker='x', linestyle='-', label='Fitness', color='red')
        plt.title("Fitness por generation")
        plt.yticks(average_fitness)
        plt.xticks(num_generations)
        plt.xlabel("Generación")
        plt.ylabel("Fitness")
        plt.legend()
        plt.grid(True)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        graphic = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close()

        result_report = [{ 'config_html': config_html, 'exec_data_html': exec_data_html, 'graphic': graphic}]
        return result_report

    @staticmethod
    def download_report(exec_id: str) -> bytes:
        """Create the file to download"""
        with open(f"routes/{exec_id}.json", "r") as f:
            result_report = json.load(f)

        app = Flask(__name__)
        template_html = """
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <title>Reporte</title>
            </head>
            <body>
                <h2>Resultados de la ejecución</h2>
                <div>
                    {% for item in content %}
                        <div class="initial-form">
                            <h3>Configuración</h3>
                            {{ item.config_html|safe }}
                            <h3>Gráfico</h3>
                            <img src="data:image/png;base64,{{ item.graphic }}" alt="Gráfico Iteración {{ item.iteration }}">
                        </div>
                            <h3>Datos de Ejecución</h3>
                            {{ item.exec_data_html|safe }}
                        <hr>
                    {% endfor %}
                </div>
            </body>
            </html>
            """

        with app.app_context():
            rendered_html = render_template_string(template_html, content=result_report)

        html_to_pdf = os.environ['wkhtmltopdf']
        pdfkit_conf = pdfkit.configuration(wkhtmltopdf=html_to_pdf)
        report = pdfkit.from_string(
            input=rendered_html,
            configuration=pdfkit_conf,
        )
        os.remove(f'routes/{exec_id}.json')
        return report
