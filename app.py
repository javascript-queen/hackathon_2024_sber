from flask import Flask, render_template, request, Response
import pandas as pd
import io
from risk_assessment import evaluate_risk, classify_risk, visualize_risks


app = Flask(__name__)

# Глобальная переменная для хранения загруженных данных
global_data = None

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    global global_data
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

        # Сохранение данных в глобальную переменную
        global_data = data

        # Преобразуем таблицу в HTML
        table_html = data.to_html(classes='data', index=False).strip()

        # Передаём данные в шаблон
        return render_template(
            "results.html",
            tables=table_html
        )
    except Exception as e:
        return f"Произошла ошибка при обработке файла: {e}"


@app.route("/plot.png")
def plot_png():
    """Маршрут для динамической генерации графика."""
    if global_data is None:
        return "Данные не найдены. Пожалуйста, загрузите файл."
    
    # Визуализация графика
    buffer = visualize_risks(global_data)
    return Response(buffer, mimetype='image/png')


@app.route("/manual", methods=["POST"])
def manual():
    global global_data
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

        # Сохраняем данные для дальнейшего использования
        global_data = data

        # Преобразуем таблицу в HTML
        table_html = data.to_html(classes='data', index=False).strip()

        return render_template(
            "results.html",
            tables=table_html
        )
    except Exception as e:
        return f"Произошла ошибка при обработке данных: {e}"


if __name__ == "__main__":
    app.run(debug=True)