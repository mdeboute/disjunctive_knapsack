# disjunctive_knapsack

Model 1 (disjunctive_knapsack milp):

```text
Usage: python3 src/milp.py <input_file>
```

Model 2 (relax the kp constraint and find the best u):

```text
Usage: python3 src/relax_kp.py <input_file> <u>
Where u is the upper bound of the u that we are searching for.
```

Model 4 (dynamic programming):

```text
Usage: python3 src/dyn_prog.py <input_file>
```

Benchmark for milp (don't forget to `chmod u+x benchmark.sh`):

```text
Usage: ./benchmark.sh <dataDir> <solDir> <model>
```

Dependencies are in the `pyproject.toml` file.
