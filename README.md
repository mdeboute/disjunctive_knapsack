# disjunctive_knapsack

Model 1:

```text
Usage: python3 src/model.py <input_file>
```

Model 2 (relax the kp constraint and find the best u):

```text
Usage: python3 src/relax_kp.py <input_file> <u>
Where u is the upper bound of the u that we are searching for.
```

Benchmark (don't forget to `chmod u+x benchmark.sh`):

```text
Usage: ./benchmark.sh <dataDir> <solDir> <model>
```

Dependencies are in the `pyproject.toml` file.
