from dataclasses import dataclass

@dataclass
class Question:
    id: str
    text: str
    points: int

@dataclass
class Choice:
    id: str
    question_id: str
    text: str
    is_correct: bool
