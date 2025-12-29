from dataclasses import dataclass

@dataclass
class User:
    id: str
    email: str
    full_name: str
    password: str
    role: str
    is_active: bool
