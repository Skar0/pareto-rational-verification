# The file setup_random_benchmarks.py should be ran first to generate the random automata if they are not generated yet

# Benchmark direct_antichain when increasing nbr of vertices in the intersection example (positive instance)
for i in {1..10000..500}
do
  {echo -n $(($i * 22 + 1)) " "} >> "benchmarks/intersection_increase_vertices-positive-direct_antichain.txt"
  {time python3 run_benchmark.py "Streett" "direct_antichain" "intersection_increase_vertices" "False" $i;} 2>> "benchmarks/intersection_increase_vertices-positive-direct_antichain.txt"
done
# Benchmark direct_antichain when increasing nbr of vertices in the intersection example (negative instance)
for i in {1..10000..500}
do
  {echo -n $(($i * 22 + 1)) " "} >> "benchmarks/intersection_increase_vertices-negative-direct_antichain.txt"
  {time python3 run_benchmark.py "Streett" "direct_antichain" "intersection_increase_vertices" "True" $i;} 2>> "benchmarks/intersection_increase_vertices-negative-direct_antichain.txt"
done


# Benchmark counter_example  when increasing nbr of vertices in the intersection example (positive instance)
for i in {1..10000..500}
do
  {echo -n $(($i * 22 + 1)) " "} >> "benchmarks/intersection_increase_vertices-positive-counter_example.txt"
  {time python3 run_benchmark.py "Streett" "counter_example" "intersection_increase_vertices" "False" $i;} 2>> "benchmarks/intersection_increase_vertices-positive-counter_example.txt"
done
# Benchmark counter_example when increasing nbr of vertices in the intersection example (negative instance)
for i in {1..10000..500}
do
  {echo -n $(($i * 22 + 1)) " "} >> "benchmarks/intersection_increase_vertices-negative-counter_example.txt"
  {time python3 run_benchmark.py "Streett" "counter_example" "intersection_increase_vertices" "True" $i;} 2>> "benchmarks/intersection_increase_vertices-negative-counter_example.txt"
done




# Benchmark direct_antichain algorithm when increasing nbr of objectives in the intersection example (positive instance)
for i in {1..14}
do
  {echo -n $(($i * 2 + 2)) " "} >> "benchmarks/intersection_increase_objectives-positive-direct_antichain.txt"
  {time python3 run_benchmark.py "Streett" "direct_antichain" "intersection_increase_objectives" "False" $i;} 2>> "benchmarks/intersection_increase_objectives-positive-direct_antichain.txt"
done
# Benchmark direct_antichain algorithm when increasing nbr of vertices in the intersection example (negative instance)
for i in {1..14}
do
  {echo -n $(($i * 2 + 2)) " "} >> "benchmarks/intersection_increase_objectives-negative-direct_antichain.txt"
  {time python3 run_benchmark.py "Streett" "direct_antichain" "intersection_increase_objectives" "True" $i;} 2>> "benchmarks/intersection_increase_objectives-negative-direct_antichain.txt"
done


# Benchmark counter_example algorithm when increasing nbr of objectives in the intersection example (positive instance)
for i in {1..14}
do
  {echo -n $(($i * 2 + 2)) " "} >> "benchmarks/intersection_increase_objectives-positive-counter_example.txt"
  {time python3 run_benchmark.py "Streett" "counter_example" "intersection_increase_objectives" "False" $i;} 2>> "benchmarks/intersection_increase_objectives-positive-counter_example.txt"
done
# Benchmark counter_example algorithm when increasing nbr of vertices in the intersection example (negative instance)
for i in {1..14}
do
  {echo -n $(($i * 2 + 2)) " "} >> "benchmarks/intersection_increase_objectives-negative-counter_example.txt"
  {time python3 run_benchmark.py "Streett" "counter_example" "intersection_increase_objectives" "True" $i;} 2>> "benchmarks/intersection_increase_objectives-negative-counter_example.txt"
done




# Benchmark direct_antichain algorithm for random complex example 4 priorities per function, 100 vertices, density 0.2
for i in {3..14}
do
  {echo -n $i " "} >> "benchmarks/direct_antichain-random-100-4-0.2.txt"
  {time python3 run_benchmark.py "Streett" "direct_antichain" "random_complex" "False" 100 0.2 $i;} 2>> "benchmarks/direct_antichain-random-100-4-0.2.txt"
done




# Benchmark direct_antichain algorithm for random complex example 4 priorities per function, 1000 vertices, density 0.2
for i in {3..14}
do
  {echo -n $i " "} >> "benchmarks/direct_antichain-random-1000-4-0.2.txt"
  {time python3 run_benchmark.py "Streett" "direct_antichain" "random_complex" "False" 1000 0.2 $i;} 2>> "benchmarks/direct_antichain-random-1000-4-0.2.txt"
done




# Benchmark counter_example algorithm for random complex example 4 priorities per function, 100 vertices, density 0.2
for i in {3..14}
do
  {echo -n $i " "} >> "benchmarks/counter_example-random-100-4-0.2.txt"
  {time python3 run_benchmark.py "Streett" "counter_example" "random_complex" "False" 100 0.2 $i;} 2>> "benchmarks/counter_example-random-100-4-0.2.txt"
done




# Benchmark counter_example algorithm for random complex example 4 priorities per function, 1000 vertices, density 0.2
for i in {3..14}
do
  {echo -n $i " "} >> "benchmarks/counter_example-random-1000-4-0.2.txt"
  {time python3 run_benchmark.py "Streett" "counter_example" "random_complex" "False" 1000 0.2 $i;} 2>> "benchmarks/counter_example-random-1000-4-0.2.txt"
done
