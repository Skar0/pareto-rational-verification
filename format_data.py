data_files = ["intersection_increase_vertices-positive-direct_antichain.txt",
              "intersection_increase_vertices-negative-direct_antichain.txt",
              "intersection_increase_vertices-positive-counter_example.txt",
              "intersection_increase_vertices-negative-counter_example.txt",
              "intersection_increase_objectives-positive-direct_antichain.txt",
              "intersection_increase_objectives-negative-direct_antichain.txt",
              "intersection_increase_objectives-positive-counter_example.txt",
              "intersection_increase_objectives-negative-counter_example.txt",
              "random-direct_antichain-100-0.2.txt",
              "random-counter_example-100-0.2.txt",
              "random-direct_antichain-100-0.5.txt",
              "random-counter_example-100-0.5.txt",
              "random-direct_antichain-1000-0.2.txt",
              "random-counter_example-1000-0.2.txt",
              "random-direct_antichain-10000-0.2.txt",
              "random-counter_example-10000-0.2.txt",
              "random-direct_antichain-100-0.2-positive.txt",
              "random-counter_example-100-0.2-positive.txt"]

for file_name in data_files:
    with open(file_name) as f:
        print(file_name)
        for line in f:
            line = line.split(" ")
            print("(" + line[0] + ", " + line[16] + ")", end=" ")
        print()