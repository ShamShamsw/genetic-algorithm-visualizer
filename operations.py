"""
operations.py - Business logic for Project 30: Genetic Algorithm Visualizer
"""

from __future__ import annotations

from datetime import datetime
import random
from statistics import mean
import time
from typing import Any, Dict, List, Sequence, Tuple

from models import (
    create_ga_config,
    create_generation_stats,
    create_individual,
    create_run_summary,
)
from storage import (
    OUTPUTS_DIR,
    ensure_data_dirs,
    load_run_catalog,
    save_generation_history,
    save_run_record,
)


def _run_id() -> str:
    """Build a compact run ID from UTC timestamp."""
    return datetime.utcnow().strftime("%Y%m%d_%H%M%S")


def _fitness_string_match(genome: str, target: str) -> float:
    """Return normalized fitness in [0,1] for target-string matching."""
    matches = sum(1 for a, b in zip(genome, target) if a == b)
    return matches / len(target)


def _random_genome(rng: random.Random, length: int, gene_pool: str) -> str:
    return "".join(rng.choice(gene_pool) for _ in range(length))


def _tournament_select(
    rng: random.Random,
    population: Sequence[Tuple[str, float]],
    tournament_size: int,
) -> str:
    contenders = rng.sample(population, k=min(tournament_size, len(population)))
    contenders.sort(key=lambda item: item[1], reverse=True)
    return contenders[0][0]


def _single_point_crossover(
    rng: random.Random,
    parent_a: str,
    parent_b: str,
    crossover_rate: float,
) -> Tuple[str, str]:
    if len(parent_a) < 2 or rng.random() > crossover_rate:
        return parent_a, parent_b
    point = rng.randint(1, len(parent_a) - 1)
    child_a = parent_a[:point] + parent_b[point:]
    child_b = parent_b[:point] + parent_a[point:]
    return child_a, child_b


def _mutate(rng: random.Random, genome: str, mutation_rate: float, gene_pool: str) -> str:
    chars = list(genome)
    for index, current in enumerate(chars):
        if rng.random() <= mutation_rate:
            replacement = rng.choice(gene_pool)
            if replacement == current and len(gene_pool) > 1:
                replacement = gene_pool[(gene_pool.index(replacement) + 1) % len(gene_pool)]
            chars[index] = replacement
    return "".join(chars)


def _diversity_ratio(population: Sequence[str]) -> float:
    if not population:
        return 0.0
    return len(set(population)) / len(population)


def _save_fitness_plot(history: List[Dict[str, Any]], run_id: str) -> str:
    """Persist a PNG chart of fitness progression.

    Returns a file path when plotting succeeds. If matplotlib is unavailable,
    a text placeholder path is returned instead.
    """
    plot_path = OUTPUTS_DIR / f"fitness_{run_id}.png"
    try:
        import matplotlib.pyplot as plt
    except Exception:
        fallback_path = OUTPUTS_DIR / f"fitness_{run_id}.txt"
        lines = [
            "Matplotlib is unavailable. Fitness points:",
            *[
                f"gen={row['generation']} best={row['best_fitness']:.4f} avg={row['avg_fitness']:.4f}"
                for row in history
            ],
        ]
        fallback_path.write_text("\n".join(lines), encoding="utf-8")
        return str(fallback_path)

    generations = [row["generation"] for row in history]
    best_values = [row["best_fitness"] for row in history]
    avg_values = [row["avg_fitness"] for row in history]
    worst_values = [row["worst_fitness"] for row in history]

    plt.figure(figsize=(9, 5))
    plt.plot(generations, best_values, label="Best Fitness", linewidth=2)
    plt.plot(generations, avg_values, label="Average Fitness", linewidth=2)
    plt.plot(generations, worst_values, label="Worst Fitness", linewidth=1.5)
    plt.title("Genetic Algorithm Fitness Evolution")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.ylim(0.0, 1.02)
    plt.grid(True, alpha=0.25)
    plt.legend()
    plt.tight_layout()
    plt.savefig(plot_path, dpi=140)
    plt.close()
    return str(plot_path)


def load_visualizer_profile() -> Dict[str, Any]:
    """Build startup profile from previously saved runs."""
    catalog = load_run_catalog()
    solved_count = sum(1 for item in catalog if item.get("solved"))
    return {
        "catalog_file": "data/runs.json",
        "runs_stored": len(catalog),
        "solved_runs": solved_count,
    }


def run_core_flow() -> Dict[str, Any]:
    """Execute one complete GA optimization run and persist artifacts."""
    ensure_data_dirs()
    config = create_ga_config()
    rng = random.Random(config["random_seed"])

    target = config["target_string"]
    genome_length = config["genome_length"]
    gene_pool = config["gene_pool"]
    pop_size = config["population_size"]

    run_id = _run_id()
    started = time.perf_counter()

    population = [_random_genome(rng, genome_length, gene_pool) for _ in range(pop_size)]
    history: List[Dict[str, Any]] = []
    best_individual = create_individual(genome="", fitness=0.0, generation=0)
    solved = False

    for generation in range(1, config["max_generations"] + 1):
        scored_population = [
            (genome, _fitness_string_match(genome, target)) for genome in population
        ]
        scored_population.sort(key=lambda item: item[1], reverse=True)

        best_genome, best_fitness = scored_population[0]
        avg_fitness = mean(score for _, score in scored_population)
        worst_fitness = scored_population[-1][1]

        best_individual = create_individual(
            genome=best_genome,
            fitness=best_fitness,
            generation=generation,
            rank=1,
        )
        solved = best_fitness >= 1.0

        history.append(
            create_generation_stats(
                generation=generation,
                best_fitness=best_fitness,
                avg_fitness=avg_fitness,
                worst_fitness=worst_fitness,
                diversity_ratio=_diversity_ratio([genome for genome, _ in scored_population]),
                best_genome=best_genome,
                solved=solved,
            )
        )

        if solved:
            break

        next_population: List[str] = [
            genome for genome, _ in scored_population[: config["elitism_count"]]
        ]

        while len(next_population) < pop_size:
            parent_a = _tournament_select(
                rng,
                scored_population,
                config["tournament_size"],
            )
            parent_b = _tournament_select(
                rng,
                scored_population,
                config["tournament_size"],
            )
            child_a, child_b = _single_point_crossover(
                rng,
                parent_a,
                parent_b,
                config["crossover_rate"],
            )
            child_a = _mutate(rng, child_a, config["mutation_rate"], gene_pool)
            child_b = _mutate(rng, child_b, config["mutation_rate"], gene_pool)
            next_population.append(child_a)
            if len(next_population) < pop_size:
                next_population.append(child_b)

        population = next_population

    elapsed_ms = (time.perf_counter() - started) * 1000.0
    history_file = save_generation_history(run_id, history)
    plot_file = _save_fitness_plot(history, run_id)

    summary = create_run_summary(
        run_id=run_id,
        solved=solved,
        generations_executed=len(history),
        best_fitness=best_individual["fitness"],
        best_genome=best_individual["genome"],
        target_string=target,
        elapsed_ms=elapsed_ms,
        artifacts={
            "history_file": history_file,
            "fitness_plot": plot_file,
        },
    )
    summary["config"] = config
    summary["history_tail"] = history[-5:]
    run_file = save_run_record(summary)
    summary["artifacts"]["run_file"] = run_file
    return summary
