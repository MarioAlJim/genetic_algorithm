"""Controller for the playground"""
import base64
import json
from io import BytesIO, StringIO
import os
from flask import render_template
from flask_babel import gettext
from matplotlib import pyplot as plt
from pandas import DataFrame, read_html
import pdfkit
from src.models.algorithm import Algorithm
from src.models.ga.genetic_algorithm import GeneticAlgorithm

class PlaygroundController:
    """Controller for the playground"""

    def __init__(self):
        """Initialize the controller"""
        self.algorithm = Algorithm()

    def set_algorithm_parameters(self, config: dict) -> None:
        """Set the algorithm parameters"""
        algorithm = config["algorithm"]
        if algorithm == "ga":
            self.algorithm = GeneticAlgorithm()
            self.algorithm.evaluation = config["sut"]
            self.algorithm.pop_size = config["param"]["population_size"]
            self.algorithm.num_generations = config["param"]["generations"]
            self.algorithm.selection_rate = float(config["param"]["selection_rate"])
            self.algorithm.selection_type = config["param"]["selection_type"]
            self.algorithm.crossover_type = config["param"]["crossover_type"]
            self.algorithm.mutation_rate = float(config["param"]["mutation_rate"])
            self.algorithm.mutation_type = config["param"]["mutation_type"]
            self.algorithm.elite_pop_rate = float(config["param"]["elite_pop_rate"])

    def start_execution(self, exec_id: str) -> dict:
        """Execute the experiment"""
        config, exec_data = self.algorithm.execute()
        content = self.generate_execution_report(config, exec_data, exec_id)

        return content

    def _get_fitness_values(self, evaluated_pop: dict) -> tuple:
        """Get the relevant fitness values for the graphic"""
        avg_fitness = []
        best_fitness = []
        fitness_by_generation = []

        for generation in evaluated_pop:
            fitness_scores = []
            for _, fitness in generation:
                fitness_scores.append(fitness)

            avg_fitness.append(round(sum(fitness_scores) / len(fitness_scores), 2))
            best_fitness.append(max(fitness_scores))
            fitness_by_generation.append(fitness_scores)

        return avg_fitness, best_fitness, fitness_by_generation

    def _generate_graphics(self, exec_data: dict) -> tuple:
        """Generate the graphics for the report"""
        num_generations = exec_data[gettext("Generation")]
        eval_pop = exec_data[gettext("Evaluated population")]
        avg_fitness, best_fitness, fitness_by_generation = self._get_fitness_values(eval_pop)

        # Generate the graphic 1
        plt.axhline(
            label=gettext('Max FS'),
            y=100,
            linestyle='--',
            color='gray'
        )
        plt.plot(
            num_generations,
            best_fitness,
            label=gettext('Best FS'),
            marker='o',
            linestyle='--',
            color='green'
        )
        plt.plot(
            num_generations,
            avg_fitness,
            label=gettext('Average FS'),
            marker='x',
            linestyle='-',
            color='blue'
        )
        for i, generation in enumerate(num_generations):
            plt.text(
                x=generation,
                y=best_fitness[i] + 1,
                s=str(best_fitness[i]),
                ha='center',
                color='black'
            )
            plt.text(
                x=generation,
                y=avg_fitness[i] + 1,
                s=str(avg_fitness[i]),
                ha='center',
                color='black'
            )
        plt.xticks(num_generations)
        plt.title(gettext("Fitness score evolution"))
        plt.xlabel(gettext("Generation"))
        plt.ylabel(gettext("Fitness Score (FS)"))
        plt.legend()
        plt.grid(True)

        # Save the graphic 1 to a buffer
        buf1 = BytesIO()
        plt.savefig(buf1, format='png')
        buf1.seek(0)
        graphic1 = base64.b64encode(buf1.read()).decode('utf-8')
        buf1.close()
        plt.close()

        # Generate the graphic 2
        plt.figure()
        generations = [str(generation) for generation in num_generations]
        plt.boxplot(fitness_by_generation, labels=generations, patch_artist=True)
        plt.title(gettext("Fitness distribution per generation"))
        plt.xlabel(gettext("Generation"))
        plt.ylabel(gettext("Fitness"))
        plt.grid(True)
        plt.tight_layout()

        # Save the graphic 2 to a buffer
        buf2 = BytesIO()
        plt.savefig(buf2, format='png')
        buf2.seek(0)
        graphic2 = base64.b64encode(buf2.read()).decode('utf-8')
        buf2.close()
        plt.close()

        return graphic1, graphic2

    def generate_execution_report(self, config: dict, exec_data: dict, exec_id: str) -> dict:
        """Generate the execution report"""
        df_config = DataFrame(config)
        config_html = df_config.transpose().to_html(header=False)
        df_exec_data = DataFrame(exec_data)
        exec_data_html = df_exec_data.to_html(index=False, justify="center")
        graphic1, graphic2 = self._generate_graphics(exec_data)
        test_suite = None
        evaluated_populations = exec_data.get(gettext("Evaluated population"), [])
        if evaluated_populations:
            # Gets the last evaluated population with '[-1]' and the first chromosome with '[0][0]'
            # The first chromosome is the best one because the population is sorted by fitness
            best_chromo = evaluated_populations[-1][0][0]
            it = iter(best_chromo)
            inputs = config.get(gettext("Evaluation inputs"), [1])
            test_suite = enumerate(zip(*[it] * inputs[0]), start=1)

        content = {
            "config_html": config_html,
            "exec_data_html": exec_data_html,
            "plot_graph": graphic1,
            "box_graph": graphic2,
            "test_suite": list(test_suite),
        }

        # Remove previous execution data if exists
        if os.path.exists(f"routes/{'exec_id'}.json"):
            os.remove(f"routes/{'exec_id'}.json")

        #save base data
        with open(f"routes/{exec_id}.json", "w", encoding='utf-8') as file:
            file.truncate(0)
            json.dump(content, file)

        return content

    @staticmethod
    def download_report(exec_id: str, lang: str) -> bytes:
        """Create the file to download"""
        with open(f"routes/{exec_id}.json", "r", encoding='utf-8') as f:
            report = json.load(f)

        rendered_html = render_template(
            "report.html",
            content=report,
            current_lang=lang
        )

        html_to_pdf = os.environ['wkhtmltopdf']
        pdfkit_conf = pdfkit.configuration(wkhtmltopdf=html_to_pdf)
        report = pdfkit.from_string(
            input=rendered_html,
            configuration=pdfkit_conf,
        )

        return report

    def get_paginated_results(self, exec_id: str, page: int) -> dict:
        """Get paginated results for the execution data"""
        with open(f"routes/{exec_id}.json", "r", encoding='utf-8') as f:
            report = json.load(f)
        df_exec_data = read_html(StringIO(report["exec_data_html"]))[0]

        page_size = 10
        total_items = len(df_exec_data)
        total_pages = (total_items + page_size - 1) // page_size
        start_index = (page - 1) * page_size
        end_index = page * page_size
        page_data_html = df_exec_data[start_index:end_index].to_html(index=False, justify="center")

        content = {
            "config_html": report.get("config_html"),
            "exec_data_html": page_data_html,
            "total_pages": total_pages,
            "current_page": page,
            "plot_graph": report.get("plot_graph"),
            "box_graph": report.get("box_graph"),
            "test_suite": report.get("test_suite"),
        }

        return content
