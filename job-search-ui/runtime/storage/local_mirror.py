import json
from pathlib import Path


def load_json_rows(path: str):
    p = Path(path)
    if not p.exists():
        return []
    return json.loads(p.read_text())
