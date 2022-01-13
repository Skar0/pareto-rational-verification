import sys
sys.path.insert(0, "/Users/clement/spot-2.10.2-install/lib/python3.8/site-packages")
import spot

from collections import deque, defaultdict


def smaller_than(p, p_prime):
    """
    :param p: the first payoff.
    :param p_prime: the second payoff.
    :return: whether p <= p_prime.
    """

    return all(p[i] <= p_prime[i] for i in range(len(p)))


def generate_smaller_payoffs(p):
    """
    :param p: a payoff.
    :return: the list of payoffs strictly smaller than p by one objective.
    """

    payoffs = []
    for i in range(len(p)):
        if p[i] == 1:
            payoffs.append(p[:i] + tuple([0]) + p[i + 1:])
    return payoffs


def generate_larger_payoffs(p):
    """
    :param p: a payoff.
    :return: the list of payoffs strictly larger than p by one objective.
    """

    payoffs = []
    for i in range(len(p)):
        if p[i] == 0:
            payoffs.append(p[:i] + tuple([1]) + p[i + 1:])
    return payoffs


def add_payoff_to_antichain(pareto_optimal_payoffs, dominating_payoff):
    """
    Add a payoff to the antichain of PO payoffs. Removes all dominated payoffs. By construction, the newly added payoff
    is strictly larger or incomparable to those of the antichain of PO payoffs and will therefore be in the new list of
    PO payoffs.
    :param pareto_optimal_payoffs: the list of PO payoffs.
    :param dominating_payoff: the new payoff to add.
    :return: the new list of PO payoffs.
    """

    # TODO use a filter to filter out smaller elements
    new_list = [dominating_payoff]

    for payoff in pareto_optimal_payoffs:
        # check if the payoff is smaller or equal to the dominated payoff (it cannot be equal as the dominating payoff
        # is strictly larger or incomparable to every payoff in the set by construction). If it is not, the payoff is
        # therefore strictly larger to or incomparable to dominating_payoff and is added to the set.
        if not smaller_than(payoff, dominating_payoff):
            new_list.append(payoff)

    return new_list


def parity_to_acceptance(colors, opposite=False):
    """
    Create an acceptance condition corresponding to a parity objective.
    :param colors: the SPOT acceptance sets used for the priority function of the parity objective.
    :param opposite: whether to create the condition for the opposite objective (satisfied iff the original is not).
    :return: the SPOT acceptance condition in string format.
    """

    # the number n used in the "parity min even n" is the number of colors used from 0 to n-1
    # the << shifts the colors to start from min_color
    min_color = min(colors)
    if not opposite:
        return spot.acc_code("parity min even "+str(len(colors))) << min_color
    else:
        return spot.acc_code("parity min odd "+str(len(colors))) << min_color


def is_payoff_realizable(p, automaton, colors_map, losing_for_0=False):
    """
    Whether the payoff is realizable.
    :param p: a payoff.
    :param automaton: the automaton.
    :param colors_map: maps each parity objective to the set of SPOT acceptance sets used to represent its priorities.
    :param losing_for_0: whether we check for the extended payoff (0, p).
    :return: whether the payoff p can be realized by a run in the automaton, i.e., whether the language of the automaton
    is empty given the acceptance condition corresponding to the payoff.
    """

    first = True
    acc = None

    # for each objective satisfied in p, create the acceptance code and add it with a conjunction
    for i in range(1, len(p) + 1):
        if p[i - 1] == 1:
            if first:
                acc = parity_to_acceptance(colors_map[i])
                first = False
            else:
                acc &= parity_to_acceptance(colors_map[i])

    # if there was no satisfied objective in the payoff, it cannot be encoded properly and we encode it as the
    # conjunction of the opposite of all objectives
    if first:
        assert True == False
        for i in range(1, len(p) + 1):
                if first:
                    acc = parity_to_acceptance(colors_map[i], opposite=True)
                    first = False
                else:
                    acc &= parity_to_acceptance(colors_map[i], opposite=True)

    # if the extended payoff is (0,p) add a conjunction with the opposite of objective 0
    if losing_for_0:
        acc &= parity_to_acceptance(colors_map[0], opposite=True)

    acceptance_condition = spot.acc_cond(acc.used_sets().max_set(), acc)
    automaton.set_acceptance(acceptance_condition)

    # the payoff is realizable if the language of the automaton is not empty
    return not automaton.is_empty()


