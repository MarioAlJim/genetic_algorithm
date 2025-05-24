"""Test suite for the Evaluation"""
import pytest
from src.models.evaluation import Evaluation
from src.models.evaluations.triangle_classification import TriangleClassification


class TestEvaluation:
    """Test class for Evaluation"""
    def test_score_1(self):
        """Graph 1

        Input: Child class instance and valid suite
        Output: List with the suite and the coverage score
        """
        evaluation = TriangleClassification()
        suite = [3, 4, 5, 5, 4, 3, 4, 3, 5]
        result = evaluation.score(suite)
        assert (
            result[0] == suite
            and isinstance(result[1], float)
        )

    def test_score_2(self):
        """Graph 2

        Input: Child class instance and invalid suite
        Output: TypeError
        """
        with pytest.raises(TypeError):
            evaluation = TriangleClassification()
            suite = ['3', '4', '5', '5', '4', '3', '4', '3', '5']
            evaluation.score(suite)

    def test_score_3(self):
        """Graph 3

        Input: Evaluation instance and valid suite
        Output: List with the suite and the coverage score as 0
        """
        evaluation = Evaluation()
        suite = [3, 4, 5, 5, 4, 3, 4, 3, 5]
        score = evaluation.score(suite)
        assert score == [suite, 0]


    def test_score_4(self):
        """Graph 3

        Input: Evaluation instance and invalid suite
        Output: List with the suite and the coverage score as 0
        """
        evaluation = Evaluation()
        suite = ['3', '4', '5', '5', '4', '3', '4', '3', '5']
        score = evaluation.score(suite)
        assert score == [suite, 0]
