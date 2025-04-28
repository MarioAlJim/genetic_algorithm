"""Controller for the playground"""
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pandas import DataFrame

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
