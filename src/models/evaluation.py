"""This file is for defining the evaluation class."""
import os
import coverage

class Evaluation:
    """Evaluation class"""
    def __init__(self) -> None:
        self._name = 'Evaluation'
        self._branches = 0
        self._inputs = 0
        self._input_type = 'Not defined'

    @property
    def name(self) -> str:
        """Get evaluation name"""
        return self._name

    @property
    def branches(self) -> int:
        """Get number of branches"""
        return self._branches

    @property
    def inputs(self) -> int:
        """Get number of inputs"""
        return self._inputs

    @property
    def input_type(self) -> str:
        """Get input type"""
        return self._input_type

    def _get_coverage(self, target_function, suite: list) -> float:
        """Measures the code coverage of the target function given a suite of inputs."""
        coverage_percent = 0
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
        default_coverage_config = os.path.join(project_root, '.coveragerc')
        cov = coverage.Coverage(config_file=default_coverage_config)
        it = iter(suite)

        with cov.collect():
            # Use zip to group the inputs from the suite and pass them to the target function
            for args in zip(*[it] * self.inputs):
                target_function(args)

        for filename in cov.get_data().measured_files():
            analysis = cov.analysis2(filename)
            executable_statements = len(analysis[1])
            statements_not_run = len(analysis[3])
            statements_run = executable_statements - statements_not_run

            coverage_percent = round(statements_run * 100 / executable_statements, 2)

        cov.erase()
        return coverage_percent

    def score(self, suite: list) -> list:
        """Evaluates the code coverage of the suite"""
        score = self._get_coverage(self._fitness_function, suite)
        return [suite, score]

    def _fitness_function(self, data: list):
        """Fitness function"""
        raise NotImplementedError('Fitness function should be implemented by child class')
