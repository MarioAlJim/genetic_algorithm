"""This file is for defining the algorithm class.

The algorithm class is the base class for all algorithms."""
from src.models.evaluations.triangle_classification import TriangleClassification

class Algorithm:
    """Algorithm base class"""
    def __init__(self):
        self._name = 'Algorithm'
        self._evaluations = [
            ['triangle-classification', TriangleClassification],
        ]
        self._evaluation = TriangleClassification()

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

    def execute(self) -> tuple:
        """Execute the algorithm"""
        raise NotImplementedError('Algorithm must implement execute method')
