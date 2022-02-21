import spot
import buddy
import random
import os
from statistics import compute_antichain, counterexample_based_statistics, \
    antichain_optimization_algorithm_statistics, compute_losing_payoffs
from verification_algorithms import is_payoff_realizable, counterexample_based_algorithm


def intersection_example(k, negative_instance=False):
    """
    Construct the automaton for the intersection example with the following encoding. We omit to give priorities to
    edges of the example which are not loops (as they are not important to determine the satisfied objectives). We use
    one acceptance set per priority per parity objective. If a vertex in the example loops and has extended payoff
    1, (1, 0, 0, 1), since there are two priorities used in each function of the example, then the loop has acceptance
    sets (0, 2, 5, 7, 8). (0 is priority 0 for the first function, 1 is priority 1 for the first function, 2 is priority
    0 for the second function, and so on).

    The resulting automaton corresponds to k copies of the intersection game, with a new "root" vertex leading to them.

    :param k: the number of objectives of Player 1 remains 4 and the number of states is 1 + k * 22.
    :param negative_instance: make the instance of the problem negative by adding a PO payoff losing for Player 0.
    :return: stats, aut, nbr_objectives, colors_map where stats are the following statistics on the automaton aut:
    size of antichain of realizable payoffs, size of set of realizable losing payoffs, size of set of all realizable
    payoffs, size of antichain approximation for the counterexample algorithm on this automaton, call statistics for the
    counterexample algorithm, size of antichain approximation for the antichain optimization algorithm on this
    automaton,  call statistics for the  antichain optimization algorithm.
    """

    bdict = spot.make_bdd_dict()
    aut = spot.make_twa_graph(bdict)
    p1 = buddy.bdd_ithvar(aut.register_ap("p"))

    # declare the number of states
    aut.new_states(1 + 22 * k)
    # states are labeled from 0, last state is going to be the new root
    new_root = (22 * k)
    aut.set_init_state(new_root)

    index = 0
    for i in range(k):

        aut.new_edge(new_root, index, p1, [])

        aut.new_edge(0 + index, 0 + index, p1, [1, 3, 5, 7, 9])

        #
        aut.new_edge(0 + index, 1 + index, p1, [])
        aut.new_edge(1 + index, 1 + index, p1, [0, 3, 5, 7, 9])

        aut.new_edge(1 + index, 2 + index, p1, [])
        aut.new_edge(2 + index, 2 + index, p1, [0, 3, 4, 7, 9])

        aut.new_edge(2 + index, 3 + index, p1, [])
        aut.new_edge(3 + index, 3 + index, p1, [0, 2, 4, 7, 9])

        aut.new_edge(1 + index, 4 + index, p1, [])
        aut.new_edge(4 + index, 4 + index, p1, [0, 3, 5, 6, 9])

        aut.new_edge(4 + index, 5 + index, p1, [])
        aut.new_edge(5 + index, 5 + index, p1, [0, 2, 5, 6, 9])

        #
        aut.new_edge(0 + index, 6 + index, p1, [])
        aut.new_edge(6 + index, 6 + index, p1, [1, 3, 4, 7, 9])

        aut.new_edge(6 + index, 7 + index, p1, [])
        aut.new_edge(7 + index, 7 + index, p1, [0, 3, 4, 7, 9])

        aut.new_edge(7 + index, 8 + index, p1, [])
        aut.new_edge(8 + index, 8 + index, p1, [0, 2, 4, 7, 9])

        aut.new_edge(6 + index, 9 + index, p1, [])
        aut.new_edge(9 + index, 9 + index, p1, [1, 3, 4, 7, 9])

        aut.new_edge(9 + index, 10 + index, p1, [])
        aut.new_edge(10 + index, 10 + index, p1, [0, 2, 4, 7, 9])

        #
        aut.new_edge(0 + index, 11 + index, p1, [])
        aut.new_edge(11 + index, 11 + index, p1, [1, 3, 5, 6, 9])

        aut.new_edge(11 + index, 12 + index, p1, [])
        aut.new_edge(12 + index, 12 + index, p1, [0, 3, 5, 6, 9])

        aut.new_edge(12 + index, 13 + index, p1, [])
        aut.new_edge(13 + index, 13 + index, p1, [0, 2, 5, 6, 9])

        aut.new_edge(11 + index, 14 + index, p1, [])
        aut.new_edge(14 + index, 14 + index, p1, [1, 3, 5, 6, 9])

        aut.new_edge(14 + index, 15 + index, p1, [])
        aut.new_edge(15 + index, 15 + index, p1, [0, 2, 5, 6, 9])

        #
        aut.new_edge(0 + index, 16 + index, p1, [])
        aut.new_edge(16 + index, 16 + index, p1, [1, 3, 5, 7, 8])

        aut.new_edge(16 + index, 17 + index, p1, [])
        aut.new_edge(17 + index, 17 + index, p1, [1, 2, 5, 7, 8])

        #
        aut.new_edge(0 + index, 18 + index, p1, [])
        aut.new_edge(18 + index, 18 + index, p1, [0, 3, 5, 6, 8])

        aut.new_edge(18 + index, 19 + index, p1, [])
        if negative_instance:
            aut.new_edge(19 + index, 19 + index, p1, [1, 2, 5, 6, 8])
        else:
            aut.new_edge(19 + index, 19 + index, p1, [0, 2, 5, 6, 8])

        #
        aut.new_edge(0 + index, 20 + index, p1, [])
        aut.new_edge(20 + index, 20 + index, p1, [1, 3, 5, 7, 8])

        aut.new_edge(20 + index, 21 + index, p1, [])
        aut.new_edge(21 + index, 21 + index, p1, [1, 3, 5, 7, 8])

        index += 22

    t = 4
    colors_map = {0: [0, 1], 1: [2, 3], 2: [4, 5], 3: [6, 7], 4: [8, 9]}

    print("--- computing payoff statistics ---")
    antichain = compute_antichain(aut, t, colors_map, is_payoff_realizable)
    all_possible_realizable, losing_payoffs = compute_losing_payoffs(aut, t, colors_map, is_payoff_realizable)
    print("--- computing counterexample algorithm statistics ---")
    _, ce_antichain_approximation, ce_exists_call_stats, ce_dominated_calls_stats, _ = \
        counterexample_based_statistics(aut, t, colors_map)
    print("--- computing antichain optimization algorithm statistics ---")
    _, ao_antichain_approximation, ao_realizable_stats, ao_realizable_losing_stats = \
        antichain_optimization_algorithm_statistics(aut, t, colors_map, is_payoff_realizable)

    stats = [len(antichain),
             len(losing_payoffs),
             len(all_possible_realizable),
             len(ce_antichain_approximation),
             ce_exists_call_stats,
             ce_dominated_calls_stats,
             len(ao_antichain_approximation),
             ao_realizable_stats,
             ao_realizable_losing_stats
             ]

    return stats, aut, t, colors_map


