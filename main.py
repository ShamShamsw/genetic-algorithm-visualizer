"""
main.py - Entry point for Project 30: Genetic Algorithm Visualizer
"""

from display import format_header, format_run_report, format_startup_guide
from models import create_ga_config
from operations import load_visualizer_profile, run_core_flow
from storage import ensure_data_dirs


def main() -> None:
    """Run one complete genetic algorithm visualization session."""
    ensure_data_dirs()
    print(format_header())

    config = create_ga_config()
    profile = load_visualizer_profile()
    print(format_startup_guide(config, profile))

    summary = run_core_flow()
    print(format_run_report(summary))


if __name__ == '__main__':
    main()
