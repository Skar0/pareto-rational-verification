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


def fpt_verification(automaton, nbr_objectives, colors_map, realizable):
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

def bad_example(nbr_objectives, automaton, colors_map, pareto_optimal_payoffs):
    """
    Whether the payoff is realizable.
    :param p: a payoff.
    :param automaton: the automaton.
    :param colors_map: maps each parity objective to the set of SPOT acceptance sets used to represent its priorities.
    :param losing_for_0: whether we check for the extended payoff (0, p).
    :return: whether the payoff p can be realized by a run in the automaton, i.e., whether the language of the automaton
    is empty given the acceptance condition corresponding to the payoff.
    """

    acc = parity_to_acceptance(colors_map[0], opposite=True)

    for payoff in pareto_optimal_payoffs:
        # whether we already found a satisfied objective in the payoff
        first_conj = True
        acc_conj = None
        # for each objective satisfied in p, create the acceptance code and add it with a conjunction
        for i in range(1, nbr_objectives + 1):
            if payoff[i - 1] == 1:
                if first_conj:
                    acc_conj = parity_to_acceptance(colors_map[i])
                    first_conj = False
                else:
                    acc_conj &= parity_to_acceptance(colors_map[i])

        # whether we already found an unsatisfied objective in the payoff
        first_disj = True
        acc_disj = None
        for i in range(1, nbr_objectives + 1):
            if payoff[i - 1] == 0:
                if first_disj:
                    acc_disj = parity_to_acceptance(colors_map[i])
                    first_disj = False
                else:
                    acc_disj |= parity_to_acceptance(colors_map[i])
        print(acc_conj)
        print(acc_disj)
        if not first_conj and not first_disj:
            acc &= (acc_conj | acc_disj)
        elif not first_conj and first_disj:
            acc &= acc_conj
        elif not first_disj and first_conj:
            acc &= acc_disj

    print(acc)
    acceptance_condition = spot.acc_cond(acc.used_sets().max_set(), acc)
    automaton.set_acceptance(acceptance_condition)

    print(automaton.is_empty())
    # the payoff is realizable if the language of the automaton is not empty
    return not automaton.is_empty()

def good_example(counter_example_payoff, automaton, colors_map):


    acc = parity_to_acceptance(colors_map[0])

    first_disj = True
    acc_disj = None
    for payoff in generate_larger_payoffs(counter_example_payoff):
        if first_conj:
                    acc_conj = parity_to_acceptance(colors_map[i])
                    first_conj = False
                else:
                    acc_conj &= parity_to_acceptance(colors_map[i])

        # whether we already found an unsatisfied objective in the payoff
        first_disj = True
        acc_disj = None
        for i in range(1, nbr_objectives + 1):
            if payoff[i - 1] == 0:
                if first_disj:
                    acc_disj = parity_to_acceptance(colors_map[i])
                    first_disj = False
                else:
                    acc_disj |= parity_to_acceptance(colors_map[i])
        print(acc_conj)
        print(acc_disj)
        if not first_conj and not first_disj:
            acc &= (acc_conj | acc_disj)
        elif not first_conj and first_disj:
            acc &= acc_conj
        elif not first_disj and first_conj:
            acc &= acc_disj

    print(acc)
    acceptance_condition = spot.acc_cond(acc.used_sets().max_set(), acc)
    automaton.set_acceptance(acceptance_condition)

    print(automaton.is_empty())
    # the payoff is realizable if the language of the automaton is not empty
    return not automaton.is_empty()

def counter_example(nbr_objectives, automaton, colors_map):

    inf_priorities = [[] for _ in range(nbr_objectives + 1)]

    # get a play with correct payoff, extract the payoff and return it
    run = automaton.accepting_run()

    for trans in run.cycle:
        i = 0
        for set in trans.acc.sets():
            inf_priorities[i].append(set)
            i += 1

    print(inf_priorities)
    min_priorities = []

    for i in range(0, nbr_objectives + 1):
        min_priorities.append(min(inf_priorities[i]))

    payoff = []
    for i in range(1, nbr_objectives + 1):
        if min_priorities[i] % 2 == min(colors_map[i]) % 2:
            payoff.append(1)
        else:
            payoff.append(0)

    return list(payoff)


def maximal_elements(pareto_optimal_payoffs, new_larger_payoff):
    # TODO might use a filter to filter out smaller elements
    new_list = []
    new_list.append(new_larger_payoff)
    for element in pareto_optimal_payoffs:
        if not smaller_than(element, new_larger_payoff):
            new_list.append(element)
    return new_list

def example_verification(automaton, nbr_objectives, colors_map, realizable):
    """
    :param automaton: the automaton.
    :param nbr_objectives: the number t of objectives of Player 1.
    :param colors_map: maps each parity objective to the set of SPOT acceptance sets used to represent its priorities.
    :param realizable: function which decides if a (extended) payoff is realizable.
    :return: whether the PRV problem is satisfied.
    """

    pareto_optimal_payoffs = [(1,1,1,1)]

    while True:
        print("ok")
        if bad_example(nbr_objectives, automaton, colors_map, pareto_optimal_payoffs):
            counter_example_payoff = counter_example(nbr_objectives, automaton, colors_map)
            if good_example(counter_example_payoff, automaton, colors_map):
                new_larger_payoff = counter_example(nbr_objectives, automaton, colors_map)
                pareto_optimal_payoffs = maximal_elements(pareto_optimal_payoffs, new_larger_payoff)
            else:
                return False
        else:
            return True



"""
from benchmark_generator import random_automaton
aut, nbr, map = random_automaton(1000, 0.5, 15)
print(fpt_verification(aut,nbr, map, is_payoff_realizable))
"""


from benchmark_generator import intersection_example
aut, nbr, map = intersection_example(1)
bad_example(nbr, aut, map, [(0,0,0,0)])

example_verification(aut,nbr,map,None)
