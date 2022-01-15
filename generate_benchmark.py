import sys
SPOT_INSTALL = "/Users/clement/spot-2.10.2-install-fixed/"
sys.path.insert(0, SPOT_INSTALL + "lib/python3.8/site-packages")
import spot
import buddy
import random
import os

from verification_algorithms import direct_antichain_algorithm, is_payoff_realizable

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
    :return: the constructed automaton without any acceptance condition.
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

    return aut, 4, {0: [0, 1], 1: [2, 3], 2: [4, 5], 3: [6, 7], 4: [8, 9]}


def intersection_example_objective_increase(k, negative_instance=False):
    """
    Construct the automaton for the intersection example where the number of objectives is incremented as follows. The
    automaton consists of k copies of the intersection game, with a new "root" vertex leading to them. In each copy,
    the two objectives for cars c2 and c2 are unique to that copy. Therefore, overall, the number of objectives of
    Player 1 is 2 + k * 2 (the first and last objectives of the example are unchanged and there are 2 unique objectives
    per copy). If in the original intersection example, some vertex v has a loop giving it payoff (0, 1, 0, 1), then if
    k=2 the payoff for that loop in the first copy is (0, 1, 0, 0, 0, 1) and  (0, 0, 0, 1, 0, 1) in the second. The
    encoding used is the same as the one used in intersection_example.

    :param k: the number of objectives of Player 1 is 2 + 2 * k and the number of states is 1 + k * 22.
    :param negative_instance: make the instance of the problem negative by adding a PO payoff losing for Player 0.
    :return: the constructed automaton without any acceptance condition.
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

    return aut, 2 + 2 * k, colors_map


def intersection_example_objective_increase_special_encoding(k, negative_instance=False):
    """
    Same as intersection_example_objective_increase but we only use one priority per priority function (which allows
    to generate a larger maximal number of priorities). In order for the example-based algorithm to work, some code
    should be uncommented in get_payoff_of_accepting_run.

    :param k: the number of objectives of Player 1 is 2 + 2 * k and the number of states is 1 + k * 22.
    :param negative_instance: make the instance of the problem negative by adding a PO payoff losing for Player 0.
    :return: the constructed automaton without any acceptance condition.
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

        omega_0_sat = [0]
        omega_0_unsat = []

        omega_1_sat = [1]
        omega_1_unsat = []

        first_suffix = []
        zero_zero = []
        zero_one = [3 + 2 * i]
        one_zero = [2 + 2 * i]

        second_suffix = []
        omega_4_sat = [2 * (k + 1)]
        omega_4_unsat = []


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

    # one single priority per function
    for i in range(3 + 2 * k):
        colors_map[i] = [i]

    return aut, 2 + 2 * k, colors_map


def random_automaton(nbr_vertices, density, nbr_objectives):
    """
    Construct a random generalized parity automaton with the following encoding. We use one acceptance set per priority
    per parity objective (0 is priority 0 for the first function, 1 is priority 1 for the first function, 2 is priority
    0 for the second function, and so on). The number of vertices of the automaton is provided by nbr_vertices and each
    vertex has a set of outgoing edges controlled by the density parameter (0 meaning a single edge and 1 meaning an
    edge to every other vertex). The nbr_objectives parameter corresponds to the number of objectives of Player 1 and
    therefore to the number of parity objectives in the automaton. The priorities are distributed evenly among the
    functions such that the total number of acceptance sets does not go past 32.

    :param nbr_vertices: number of vertices in the generated automaton.
    :param density: between 0 (single outgoing edge) and 1 (fully connected graph).
    :param nbr_objectives: number of objectives for Player 1 (max is 15).
    :return: the constructed automaton.
    """
    total_nbr_objectives = nbr_objectives + 1
    total_nbr_sets = 32
    nbr_priorities_per_objective = total_nbr_sets//total_nbr_objectives

    actual_number = nbr_priorities_per_objective * total_nbr_objectives
    colors_map = {}

    current_min = 0
    for i in range(total_nbr_objectives):
        colors_map[i] = list(range(current_min, current_min + nbr_priorities_per_objective))
        current_min += nbr_priorities_per_objective

    file_path = "random_automata/random-" + str(nbr_vertices) + "-" + str(density) + "-" + str(nbr_objectives) + ".hoa"
    # if the automaton has already been generated
    if os.path.isfile(file_path):
        aut = None
        for a in spot.automata(file_path):
            aut = a
        return aut, nbr_objectives, colors_map

    # -H is output in hoa, A is the acceptance condition with the number of sets, Q is the number of vertices, n is the
    # number of automata and 1 is the number of atomic propositions
    aut = next(spot.automata(SPOT_INSTALL + "bin/randaut -A" + str(actual_number) + " -H -Q" + str(nbr_vertices) +
                             " -e" + str(density) + " -n1 1|"))
    # using the actual number of acceptance sets might not be necessary when generating a random aut since they are
    # replaced.

    # each transition in the automaton will have one acceptance set (priority) per priority function
    for s in range(0, aut.num_states()):

        # outgoing transition from s, they should all have the same priority vector (the original arena is state-based)
        transition_priorities = []

        # for each function, select a random acceptance set (priority) between its min and max set
        for i in range(total_nbr_objectives):
            transition_priorities.append(random.randint(min(colors_map[i]), max(colors_map[i])))

        # add the same vector for each transition
        for t in aut.out(s):
            t.acc = spot.mark_t(transition_priorities)

    # if the automaton is newly generated, save it
    aut.save(file_path)

    return aut, nbr_objectives, colors_map


