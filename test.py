import unittest
from verification_algorithms import *
from benchmark_generator import *
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

    def test_counter_example(self):

        for size in range(1, 100, 10):
            automaton, nbr_objectives, colors_map = intersection_example(size)
            self.assertTrue(counter_example_based_algorithm(automaton, nbr_objectives, colors_map))

        for size in range(1, 100, 10):
            automaton, nbr_objectives, colors_map = intersection_example(size, negative_instance=True)
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

        import time

        for size in range(10, 100000, 100):
            print("Number of states " + str(size))

            automaton, nbr_objectives, colors_map = random_automaton(size, 0.5, 10)

            print(colors_map)

            start = time.time()
            result_direct_antichain = direct_antichain_algorithm(automaton, nbr_objectives, colors_map,
                                                                 is_payoff_realizable)
            print(result_direct_antichain)

            end = time.time()
            print("Direct antichain time " + str(end - start))

            start = time.time()
            result_counter_example = counter_example_based_algorithm(automaton, nbr_objectives, colors_map)

            print(result_counter_example)

            end = time.time()
            print("Counter example time " + str(end - start))
            self.assertEqual(result_direct_antichain, result_counter_example)


if __name__ == '__main__':
    unittest.main()
