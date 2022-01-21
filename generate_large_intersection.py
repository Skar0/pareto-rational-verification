from generate_benchmark import *
import statistics
import time

try:
    os.mkdir('random_large_antichain')
except FileExistsError:
    pass

save_file = "intersection-increase-vertices-10000.txt"
size = 10000
gen_positivity = False

for i in list(range(size, 0, -500)):

    temp_antichain_sizes = []
    temp_nbr_payoffs_losing_player_0 = []
    temp_nbr_payoffs_realizable = []

    temp_counter_example_antichain_sizes = []
    temp_counter_example_nbr_calls = []
    temp_counter_example_nbr_calls_exists = []
    temp_counter_example_mean_time_calls_exists = []

    temp_counter_example_nbr_calls_dominated = []
    temp_counter_example_mean_time_calls_dominated = []


    temp_direct_antichain_antichain_sizes = []
    temp_direct_antichain_nbr_calls = []
    temp_direct_antichain_nbr_calls1 = []
    temp_direct_antichain_mean_time_calls1 = []

    temp_direct_antichain_nbr_calls2 = []
    temp_direct_antichain_mean_time_calls2 = []

    counter_example_times_process = []
    direct_antichain_times_process = []

    counter_example_times_perf_counter = []
    direct_antichain_times_perf_counter = []

    counter_example_times = []
    direct_antichain_times = []

    for j in range(1, 2):

        print("-------------------- Trying to find " + str(i) + " - " + str(j) + " --------------------")

        stats, aut, nbr, colors = intersection_example(i, negative_instance=gen_positivity)

        temp_antichain_sizes.append(stats[0])
        temp_nbr_payoffs_losing_player_0.append(stats[1])
        temp_nbr_payoffs_realizable.append(stats[2])
        temp_counter_example_antichain_sizes.append(stats[3])

        temp_counter_example_nbr_calls_exists.append(stats[4][0])
        temp_counter_example_mean_time_calls_exists.append(float("%.2f" % statistics.mean(stats[4][1])))

        temp_counter_example_nbr_calls_dominated.append(stats[5][0])
        temp_counter_example_mean_time_calls_dominated.append(float("%.2f" % statistics.mean(stats[5][1])))

        temp_counter_example_nbr_calls.append(stats[4][0] + stats[5][0])


        temp_direct_antichain_antichain_sizes.append(stats[6])

        temp_direct_antichain_nbr_calls1.append(stats[7][0])
        temp_direct_antichain_mean_time_calls1.append(float("%.2f" % statistics.mean(stats[7][1])))

        temp_direct_antichain_nbr_calls2.append(stats[8][0])
        temp_direct_antichain_mean_time_calls2.append(float("%.2f" % statistics.mean(stats[8][1])))

        temp_direct_antichain_nbr_calls.append(stats[7][0] + stats[8][0])

        print(" ----- computing CE time -----")

        start_time_process = time.process_time()
        start_time_perf = time.perf_counter()
        start = time.time()

        positivity = counter_example_based_algorithm(aut, nbr, colors)

        end_time_process = time.process_time()
        end_time_perf = time.perf_counter()
        end = time.time()

        assert positivity == gen_positivity

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

        assert positivity == gen_positivity

        direct_antichain_times_process.append(float('%.2f' % (end_time_process - start_time_process)))
        direct_antichain_times_perf_counter.append(float('%.2f' % (end_time_perf - start_time_perf)))
        direct_antichain_times.append(float('%.2f' % (end - start)))

        print(temp_antichain_sizes)
        print(temp_nbr_payoffs_losing_player_0)
        print(temp_nbr_payoffs_realizable)

        print(temp_counter_example_antichain_sizes)
        print(temp_counter_example_nbr_calls_exists)
        print(temp_counter_example_mean_time_calls_exists)
        print(temp_counter_example_nbr_calls_dominated)
        print(temp_counter_example_mean_time_calls_dominated)
        print(temp_counter_example_nbr_calls)

        print(counter_example_times_process)
        print(counter_example_times_perf_counter)

        print(temp_direct_antichain_antichain_sizes)
        print(temp_direct_antichain_nbr_calls1)
        print(temp_direct_antichain_mean_time_calls1)
        print(temp_direct_antichain_nbr_calls2)
        print(temp_direct_antichain_mean_time_calls2)
        print(temp_direct_antichain_nbr_calls)

        print(direct_antichain_times_process)
        print(direct_antichain_times_perf_counter)

    f = open(save_file, "a")

    f.write("Size " + str(i) + "\n")

    f.write("Antichain sizes " + str(temp_antichain_sizes) + "\n")
    f.write("Number of payoffs losing P0 " + str(temp_nbr_payoffs_losing_player_0) + "\n")
    f.write("Number of payoffs realizable " + str(temp_nbr_payoffs_realizable) + "\n")

    f.write("CE antichain sizes " + str(temp_counter_example_antichain_sizes) + "\n")

    f.write("CE exists calls " + str(temp_counter_example_nbr_calls_exists) + "\n")
    f.write("CE exists calls times " + str(temp_counter_example_mean_time_calls_exists) + "\n")
    f.write("CE dominated calls " + str(temp_counter_example_nbr_calls_dominated) + "\n")
    f.write("CE dominated calls times " + str(temp_counter_example_mean_time_calls_dominated) + "\n")
    f.write("CE total nbr calls " + str(temp_counter_example_nbr_calls) + "\n")

    f.write("CE times process " + str(counter_example_times_process) + "\n")
    f.write("CE times perf " +str(counter_example_times_perf_counter) + "\n")
    f.write("CE times " +str(counter_example_times) + "\n")

    f.write("DA antichain sizes " + str(temp_direct_antichain_antichain_sizes) + "\n")

    f.write("DA call1 calls " + str(temp_direct_antichain_nbr_calls1) + "\n")
    f.write("DA call1 calls times " + str(temp_direct_antichain_mean_time_calls1) + "\n")
    f.write("DA call2 calls " + str(temp_direct_antichain_nbr_calls2) + "\n")
    f.write("DA call2 calls times " + str(temp_direct_antichain_mean_time_calls2) + "\n")
    f.write("DA total nbr calls " +str(temp_direct_antichain_nbr_calls) + "\n")

    f.write("DA times process " + str(direct_antichain_times_process) + "\n")
    f.write("DA times perf " +str(direct_antichain_times_perf_counter) + "\n")
    f.write("DA times " + str(direct_antichain_times) + "\n")
    f.write("\n")

    f.write("%.2f" % statistics.mean(counter_example_times_process) + ", ")
    f.write("%.2f" % statistics.mean(counter_example_times_perf_counter) + ", ")
    f.write("%.2f" % statistics.mean(counter_example_times) + "\n")


    f.write("%.2f" % statistics.mean(direct_antichain_times_process) + ", ")
    f.write("%.2f" % statistics.mean(direct_antichain_times_perf_counter) + ", ")
    f.write("%.2f" % statistics.mean(direct_antichain_times) + "\n")

    f.write("Mean Antichain Size " + "%.2f" % statistics.mean(temp_antichain_sizes) + "\n")
    f.write("Number Losing Payoffs " + "%.2f" % statistics.mean(temp_nbr_payoffs_losing_player_0) + "\n")
    f.write("Number Realizable Payoffs " + "%.2f" % statistics.mean(temp_nbr_payoffs_realizable) + "\n")

    f.write("CE mean antichain size " + "%.2f" % statistics.mean(temp_counter_example_antichain_sizes) + "\n")
    f.write("CE nbr exists calls " + "%.2f" % statistics.mean(temp_counter_example_nbr_calls_exists) + "\n")
    f.write("CE mean exists time " + "%.2f" % statistics.mean(temp_counter_example_mean_time_calls_exists) + "\n")
    f.write("CE nbr dominated calls " + "%.2f" % statistics.mean(temp_counter_example_nbr_calls_dominated) + "\n")
    f.write("CE mean dominated time " + "%.2f" % statistics.mean(temp_counter_example_mean_time_calls_dominated) + "\n")

    f.write("CE total nbr calls " + "%.2f" % statistics.mean(temp_counter_example_nbr_calls) + "\n")



    f.write("DA mean antichain size " + "%.2f" % statistics.mean(temp_direct_antichain_antichain_sizes) + "\n")
    f.write("DA nbr call1 calls " + "%.2f" % statistics.mean(temp_direct_antichain_nbr_calls1) + "\n")
    f.write("DA mean call1 time " + "%.2f" % statistics.mean(temp_direct_antichain_mean_time_calls1) + "\n")
    f.write("DA nbr call2 calls " + "%.2f" % statistics.mean(temp_direct_antichain_nbr_calls2) + "\n")
    f.write("DA mean call2 time " + "%.2f" % statistics.mean(temp_direct_antichain_mean_time_calls2) + "\n")

    f.write("DA total nbr calls " + "%.2f" % statistics.mean(temp_direct_antichain_nbr_calls) + "\n")

    f.write("\n")
    f.write("\n")
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