risk_assessment_project/
│
├── app.py                        # Основной файл Flask-приложения
├── risk_assessment.py            # Логика оценки риска (алгоритмы и функции)
├── requirements.txt              # Список зависимостей (Flask, pandas, matplotlib)
├── templates/                    # HTML-шаблоны для Flask
│   ├── index.html                # Главная страница для загрузки CSV
│   ├── results.html              # Страница с результатами оценки риска
│
├── static/                       # Статические файлы для Flask (если нужны)
│   ├── styles.css                # CSS-стили для улучшения внешнего вида
│   └── script.js                 # JavaScript для дополнительной интерактивности (если нужно)
│
├── data/                         # Папка для данных
│   ├── releases.csv              # Пример CSV-файла с параметрами релизов
│   └── example_output.csv        # Пример выходного файла с оценкой риска
│
├── plots/                        # Папка для сохранения графиков
│   └── risk_distribution.png     # График распределения рисков
│
└── README.md                     # Документация проекта