def direct_antichain_algorithm(automaton, nbr_objectives, colors_map, realizable):
    """
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

    while queue:
        p = queue.popleft()

        if not any(smaller_than(p, p_prime) for p_prime in pareto_optimal_payoffs):

            if realizable(p, automaton, colors_map):

                pareto_optimal_payoffs.append(p)

                if realizable(p, automaton, colors_map, losing_for_0=True):

                    return False
            else:

                for p_star in generate_smaller_payoffs(p):

                    if (not any(smaller_than(p_star, p_prime) for p_prime in pareto_optimal_payoffs)) and \
                            not visited[p_star]:

                        queue.append(p_star)
                        visited[p_star] = 1

    return True


def conjunction_of_satisfied_objectives_in_p(nbr_objectives, p, colors_map):
    """
    Create the conjunction of acceptance codes for each objective satisfied in the payoff p.
    :param nbr_objectives: number of objectives of Player 1.
    :param p: a payoff.
    :param colors_map: maps each parity objective to the set of SPOT acceptance sets used to represent its priorities.
    :return: the required conjunction, and None if there are no satisfied objectives.
    """

    # whether we already found a satisfied objective in the payoff
    first = True
    acc = None

    # for each objective satisfied in p, create the acceptance code and add it with a conjunction
    for i in range(1, nbr_objectives + 1):

        if p[i - 1] == 1:

            # if this is the first objective to be satisfied
            if first:
                acc = parity_to_acceptance(colors_map[i])
                first = False
            else:
                acc &= parity_to_acceptance(colors_map[i])

    return acc


def disjunction_of_unsatisfied_objectives_in_p(nbr_objectives, p, colors_map):
    """
    Create the disjunction of acceptance codes for each objective unsatisfied in the payoff p.
    :param nbr_objectives: number of objectives of Player 1.
    :param p: a payoff.
    :param colors_map: maps each parity objective to the set of SPOT acceptance sets used to represent its priorities.
    :return: the required disjunction, and None if there are no unsatisfied objectives.
    """

    # whether we already found an unsatisfied objective in the payoff
    first = True
    acc = None

    # for each objective unsatisfied in p, create the acceptance code and add it with a disjunction
    for i in range(1, nbr_objectives + 1):

        if p[i - 1] == 0:

            # if this is the first objective to be satisfied
            if first:
                acc = parity_to_acceptance(colors_map[i])
                first = False
            else:
                acc |= parity_to_acceptance(colors_map[i])

    return acc


def counter_example_exists(nbr_objectives, automaton, colors_map, pareto_optimal_payoffs):
    """
    Check for the existence of a run with a payoff equal or larger or incomparable to every payoff in the current
    antichain of PO payoffs and that is losing for Player 0.
    :param nbr_objectives: number of objectives of Player 1.
    :param automaton: the automaton.
    :param colors_map: maps each parity objective to the set of SPOT acceptance sets used to represent its priorities.
    :param pareto_optimal_payoffs: current antichain of PO payoffs.
    :return: whether an accepting run for the condition mentioned above exists.
    """

    # acceptance condition should be losing for Player 0
    acc = parity_to_acceptance(colors_map[0], opposite=True)

    # for each PO payoff in the antichain, we want the conjunction of its satisfied objectives (meaning accepting runs
    # whose payoff is equal or larger to this payoff) and add it to a disjunction of its unsatisfied objectives (meaning
    # accepting runs whose payoff is incomparable to or strictly larger than this payoff). We combine the two with a
    # disjunction since it should satisfy either condition and this is combined as a conjunction for every PO payoff.
    for payoff in pareto_optimal_payoffs:

        conj_of_sat_obj_in_payoff = conjunction_of_satisfied_objectives_in_p(nbr_objectives, payoff, colors_map)

        disj_of_unsat_obj_in_payoff = disjunction_of_unsatisfied_objectives_in_p(nbr_objectives, payoff, colors_map)

        # the two should be combined with a disjunction, but it may be the case that either is empty in case of all 0 or
        # all 1 in payoffs

        # if they are not empty, we do a disjunction between them and add them to the acceptance as a conjunction
        if (conj_of_sat_obj_in_payoff is not None) and (disj_of_unsat_obj_in_payoff is not None):
            temp = conj_of_sat_obj_in_payoff | disj_of_unsat_obj_in_payoff
            acc &= temp
        # if the conjunction is not empty but the disjunction is, only add the conjunction to the acceptance
        elif (conj_of_sat_obj_in_payoff is not None) and (disj_of_unsat_obj_in_payoff is None):
            acc &= conj_of_sat_obj_in_payoff
        # if the disjunction is not empty but the conjunction is, only add the disjunction to the acceptance
        elif (disj_of_unsat_obj_in_payoff is not None) and (conj_of_sat_obj_in_payoff is None):
            acc &= disj_of_unsat_obj_in_payoff

    # notice that if there are no payoffs in pareto_optimal_payoffs, we only ask for a losing play for Player 0

    acceptance_condition = spot.acc_cond(acc.used_sets().max_set(), acc)
    automaton.set_acceptance(acceptance_condition)

    return not automaton.is_empty()


def counter_example_dominated(nbr_objectives, automaton, colors_map, counter_example_payoff):
    """
    Check for the existence of a run with a payoff strictly larger to counter_example_payoff and that is winning for
    Player 0.
    :param nbr_objectives: number of objectives of Player 1.
    :param automaton: the automaton.
    :param colors_map: maps each parity objective to the set of SPOT acceptance sets used to represent its priorities.
    :param counter_example_payoff: the counter-example payoff to dominate.
    :return: whether an accepting run for the condition mentioned above exists.
    """

    # acceptance condition should be winning for Player 0
    acc = parity_to_acceptance(colors_map[0])

    first = False
    disj_for_each_payoffs = None

    # for each payoff strictly larger than counter_example_payoff by one objective, we want the conjunction of its
    # satisfied objectives (meaning accepting runs whose payoff is equal or larger to this payoff). We combine them with
    # a disjunction since we want a run with at least a strictly larger payoff.
    for payoff in generate_larger_payoffs(counter_example_payoff):

        conj_of_sat_obj_in_payoff = conjunction_of_satisfied_objectives_in_p(nbr_objectives, payoff, colors_map)

        # if this is the first conjunction in the disjunction; notice that the conjunction can never be empty as
        # there is at least one objective satisfied in payoff (since the smallest payoffs yielded by the call contain
        # exactly one satisfied objective).
        if first:
            disj_for_each_payoffs = conj_of_sat_obj_in_payoff
            first = False
        else:
            disj_for_each_payoffs |= conj_of_sat_obj_in_payoff

    # notice that if there are no payoffs larger than the counter example payoff (as it only contains ones), we return
    # false as it cannot be dominated.
    if disj_for_each_payoffs is None:
        return False
    # if the disjunction is not empty (at least one larger payoff exists), do a conjunction with acc
    else:
        acc &= disj_for_each_payoffs

    acceptance_condition = spot.acc_cond(acc.used_sets().max_set(), acc)
    automaton.set_acceptance(acceptance_condition)

    return not automaton.is_empty()


def get_payoff_of_accepting_run(nbr_objectives, automaton, colors_map):
    """
    Retrieve an accepting run of the automaton and compute the payoff of this run.
    :param nbr_objectives: number of objectives of Player 1.
    :param automaton: the automaton.
    :param colors_map: maps each parity objective to the set of SPOT acceptance sets used to represent its priorities.
    :return: the payoff of an accepting run of the automaton.
    """

    # priorities occurring infinitely often for each priority function
    inf_priorities = [[] for _ in range(nbr_objectives + 1)]

    # retrieve an accepting run for the current acceptance condition
    run = automaton.accepting_run()

    # for each transition in the cycle part of the run
    for trans in run.cycle:
        i = 0
        # for each acceptance set in the transition (of which there are nbr_objectives + 1 by construction)
        for acc_set in trans.acc.sets():
            # add the acceptance set to the list of occurring priorities for the correct function
            inf_priorities[i].append(acc_set)
            i += 1

    # minimum priorities occurring infinitely often
    min_priorities = []
    for i in range(0, nbr_objectives + 1):
        min_priorities.append(min(inf_priorities[i]))

    # compute the payoff from this minimum priority (acceptance set) occurring infinitely often, omitting Player 0
    payoff = []
    for i in range(1, nbr_objectives + 1):
        # if the minimum priority and minimum acceptance set from colors_map given a parity objective are of the same
        # parity then the objective is satisfied.
        if (min_priorities[i] % 2) == (min(colors_map[i]) % 2):
            payoff.append(1)
        else:
            payoff.append(0)

    # return the payoff (which are tuples)
    return tuple(payoff)


def counter_example_based_algorithm(automaton, nbr_objectives, colors_map):
    """
    :param automaton: the automaton.
    :param nbr_objectives: the number t of objectives of Player 1.
    :param colors_map: maps each parity objective to the set of SPOT acceptance sets used to represent its priorities.
    :return: whether the PRV problem is satisfied.
    """

    pareto_optimal_payoffs = []

    while True:
        if counter_example_exists(nbr_objectives, automaton, colors_map, pareto_optimal_payoffs):

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

                return False
        else:

            # there are no counter examples, hence the instance is true

            return True
