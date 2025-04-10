"""This file is for defining the fitness functions."""
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

    def score(self, pop: list, expected_solution: str) -> list:
        """Fitness function method"""
        raise NotImplementedError('Fitness function should be implemented by child class')

class TriangleClassification(Evaluation):
    """Triangle classification class"""
    def __init__(self) -> None:
        super().__init__()
        self._name = 'triangle-classification'
        self._expected_solutions = ['scalene', 'equilateral', 'isosceles', 'invalid', 'out of range']

    def score(self, chromo: list, expected_solution: str) -> list:
        """Evaluates the chromosomes in the population

        I.E.
        Expected solution input: Equilateral
        Population input: [[3,3,3], [1,2,3]]
        Output: [[[3,3,3], 0], [[1,2,3], 1]]
        """
        # Classify the triangle
        classification = None
        a = chromo[0]
        b = chromo[1]
        c = chromo[2]

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

        return [chromo, score]
