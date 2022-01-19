from generate_benchmark import *
import statistics
import time

try:
    os.mkdir('random_large_antichain')
except FileExistsError:
    pass

for i in list(range(15, 4, -1)):

    temp_antichain_sizes = []
    temp_nbr_payoffs_losing_player_0 = []
    temp_counter_example_antichain_sizes = []
    temp_counter_example_nbr_calls = []
    temp_direct_antichain_antichain_sizes = []
    temp_direct_antichain_nbr_calls = []

    counter_example_times_process = []
    direct_antichain_times_process = []

    counter_example_times_perf_counter = []
    direct_antichain_times_perf_counter = []

    counter_example_times = []
    direct_antichain_times = []

    for j in range(1, 21):

        print("Size 100, density 0.2, number of objectives for Player 1: " + str(i) + "-" + str(j))

        stats, aut, nbr, colors = random_large_antichain(500, 0.2, i, 0.1, 0.5, False, str(j))

        temp_antichain_sizes.append(stats[0])
        temp_nbr_payoffs_losing_player_0.append(stats[1])
        temp_counter_example_antichain_sizes.append(stats[2])
        temp_counter_example_nbr_calls.append(stats[3])
        temp_direct_antichain_antichain_sizes.append(stats[4])
        temp_direct_antichain_nbr_calls.append(stats[5])

        print(" ----- computing CE time -----")

        start_time_process = time.process_time()
        start_time_perf = time.perf_counter()
        start = time.time()

        positivity = counter_example_based_algorithm(aut, nbr, colors)

        end_time_process = time.process_time()
        end_time_perf = time.perf_counter()
        end = time.time()

        counter_example_times_process.append(float('%.2f' % (end_time_process - start_time_process)))
        counter_example_times_perf_counter.append(float('%.2f' % (end_time_perf - start_time_perf)))
        counter_example_times.append(float('%.2f' % (end - start)))

        print(" ----- computing DA time -----")

        start_time_process = time.process_time()
        start_time_perf = time.perf_counter()
        start = time.time()

        positivity = direct_antichain_algorithm(aut, nbr, colors, is_payoff_realizable)

        end_time_process = time.process_time()
        end_time_perf = time.perf_counter()
        end = time.time()

        direct_antichain_times_process.append(float('%.2f' % (end_time_process - start_time_process)))
        direct_antichain_times_perf_counter.append(float('%.2f' % (end_time_perf - start_time_perf)))
        direct_antichain_times.append(float('%.2f' % (end - start)))

        print(temp_antichain_sizes)
        print(temp_nbr_payoffs_losing_player_0)

        print(temp_counter_example_antichain_sizes)
        print(temp_counter_example_nbr_calls)
        print(counter_example_times_process)
        print(counter_example_times_perf_counter)

        print(temp_direct_antichain_antichain_sizes)
        print(temp_direct_antichain_nbr_calls)
        print(direct_antichain_times_process)
        print(direct_antichain_times_perf_counter)

    f = open("statistics_negative_instances.txt", "a")

    f.write("Size " + str(i) + "\n")

    f.write(str(temp_antichain_sizes) + "\n")
    f.write(str(temp_nbr_payoffs_losing_player_0) + "\n")

    f.write(str(temp_counter_example_antichain_sizes) + "\n")
    f.write(str(temp_counter_example_nbr_calls) + "\n")
    f.write(str(counter_example_times_process) + "\n")
    f.write(str(counter_example_times_perf_counter) + "\n")
    f.write(str(counter_example_times) + "\n")

    f.write(str(temp_direct_antichain_antichain_sizes) + "\n")
    f.write(str(temp_direct_antichain_nbr_calls) + "\n")
    f.write(str(direct_antichain_times_process) + "\n")
    f.write(str(direct_antichain_times_perf_counter) + "\n")
    f.write(str(direct_antichain_times) + "\n")

    f.write("%.2f" % statistics.mean(counter_example_times_process) + ", ")
    f.write("%.2f" % statistics.mean(counter_example_times_perf_counter) + ", ")
    f.write("%.2f" % statistics.mean(counter_example_times) + "\n")


    f.write("%.2f" % statistics.mean(direct_antichain_times_process) + ", ")
    f.write("%.2f" % statistics.mean(direct_antichain_times_perf_counter) + ", ")
    f.write("%.2f" % statistics.mean(direct_antichain_times) + "\n")

    f.write("%.2f" % statistics.mean(temp_antichain_sizes) + ", ")
    f.write("%.2f" % statistics.mean(temp_nbr_payoffs_losing_player_0) + ", ")
    f.write("%.2f" % statistics.mean(temp_counter_example_antichain_sizes) + ", ")
    f.write("%.2f" % statistics.mean(temp_counter_example_nbr_calls) + ", ")
    f.write("%.2f" % statistics.mean(temp_direct_antichain_antichain_sizes) + ", ")
    f.write("%.2f" % statistics.mean(temp_direct_antichain_nbr_calls) + "\n")

    f.write("\n")

    f.close()

"""
for i in list(range(15, 4, -1)):

    temp_antichain_sizes = []
    temp_nbr_payoffs_losing_player_0 = []
    temp_counter_example_antichain_sizes = []
    temp_counter_example_nbr_calls = []
    temp_direct_antichain_antichain_sizes = []
    temp_direct_antichain_nbr_calls = []

    for j in range(1, 11):
        print("Size 100, density 0.2, number of objectives for Player 1: " + str(i) + "-" + str(j))

        stats, aut, nbr, colors = random_large_antichain(500, 0.2, i, 0.1, 0.5, False, str(j))

        temp_antichain_sizes.append(stats[0])
        temp_nbr_payoffs_losing_player_0.append(stats[1])
        temp_counter_example_antichain_sizes.append(stats[2])
        temp_counter_example_nbr_calls.append(stats[3])
        temp_direct_antichain_antichain_sizes.append(stats[4])
        temp_direct_antichain_nbr_calls.append(stats[5])

        print(temp_antichain_sizes)
        print(temp_nbr_payoffs_losing_player_0)
        print(temp_counter_example_antichain_sizes)
        print(temp_counter_example_nbr_calls)
        print(temp_direct_antichain_antichain_sizes)
        print(temp_direct_antichain_nbr_calls)

    f = open("stats_negative.txt", "a")

    f.write("Size " + str(i) + "\n")

    f.write(str(temp_antichain_sizes) + "\n")
    f.write(str(temp_nbr_payoffs_losing_player_0) + "\n")
    f.write(str(temp_counter_example_antichain_sizes) + "\n")
    f.write(str(temp_counter_example_nbr_calls) + "\n")
    f.write(str(temp_direct_antichain_antichain_sizes) + "\n")
    f.write(str(temp_direct_antichain_nbr_calls) + "\n")

    f.write("%.2f" % statistics.mean(temp_antichain_sizes) + " ,")
    f.write("%.2f" % statistics.mean(temp_nbr_payoffs_losing_player_0) + " ,")
    f.write("%.2f" % statistics.mean(temp_counter_example_antichain_sizes) + " ,")
    f.write("%.2f" % statistics.mean(temp_counter_example_nbr_calls) + " ,")
    f.write("%.2f" % statistics.mean(temp_direct_antichain_antichain_sizes) + " ,")
    f.write("%.2f" % statistics.mean(temp_direct_antichain_nbr_calls) + " ,\n")

    f.write("\n")

    f.close()

"""
# pour negatif         stats, aut, nbr, colors = random_large_antichain(100, 0.2, i, 0.2, 0.5, False, str(j))
"""
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
"""
