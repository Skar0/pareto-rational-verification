import unittest
from verification_algorithms import *
from generate_benchmark import *
import random


class TestAlgorithms(unittest.TestCase):

    def setUp(self):
        random.seed(10)

    def test_direct_antichain(self):

        for size in range(1, 100, 10):
            automaton, nbr_objectives, colors_map = intersection_example(size)
            self.assertTrue(direct_antichain_algorithm(automaton, nbr_objectives, colors_map, is_payoff_realizable))

        for size in range(1, 100, 10):
            automaton, nbr_objectives, colors_map = intersection_example(size, negative_instance=True)
            self.assertFalse(direct_antichain_algorithm(automaton, nbr_objectives, colors_map, is_payoff_realizable))

        for size in range(1, 7):
            automaton, nbr_objectives, colors_map = intersection_example_objective_increase(size)
            self.assertTrue(direct_antichain_algorithm(automaton, nbr_objectives, colors_map, is_payoff_realizable))

        for size in range(1, 7):
            automaton, nbr_objectives, colors_map = intersection_example_objective_increase(size, negative_instance=True)
            self.assertFalse(direct_antichain_algorithm(automaton, nbr_objectives, colors_map, is_payoff_realizable))

    def test_counter_example(self):

        for size in range(1, 100, 10):
            automaton, nbr_objectives, colors_map = intersection_example(size)
            self.assertTrue(counter_example_based_algorithm(automaton, nbr_objectives, colors_map))

        for size in range(1, 100, 10):
            automaton, nbr_objectives, colors_map = intersection_example(size, negative_instance=True)
            self.assertFalse(counter_example_based_algorithm(automaton, nbr_objectives, colors_map))

        for size in range(1, 7):
            automaton, nbr_objectives, colors_map = intersection_example_objective_increase(size)
            self.assertTrue(counter_example_based_algorithm(automaton, nbr_objectives, colors_map))

        for size in range(1, 7):
            automaton, nbr_objectives, colors_map = intersection_example_objective_increase(size, negative_instance=True)
            self.assertFalse(counter_example_based_algorithm(automaton, nbr_objectives, colors_map))

    def test_consistency(self):

        for size in range(1, 100, 10):
            automaton, nbr_objectives, colors_map = intersection_example(size)
            result_direct_antichain = direct_antichain_algorithm(automaton, nbr_objectives, colors_map,
                                                                 is_payoff_realizable)
            result_counter_example = counter_example_based_algorithm(automaton, nbr_objectives, colors_map)
            self.assertEqual(result_direct_antichain, result_counter_example)

        for size in range(1, 100, 10):
            automaton, nbr_objectives, colors_map = intersection_example(size, negative_instance=True)
            result_direct_antichain = direct_antichain_algorithm(automaton, nbr_objectives, colors_map,
                                                                 is_payoff_realizable)
            result_counter_example = counter_example_based_algorithm(automaton, nbr_objectives, colors_map)
            self.assertEqual(result_direct_antichain, result_counter_example)

        for nbr_obj in range(2, 30):

            automaton, nbr_objectives, colors_map = random_automaton(100, 0.2, nbr_obj)

            result_direct_antichain = direct_antichain_algorithm(automaton, nbr_objectives, colors_map,
                                                                 is_payoff_realizable)

            automaton, nbr_objectives, colors_map = random_automaton(100, 0.2, nbr_obj)

            result_counter_example = counter_example_based_algorithm(automaton, nbr_objectives, colors_map)

            self.assertEqual(result_direct_antichain, result_counter_example)

            automaton, nbr_objectives, colors_map = random_automaton(1000, 0.2, nbr_obj)

            result_direct_antichain = direct_antichain_algorithm(automaton, nbr_objectives, colors_map,
                                                                 is_payoff_realizable)

            automaton, nbr_objectives, colors_map = random_automaton(1000, 0.2, nbr_obj)

            result_counter_example = counter_example_based_algorithm(automaton, nbr_objectives, colors_map)

            self.assertEqual(result_direct_antichain, result_counter_example)

            automaton, nbr_objectives, colors_map = random_automaton(10000, 0.2, nbr_obj)

            result_direct_antichain = direct_antichain_algorithm(automaton, nbr_objectives, colors_map,
                                                                 is_payoff_realizable)

            automaton, nbr_objectives, colors_map = random_automaton(10000, 0.2, nbr_obj)

            result_counter_example = counter_example_based_algorithm(automaton, nbr_objectives, colors_map)

            self.assertEqual(result_direct_antichain, result_counter_example)

if __name__ == '__main__':
    unittest.main()
