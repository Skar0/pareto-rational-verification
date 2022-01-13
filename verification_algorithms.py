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
