from __future__ import annotations

from typing import Dict, List, Tuple


def write_report_txt(
    path: str,
    ranking: List[Tuple[str, int]],
    inactive_users: List[str],
    top_n: int = 3
) -> None:
    """
    Genera un reporte TXT simple y profesional:
    - Top N ranking
    - Usuarios inactivos
    """
    with open(path, "w", encoding="utf-8") as f:
        f.write("=== REPORTE ACADEMIA XP ===\n\n")

        f.write(f"Top {top_n} Ranking (Quiz):\n")
        if not ranking:
            f.write("- (sin datos)\n")
        else:
            for i, (user_name, points) in enumerate(ranking[:top_n], start=1):
                f.write(f"{i}. {user_name} — {points} pts\n")

        f.write("\nUsuarios inactivos:\n")
        if not inactive_users:
            f.write("- (ninguno)\n")
        else:
            for name in inactive_users:
                f.write(f"- {name}\n")
