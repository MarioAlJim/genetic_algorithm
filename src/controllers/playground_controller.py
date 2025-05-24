"""Controller for the playground"""
import base64
import io
import json
import os
import pdfkit

from flask import render_template
from flask_babel import lazy_gettext as _, force_locale
from matplotlib import pyplot as plt
from pandas import DataFrame, Series

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

    def generate_execution_report(self, config, exec_data) -> list:
        """Generate the execution report"""
        config = DataFrame(config)
        exec_data = DataFrame(exec_data)
        config_html = config.transpose().to_html(header=False)
        exec_data_html = exec_data.to_html(index=False, justify="center")
        num_generations = exec_data[_("Generation")]
        data_generations = exec_data[_("Evaluated population")]

        graphics = self.generate_graphics(num_generations, data_generations)

        result_report = [{ 'config_html': config_html, 'exec_data_html': exec_data_html, 'plot_grap': graphics[0], 'box_graph': graphics[1] }]
        return result_report

    @staticmethod
    def generate_graphics(num_generations: list, data_generations: Series) -> list:
        """Generate report graphs"""
        graphics = []
        fitness = []

        for generation in data_generations:
            fitness.append([chromo_fitness[1] for chromo_fitness in generation])
        average_fitness_per_generation = [round(sum(pop) / len(pop), 2) for pop in fitness]
        best_fitness_per_generation = [max(pop) for pop in fitness]

        # === First graph: Fitness ===
        plt.figure()
        plt.plot(num_generations, best_fitness_per_generation,
                 marker="o", linestyle="-", color="blue", label=_("Best fitness per generation"))
        plt.plot(num_generations, average_fitness_per_generation,
                 marker='x', linestyle='-', color='red', label=_("Average fitness per generation"))
        plt.axhline(y=100, linestyle='--', color='gray', label=_("Max fitness value (100)"))
        for i in range(len(num_generations)):
            plt.text(num_generations[i], best_fitness_per_generation[i] + 2,
                     str(best_fitness_per_generation[i]), ha='center', color='black')
            plt.text(num_generations[i], average_fitness_per_generation[i] + 2,
                     str(average_fitness_per_generation[i]), ha='center', color='black')
        plt.title(_('Fitness per generation'))
        plt.xlabel(_('Generation'))
        plt.ylabel(_('Fitness'))
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        buf1 = io.BytesIO()
        plt.savefig(buf1, format='png')
        buf1.seek(0)
        graphics.append(base64.b64encode(buf1.read()).decode('utf-8'))
        buf1.close()
        plt.close()

        # === First graph: Fitness ===
        plt.figure()
        plt.boxplot(fitness, labels=[str(gen) for gen in num_generations], patch_artist=True)
        plt.title(_('Fitness distribution per generation'))
        plt.xlabel(_('Generation'))
        plt.ylabel(_('Fitness'))
        plt.grid(True)
        plt.tight_layout()

        buf2 = io.BytesIO()
        plt.savefig(buf2, format='png')
        buf2.seek(0)
        graphics.append(base64.b64encode(buf2.read()).decode('utf-8'))
        buf2.close()
        plt.close()

        return graphics

    @staticmethod
    def download_report(exec_id: str, lang: str) -> bytes:
        """Create the file to download"""
        with open(f"routes/{exec_id}.json", "r") as f:
            result_report = json.load(f)

        with force_locale(lang):  # o 'en', 'fr', etc.
            rendered_html = render_template(
                "download_format.html",
                content=result_report,
                current_lang=lang
            )

        html_to_pdf = os.environ['wkhtmltopdf']
        pdfkit_conf = pdfkit.configuration(wkhtmltopdf=html_to_pdf)
        report = pdfkit.from_string(
            input=rendered_html,
            configuration=pdfkit_conf,
        )
        os.remove(f'routes/{exec_id}.json')
        return report
