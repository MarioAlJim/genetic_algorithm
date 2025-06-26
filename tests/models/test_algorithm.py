"""Test suite for Algorithm class"""
import pytest
from src.models.algorithm import Algorithm

class TestAlgorithm:
    """Test class for Algorithm"""
    def test_evaluation_1(self):
        """Valid input: Implemented evaluation"""
        algorithm = Algorithm()
        algorithm.evaluation = 'triangle-classification'
        assert algorithm.evaluation == 'Triangle Classification'

    def test_evaluation_2(self):
        """Invalid input: Not implemented evaluation"""
        evaluation = 'pythagorean-problem'
        algorithm = Algorithm()
        with pytest.raises(ValueError):
            algorithm.evaluation = evaluation

    def test_evaluation_3(self):
        """Invalid input: Not a string"""
        evaluation = 1
        algorithm = Algorithm()
        with pytest.raises(ValueError):
            algorithm.evaluation = evaluation
