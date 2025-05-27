"""Controller for the playground"""
import base64
import io
import json
import os
import pdfkit
from flask import render_template, Flask
from flask_babel import gettext
from matplotlib import pyplot as plt
from pandas import DataFrame
from src.models.algorithm import Algorithm
from src.models.ga.genetic_algorithm import GeneticAlgorithm

class PlaygroundController:
    """Controller for the playground"""

    def __init__(self):
        """Initialize the controller"""
        self.algorithm = Algorithm()

    def set_algorithm_parameters(self, config: dict) -> None:
        """Set the algorithm parameters"""
        algorithm = config.get("algorithm")
        if algorithm == "ga":
            self.algorithm = GeneticAlgorithm()
            self.algorithm.pop_size = config.get("population_size")
            self.algorithm.num_generations = config.get("generations")
            self.algorithm.selection_rate = config.get("selection_rate")
            self.algorithm.selection_type = config.get("selection_type")
            self.algorithm.crossover_type = config.get("crossover_type")
            self.algorithm.mutation_rate = config.get("mutation_rate")
            self.algorithm.mutation_type = config.get("mutation_type")
            self.algorithm.expected_solution = config.get("expected_solution")
            self.algorithm.elite_pop_rate = config.get("elite_pop_rate")

    def start_execution(self, exec_id: str) -> list:
        """Execute the experiment"""
        config, exec_data = self.algorithm.execute()
        content = self.generate_execution_report(config, exec_data)
        with open(f"routes/{exec_id}.json", "w", encoding='utf-8') as file:
            file.truncate(0)
            json.dump(content, file)
        return content

    def _generate_tables(self, config: dict, exec_data: dict) -> tuple:
        """Generate the tables for the report"""
        config = DataFrame(config)
        exec_data = DataFrame(exec_data)

        if isinstance(self.algorithm, GeneticAlgorithm):
            config = config.rename(columns={
                "Evaluation type": gettext("Evaluation type"),
                "Algorithm": gettext("Algorithm"),
                "Generations": gettext("Generations"),
                "Population size": gettext("Population size"),
                "Chromosome length": gettext("Chromosome length"),
                "Gen type": gettext("Gen type"),
                "Selection type": gettext("Selection type"),
                "Selection rate": gettext("Selection rate"),
                "Crossover type": gettext("Crossover type"),
                "Mutation type": gettext("Mutation type"),
                "Mutation rate": gettext("Mutation rate"),
                "Elite population rate": gettext("Elite population rate"),
            })
            exec_data = exec_data.rename(columns={
                "Generation": gettext("Generation"),
                "Initial population": gettext("Initial population"),
                "Selected population": gettext("Selected population"),
                "Crossover population": gettext("Crossover population"),
                "Mutated population": gettext("Mutated population"),
                "Evaluated population": gettext("Evaluated population"),
            })

        return config, exec_data

    def _get_relevant_fitness_values(self, evaluated_pop: dict) -> tuple:
        """Get the relevant fitness values for the graphic"""
        avg_fitness = []
        best_fitness = []

        for generation in evaluated_pop:
            fitness_scores = []
            for _, fitness in generation:
                fitness_scores.append(fitness)

            avg_fitness.append(sum(fitness_scores) / len(fitness_scores))
            best_fitness.append(max(fitness_scores))

        return avg_fitness, best_fitness

    def generate_execution_report(self, config: dict, exec_data: dict) -> list:
        """Generate the execution report"""
        df_config, df_exec_data = self._generate_tables(config, exec_data)
        config_html = df_config.transpose().to_html(header=False)
        exec_data_html = df_exec_data.to_html(index=False, justify="center")

        # Generate the graphic
        num_generations = df_exec_data["Generation"]
        data_generations = df_exec_data["Evaluated population"]
        avg_fitness, best_fitness = self._get_relevant_fitness_values(data_generations)
        plt.plot(
            num_generations,
            avg_fitness,
            marker='o',
            linestyle='-',
            label=gettext('Average score'),
            color='blue'
        )
        plt.plot(
            num_generations,
            best_fitness,
            marker='o',
            linestyle='-',
            label=gettext('Best score'),
            color='green'
        )
        plt.yticks(best_fitness + avg_fitness)
        plt.xticks(num_generations)
        plt.xlabel(gettext("Generation"))
        plt.ylabel(gettext("Fitness score"))
        plt.legend()
        plt.grid(True)

        # Save the graphic to a buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        graphic = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close()

        return [{
            "config_html": config_html,
            "exec_data_html": exec_data_html,
            "graphic": graphic
        }]

    @staticmethod
    def download_report(exec_id: str) -> bytes:
        """Create the file to download"""
        with open(f"routes/{exec_id}.json", "r", encoding='utf-8') as f:
            result_report = json.load(f)

        html_to_pdf = os.environ['wkhtmltopdf']
        pdfkit_conf = pdfkit.configuration(wkhtmltopdf=html_to_pdf)
        report = pdfkit.from_string(
            input=render_template(
                template_name_or_list="report.html",
                content=result_report
            ),
            configuration=pdfkit_conf,
        )
        os.remove(f"routes/{exec_id}.json")
        return report
