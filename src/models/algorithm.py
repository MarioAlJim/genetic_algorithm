"""This file is for defining the algorithm class.

The algorithm class is the base class for all algorithms."""
from src.models.evaluation import TriangleClassification

class Algorithm:
    """Algorithm base class"""
    def __init__(self):
        self._name = 'Algorithm'
        self._evaluations = [
            ['triangle-classification', TriangleClassification],
        ]
        self._evaluation = TriangleClassification()
        self._expected_solution = 'scalene'

    @property
    def name(self) -> str:
        """Get algorithm name"""
        return self._name

    @property
    def evaluation(self) -> str:
        """Get evaluation"""
        return self._evaluation.name

    @evaluation.setter
    def evaluation(self, evaluation) -> None:
        """Set evaluation"""
        for name, eval_class in self._evaluations:
            if name == evaluation:
                self._evaluation = eval_class()
                return

        raise ValueError('Evaluation must be a valid value: ', self._evaluations)

    @property
    def expected_solution(self) -> str:
        """Get expected solution"""
        return self._expected_solution

    @expected_solution.setter
    def expected_solution(self, expected_solution) -> None:
        """Set expected solution"""
        expected_solutions = self._evaluation.expected_solutions

        if expected_solution not in expected_solutions:
            raise ValueError('Expected solution must be: ', expected_solutions)

        self._expected_solution = expected_solution
