"""Controller for the playground"""
from pandas import DataFrame
import pdfkit

class PlaygroundController:
    """Controller for the playground"""

    def __init__(self):
        """Initialize the controller"""
        pass

    def start_execution(self):
        """Execute the playground"""
        pass

    def set_algorithm_parameters(self, config: dict) -> None:
        """Set the algorithm parameters"""
        pass

    def evaluate_coverage(self, test_data: list) -> float:
        """Evaluate the coverage of the test data"""
        pass

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

        pdfkit_conf = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
        pdfkit.from_string(
            input=html_content,
            output_path='playground_report.pdf',
            configuration=pdfkit_conf,
        )