def intersection_example_objective_increase(k, negative_instance=False):
    """
    Construct the automaton for the intersection example where the number of objectives is incremented as follows. The
    automaton consists of k copies of the intersection game, with a new "root" vertex leading to them. In each copy,
    the two objectives for cars c2 and c3 are unique to that copy. Therefore, overall, the number of objectives of
    Player 1 is 2 + k * 2 (the first and last objectives of the example are unchanged and there are 2 unique objectives
    per copy). If in the original intersection example, some vertex v has a loop giving it payoff (0, 1, 0, 1), then if
    k=2 the payoff for that loop in the first copy is (0, 1, 0, 0, 0, 1) and  (0, 0, 0, 1, 0, 1) in the second. The
    encoding used is the same as the one used in intersection_example.

    :param k: the number of objectives of Player 1 is 2 + 2 * k and the number of states is 1 + k * 22.
    :param negative_instance: make the instance of the problem negative by adding a PO payoff losing for Player 0.
    :return: stats, aut, nbr_objectives, colors_map where stats are the following statistics on the automaton aut:
    size of antichain of realizable payoffs, size of set of realizable losing payoffs, size of set of all realizable
    payoffs, size of antichain approximation for the counterexample algorithm on this automaton, call statistics for the
    counterexample algorithm, size of antichain approximation for the antichain optimization algorithm on this
    automaton,  call statistics for the  antichain optimization algorithm.
    """

    bdict = spot.make_bdd_dict()
    aut = spot.make_twa_graph(bdict)
    p1 = buddy.bdd_ithvar(aut.register_ap("p"))

    # declare the number of states
    aut.new_states(1 + 22 * k)
    # states are labeled from 0, last state is going to be the new root
    new_root = (22 * k)
    aut.set_init_state(new_root)

    index = 0

    for i in range(k):

        # the satisfied objectives, properly shifted to create the payoffs
        omega_0_sat = [0]
        omega_0_unsat = [1]

        omega_1_sat = [2]
        omega_1_unsat = [3]

        first_suffix = list(range(5, 5 + 4 * i, 2))
        zero_zero = [5 + 4 * i, 7 + 4 * i]
        zero_one = [5 + 4 * i, 6 + 4 * i]
        one_zero = [4 + 4 * i, 7 + 4 * i]

        second_suffix = list(range(9 + 4 * i, 1 + 4 * (k + 1), 2))
        omega_4_sat = [4 * (k + 1)]
        omega_4_unsat = [4 * (k + 1) + 1]

        aut.new_edge(new_root, index, p1, [])

        aut.new_edge(0 + index, 0 + index, p1,
                     omega_0_unsat + omega_1_unsat + first_suffix + zero_zero + second_suffix + omega_4_unsat)

        #
        aut.new_edge(0 + index, 1 + index, p1, [])
        aut.new_edge(1 + index, 1 + index, p1,
                     omega_0_sat + omega_1_unsat + first_suffix + zero_zero + second_suffix + omega_4_unsat)

        aut.new_edge(1 + index, 2 + index, p1, [])
        aut.new_edge(2 + index, 2 + index, p1,
                     omega_0_sat + omega_1_unsat + first_suffix + one_zero + second_suffix + omega_4_unsat)

        aut.new_edge(2 + index, 3 + index, p1, [])
        aut.new_edge(3 + index, 3 + index, p1,
                     omega_0_sat + omega_1_sat + first_suffix + one_zero + second_suffix + omega_4_unsat)

        aut.new_edge(1 + index, 4 + index, p1, [])
        aut.new_edge(4 + index, 4 + index, p1,
                     omega_0_sat + omega_1_unsat + first_suffix + zero_one + second_suffix + omega_4_unsat)

        aut.new_edge(4 + index, 5 + index, p1, [])
        aut.new_edge(5 + index, 5 + index, p1,
                     omega_0_sat + omega_1_sat + first_suffix + zero_one + second_suffix + omega_4_unsat)

        #
        aut.new_edge(0 + index, 6 + index, p1, [])
        aut.new_edge(6 + index, 6 + index, p1,
                     omega_0_unsat + omega_1_unsat + first_suffix + one_zero + second_suffix + omega_4_unsat)

        aut.new_edge(6 + index, 7 + index, p1, [])
        aut.new_edge(7 + index, 7 + index, p1,
                     omega_0_sat + omega_1_unsat + first_suffix + one_zero + second_suffix + omega_4_unsat)

        aut.new_edge(7 + index, 8 + index, p1, [])
        aut.new_edge(8 + index, 8 + index, p1,
                     omega_0_sat + omega_1_sat + first_suffix + one_zero + second_suffix + omega_4_unsat)

        aut.new_edge(6 + index, 9 + index, p1, [])
        aut.new_edge(9 + index, 9 + index, p1,
                     omega_0_unsat + omega_1_unsat + first_suffix + one_zero + second_suffix + omega_4_unsat)

        aut.new_edge(9 + index, 10 + index, p1, [])
        aut.new_edge(10 + index, 10 + index, p1,
                     omega_0_sat + omega_1_sat + first_suffix + one_zero + second_suffix + omega_4_unsat)

        #
        aut.new_edge(0 + index, 11 + index, p1, [])
        aut.new_edge(11 + index, 11 + index, p1,
                     omega_0_unsat + omega_1_unsat + first_suffix + zero_one + second_suffix + omega_4_unsat)

        aut.new_edge(11 + index, 12 + index, p1, [])
        aut.new_edge(12 + index, 12 + index, p1,
                     omega_0_sat + omega_1_unsat + first_suffix + zero_one + second_suffix + omega_4_unsat)

        aut.new_edge(12 + index, 13 + index, p1, [])
        aut.new_edge(13 + index, 13 + index, p1,
                     omega_0_sat + omega_1_sat + first_suffix + zero_one + second_suffix + omega_4_unsat)

        aut.new_edge(11 + index, 14 + index, p1, [])
        aut.new_edge(14 + index, 14 + index, p1,
                     omega_0_unsat + omega_1_unsat + first_suffix + zero_one + second_suffix + omega_4_unsat)

        aut.new_edge(14 + index, 15 + index, p1, [])
        aut.new_edge(15 + index, 15 + index, p1,
                     omega_0_sat + omega_1_sat + first_suffix + zero_one + second_suffix + omega_4_unsat)

        #
        aut.new_edge(0 + index, 16 + index, p1, [])
        aut.new_edge(16 + index, 16 + index, p1,
                     omega_0_unsat + omega_1_unsat + first_suffix + zero_zero + second_suffix + omega_4_sat)

        aut.new_edge(16 + index, 17 + index, p1, [])
        aut.new_edge(17 + index, 17 + index, p1,
                     omega_0_unsat + omega_1_sat + first_suffix + zero_zero + second_suffix + omega_4_sat)

        #
        aut.new_edge(0 + index, 18 + index, p1, [])
        aut.new_edge(18 + index, 18 + index, p1,
                     omega_0_sat + omega_1_unsat + first_suffix + zero_one + second_suffix + omega_4_sat)

        aut.new_edge(18 + index, 19 + index, p1, [])
        if negative_instance:
            aut.new_edge(19 + index, 19 + index, p1,
                         omega_0_unsat + omega_1_sat + first_suffix + zero_one + second_suffix + omega_4_sat)
        else:
            aut.new_edge(19 + index, 19 + index, p1,
                         omega_0_sat + omega_1_sat + first_suffix + zero_one + second_suffix + omega_4_sat)

        #
        aut.new_edge(0 + index, 20 + index, p1, [])
        aut.new_edge(20 + index, 20 + index, p1,
                     omega_0_unsat + omega_1_unsat + first_suffix + zero_zero + second_suffix + omega_4_sat)

        aut.new_edge(20 + index, 21 + index, p1, [])
        aut.new_edge(21 + index, 21 + index, p1,
                     omega_0_unsat + omega_1_unsat + first_suffix + zero_zero + second_suffix + omega_4_sat)

        index += 22

    colors_map = {}

    for i in range(3 + 2 * k):
        colors_map[i] = [i * 2, i * 2 + 1]

    t = 2 + 2 * k

    print("--- computing payoff statistics ---")
    antichain = compute_antichain(aut, t, colors_map, is_payoff_realizable)
    all_possible_realizable, losing_payoffs = compute_losing_payoffs(aut, t, colors_map, is_payoff_realizable)
    print("--- computing counterexample algorithm statistics ---")
    _, ce_antichain_approximation, ce_exists_call_stats, ce_dominated_calls_stats, _ = \
        counterexample_based_statistics(aut, t, colors_map)
    print("--- computing antichain optimization algorithm statistics ---")
    _, ao_antichain_approximation, ao_realizable_stats, ao_realizable_losing_stats = \
        antichain_optimization_algorithm_statistics(aut, t, colors_map, is_payoff_realizable)

    stats = [len(antichain),
             len(losing_payoffs),
             len(all_possible_realizable),
             len(ce_antichain_approximation),
             ce_exists_call_stats,
             ce_dominated_calls_stats,
             len(ao_antichain_approximation),
             ao_realizable_stats,
             ao_realizable_losing_stats
             ]

    return stats, aut, t, colors_map


