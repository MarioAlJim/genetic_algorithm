"""Test suite for the GeneticAlgorithm class."""
import pytest
from src.models.ga.genetic_algorithm import GeneticAlgorithm

class TestGeneticAlgorithm:
    """Test class for the GeneticAlgorithm class."""
    def test_pop_size_1(self):
        """Valid input: Integer greater or equal to 1"""
        pop_size = 1
        ga = GeneticAlgorithm()
        ga.pop_size = pop_size
        assert ga.pop_size == pop_size

    def test_pop_size_2(self):
        """Valid input: Integer less or equal to 10"""
        pop_size = 10
        ga = GeneticAlgorithm()
        ga.pop_size = pop_size
        assert ga.pop_size == pop_size

    def test_pop_size_3(self):
        """Invalid input: Integer less than 1"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.pop_size = 0

    def test_pop_size_4(self):
        """Invalid input: Integer greater than 10"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.pop_size = 11

    def test_pop_size_5(self):
        """Invalid input: Not an integer"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.pop_size = 1.15

    def test_num_generations_1(self):
        """Valid input: Integer greater or equal to 1"""
        num_generations = 1
        ga = GeneticAlgorithm()
        ga.num_generations = num_generations
        assert ga.num_generations == num_generations

    def test_num_generations_2(self):
        """Valid input: Integer less or equal to 100"""
        num_generations = 10
        ga = GeneticAlgorithm()
        ga.num_generations = num_generations
        assert ga.num_generations == num_generations

    def test_num_generations_3(self):
        """Invalid input: Integer less than 1"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.num_generations = 0

    def test_num_generations_4(self):
        """Invalid input: Integer greater than 10"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.num_generations = 11

    def test_num_generations_5(self):
        """Invalid input: Not an integer"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.num_generations = 1.15

    def test_selection_rate_1(self):
        """Valid input: Value greater than 0.0"""
        selection_rate = 0.1
        ga = GeneticAlgorithm()
        ga.selection_rate = selection_rate
        assert ga.selection_rate == selection_rate

    def test_selection_rate_2(self):
        """Valid input: Value less or equal to 1.0"""
        selection_rate = 1.0
        ga = GeneticAlgorithm()
        ga.selection_rate = selection_rate
        assert ga.selection_rate == selection_rate

    def test_selection_rate_3(self):
        """Invalid input: Value less or equal than 0.0"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.selection_rate = 0.0

    def test_selection_rate_4(self):
        """Invalid input: Value greater than 1.0"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.selection_rate = 1.1

    def test_selection_rate_5(self):
        """Invalid input: Value not a float"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.selection_rate = 1

    def test_selection_type_1(self):
        """Valid input: Implemented selection type"""
        selection_type = 'random'
        ga = GeneticAlgorithm()
        ga.selection_type = selection_type
        assert ga.selection_type == selection_type

    def test_selection_type_2(self):
        """Invalid input: Not implemented selection type"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.selection_type = 'arbitrary'

    def test_selection_type_3(self):
        """Invalid input: Not a string"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.selection_type = 1

    def test_crossover_type_1(self):
        """Valid input: Implemented crossover type"""
        crossover_type = 'uniform'
        ga = GeneticAlgorithm()
        ga.crossover_type = crossover_type
        assert ga.crossover_type == crossover_type

    def test_crossover_type_2(self):
        """Invalid input: Not implemented crossover type"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.crossover_type = 'infinite-point'

    def test_crossover_type_3(self):
        """Invalid input: Not a string"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.crossover_type = 1

    def test_mutation_rate_1(self):
        """Valid input: Value greater or equal to 0.0"""
        mutation_rate = 0.0
        ga = GeneticAlgorithm()
        ga.mutation_rate = mutation_rate
        assert ga.mutation_rate == mutation_rate

    def test_mutation_rate_2(self):
        """Valid input: Value less or equal to 1.0"""
        mutation_rate = 1.0
        ga = GeneticAlgorithm()
        ga.mutation_rate = mutation_rate
        assert ga.mutation_rate == mutation_rate

    def test_mutation_rate_3(self):
        """Invalid input: Value less than 0.0"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.mutation_rate = -0.1

    def test_mutation_rate_4(self):
        """Invalid input: Value greater than 1.0"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.mutation_rate = 1.1

    def test_mutation_rate_5(self):
        """Invalid input: Value not a float"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.mutation_rate = 1

    def test_mutation_type_1(self):
        """Valid input: Implemented mutation type"""
        mutation_type = 'random-resetting'
        ga = GeneticAlgorithm()
        ga.mutation_type = mutation_type
        assert ga.mutation_type == mutation_type

    def test_mutation_type_2(self):
        """Invalid input: Not implemented mutation type"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.mutation_type = 'random-bits'

    def test_mutation_type_3(self):
        """Invalid input: Not a string"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.mutation_type = 1

    def test_elitism_rate_1(self):
        """Valid input: Value greater or equal to 0.0"""
        elitism_rate = 0.0
        ga = GeneticAlgorithm()
        ga.elitism_rate = elitism_rate
        assert ga.elitism_rate == elitism_rate

    def test_elitism_rate_2(self):
        """Valid input: Value less or equal to 1.0"""
        elitism_rate = 1.0
        ga = GeneticAlgorithm()
        ga.elitism_rate = elitism_rate
        assert ga.elitism_rate == elitism_rate

    def test_elitism_rate_3(self):
        """Invalid input: Value less than 0.0"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.elitism_rate = -0.1

    def test_elitism_rate_4(self):
        """Invalid input: Value greater than 1.0"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.elitism_rate = 1.1

    def test_elitism_rate_5(self):
        """Invalid input: Value not a float"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.elitism_rate = 1

    def test_execute_1(self):
        """Graph 1

        Input: GA parameters configured
        Output: Configuration dict with selected GA parameters
        """
        ga = GeneticAlgorithm()
        num_generations = 5
        pop_size = 10
        selection_type = 'random'
        selection_rate = 0.3
        crossover_type = 'uniform'
        mutation_type = 'random-resetting'
        mutation_rate = 0.4
        elitism_rate = 0.1

        ga.num_generations = num_generations
        ga.pop_size = pop_size
        ga.selection_type = selection_type
        ga.selection_rate = selection_rate
        ga.crossover_type = crossover_type
        ga.mutation_type = mutation_type
        ga.mutation_rate = mutation_rate
        ga.elitism_rate = elitism_rate
        config, _ = ga.execute()

        assert (
            config["Generations"] == [num_generations]
            and config["Population size"] == [pop_size]
            and config["Selection type"] == [selection_type]
            and config["Selection rate"] == [selection_rate]
            and config["Crossover type"] == [crossover_type]
            and config["Mutation type"] == [mutation_type]
            and config["Mutation rate"] == [mutation_rate]
            and config["Elitism rate"] == [elitism_rate]
        )

    def test_execute_2(self):
        """Graph 2

        Input: Some GA parameters configured
        Output: Configuration dict with selected GA parameters
        """
        ga = GeneticAlgorithm()
        pop_size = 10
        selection_type = 'random'
        crossover_type = 'uniform'
        mutation_type = 'random-resetting'
        elitism_rate = 0.0

        ga.pop_size = pop_size
        ga.selection_type = selection_type
        ga.crossover_type = crossover_type
        ga.mutation_type = mutation_type
        ga.elitism_rate = elitism_rate
        config, _ = ga.execute()

        assert (
            config["Generations"] == [ga.num_generations]
            and config["Population size"] == [pop_size]
            and config["Selection type"] == [selection_type]
            and config["Selection rate"] == [ga.selection_rate]
            and config["Crossover type"] == [crossover_type]
            and config["Mutation type"] == [mutation_type]
            and config["Mutation rate"] == [ga.mutation_rate]
            and config["Elitism rate"] == [elitism_rate]
        )

    def test_execute_3(self):
        """Graph 3

        Input: No GA parameters configured
        Output: Configuration dict with predefined GA parameters
        """
        ga = GeneticAlgorithm()
        config, _ = ga.execute()

        assert (
            config["Generations"] == [ga.num_generations]
            and config["Population size"] == [ga.pop_size]
            and config["Selection type"] == [ga.selection_type]
            and config["Selection rate"] == [ga.selection_rate]
            and config["Crossover type"] == [ga.crossover_type]
            and config["Mutation type"] == [ga.mutation_type]
            and config["Mutation rate"] == [ga.mutation_rate]
            and config["Elitism rate"] == [ga.elitism_rate]
        )
