"""
models.py - Data models for Project 30: Genetic Algorithm Visualizer
====================================================================

Defines:
    - GA configuration records
    - Individual genome records
    - Generation metric records
    - Run summary records
"""

from datetime import datetime
from typing import Any, Dict, List, Optional


def _utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp string."""
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def create_ga_config(
    target_string: str = "EVOLVE THIS PHRASE",
    population_size: int = 140,
    max_generations: int = 220,
    mutation_rate: float = 0.03,
    crossover_rate: float = 0.85,
    elitism_count: int = 3,
    tournament_size: int = 4,
    random_seed: int = 42,
) -> Dict[str, Any]:
    """Create a validated GA configuration record."""
    gene_pool = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
    target = target_string.strip().upper() or "HELLO"
    return {
        "problem_type": "string_match",
        "target_string": target,
        "genome_length": len(target),
        "gene_pool": gene_pool,
        "population_size": max(10, int(population_size)),
        "max_generations": max(1, int(max_generations)),
        "mutation_rate": min(1.0, max(0.0, float(mutation_rate))),
        "crossover_rate": min(1.0, max(0.0, float(crossover_rate))),
        "elitism_count": max(1, int(elitism_count)),
        "tournament_size": max(2, int(tournament_size)),
        "random_seed": int(random_seed),
        "created_at": _utc_timestamp(),
    }


def create_individual(
    genome: str,
    fitness: float,
    generation: int,
    rank: Optional[int] = None,
) -> Dict[str, Any]:
    """Create an individual genome record."""
    return {
        "genome": genome,
        "fitness": float(fitness),
        "generation": int(generation),
        "rank": rank,
    }


def create_generation_stats(
    generation: int,
    best_fitness: float,
    avg_fitness: float,
    worst_fitness: float,
    diversity_ratio: float,
    best_genome: str,
    solved: bool,
) -> Dict[str, Any]:
    """Create a generation metrics record."""
    return {
        "generation": int(generation),
        "best_fitness": float(best_fitness),
        "avg_fitness": float(avg_fitness),
        "worst_fitness": float(worst_fitness),
        "diversity_ratio": float(diversity_ratio),
        "best_genome": best_genome,
        "solved": bool(solved),
        "timestamp": _utc_timestamp(),
    }


def create_run_summary(
    run_id: str,
    solved: bool,
    generations_executed: int,
    best_fitness: float,
    best_genome: str,
    target_string: str,
    elapsed_ms: float,
    artifacts: Dict[str, str],
) -> Dict[str, Any]:
    """Create a final run summary for reporting and persistence."""
    return {
        "run_id": run_id,
        "solved": bool(solved),
        "generations_executed": int(generations_executed),
        "best_fitness": float(best_fitness),
        "best_genome": best_genome,
        "target_string": target_string,
        "elapsed_ms": float(elapsed_ms),
        "match_percent": round(float(best_fitness) * 100.0, 2),
        "artifacts": artifacts,
        "finished_at": _utc_timestamp(),
    }


def create_record(**kwargs: Any) -> Dict[str, Any]:
    """Backwards-compatible generic record factory."""
    return dict(kwargs)
