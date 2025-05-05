from src.models.evaluation import TriangleClassification
from src.controllers.coverage_evaluator import get_coverage
import pytest

triangle_evaluator = TriangleClassification()

class TestCoverageEvaluator:
    """Test class for coverage evaluator."""

    @pytest.fixture
    def triangle_inputs(self):
        """Fixture for triangle inputs."""
        return [
            [3, 3, 3],   # Equilateral
            [3, 4, 5],   # Scalene
            [2, 2, 3],   # Isosceles
            [1, 2, 3],   # Not a triangle
            [0, 0, 0],   # Invalid
            [10, 10, 20], # Out of range
        ]

    def test_coverage_output_structure(self, triangle_inputs):
        """Test the structure of the coverage output."""
        result = get_coverage(triangle_evaluator.classify_triangle, triangle_inputs)

        assert isinstance(result, dict)
        assert "coverage_summary" in result
        assert "coverage_percent" in result

        summary = result["coverage_summary"]
        assert isinstance(summary, dict)
        assert len(summary) > 0

        for file_summary in summary.values():
            assert "total_statements" in file_summary
            assert "executed_statements" in file_summary
            assert "missing_statements" in file_summary
            assert file_summary["total_statements"] >= file_summary["executed_statements"]

        assert 0 <= result["coverage_percent"] <= 100

    def test_get_coverage_advanced(self):
        """Test the coverage evaluation with a more complex dataset."""
        inputs = [
            [12, 12, 12],     # Equilateral
            [1, 2, 3],     # Not a triangle
            [3, 4, 5],     # Scalene
            [2, 2, 3],     # Isosceles
            [0, 0, 0],     # Invalid
            [10, 10, 20],  # Out of range
            [1, 1, 2],     # Not a triangle
            [5, 5, 5],     # Equilateral
            [7, 8, 9],     # Scalene
            [4, 4, 6],     # Isosceles
        ]
        result = get_coverage(triangle_evaluator.classify_triangle, inputs)
        print(result)
        assert result["coverage_percent"] == 100

    def test_get_coverage_empty(self):
        """Test the coverage evaluation with an empty dataset."""
        inputs = []
        result = get_coverage(triangle_evaluator.classify_triangle, inputs)
        assert result["coverage_percent"] == 0

    def test_get_coverage_invalid_input(self):
        """Test the coverage evaluation with invalid input."""
        inputs = [
            [3, 3, 'a'],   # Invalid input
            [None, None, None],  # Invalid input
            [1, 2],  # Not enough sides
        ]
        result = get_coverage(triangle_evaluator.classify_triangle, inputs)
        assert result["coverage_percent"] == 37.5

    def test_get_coverage_large_dataset(self):
        """Test the coverage evaluation with a large dataset."""
        inputs = [[i, i, i] for i in range(20)]  # Equilateral triangles
        result = get_coverage(triangle_evaluator.classify_triangle, inputs)
        assert result["coverage_percent"] == 75

    def test_partial_coverage_detection_1(self):
        """Test the coverage detection with a partial population."""
        inputs = [
            [3, 3, 3],  # Solo equilateral
            [3, 4, 5],  # Scalene
            [2, 2, 3],  # Isosceles
            [0, 0, 0],  # Out of range
            [10, 10, 20],  # Invalid
        ]
        result = get_coverage(triangle_evaluator.classify_triangle, inputs)
        assert result["coverage_percent"] == 100

    def test_partial_coverage_detection_2(self):
        """Test the coverage detection with a partial population."""
        inputs = [
            [3, 3, 3],  # Solo equilateral
            [2, 2, 3],  # Isosceles
            [0, 0, 0],  # Out of range
            [10, 10, 20],  # Invalid
        ]
        result = get_coverage(triangle_evaluator.classify_triangle, inputs)
        assert result["coverage_percent"] == 93.75

    def test_partial_coverage_detection_3(self):
        """Test the coverage detection with a partial population."""
        inputs = [
            [3, 3, 3],  # Solo equilateral
            [3, 4, 5],  # Scalene
            [2, 2, 3],  # Isosceles
            [10, 10, 20],  # Invalid
        ]
        result = get_coverage(triangle_evaluator.classify_triangle, inputs)
        assert result["coverage_percent"] == 93.75

    def test_partial_coverage_detection_4(self):
        """Test the coverage detection with a partial population."""
        inputs = [
            [3, 3, 3],  # Solo equilateral
            [3, 4, 5],  # Scalene
            [2, 2, 3],  # Isosceles
            [10, 10, 20],  # Invalid
        ]
        result = get_coverage(triangle_evaluator.classify_triangle, inputs)
        assert result["coverage_percent"] == 93.75

    def test_partial_coverage_detection_5(self):
        """Test the coverage detection with a partial population."""
        inputs = [
            [3, 4, 5],  # Scalene
            [2, 2, 3],  # Isosceles
            [0, 0, 0],  # Out of range
            [10, 10, 20],  # Invalid
        ]
        result = get_coverage(triangle_evaluator.classify_triangle, inputs)
        assert result["coverage_percent"] == 93.75