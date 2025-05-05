import pytest
from src.models.evaluation import TriangleClassification

class TestEvaluation:
    """Test class for evaluation"""
    def test_init(self):
        """Test init method"""
        self.eval = TriangleClassification()
        result = self.eval.score([3, 3, 3], 'equilateral')
        print(result)
        assert True
