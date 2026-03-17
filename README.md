# Beginner Project 30: Genetic Algorithm Visualizer

**Time:** 4-6 hours  
**Difficulty:** Intermediate Beginner  
**Focus:** Evolutionary optimization, selection/crossover/mutation, fitness tracking, and run visualization

---

## Why This Project?

Genetic algorithms are a practical way to solve optimization problems when exact methods are hard or expensive. This project helps you learn how stochastic search converges over generations and how parameter choices affect convergence speed and solution quality.

This project teaches evolutionary computation where you can:

- represent candidate solutions as genomes,
- define a normalized fitness function for optimization,
- evolve populations with tournament selection,
- combine genes via single-point crossover,
- explore mutation for search-space diversity,
- track best/average/worst fitness over generations,
- visualize optimization progression with charts,
- persist run summaries and full generation histories,
- tune parameters (mutation, elitism, population size),
- and evaluate convergence behavior across repeated runs.

---

## More Projects

You can access this project and more in this separate repository:

[student-interview-prep](https://github.com/ShamShamsw/student-interview-prep.git)

---

## What You Will Build

You will build a genetic algorithm visualizer that:

1. Encodes candidate solutions as fixed-length genomes.
2. Solves a string-matching optimization target using normalized fitness.
3. Initializes a reproducible random population from a configurable gene pool.
4. Applies tournament selection to choose fitter parents.
5. Uses single-point crossover to create child genomes.
6. Mutates genes probabilistically to maintain exploration.
7. Preserves elite individuals between generations.
8. Tracks generation metrics (best/avg/worst fitness and diversity).
9. Exports run artifacts (run summary JSON, history JSON, fitness chart).
10. Prints a readable terminal report showing optimization progress and outcomes.

---

## Requirements

- Python 3.11+
- `matplotlib` (for fitness evolution chart export)

Install with:

```bash
pip install -r requirements.txt
```

---

## Example Session

```text
======================================================================
   GENETIC ALGORITHM VISUALIZER
======================================================================

Configuration:
   Problem type:         string_match
   Target string:        EVOLVE THIS PHRASE
   Population size:      140
   Max generations:      220
   Crossover rate:       0.85
   Mutation rate:        0.03
   Elitism count:        3
   Tournament size:      4
   Random seed:          42

Startup:
   Data directory:       data/
   Outputs directory:    data/outputs/
   Run catalog:          data/runs.json (loaded 0 runs)
   Solved historical:    0

---

Run complete:
   Run ID:               20260316_211530
   Status:               Solved
   Generations executed: 88
   Best fitness:         1.0000 (100.00% match)
   Best genome:          EVOLVE THIS PHRASE
   Target string:        EVOLVE THIS PHRASE
   Elapsed time:         196.48 ms

Recent generations:
   Gen | Best    | Avg     | Worst   | Diversity | Best Genome
   ----+---------+---------+---------+-----------+------------------------------
    84 | 0.9444 | 0.8201 | 0.6111 | 0.714     | EVOLVE THIS PHRASE
    85 | 0.9444 | 0.8262 | 0.6111 | 0.700     | EVOLVE THIS PHRASE
    86 | 0.9444 | 0.8325 | 0.6667 | 0.686     | EVOLVE THIS PHRASE
    87 | 0.9444 | 0.8412 | 0.6667 | 0.679     | EVOLVE THIS PHRASE
    88 | 1.0000 | 0.8537 | 0.6667 | 0.671     | EVOLVE THIS PHRASE

Artifacts saved:
   Run record:           data/outputs/run_20260316_211530.json
   Generation history:   data/outputs/history_20260316_211530.json
   Fitness chart:        data/outputs/fitness_20260316_211530.png
```

---

## Run

```bash
python main.py
```
