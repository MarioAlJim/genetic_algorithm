from src.problems.triangle_classifier import classify_triangle
from src.controllers.coverage_evaluator import get_coverage
import pytest

# ----------- Dummy dataset for coverage ----------------
@pytest.fixture
def triangle_inputs():
    return [
        (3, 3, 3),   # Equilateral
        (3, 3, 2),   # Isosceles
        (3, 4, 5),   # Scalene
        (1, 2, 3),   # Not a triangle (inequality)
        (0, 1, 1),   # Not a triangle (invalid sides)
    ]

# ----------- Basic test ----------------
def test_coverage_output_structure(triangle_inputs):
    result = get_coverage(classify_triangle, triangle_inputs)

    # Validación de estructura
    assert isinstance(result, dict)
    assert "coverage_summary" in result
    assert "coverage_percent" in result

    summary = result["coverage_summary"]
    assert isinstance(summary, dict)
    assert len(summary) > 0  # Al menos un archivo debe haberse medido

    # Comprobamos campos esperados en cada archivo
    for file_summary in summary.values():
        assert "total_statements" in file_summary
        assert "executed_statements" in file_summary
        assert "missing_statements" in file_summary

        assert file_summary["total_statements"] >= file_summary["executed_statements"]

    # La cobertura debe estar entre 0 y 100
    assert 0 <= result["coverage_percent"] <= 100


# ----------- Test con población incompleta ----------------
def test_partial_coverage_detection():
    # Solo un caso ejecutado, no cubrirá todo
    inputs = [
        (3, 3, 3),   # Solo equilateral
    ]

    result = get_coverage(classify_triangle, inputs)

    assert result["coverage_percent"] == 40


def test_get_coverage_advanced():
    # Aquí puedes definir las entradas para probar
    inputs = [
        (12, 12, 12),     # Equilateral
        (1, 2, 3),     # Not a triangle
    ]
    result = get_coverage(classify_triangle, inputs)
    assert result["coverage_percent"] == 50