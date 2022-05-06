# disjunctive_knapsack

Model 1 (disjunctive_knapsack milp):

```text
Usage: python3 src/milp.py <input_file>
```

Model 2 (relax the kp constraint and find the best u):

```text
Usage: python3 src/relax_kp.py <input_file> <e>
Where <e> (optional) is the epsilon value. Less is <e> more precise will be u.
Default value is 0.001.
```

Model 3 (relax the disjunctive constraint and find the best v):

```text
Usage: python3 src/relax_disj.py <input_file> <e>
Where <e> (optional) is the epsilon value. Less is <e> more precise will be v.
Default value is 0.01.
```

Model 4 (dynamic programming):

```text
Usage: python3 src/dyn_prog.py <input_file>
```

Benchmark for model 1 (the initial milp) (don't forget to `chmod u+x benchmark.sh`):

```text
Usage: ./benchmark.sh <dataDir> <solDir> <model>
```

Dependencies are in the `pyproject.toml` file.
