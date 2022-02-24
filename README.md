# Pareto-Rational Verification
Implementation of verification algorithms for the Pareto-Rational Verification problem (PRV problem). This python implementation uses [SPOT](https://spot.lrde.epita.fr) as a library to manipulate automata with general acceptance conditions. This code was implemented by Clément Tamines, University of Mons ([website](https://clement.tamin.es)).

## Structure of the repository

- `verification_algorithms.py` contains the implementation of the antichain optimization algorithm and of the counterexample-based algorithm to solve the PRV problem.
- `benchmarks.py` contains functions to generate benchmarks for the intersection example as well as random benchmarks with large antichains of realizable payoffs.
- `benchmarks_statistics.py` contains functions to retrieve useful information on the benchmarks such as the size of the antichain of realizable payoffs or the total number of realizable payoffs.
- `run_benchmarks.py` contains functions to run the benchmarks with increasing value of some parameters and to parse the results into plotable .dat files. The benchmark results displayed in the paper were generated with the parameters used at the end of this file.
- `benchmarks_results/` contains the files generated for the benchmarks, which report interesting statistics on the benchmarks as well as the running time for both algorithms. The .dat files are also stored here.
- `random_automata/` contains the random automata generated when running the random benchmarks. The running time of both algorithms for random benchmarks in the paper are for these automata.

## Reusing

The format of the automaton expected by the verification algorithms (implemented in `verification_algorithms.py`) is described in the documentation of the functions generating benchmarks in `benchmarks.py`. This code can easily be reused to solve the PRV problem on other instances by implementing a function with the same signature as those in `benchmarks.py`. The algorithms can be modified to perform operations differently as they are implemented using several functions that can be replaced with different implementations.

## Installation
We use [SPOT](https://spot.lrde.epita.fr)'s python bindings to manipulate automata, representing the input for the PRV problem. 
Installing SPOT with those bindings is therefore required to run our code. The version of SPOT should be at least 2.10.3 (a bug present in the previous versions sometimes prevented our algorithms from terminating).
In addition, SPOT should be installed with the `--enable-max-accsets=64` option in order to be able to run the benchmarks. The rest of the python code was written in python 3.8.

From project root, run `tar -xf random_automata/random_automata_positive.tar.xz --directory random_automata/ --strip-components=1` and `tar -xf random_automata/random_automata_negative.tar.xz --directory random_automata/ --strip-components=1` to decompress the random automata already generated to reproduce the benchmarks.
## Citing
If you use this software for your academic work, please cite the following paper on the PRV problem and related algorithms:
