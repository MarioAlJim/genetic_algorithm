"""This file is for defining the triangle classification evaluation."""
# no cover: start
from src.models.evaluation import Evaluation
# no cover: stop
class TriangleClassification(Evaluation):
    """Triangle classification class"""

    # no cover: start
    def __init__(self) -> None:
        super().__init__()
        self._name = 'triangle-classification'
        self._branches = 5
        self._inputs = 3

    def score(self, suite: list) -> list:
        """Evaluates the code coverage of the suite"""
        score = self._get_coverage(self.classify_triangle, suite)

        return [suite, score]

    # no cover: stop
    @staticmethod
    def classify_triangle(data: list) -> str:
        """Classifies the triangle based on the given lengths"""
        classification = "out of range"
        a = data[0]
        b = data[1]
        c = data[2]

        if a > 0 and b > 0 and c > 0:
            if a + b > c and b + c > a and c + a > b:
                if a != b and b != c and c != a:
                    classification = 'scalene'
                elif a == b == c:
                    classification = 'equilateral'
                elif ((a == b != c) or
                      (a == c != b) or
                      (b == c != a)):
                    classification = 'isosceles'
            else:
                classification = 'invalid'
        else:
            classification = 'out of range'

        return classification
