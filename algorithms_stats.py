import time
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

    counter_realizable = 0

    counter_realizable_losing = 0

    realizable_times = []

    realizable_losing_times = []

    while queue:

        p = queue.popleft()

        if not any(smaller_than(p, p_prime) for p_prime in pareto_optimal_payoffs):

            start_time_process = time.process_time()

            is_realizable = realizable(p, automaton, colors_map)

            end_time_process = time.process_time()

            counter_realizable += 1

            realizable_times.append(end_time_process-start_time_process)

            if is_realizable:

                pareto_optimal_payoffs.append(p)

                start_time_process = time.process_time()

                is_realizable_losing = realizable(p, automaton, colors_map, losing_for_0=True)

                end_time_process = time.process_time()

                counter_realizable_losing += 1

                realizable_losing_times.append(end_time_process - start_time_process)

                if is_realizable_losing:

                    return False, pareto_optimal_payoffs, [counter_realizable, realizable_times], [counter_realizable_losing, realizable_losing_times]
            else:

                for p_star in generate_smaller_payoffs(p):

                    if (not any(smaller_than(p_star, p_prime) for p_prime in pareto_optimal_payoffs)) and \
                            not visited[p_star]:

                        queue.append(p_star)
                        visited[p_star] = 1

    return True,  pareto_optimal_payoffs, [counter_realizable, realizable_times], [counter_realizable_losing, realizable_losing_times]


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

    counter_exists = 0

    counter_dominated = 0

    exists_times = []

    dominated_times = []

    while True:

        start_time_process = time.process_time()

        counter_example_ex = counter_example_exists(nbr_objectives, automaton, colors_map, pareto_optimal_payoffs)

        end_time_process = time.process_time()

        counter_exists += 1

        exists_times.append(end_time_process - start_time_process)

        if counter_example_ex:

            # the call to counter_example_exists modifies the acceptance condition of the automaton to check for a
            # counter example (run losing for Player 0 with payoff not dominated by a payoff in pareto_optimal_payoffs).
            # If such a counter example exists, it is an accepting run of this automaton and we retrieve its actual
            # payoff.

            counter_example_payoff = get_payoff_of_accepting_run(nbr_objectives, automaton, colors_map)

            start_time_process = time.process_time()

            counter_example_dom = counter_example_dominated(nbr_objectives, automaton, colors_map, counter_example_payoff)

            end_time_process = time.process_time()

            counter_dominated += 1

            dominated_times.append(end_time_process - start_time_process)

            if counter_example_dom:

                # the call to counter_example_dominated modifies the acceptance condition of the automaton to check
                # whether the counter example payoff is dominated by some other payoff (winning for Player 0 and
                # strictly larger than that of counter_example_payoff). If such a larger payoff exists, it is the payoff
                # of an accepting run of this automaton and we retrieve its actual payoff.

                dominating_payoff = get_payoff_of_accepting_run(nbr_objectives, automaton, colors_map)

                # update the set of PO payoffs with this new payoff
                pareto_optimal_payoffs = add_payoff_to_antichain(pareto_optimal_payoffs, dominating_payoff)

            else:

                # a counter example is not dominated by another payoff, hence the instance is false

                return False, pareto_optimal_payoffs, [counter_exists, exists_times], [counter_dominated, dominated_times]
        else:

            # there are no counter examples, hence the instance is true

            return True, pareto_optimal_payoffs, [counter_exists, exists_times], [counter_dominated, dominated_times]


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

    all_realizable_payoffs = []

    losing_payoffs = []

    queue = deque()

    queue.append(maximal_payoff)

    visited = defaultdict(int)

    while queue:

        p = queue.popleft()

        if realizable(p, automaton, colors_map, losing_for_0=True):

            losing_payoffs.append(p)

        if realizable(p, automaton, colors_map):

            all_realizable_payoffs.append(p)

        for p_star in generate_smaller_payoffs(p):

            if not visited[p_star]:

                queue.append(p_star)
                visited[p_star] = 1

    return all_realizable_payoffs, losing_payoffs