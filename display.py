"""
display.py - Presentation helpers for Project 30: Genetic Algorithm Visualizer
"""

from typing import Any, Dict, List


def format_header() -> str:
    """Format session header banner."""
    return (
        "=" * 70
        + "\n"
        + "   GENETIC ALGORITHM VISUALIZER\n"
        + "=" * 70
    )


def format_startup_guide(config: Dict[str, Any], profile: Dict[str, Any]) -> str:
    """Format startup configuration and saved-run profile."""
    lines = [
        "",
        "Configuration:",
        f"   Problem type:         {config['problem_type']}",
        f"   Target string:        {config['target_string']}",
        f"   Population size:      {config['population_size']}",
        f"   Max generations:      {config['max_generations']}",
        f"   Crossover rate:       {config['crossover_rate']:.2f}",
        f"   Mutation rate:        {config['mutation_rate']:.2f}",
        f"   Elitism count:        {config['elitism_count']}",
        f"   Tournament size:      {config['tournament_size']}",
        f"   Random seed:          {config['random_seed']}",
        "",
        "Startup:",
        f"   Data directory:       data/",
        f"   Outputs directory:    data/outputs/",
        f"   Run catalog:          {profile['catalog_file']} (loaded {profile['runs_stored']} runs)",
        f"   Solved historical:    {profile['solved_runs']}",
        "",
        "---",
    ]
    return "\n".join(lines)


def format_generation_preview(history_tail: List[Dict[str, Any]]) -> str:
    """Format a compact table for the last few generations."""
    if not history_tail:
        return "No generation history available."

    lines = [
        "Recent generations:",
        "   Gen | Best    | Avg     | Worst   | Diversity | Best Genome",
        "   ----+---------+---------+---------+-----------+------------------------------",
    ]
    for row in history_tail:
        lines.append(
            "   "
            f"{row['generation']:>3} | "
            f"{row['best_fitness']:.4f} | "
            f"{row['avg_fitness']:.4f} | "
            f"{row['worst_fitness']:.4f} | "
            f"{row['diversity_ratio']:.3f}     | "
            f"{row['best_genome'][:30]}"
        )
    return "\n".join(lines)


def format_run_report(summary: Dict[str, Any]) -> str:
    """Format final run report."""
    status = "Solved" if summary["solved"] else "Stopped at generation limit"
    lines = [
        "",
        "Run complete:",
        f"   Run ID:               {summary['run_id']}",
        f"   Status:               {status}",
        f"   Generations executed: {summary['generations_executed']}",
        f"   Best fitness:         {summary['best_fitness']:.4f} ({summary['match_percent']:.2f}% match)",
        f"   Best genome:          {summary['best_genome']}",
        f"   Target string:        {summary['target_string']}",
        f"   Elapsed time:         {summary['elapsed_ms']:.2f} ms",
        "",
        format_generation_preview(summary.get("history_tail", [])),
        "",
        "Artifacts saved:",
        f"   Run record:           {summary['artifacts']['run_file']}",
        f"   Generation history:   {summary['artifacts']['history_file']}",
        f"   Fitness chart:        {summary['artifacts']['fitness_plot']}",
    ]
    return "\n".join(lines)


def format_message(message: str) -> str:
    """Format a user-facing message string."""
    return f'[Project 30] {message}'
