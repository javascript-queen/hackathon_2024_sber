from flask import Flask, render_template, request
import pandas as pd
from risk_assessment import evaluate_risk, classify_risk, visualize_risks, visualize_table

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return "Файл не найден"
    file = request.files['file']
    if file.filename == '':
        return "Файл не выбран"
    
    try:
        # Загрузка данных
        data = pd.read_csv(file)
        if data.empty:
            return "Загруженный файл пуст."

        # Расчёт оценок
        data['Risk Score'] = data.apply(evaluate_risk, axis=1)
        data['Risk Level'] = data.apply(lambda row: classify_risk(row['Risk Score'], row), axis=1)
        
        # Визуализация данных
        visualize_risks(data)
        visualize_table(data)

        # Преобразуем таблицу в HTML
        table_html = data.to_html(classes='data', index=False).strip()

        # Передаём данные в шаблон
        return render_template(
            "results.html",
            tables=table_html  # Убираем лишние квадратные скобки
        )
    except Exception as e:
        return f"Произошла ошибка при обработке файла: {e}"

@app.route("/manual", methods=["POST"])
def manual():
    try:
        # Получаем данные из формы
        form_data = {
            "business_importance": int(request.form.get("business_importance")),
            "technical_complexity": int(request.form.get("technical_complexity")),
            "urgency": int(request.form.get("urgency")),
            "data_quality": int(request.form.get("data_quality")),
            "team_experience": int(request.form.get("team_experience")),
            "regulatory_compliance": int(request.form.get("regulatory_compliance")),
            "legal_impact": int(request.form.get("legal_impact")),
            "financial_risk": int(request.form.get("financial_risk")),
            "integration_level": int(request.form.get("integration_level")),
            "stability_of_previous_releases": int(request.form.get("stability_of_previous_releases")),
            "testing_maturity": int(request.form.get("testing_maturity")),
            "backup_plan": int(request.form.get("backup_plan"))
        }

        # Создаём DataFrame
        data = pd.DataFrame([form_data])

        # Расчёт оценки риска
        data['Risk Score'] = data.apply(evaluate_risk, axis=1)
        data['Risk Level'] = data.apply(lambda row: classify_risk(row['Risk Score'], row), axis=1)

        # Визуализация графика и таблицы
        visualize_risks(data)
        visualize_table(data)

        # Преобразуем таблицу в HTML
        table_html = data.to_html(classes='data', index=False).strip()

        return render_template(
            "results.html",
            tables=table_html  # Убираем квадратные скобки
        )
    except Exception as e:
        return f"Произошла ошибка при обработке данных: {e}"

if __name__ == "__main__":
    app.run(debug=True)