def random_automaton_positive_instances(nbr_vertices, density, nbr_objectives):
    """
    Same as random_automaton but only yields positive instances of the problem.

    :param nbr_vertices: number of vertices in the generated automaton.
    :param density: between 0 (single outgoing edge) and 1 (fully connected graph).
    :param nbr_objectives: number of objectives for Player 1 (max is 15).
    :return: the constructed automaton.
    """
    total_nbr_objectives = nbr_objectives + 1
    total_nbr_sets = 32
    nbr_priorities_per_objective = total_nbr_sets//total_nbr_objectives

    actual_number = nbr_priorities_per_objective * total_nbr_objectives
    colors_map = {}

    current_min = 0
    for i in range(total_nbr_objectives):
        colors_map[i] = list(range(current_min, current_min + nbr_priorities_per_objective))
        current_min += nbr_priorities_per_objective

    file_path = "random_automata/random-" + str(nbr_vertices) + "-" + str(density) + "-" + str(nbr_objectives) + \
                "-positive.hoa"
    # if the automaton has already been generated
    if os.path.isfile(file_path):
        aut = None
        for a in spot.automata(file_path):
            aut = a
        return aut, nbr_objectives, colors_map

    found = False
    aut = None

    while not found:
        # -H is output in hoa, A is the acceptance condition with the number of sets, Q is the number of vertices, n is the
        # number of automata and 1 is the number of atomic propositions
        aut = next(spot.automata(SPOT_INSTALL + "bin/randaut -A" + str(actual_number) + " -H -Q" + str(nbr_vertices) +
                                 " -e" + str(density) + " -n1 1|"))
        # using the actual number of acceptance sets might not be necessary when generating a random aut since they are
        # replaced.

        # each transition in the automaton will have one acceptance set (priority) per priority function
        for s in range(0, aut.num_states()):

            # outgoing transition from s, they should all have the same priority vector (the original arena is state-based)
            transition_priorities = []

            # min even priority will appear more often to satisfy objective of Player 0 more often
            test = random.random()
            if test <= 0.2:
                transition_priorities.append(random.randint(min(colors_map[0]), max(colors_map[0])))
            else:
                transition_priorities.append(min(colors_map[0]))


            # for each function, select a random acceptance set (priority) between its min and max set
            for i in range(1, total_nbr_objectives):
                transition_priorities.append(random.randint(min(colors_map[i]), max(colors_map[i])))

            # add the same vector for each transition
            for t in aut.out(s):
                t.acc = spot.mark_t(transition_priorities)

        found = direct_antichain_algorithm(aut, nbr_objectives, colors_map, is_payoff_realizable)

    # if the automaton is newly generated, save it
    aut.save(file_path)

    return aut, nbr_objectives, colors_map

