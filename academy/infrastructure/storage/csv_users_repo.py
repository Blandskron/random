import csv
from academy.domain.users.models import User

def load_users(path: str) -> dict:
    users = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            users[r["email"]] = User(
                id=r["id"],
                email=r["email"],
                full_name=r["full_name"],
                password=r["password"],
                role=r["role"],
                is_active=bool(int(r["is_active"]))
            )
    return users
