"""
storage.py - Persistence layer for Project 30: Genetic Algorithm Visualizer
"""

from pathlib import Path
import json
from typing import Any, Dict, List

DATA_DIR = Path(__file__).resolve().parent / 'data'
OUTPUTS_DIR = DATA_DIR / 'outputs'
CATALOG_FILE = DATA_DIR / 'runs.json'


def ensure_data_dirs() -> None:
    """Create local data and outputs directories if they do not exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def ensure_data_dir() -> None:
    """Backwards-compatible alias for older scaffold code."""
    ensure_data_dirs()


def get_run_files() -> List[Path]:
    """Return all saved run files from outputs directory."""
    ensure_data_dirs()
    return sorted(OUTPUTS_DIR.glob("run_*.json"))


def load_run_catalog() -> List[Dict[str, Any]]:
    """Load run catalog entries from disk."""
    ensure_data_dirs()
    if not CATALOG_FILE.exists():
        return []
    try:
        data = json.loads(CATALOG_FILE.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def save_run_catalog(catalog: List[Dict[str, Any]]) -> None:
    """Persist run catalog to disk."""
    ensure_data_dirs()
    CATALOG_FILE.write_text(json.dumps(catalog, indent=2), encoding='utf-8')


def save_run_record(run_record: Dict[str, Any]) -> str:
    """Persist one run record in outputs and update run catalog.

    Returns:
        str: Absolute path to the saved run JSON file.
    """
    ensure_data_dirs()
    run_id = run_record["run_id"]
    file_path = OUTPUTS_DIR / f"run_{run_id}.json"
    file_path.write_text(json.dumps(run_record, indent=2), encoding='utf-8')

    catalog = load_run_catalog()
    catalog.append(
        {
            "run_id": run_id,
            "solved": run_record.get("solved", False),
            "best_fitness": run_record.get("best_fitness", 0.0),
            "target_string": run_record.get("target_string", ""),
            "finished_at": run_record.get("finished_at", ""),
            "run_file": str(file_path),
        }
    )
    save_run_catalog(catalog)
    return str(file_path)


def save_generation_history(run_id: str, history: List[Dict[str, Any]]) -> str:
    """Persist generation history for a run.

    Returns:
        str: Absolute path to the saved history JSON file.
    """
    ensure_data_dirs()
    history_path = OUTPUTS_DIR / f"history_{run_id}.json"
    history_path.write_text(json.dumps(history, indent=2), encoding='utf-8')
    return str(history_path)


def load_json(filename: str):
    """Load JSON data from the local data directory."""
    ensure_data_dirs()
    path = DATA_DIR / filename
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding='utf-8'))


def save_json(filename: str, data: Any) -> None:
    """Save JSON data to the local data directory."""
    ensure_data_dirs()
    path = DATA_DIR / filename
    path.write_text(json.dumps(data, indent=2), encoding='utf-8')
