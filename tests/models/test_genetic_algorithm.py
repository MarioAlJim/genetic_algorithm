import pytest
from src.models.ga.genetic_algorithm import GeneticAlgorithm

class TestGeneticAlgorithm:
    """Test class for the GeneticAlgorithm class."""
    def test_gen_type_1(self):
        """Valid input"""
        gen_type = 'real-number'
        ga = GeneticAlgorithm()
        ga.gen_type = gen_type
        assert ga.gen_type == gen_type

    def test_gen_type_2(self):
        """Invalid input"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.gen_type = 'invalid-gen-type'

    def test_chromo_len_1(self):
        """Valid input"""
        chromo_len = 4
        ga = GeneticAlgorithm()
        ga.chromo_len = chromo_len
        assert ga.chromo_len == chromo_len

    def test_chromo_len_2(self):
        """Input below the allowed values"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.chromo_len = -1

    def test_chromo_len_3(self):
        """Input above the allowed values"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.chromo_len = 10000

    def test_pop_size_1(self):
        """Valid input"""
        pop_size = 4
        ga = GeneticAlgorithm()
        ga.pop_size = pop_size
        assert ga.pop_size == pop_size

    def test_pop_size_2(self):
        """Input below the allowed values"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.pop_size = 0

    def test_pop_size_3(self):
        """Input above the allowed values"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.pop_size = 10000

    def test_num_generations_1(self):
        """Valid input"""
        num_generations = 10
        ga = GeneticAlgorithm()
        ga.num_generations = num_generations
        assert ga.num_generations == num_generations

    def test_num_generations_2(self):
        """Input below the allowed values"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.num_generations = 0

    def test_num_generations_3(self):
        """Input above the allowed values"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.num_generations = 10000

    def test_fitness_function_1(self):
        """Valid input"""
        fitness_function = 'triangle-classification'
        ga = GeneticAlgorithm()
        ga.fitness_function = fitness_function
        assert ga.fitness_function == fitness_function

    def test_fitness_function_2(self):
        """Invalid input"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.fitness_function = 'invalid-function'

    def test_expected_solution_1(self):
        """Valid input"""
        expected_solution = 'scalene'
        ga = GeneticAlgorithm()
        ga.expected_solution = expected_solution
        assert ga.expected_solution == expected_solution

    def test_expected_solution_2(self):
        """Valid input"""
        expected_solution = 'equilateral'
        ga = GeneticAlgorithm()
        ga.expected_solution = expected_solution
        assert ga.expected_solution == expected_solution

    def test_expected_solution_3(self):
        """Valid input"""
        expected_solution = 'isosceles'
        ga = GeneticAlgorithm()
        ga.expected_solution = expected_solution
        assert ga.expected_solution == expected_solution

    def test_expected_solution_4(self):
        """Valid input"""
        expected_solution = 'invalid'
        ga = GeneticAlgorithm()
        ga.expected_solution = expected_solution
        assert ga.expected_solution == expected_solution

    def test_expected_solution_5(self):
        """Valid input"""
        expected_solution = 'out of range'
        ga = GeneticAlgorithm()
        ga.expected_solution = expected_solution
        assert ga.expected_solution == expected_solution

    def test_expected_solution_6(self):
        """Invalid input"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.expected_solution = 'Not in the range of solutions'

    def test_expected_solution_7(self):
        """Invalid input"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.expected_solution = 0

    def test_selection_rate_1(self):
        """Valid input"""
        selection_rate = 0.5
        ga = GeneticAlgorithm()
        ga.selection_rate = selection_rate
        assert ga.selection_rate == selection_rate

    def test_selection_rate_2(self):
        """Input below the allowed values"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.selection_rate = -0.1

    def test_selection_rate_3(self):
        """Input above the allowed values"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.selection_rate = 1.1

    def test_selection_type_1(self):
        """Valid input"""
        selection_type = 'steady-state'
        ga = GeneticAlgorithm()
        ga.selection_type = selection_type
        assert ga.selection_type == selection_type

    def test_selection_type_2(self):
        """Invalid input"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.selection_type = 'master-chief'

    def test_crossover_type_1(self):
        """Valid input"""
        crossover_type = 'two-point'
        ga = GeneticAlgorithm()
        ga.crossover_type = crossover_type
        assert ga.crossover_type == crossover_type

    def test_crossover_type_2(self):
        """Invalid input"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.crossover_type = 'infinite-point'

    def test_mutation_rate_1(self):
        """Valid input"""
        mutation_rate = 0.5
        ga = GeneticAlgorithm()
        ga.mutation_rate = mutation_rate
        assert ga.mutation_rate == mutation_rate

    def test_mutation_rate_2(self):
        """Input below the allowed values"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.mutation_rate = -0.1

    def test_mutation_rate_3(self):
        """Input above the allowed values"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.mutation_rate = 1.1

    def test_mutation_type_1(self):
        """Valid input"""
        mutation_type = 'random-resetting'
        ga = GeneticAlgorithm()
        ga.mutation_type = mutation_type
        assert ga.mutation_type == mutation_type

    def test_mutation_type_2(self):
        """Invalid input"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.mutation_type = 'random-selection'

    def test_current_pop_1(self):
        """Valid input"""
        current_pop = [[1,2,3],[4,5,6]]
        ga = GeneticAlgorithm()
        ga.current_pop = current_pop
        assert ga.current_pop == current_pop

    def test_current_pop_2(self):
        """Invalid input"""
        ga = GeneticAlgorithm()
        with pytest.raises(ValueError):
            ga.current_pop = []

    def test_create_gen(self):
        """Verifies the output gen type"""
        ga = GeneticAlgorithm()
        ga.gen_type = 'real-number'
        gen = ga.create_gen()
        assert isinstance(gen, float)

    def test_init_pop_1(self):
        """Verifies the output type"""
        ga = GeneticAlgorithm()
        pop = ga.init_pop()
        assert isinstance(pop, list)

    def test_init_pop_2(self):
        """Verifies the output population len"""
        ga = GeneticAlgorithm()
        pop = ga.init_pop()
        assert len(pop) == ga.pop_size

    def test_init_pop_3(self):
        """Verifies the output chromosome len"""
        ga = GeneticAlgorithm()
        pop = ga.init_pop()
        assert len(pop[0][0]) == ga.chromo_len

    def test_evaluate_pop_1(self):
        """Verifies the output type"""
        ga = GeneticAlgorithm()
        initial_pop = [[71, 3, 62], [84, 8, 45], [74, 93, 34]]
        evaluated_pop = ga.evaluate(initial_pop)
        assert isinstance(evaluated_pop, list)

    def test_evaluate_pop_2(self):
        """Verifies the output population len"""
        ga = GeneticAlgorithm()
        initial_pop = [[71, 3, 62], [84, 8, 45], [74, 93, 34]]
        evaluated_pop = ga.evaluate(initial_pop)
        assert len(initial_pop) == len(evaluated_pop)

    def test_evaluate_pop_3(self):
        """Verifies the output evaluation type"""
        ga = GeneticAlgorithm()
        initial_pop = [[71, 3, 62], [84, 8, 45], [74, 93, 34]]
        evaluated_pop = ga.evaluate(initial_pop)
        evaluations = []

        for eval_chromo in evaluated_pop:
            evaluations.append(eval_chromo[1])

        assert all(isinstance(e, int) for e in evaluations)

    def test_selection_1(self):
        """Verifies the output type"""
        ga = GeneticAlgorithm()
        ga.init_pop()
        selected_pop = ga.select(ga.current_pop)
        assert isinstance(selected_pop, list)

    def test_selection_2(self):
        """Verifies the output population len"""
        ga = GeneticAlgorithm()
        ga.init_pop()
        selected_pop = ga.select(ga.current_pop)
        sel_pop_size = int(ga.selection_rate * ga.pop_size)
        assert len(selected_pop) == sel_pop_size

    def test_crossover_1(self):
        """Verifies the output type"""
        ga = GeneticAlgorithm()
        ga.init_pop()
        sel_pop = ga.select(ga.current_pop)
        cross_pop = ga.cross(sel_pop)
        assert isinstance(cross_pop, list)

    def test_crossover_2(self):
        """Verifies the output population len"""
        ga = GeneticAlgorithm()
        ga.init_pop()
        sel_pop = ga.select(ga.current_pop)
        cross_pop = ga.cross(sel_pop)
        assert len(cross_pop) == ga.pop_size

    def test_mutate_1(self):
        """Verifies the output type"""
        ga = GeneticAlgorithm()
        ga.init_pop()
        sel_pop = ga.select(ga.current_pop)
        cross_pop = ga.cross(sel_pop)
        mutated_pop = ga.mutate(cross_pop)
        assert isinstance(mutated_pop, list)

    def test_mutate_2(self):
        """Verifies the output population len"""
        ga = GeneticAlgorithm()
        ga.init_pop()
        sel_pop = ga.select(ga.current_pop)
        cross_pop = ga.cross(sel_pop)
        mutated_pop = ga.mutate(cross_pop)
        assert len(mutated_pop) == ga.pop_size

    def test_execute_1(self):
        """Verifies the output type"""
        ga = GeneticAlgorithm()
        ga.num_generations = 4
        ga.init_pop()
        report = ga.execute()
        assert isinstance(report, tuple)
