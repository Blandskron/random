import csv
from academy.config import DATA_OUTPUT

def run_quiz(user, questions, choices):
    total = 0
    answers_path = f"{DATA_OUTPUT}/answers.csv"

    with open(answers_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        for q in questions.values():
            print("\n", q.text)
            opts = choices[q.id]
            for i, c in enumerate(opts):
                print(f"{i+1}. {c.text}")

            selected = int(input("Opción: ")) - 1
            choice = opts[selected]

            earned = q.points if choice.is_correct else 0
            total += earned

            writer.writerow([user.id, q.id, choice.id, earned])

    print(f"\nPuntaje obtenido: {total}")
