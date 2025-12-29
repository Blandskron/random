import csv
from academy.domain.missions.models import Mission

def load_missions(path: str) -> dict:
    missions = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            missions[r["code"]] = Mission(
                r["code"], r["title"], int(r["max_xp"]), r["category"]
            )
    return missions
