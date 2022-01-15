from generate_benchmark import *
from verification_algorithms import *


if __name__ == "__main__":

    encoding = sys.argv[1]
    algorithm = sys.argv[2]
    benchmark = sys.argv[3]
    negative_instance = eval(sys.argv[4])
    parameters = [int(i) for i in sys.argv[5:]]

    if encoding == "Streett":

        if algorithm == "direct_antichain":

            if benchmark == "intersection_increase_vertices":

                nbr_copies = parameters[0]

                if not negative_instance:
                    automaton, nbr_objectives, colors_map = intersection_example(nbr_copies)
                else:
                    automaton, nbr_objectives, colors_map = intersection_example(nbr_copies, negative_instance=True)

                result = direct_antichain_algorithm(automaton, nbr_objectives, colors_map, is_payoff_realizable)

            elif benchmark == "intersection_increase_objectives":

                # number of objectives is 2 + 2 * nbr_copies
                nbr_copies = parameters[0]

                if not negative_instance:
                    automaton, nbr_objectives, colors_map = intersection_example_objective_increase(nbr_copies)
                else:
                    automaton, nbr_objectives, colors_map = intersection_example_objective_increase(nbr_copies, negative_instance=True)

                result = direct_antichain_algorithm(automaton, nbr_objectives, colors_map, is_payoff_realizable)

            elif benchmark == "random":

                nbr_vertices = parameters[0]
                density = parameters[1]
                nbr_objectives = parameters[2]

                automaton, nbr_objectives, colors_map = random_automaton(nbr_vertices, density, nbr_objectives)

                result = direct_antichain_algorithm(automaton, nbr_objectives, colors_map, is_payoff_realizable)

        elif algorithm == "counter_example":

            if benchmark == "intersection_increase_vertices":

                nbr_copies = parameters[0]

                if not negative_instance:
                    automaton, nbr_objectives, colors_map = intersection_example(nbr_copies)
                else:
                    automaton, nbr_objectives, colors_map = intersection_example(nbr_copies, negative_instance=True)

                result = counter_example_based_algorithm(automaton, nbr_objectives, colors_map)

            elif benchmark == "intersection_increase_objectives":

                # number of objectives is 2 + 2 * nbr_copies
                nbr_copies = parameters[0]

                if not negative_instance:
                    automaton, nbr_objectives, colors_map = intersection_example_objective_increase(nbr_copies)
                else:
                    automaton, nbr_objectives, colors_map = intersection_example_objective_increase(nbr_copies, negative_instance=True)

                result = counter_example_based_algorithm(automaton, nbr_objectives, colors_map)

            elif benchmark == "random":

                nbr_vertices = parameters[0]
                density = parameters[1]
                nbr_objectives = parameters[2]

                automaton, nbr_objectives, colors_map = random_automaton(nbr_vertices, density, nbr_objectives)

                result = counter_example_based_algorithm(automaton, nbr_objectives, colors_map)

        else:
            assert True == False