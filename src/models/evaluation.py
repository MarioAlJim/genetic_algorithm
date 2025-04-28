"""This file is for defining the evaluations."""
class Evaluation:
    """Evaluation class"""
    def __init__(self) -> None:
        self._name = 'Evaluation'
        self._expected_solutions = []

    @property
    def name(self) -> str:
        """Get evaluation name"""
        return self._name

    @property
    def expected_solutions(self) -> list:
        """Get expected solutions"""
        return self._expected_solutions

    def score(self, data: list, expected_solution: str) -> list:
        """Evaluation method"""
        raise NotImplementedError('Evaluation method should be implemented by child class')

class TriangleClassification(Evaluation):
    """Triangle classification class"""
    def __init__(self) -> None:
        super().__init__()
        self._name = 'triangle-classification'
        self._expected_solutions = [
            'scalene',
            'equilateral',
            'isosceles',
            'invalid',
            'out of range'
        ]

    def score(self, data: list, expected_solution: str) -> list:
        """Evaluates the generated data

        I.E.
        Expected solution input: equilateral
        Input: [3,3,3]
        Output: [[3,3,3], 0]
        """
        # Classify the triangle
        classification = None
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

        # Score the chromosome
        score = 0

        if classification == expected_solution:
            score = 1

        return [data, score]
