# random
Proyecto educativo
academy_xp/
├─ data/
│  ├─ input/
│  │  ├─ users.csv
│  │  ├─ missions.csv
│  │  ├─ questions.csv
│  │  └─ choices.csv
│  └─ output/
│     ├─ submissions.csv
│     ├─ answers.csv
│     ├─ results.csv
│     └─ report.txt
└─ src/
   └─ academy/
      ├─ main.py
      ├─ config.py
      ├─ common/
      │  ├─ errors.py
      │  └─ utils.py
      ├─ domain/
      │  ├─ users/models.py
      │  ├─ missions/models.py
      │  └─ quiz/models.py
      ├─ application/
      │  ├─ auth_service.py
      │  ├─ mission_service.py
      │  ├─ quiz_service.py
      │  └─ report_service.py
      └─ infrastructure/
         └─ storage/
            ├─ csv_users_repo.py
            ├─ csv_missions_repo.py
            ├─ csv_quiz_repo.py
            ├─ csv_results_repo.py
            └─ txt_report_writer.py
