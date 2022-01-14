# Benchmark direct_antichain algorithm when increasing nbr of vertices in the intersection example (positive instance)
for i in {1..10000..500}
do
  {echo -n $(($i * 22 + 1)) " "} >> "intersection_increase_vertices-positive-direct_antichain.txt"
  {time python3 run_benchmark.py "Streett" "direct_antichain" "intersection_increase_vertices" "False" $i;} 2>> "intersection_increase_vertices-positive-direct_antichain.txt"
done
# Benchmark direct_antichain algorithm when increasing nbr of vertices in the intersection example (negative instance)
for i in {1..10000..500}
do
  {echo -n $(($i * 22 + 1)) " "} >> "intersection_increase_vertices-negative-direct_antichain.txt"
  {time python3 run_benchmark.py "Streett" "direct_antichain" "intersection_increase_vertices" "True" $i;} 2>> "intersection_increase_vertices-negative-direct_antichain.txt"
done


# Benchmark counter_example algorithm when increasing nbr of vertices in the intersection example (positive instance)
for i in {1..10000..500}
do
  {echo -n $(($i * 22 + 1)) " "} >> "intersection_increase_vertices-positive-counter_example.txt"
  {time python3 run_benchmark.py "Streett" "counter_example" "intersection_increase_vertices" "False" $i;} 2>> "intersection_increase_vertices-positive-counter_example.txt"
done
# Benchmark counter_example algorithm when increasing nbr of vertices in the intersection example (negative instance)
for i in {1..10000..500}
do
  {echo -n $(($i * 22 + 1)) " "} >> "intersection_increase_vertices-negative-counter_example.txt"
  {time python3 run_benchmark.py "Streett" "counter_example" "intersection_increase_vertices" "True" $i;} 2>> "intersection_increase_vertices-negative-counter_example.txt"
done




# Benchmark direct_antichain algorithm when increasing nbr of objectives in the intersection example (positive instance)
for i in {1..6}
do
  {echo -n $(($i * 2 + 2)) " "} >> "intersection_increase_objectives-positive-direct_antichain.txt"
  {time python3 run_benchmark.py "Streett" "direct_antichain" "intersection_increase_objectives" "False" $i;} 2>> "intersection_increase_objectives-positive-direct_antichain.txt"
done
# Benchmark direct_antichain algorithm when increasing nbr of vertices in the intersection example (negative instance)
for i in {1..6}
do
  {echo -n $(($i * 2 + 2)) " "} >> "intersection_increase_objectives-negative-direct_antichain.txt"
  {time python3 run_benchmark.py "Streett" "direct_antichain" "intersection_increase_objectives" "True" $i;} 2>> "intersection_increase_objectives-negative-direct_antichain.txt"
done


# Benchmark counter_example algorithm when increasing nbr of objectives in the intersection example (positive instance)
for i in {1..6}
do
  {echo -n $(($i * 2 + 2)) " "} >> "intersection_increase_objectives-positive-counter_example.txt"
  {time python3 run_benchmark.py "Streett" "counter_example" "intersection_increase_objectives" "False" $i;} 2>> "intersection_increase_objectives-positive-counter_example.txt"
done
# Benchmark counter_example algorithm when increasing nbr of vertices in the intersection example (negative instance)
for i in {1..6}
do
  {echo -n $(($i * 2 + 2)) " "} >> "intersection_increase_objectives-negative-counter_example.txt"
  {time python3 run_benchmark.py "Streett" "counter_example" "intersection_increase_objectives" "True" $i;} 2>> "intersection_increase_objectives-negative-counter_example.txt"
done



# Benchmark direct_antichain algorithm when increasing nbr of objectives in a random automaton 100 vertices 0.2 density
for i in {2..29}
do
  {echo -n $i " "} >> "random-direct_antichain-100-0.2.txt"
  {time python3 run_benchmark.py "Streett" "direct_antichain" "random" "True" 100 0.2 $i;} 2>> "random-direct_antichain-100-0.2.txt"
done
# Benchmark counter_example algorithm when increasing nbr of objectives in a random automaton 100 vertices 0.2 density
for i in {2..29}
do
  {echo -n $i " "} >> "random-counter_example-100-0.2.txt"
  {time python3 run_benchmark.py "Streett" "counter_example" "random" "True" 100 0.2 $i;} 2>> "random-counter_example-100-0.2.txt"
done



# Benchmark direct_antichain algorithm when increasing nbr of objectives in a random automaton 100 vertices 0.5 density
for i in {2..29}
do
  {echo -n $i " "} >> "random-direct_antichain-100-0.5.txt"
  {time python3 run_benchmark.py "Streett" "direct_antichain" "random" "True" 100 0.5 $i;} 2>> "random-direct_antichain-100-0.5.txt"
done
# Benchmark counter_example algorithm when increasing nbr of objectives in a random automaton 100 vertices 0.5 density
for i in {2..29}
do
  {echo -n $i " "} >> "random-counter_example-100-0.5.txt"
  {time python3 run_benchmark.py "Streett" "counter_example" "random" "True" 100 0.5 $i;} 2>> "random-counter_example-100-0.5.txt"
done



# Benchmark direct_antichain algorithm when increasing nbr of objectives in a random automaton 1000 vertices 0.2 density
for i in {2..29}
do
  {echo -n $i " "} >> "random-direct_antichain-1000-0.2.txt"
  {time python3 run_benchmark.py "Streett" "direct_antichain" "random" "True" 1000 0.2 $i;} 2>> "random-direct_antichain-1000-0.2.txt"
done
# Benchmark counter_example algorithm when increasing nbr of objectives in a random automaton 1000 vertices 0.2 density
for i in {2..29}
do
  {echo -n $i " "} >> "random-counter_example-1000-0.2.txt"
  {time python3 run_benchmark.py "Streett" "counter_example" "random" "True" 1000 0.2 $i;} 2>> "random-counter_example-1000-0.2.txt"
done




# Benchmark direct_antichain algorithm when increasing nbr of objectives in a random automaton 10000 vertices 0.2 density
for i in {2..29}
do
  {echo -n $i " "} >> "random-direct_antichain-10000-0.2.txt"
  {time python3 run_benchmark.py "Streett" "direct_antichain" "random" "True" 10000 0.2 $i;} 2>> "random-direct_antichain-10000-0.2.txt"
done
# Benchmark counter_example algorithm when increasing nbr of objectives in a random automaton 10000 vertices 0.2 density
for i in {2..29}
do
  {echo -n $i " "} >> "random-counter_example-10000-0.2.txt"
  {time python3 run_benchmark.py "Streett" "counter_example" "random" "True" 10000 0.2 $i;} 2>> "random-counter_example-10000-0.2.txt"
done