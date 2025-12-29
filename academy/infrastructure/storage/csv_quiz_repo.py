import csv
from academy.domain.quiz.models import Question, Choice

def load_questions(q_path, c_path):
    questions = {}
    choices = {}

    with open(q_path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            questions[r["question_id"]] = Question(
                r["question_id"], r["text"], int(r["points"])
            )

    with open(c_path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            c = Choice(
                r["choice_id"], r["question_id"], r["text"], bool(int(r["is_correct"]))
            )
            choices.setdefault(c.question_id, []).append(c)

    return questions, choices
