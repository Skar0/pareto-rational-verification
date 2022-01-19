from collections import deque, defaultdict

from verification_algorithms import smaller_than, generate_smaller_payoffs, counter_example_exists, \
    get_payoff_of_accepting_run, counter_example_dominated, add_payoff_to_antichain


def direct_antichain_algorithm_statistics(automaton, nbr_objectives, colors_map, realizable):
    """
    Direct antichain algorithm used for statistics. Returns the antichain approximation and the number
    of calls to automata emptiness.
    :param automaton: the automaton.
    :param nbr_objectives: the number t of objectives of Player 1.
    :param colors_map: maps each parity objective to the set of SPOT acceptance sets used to represent its priorities.
    :param realizable: function which decides if a (extended) payoff is realizable.
    :return: whether the PRV problem is satisfied.
    """
    maximal_payoff = tuple([1] * nbr_objectives)

    pareto_optimal_payoffs = []

    queue = deque()

    queue.append(maximal_payoff)

    visited = defaultdict(int)

    counter = 0

    while queue:

        p = queue.popleft()

        if not any(smaller_than(p, p_prime) for p_prime in pareto_optimal_payoffs):

            if realizable(p, automaton, colors_map):

                counter += 2

                pareto_optimal_payoffs.append(p)

                if realizable(p, automaton, colors_map, losing_for_0=True):

                    return False, counter, pareto_optimal_payoffs
            else:

                counter += 1

                for p_star in generate_smaller_payoffs(p):

                    if (not any(smaller_than(p_star, p_prime) for p_prime in pareto_optimal_payoffs)) and \
                            not visited[p_star]:

                        queue.append(p_star)
                        visited[p_star] = 1

    return True, pareto_optimal_payoffs, counter


def counter_example_based_statistics(automaton, nbr_objectives, colors_map):
    """
    Counter-example based algorithm used for statistics. Returns the antichain approximation and the number
    of calls to automata emptiness.
    :param automaton: the automaton.
    :param nbr_objectives: the number t of objectives of Player 1.
    :param colors_map: maps each parity objective to the set of SPOT acceptance sets used to represent its priorities.
    :return: whether the PRV problem is satisfied.
    """

    pareto_optimal_payoffs = []

    counter = 0

    while True:

        if counter_example_exists(nbr_objectives, automaton, colors_map, pareto_optimal_payoffs):

            counter += 2

            # the call to counter_example_exists modifies the acceptance condition of the automaton to check for a
            # counter example (run losing for Player 0 with payoff not dominated by a payoff in pareto_optimal_payoffs).
            # If such a counter example exists, it is an accepting run of this automaton and we retrieve its actual
            # payoff.

            counter_example_payoff = get_payoff_of_accepting_run(nbr_objectives, automaton, colors_map)

            if counter_example_dominated(nbr_objectives, automaton, colors_map, counter_example_payoff):

                # the call to counter_example_dominated modifies the acceptance condition of the automaton to check
                # whether the counter example payoff is dominated by some other payoff (winning for Player 0 and
                # strictly larger than that of counter_example_payoff). If such a larger payoff exists, it is the payoff
                # of an accepting run of this automaton and we retrieve its actual payoff.

                dominating_payoff = get_payoff_of_accepting_run(nbr_objectives, automaton, colors_map)

                # update the set of PO payoffs with this new payoff
                pareto_optimal_payoffs = add_payoff_to_antichain(pareto_optimal_payoffs, dominating_payoff)

            else:

                # a counter example is not dominated by another payoff, hence the instance is false

                return False, pareto_optimal_payoffs, counter
        else:

            counter += 1

            # there are no counter examples, hence the instance is true

            return True, pareto_optimal_payoffs, counter


def compute_antichain(automaton, nbr_objectives, colors_map, realizable):
    """
    Computes and returns the antichain of realizable payoffs in the automaton.
    :param automaton: the automaton.
    :param nbr_objectives: the number t of objectives of Player 1.
    :param colors_map: maps each parity objective to the set of SPOT acceptance sets used to represent its priorities.
    :param realizable: function which decides if a (extended) payoff is realizable.
    :return: the antichain of realizable payoffs in the automaton.
    """

    maximal_payoff = tuple([1] * nbr_objectives)

    pareto_optimal_payoffs = []

    queue = deque()

    queue.append(maximal_payoff)

    visited = defaultdict(int)

    while queue:

        p = queue.popleft()

        if not any(smaller_than(p, p_prime) for p_prime in pareto_optimal_payoffs):

            if realizable(p, automaton, colors_map):

                pareto_optimal_payoffs.append(p)

            else:

                for p_star in generate_smaller_payoffs(p):

                    if (not any(smaller_than(p_star, p_prime) for p_prime in pareto_optimal_payoffs)) and \
                            not visited[p_star]:

                        queue.append(p_star)
                        visited[p_star] = 1

    return pareto_optimal_payoffs


def compute_losing_payoffs(automaton, nbr_objectives, colors_map, realizable):
    """
    Computes and returns the antichain of realizable payoffs in the automaton as well as the set of payoffs p such that
    (0, p) is realizable.
    :param automaton: the automaton.
    :param nbr_objectives: the number t of objectives of Player 1.
    :param colors_map: maps each parity objective to the set of SPOT acceptance sets used to represent its priorities.
    :param realizable: function which decides if a (extended) payoff is realizable.
    :return: the antichain of realizable payoffs in the automaton.
    """

    maximal_payoff = tuple([1] * nbr_objectives)

    pareto_optimal_payoffs = []

    queue = deque()

    queue.append(maximal_payoff)

    visited = defaultdict(int)

    while queue:

        p = queue.popleft()

        if realizable(p, automaton, colors_map, losing_for_0=True):

            pareto_optimal_payoffs.append(p)

        for p_star in generate_smaller_payoffs(p):

            if not visited[p_star]:

                queue.append(p_star)
                visited[p_star] = 1

    return pareto_optimal_payoffs