def random_automaton(nbr_vertices, density, nbr_objectives, proba_even_general, proba_even_0, positivity, name):
    """
    Construct a random instance of the PRV problem as follows. Create a generalized parity automaton (corresponding to
    an instance where both players have parity objectives) with the following encoding. We use one acceptance set per
    priority per parity objective. The number of priorities per objective is 4 (therefore 0 is priority 0 for the first
    function, 1 is priority 1 for the first function, ..., 4 is priority 0 for the second function, and so on). The
    number of vertices of the automaton is provided by nbr_vertices and each vertex has a set of outgoing edges
    controlled by the density parameter (0 meaning a single edge and 1 meaning edges to every other vertices). The
    nbr_objectives parameter corresponds to the number of objectives of Player 1 and therefore to the number of parity
    objectives in the automaton. Note that SPOT allows for 32 acceptance sets if not compiled for a larger number. In
    order to avoid small antichains of realizable payoffs (e.g. cases where this antichain only contains (1, ..., 1)),
    the antichain of realizable payoffs in the automaton must contain at least nbr_objectives elements. Some probability
    parameters regulate the occurrence of even priorities in some functions which affects the size of this antichain and
    whether the instance is positive or negative. The positivity parameter specifies if the generated instance should be
    positive or negative. Instances keep being generated until they match required positivity and antichain size. The
    final automaton is saved to a random_automata/ folder in HOA format with the following name:
    "random-nbr_vertices-density-nbr_objectives-proba_even_general-proba_even_0-positivity-name.hoa". If this name
    already exists (and a random automaton with the required parameters has already been generated, we load this
    automaton instead of generating a new one).

    :param nbr_vertices: number of vertices in the generated automaton.
    :param density: between 0 (single outgoing edge) and 1 (fully connected graph).
    :param nbr_objectives: number of objectives for Player 1.
    :param proba_even_general: the probability of even priorities for functions 0 to nbr_objectives (if not positivity)
    and only of functions 1 to nbr_objectives (if positivity), used to control the size of the antichain of realizable
    payoffs.
    :param proba_even_0: the probability of even priorities for function 0 (if positivity), used to generate positive
    instances more often.
    :param positivity: whether we want a positive or negative instance of the problem
    :param name: since we might want to generate several automata with the same parameters we append a name to it.
    :return: stats, aut, nbr_objectives, colors_map where stats are the following statistics on the automaton aut:
    size of antichain of realizable payoffs, size of set of realizable losing payoffs, size of set of all realizable
    payoffs, size of antichain approximation for the counterexample algorithm on this automaton, call statistics for the
    counterexample algorithm, size of antichain approximation for the antichain optimization algorithm on this
    automaton,  call statistics for the  antichain optimization algorithm.
    """

    total_nbr_objectives = nbr_objectives + 1

    nbr_priorities_per_objective = 4

    actual_number = nbr_priorities_per_objective * total_nbr_objectives

    colors_map = {}

    current_min = 0
    for i in range(total_nbr_objectives):
        colors_map[i] = list(range(current_min, current_min + nbr_priorities_per_objective))
        current_min += nbr_priorities_per_objective

    file_path = "random_automata/random-" + str(nbr_vertices) + "-" + str(density) + "-" + str(nbr_objectives) + "-" + \
                str(proba_even_general) + "-" + str(proba_even_0) + "-" + str(positivity) + "-" + name + ".hoa"

    # if the automaton has already been generated
    if os.path.isfile(file_path):
        aut = None
        for a in spot.automata(file_path):
            aut = a

        print("--- automaton exists in random_automata/ ---")
        print("--- computing payoff statistics ---")
        antichain = compute_antichain(aut, nbr_objectives, colors_map, is_payoff_realizable)
        all_possible_realizable, losing_payoffs = compute_losing_payoffs(aut, nbr_objectives, colors_map,
                                                                         is_payoff_realizable)
        print("--- computing counterexample algorithm statistics ---")
        _, ce_antichain_approximation, ce_exists_call_stats, ce_dominated_calls_stats, _ = \
            counterexample_based_statistics(aut, nbr_objectives, colors_map)
        print("--- computing antichain optimization algorithm statistics ---")
        _, ao_antichain_approximation, ao_realizable_stats, ao_realizable_losing_stats = \
            antichain_optimization_algorithm_statistics(aut, nbr_objectives, colors_map, is_payoff_realizable)

        stats = [len(antichain),
                 len(losing_payoffs),
                 len(all_possible_realizable),
                 len(ce_antichain_approximation),
                 ce_exists_call_stats,
                 ce_dominated_calls_stats,
                 len(ao_antichain_approximation),
                 ao_realizable_stats,
                 ao_realizable_losing_stats
                 ]

        return stats, aut, nbr_objectives, colors_map

    # else try and generate automaton
    antichain = []
    aut = None
    instance_positivity = not positivity

    # while expected antichain size and positivity not achieved, keep generating
    while len(antichain) < nbr_objectives or instance_positivity != positivity:

        print("--- choosing random seed ---")

        # use a seed for randaut
        seed = random.randint(1, 9223372036854775807)

        print("--- calling randaut to generate automaton structure ---")

        # -H is output in hoa, A is the acceptance condition with the number of sets, Q is the number of vertices,
        # n is the number of automata and 1 is the number of atomic propositions
        aut = next(spot.automata("randaut -A" + str(actual_number) + " -H -Q" + str(nbr_vertices) + " -e" + str(density)
                                 + " --seed " + str(seed) + " -n1 1|"))
        # using the actual number of acceptance sets might not be necessary when generating a random aut since they are
        # replaced.

        print("--- assigning priorities to the structure ---")

        # each transition in the automaton will have one acceptance set (priority) per priority function
        for s in range(0, aut.num_states()):

            transition_priorities = []

            # for each function, select a random acceptance set (priority) between its min and max set
            for i in range(0, total_nbr_objectives):

                # if the current function is Player 0's
                if i == 0:
                    test_positive = random.random()

                    # with probability proba_even_0, add a random priority
                    if test_positive <= proba_even_0:
                        transition_priorities.append(random.randint(min(colors_map[0]), max(colors_map[0])))
                    else:
                        # with 1 - proba_even_0, add the smallest even priority
                        transition_priorities.append(min(colors_map[0]))
                else:
                    # with probability proba_even_general the priority is even

                    test_even = random.random()

                    if test_even <= proba_even_general:

                        # notice that min(colors_map[i]) may be odd but actually corresponds to the minimum even
                        # priority according to the ith priority function
                        even_priority = min(colors_map[i]) + 1

                        # while we have not selected a priority of the same parity as minimum (which corresponds to an
                        # even priority in the logic of the priority functions)
                        while even_priority % 2 != (min(colors_map[i]) % 2):
                            # if there are more than two priorities in the color mapping for function i, we never use
                            # the smallest even priority as objectives are too often satisfied yielding payoff (1,...,1)
                            even_priority = random.randint(min(colors_map[i]) + 2, max(colors_map[i]))

                        transition_priorities.append(even_priority)

                    # else we select an odd priority
                    else:

                        odd_priority = min(colors_map[i])

                        # while we have not selected a priority of the same parity as minimum + 1 (which corresponds to
                        # an odd priority in the logic of the priority functions)
                        while odd_priority % 2 != ((min(colors_map[i]) + 1) % 2):
                            odd_priority = random.randint(min(colors_map[i]), max(colors_map[i]))
                        transition_priorities.append(odd_priority)

                # outgoing transition from s all have the same priority vector as the original arena is state-based.
                for t in aut.out(s):
                    t.acc = spot.mark_t(transition_priorities)

        print("--- computing payoff statistics ---")
        antichain = compute_antichain(aut, nbr_objectives, colors_map, is_payoff_realizable)
        print("- generated automaton antichain size " + str(len(antichain)))
        print("- generated automaton antichain " + str(antichain))
        print("--- computing positivity ---")
        instance_positivity = counterexample_based_algorithm(aut, nbr_objectives, colors_map)
        print("- generated automaton positivity " + str(instance_positivity))

    # calling statistics functions for statistics purposes once an adequate automaton is found.

    print("--------- adequate automaton found ---------")
    print("--- computing payoff statistics ---")
    all_possible_realizable, losing_payoffs = compute_losing_payoffs(aut, nbr_objectives, colors_map,
                                                                     is_payoff_realizable)
    print("--- computing counterexample algorithm statistics ---")
    _, ce_antichain_approximation, ce_exists_call_stats, ce_dominated_calls_stats, _ = \
        counterexample_based_statistics(aut, nbr_objectives, colors_map)
    print("--- computing antichain optimization algorithm statistics ---")
    _, ao_antichain_approximation, ao_realizable_stats, ao_realizable_losing_stats = \
        antichain_optimization_algorithm_statistics(aut, nbr_objectives, colors_map, is_payoff_realizable)

    stats = [len(antichain),
             len(losing_payoffs),
             len(all_possible_realizable),
             len(ce_antichain_approximation),
             ce_exists_call_stats,
             ce_dominated_calls_stats,
             len(ao_antichain_approximation),
             ao_realizable_stats,
             ao_realizable_losing_stats
             ]

    print("--- saving automaton ---")
    # if the automaton is newly generated, save it
    aut.save(file_path)

    return stats, aut, nbr_objectives, colors_map
