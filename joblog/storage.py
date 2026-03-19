import json
from pathlib import Path
from typing import Any

DATA_PATH = Path("joblog.json")


def load_data() -> dict[str, Any]:
    if not DATA_PATH.exists():
        return {"next_id": 1, "items": []}
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def save_data(data: dict[str, Any]) -> None:
    DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
