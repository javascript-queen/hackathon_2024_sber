import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Устанавливаем безголовый бэкэнд
import matplotlib.pyplot as plt


# Весовые коэффициенты для критериев
WEIGHTS = {
    "business_importance": 0.2,   # Важность бизнес-процессов
    "technical_complexity": 0.15, # Техническая сложность
    "urgency": 0.1,               # Срочность
    "data_quality": 0.15,         # Качество данных
    "team_experience": 0.1,       # Опыт команды
    "integration_level": 0.1,     # Уровень интеграции
    "stability_of_previous_releases": 0.1, # Стабильность предыдущих релизов
    "testing_maturity": 0.05,     # Зрелость процессов тестирования
    "backup_plan": 0.05,           # Наличие резервного плана
    "regulatory_compliance": 0.2,  # Соответствие нормативным требованиям
    "legal_impact": 0.25,         # Юридическое влияние
    "financial_risk": 0.2,        # Финансовые риски
}

# Функция оценки риска по каждому параметру
def evaluate_risk(row):
    """
    Рассчитывает общий риск на основе веса метрик.
    """
    risk_score = sum(row.get(param, 0) * WEIGHTS.get(param, 0) for param in WEIGHTS)
    return risk_score

# Функция классификации уровня риска
def classify_risk(risk_score, row=None):
    """
    Классифицирует уровень риска на основе итогового балла.
    Учитывает юридический или финансовый критический риск.
    """
    # Если заданы юридический или финансовый критический риск
    if row is not None:
        if row.get("legal_impact", 0) >= 4 or row.get("regulatory_compliance", 0) >= 4:
            return "Юридический критический"
        if row.get("financial_risk", 0) >= 4:
            return "Финансовый критический"
    
    # Общие уровни риска
    if risk_score < 2:
        return "Низкий"
    elif 2 <= risk_score < 3:
        return "Средний"
    elif 3 <= risk_score < 4:
        return "Высокий"
    elif 4 <= risk_score < 5:
        return "Очень высокий"
    else:
        return "Неприемлемый"
    
# Визуализация графиков
def visualize_risks(data):
    """
    Создаёт график распределения уровней риска.
    """
    risk_counts = data['Risk Level'].value_counts()

    # Создание графика
    plt.figure(figsize=(10, 6))
    bars = plt.bar(risk_counts.index, risk_counts.values, color=['#4CAF50', '#FFC107', '#FF5722', '#F44336', '#9C27B0'])

    # Настройка осей
    plt.title('Распределение уровней риска', fontsize=16)
    plt.xlabel('Уровень риска', fontsize=14)
    plt.ylabel('Количество', fontsize=14)
    plt.xticks(rotation=0, fontsize=12)  # Наклон подписей
    plt.yticks(fontsize=12)

    # Добавление значений на столбцы
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, str(height), ha='center', va='bottom', fontsize=12)

    # Сохранение графика
    plt.savefig("static/risk_distribution.png", bbox_inches='tight')
    plt.close()

def visualize_table(data):
    """
    Создаёт таблицу из данных с увеличенным текстом и высотой строк.
    Сохраняет таблицу в файл.
    """
    # Установка размера фигуры
    fig, ax = plt.subplots(figsize=(30, len(data) * 0.9))  # Увеличиваем высоту фигуры
    ax.axis('tight')
    ax.axis('off')

    # Данные для таблицы
    columns = list(data.columns)
    rows = data.values

    # Создание таблицы
    table = ax.table(
        cellText=rows,
        colLabels=columns,
        cellLoc='center',
        loc='center'
    )

    # Стилизация таблицы
    table.auto_set_font_size(False)
    table.set_fontsize(20)  # Увеличиваем шрифт текста
    table.auto_set_column_width(col=list(range(len(columns))))

    # Установка высоты строк
    for (row, col), cell in table.get_celld().items():
        if row == 0:  # Заголовок
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor('#4CAF50')  # Зеленый цвет
            cell.set_height(0.6)  # Высота строки заголовка
        else:
            cell.set_height(0.3)  # Высота строки данных

    # Сохраняем таблицу в файл
    plt.savefig("static/risk_table.png", bbox_inches="tight")
    plt.close()