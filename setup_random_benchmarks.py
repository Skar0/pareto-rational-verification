from generate_benchmark import *

try:
    os.mkdir('random_automata_complex_64')
except FileExistsError:
    pass

print("Generating complex random automata")

for i in range(3, 16):
    print("Size 100, density 0.2, number of objectives for Player 1: " + str(i))
    aut, nbr, colors = random_automaton_complex_antichain_64(100, 0.2, i)
    antichain = compute_antichain(aut, nbr, colors, is_payoff_realizable)
    print("Size of the antichain " + str(len(antichain)))
    print("Antichain " + str(antichain))
    print()

for i in range(3, 16):
    print("Size 1000, density 0.2, number of objectives for Player 1: " + str(i))
    aut, nbr, colors = random_automaton_complex_antichain_64(1000, 0.2, i)
    antichain = compute_antichain(aut, nbr, colors, is_payoff_realizable)
    print("Size of the antichain " + str(len(antichain)))
    print("Antichain " + str(antichain))
    print()
