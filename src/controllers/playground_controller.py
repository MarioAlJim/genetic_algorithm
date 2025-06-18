"""Controller for the playground"""
import base64
import json
import os
import pdfkit
from io import BytesIO, StringIO
from flask import render_template, current_app
from flask_babel import gettext
from matplotlib import pyplot as plt
from pandas import DataFrame, read_html
from src.models.algorithm import Algorithm
from src.models.ga.genetic_algorithm import GeneticAlgorithm

class PlaygroundController:
    """Controller for the playground"""

    def __init__(self):
        """Initialize the controller"""
        self.algorithm = Algorithm()
        self.temp_dir = current_app.config['TEMP_DIR']

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

    def _generate_graphics(self, df_exec_data: dict) -> tuple:
        """Generate the graphics for the report"""
        num_generations = df_exec_data["Generation"]
        eval_pop = df_exec_data["Evaluated population"]

        total = len(eval_pop)
        elements = 10

        if total > elements:
            step = (total - 1) / (elements - 1)
            selected_indices = [round(i * step) for i in range(elements)]
            selected_indices = sorted(set(selected_indices))
            i = 0
            while len(selected_indices) < elements and i < total:
                if i not in selected_indices:
                    selected_indices.append(i)
                i += 1
            selected_indices = sorted(selected_indices[:elements])
            eval_pop = [eval_pop[i] for i in selected_indices]
            num_generations = [num_generations[i] for i in selected_indices]

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
        report_file = os.path.join(self.temp_dir, f"{exec_id}.json")

        df_config = DataFrame(config)
        config_html = df_config.transpose().to_html(header=False)
        df_exec_data = DataFrame(exec_data)
        exec_data_html = df_exec_data.to_html(index=False, justify="center")

        graphic1, graphic2 = self._generate_graphics(exec_data)

        test_suite = None
        evaluated_populations = exec_data.get("Evaluated population", [])
        if evaluated_populations:
            # Gets the last evaluated population with '[-1]' and the first chromosome with '[0][0]'
            # The first chromosome is the best one because the population is sorted by fitness
            best_chromo = evaluated_populations[-1][0][0]
            it = iter(best_chromo)
            inputs = config.get("Evaluation inputs", [1])
            test_suite = enumerate(zip(*[it] * inputs[0]), start=1)

        content = {
            "config": config,
            "config_html": config_html,
            "exec_data": exec_data,
            "exec_data_html": exec_data_html,
            "plot_graph": graphic1,
            "box_graph": graphic2,
            "test_suite": list(test_suite),
        }

        # Remove previous execution data if exists
        if os.path.exists(report_file):
            os.remove(report_file)

        #save base data
        with open(report_file, "w", encoding='utf-8') as file:
            file.truncate(0)
            json.dump(content, file, indent=2)

        return content

    def download_report(self, exec_id: str, lang: str, algorithm: str) -> bytes:
        """Create the file to download"""
        report_file = os.path.join(self.temp_dir, f"{exec_id}.json")

        with open(report_file, "r", encoding='utf-8') as f:
            report = json.load(f)

        df_config, df_exec_data = self.translate_tables(
            report.get("config"),
            report.get("exec_data")
        )
        config_html = df_config.transpose().to_html(header=False)
        page_data_html = df_exec_data.to_html(index=False, justify="center")

        rendered_html = render_template(
            "report.html",
            content=report,
            current_lang=lang,
            algorithm=algorithm,
            config_html=config_html,
            exec_data_html=page_data_html,
        )

        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
        wkhtmltopdf_path = os.path.join(project_root, 'tools', 'wkhtmltopdf.exe')
        pdfkit_conf = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
        report = pdfkit.from_string(
            input=rendered_html,
            configuration=pdfkit_conf,
            css=[
                os.path.join(project_root,"src/static/css/report_style.css"),
            ],
            output_path=False
        )

        return report

    def translate_tables(self, config: dict, exec_data: dict) -> tuple:
        """Translate the tables to the current language"""
        df_config = DataFrame(config)
        for column in df_config.columns:
            column_idx = df_config.columns.get_loc(column)
            value = df_config.iloc[0, column_idx]

            if isinstance(value, str):
                df_config.iloc[0, column_idx] = gettext(value)

            if isinstance(column, str):
                translated_element = gettext(column)
                df_config.rename(columns={column: translated_element}, inplace=True)

        df_exec_data = DataFrame(exec_data)
        for column in df_exec_data.columns:
            if isinstance(column, str):
                translated_element = gettext(column)
                df_exec_data.rename(columns={column: translated_element}, inplace=True)

        return df_config, df_exec_data

    def update_page_data(self, exec_id: str, page: int) -> dict:
        """Get paginated results for the execution data"""
        report_file = os.path.join(self.temp_dir, f"{exec_id}.json")
        with open(report_file, "r", encoding='utf-8') as f:
            report = json.load(f)

        df_config, df_exec_data = self.translate_tables(
            report.get("config"),
            report.get("exec_data")
        )

        # Paginate execution data
        page_size = 10
        total_items = len(df_exec_data)
        total_pages = (total_items + page_size - 1) // page_size
        start_index = (page - 1) * page_size
        end_index = page * page_size

        config_html = df_config.transpose().to_html(header=False)
        page_data_html = df_exec_data[start_index:end_index].to_html(index=False, justify="center")

        content = {
            "config": report.get("config"),
            "config_html": config_html,
            "exec_data": report.get("exec_data"),
            "exec_data_html": page_data_html,
            "total_pages": total_pages,
            "current_page": page,
            "plot_graph": report.get("plot_graph"),
            "box_graph": report.get("box_graph"),
            "test_suite": report.get("test_suite"),
        }

        return content
