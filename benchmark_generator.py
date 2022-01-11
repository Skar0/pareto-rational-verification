import sys
SPOT_INSTALL = "/Users/clement/spot-2.10.2-install/"
sys.path.insert(0, SPOT_INSTALL + "lib/python3.8/site-packages")
import spot
import buddy
import random

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

    '''
    for s in range(0, aut.num_states()):
        for t in aut.out(s):
            t.acc = spot.mark_t([0, 2, 3])

    for s in range(0, aut.num_states()):
        print("State {}:".format(s))
        for t in aut.out(s):
            print("  edge({} -> {})".format(t.src, t.dst))
            # bdd_print_formula() is designed to print on a std::ostream, and
            # is inconvenient to use in Python.  Instead we use
            # bdd_format_formula() as this simply returns a string.
            print("    label =", spot.bdd_format_formula(bdict, t.cond))
            print("    acc sets =", t.acc)
    '''

    print(aut.to_str("dot"))


    return aut, 4, {0: [0, 1], 1: [2, 3], 2: [4, 5], 3: [6, 7], 4: [8, 9]}


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
    colors_map = {}

    current_min = 0
    for i in range(total_nbr_objectives):
        colors_map[i] = list(range(current_min, current_min + nbr_priorities_per_objective))
        current_min += nbr_priorities_per_objective

    # -H is output in hoa, A is the acceptance condition with the number of sets, Q is the number of vertices, n is the
    # number of automata and 1 is the number of atomic propositions
    aut = next(spot.automata(SPOT_INSTALL + "bin/randaut -A1 -H -Q+" + str(nbr_vertices) + " -e" +
                             str(density) + " -n1 1|"))

    # each transition in the automaton will have one acceptance set (priority) per priority function
    for s in range(0, aut.num_states()):
        for t in aut.out(s):
            transition_priorities = []
            for i in range(total_nbr_objectives):
                transition_priorities.append(random.randint(min(colors_map[i]), max(colors_map[i])))
            t.acc = spot.mark_t(transition_priorities)

    return aut, nbr_objectives, colors_map
