from dataclasses import dataclass

@dataclass
class Mission:
    code: str
    title: str
    max_xp: int
    category: str
