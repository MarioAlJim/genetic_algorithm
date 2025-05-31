"""Controller for the playground"""
import base64
import io
import json
import os
import pdfkit
from flask import render_template
from flask_babel import force_locale, gettext
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

    def _generate_graphics(self, df_exec_data: DataFrame) -> tuple:
        """Generate the graphics for the report"""
        num_generations = df_exec_data[gettext("Generation")]
        eval_pop = df_exec_data[gettext("Evaluated population")]
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
        buf1 = io.BytesIO()
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
        buf2 = io.BytesIO()
        plt.savefig(buf2, format='png')
        buf2.seek(0)
        graphic2 = base64.b64encode(buf2.read()).decode('utf-8')
        buf2.close()
        plt.close()

        return graphic1, graphic2

    def generate_execution_report(self, config: dict, exec_data: dict, exec_id: str) -> dict:
        """Generate the execution report"""
        df_config = DataFrame(config)
        df_exec_data = DataFrame(exec_data)
        config_html = df_config.transpose().to_html(header=False)

        graphic1, graphic2 = self._generate_graphics(df_exec_data)

        content = {
            "config_html": config_html,
            "exec_data_html": df_exec_data.to_dict(orient='records'),
            "plot_graph": graphic1,
            "box_graph": graphic2
        }

        #save base data
        with open(f"routes/{exec_id}.json", "w", encoding='utf-8') as file:
            file.truncate(0)
            json.dump(content, file)

        #create first page
        page_size = 10
        total_items = len(df_exec_data)
        total_pages = (total_items + page_size - 1) // page_size
        page_number = 1
        start_index = (page_number - 1) * page_size
        end_index = page_number * page_size
        page_data_html = df_exec_data[start_index:end_index].to_html(index=False, justify="center")

        #add page and return
        content["exec_data_html"] = page_data_html
        content["total_pages"] = total_pages
        content["current_page"] = page_number

        return content

    @staticmethod
    def download_report(exec_id: str, lang: str) -> bytes:
        """Create the file to download"""
        with open(f"routes/{exec_id}.json", "r", encoding='utf-8') as f:
            result_report = json.load(f)

        exec_data_html = DataFrame(result_report['exec_data_html']).to_html(index=False, justify="center")
        result_report["exec_data_html"] = exec_data_html

        rendered_html = render_template(
            "report.html",
            content=result_report,
            current_lang=lang
        )

        html_to_pdf = os.environ['wkhtmltopdf']
        pdfkit_conf = pdfkit.configuration(wkhtmltopdf=html_to_pdf)
        report = pdfkit.from_string(
            input=rendered_html,
            configuration=pdfkit_conf,
        )
        return report

    def get_paginated_results(self, exec_id: str, page: int):
        with open(f"routes/{exec_id}.json", "r", encoding='utf-8') as f:
            current_report = json.load(f)
        df_exec_data = DataFrame(current_report.get("exec_data_html"))

        page_size = 10
        total_items = len(df_exec_data)
        total_pages = (total_items + page_size - 1) // page_size
        start_index = (page - 1) * page_size
        end_index = page * page_size
        page_data_html = df_exec_data[start_index:end_index].to_html(index=False, justify="center")

        content = {
            "config_html": current_report.get("config_html"),
            "exec_data_html": page_data_html,
            "total_pages": total_pages,
            "current_page": page,
            "plot_graph": current_report.get("plot_graph"),
            "box_graph": current_report.get("box_graph")
        }

        return content
