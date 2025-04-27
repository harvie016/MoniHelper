# connect.py
from g4f.client import Client
from monitoring import run_cpu_stress
import asyncio

async def main():
    # Запускаем стресс-тест и получаем результаты
    max_values = await run_cpu_stress(60)
    
    # Формируем запрос с реальными данными
    query = f"""
    Проанализируйте данные стресс-теста компьютера:
    - Максимальная загрузка CPU: {max_values[0]:.1f}%
    - Максимальная температура CPU: {max_values[1]:.1f}°C
    - Максимальное использование памяти: {max_values[2]:.1f}%
    - Максимальная частота CPU: {max_values[3]:.1f} MHz

    На основании этих данных:
    1. Оцените стабильность работы системы
    2. Предположите возможные узкие места
    3. Дайте рекомендации по оптимизации
    4. Спрогнозируйте вероятность сбоев оборудования


    Ответ представьте на русском языке в формате технического отчёта.
    """
    
    # Отправляем запрос в GPT
    client = Client()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": query}],
        web_search=False
    )
    
    print("\nАнализ результатов стресс-теста:")
    print(response.choices[0].message.content)

if __name__ == "__main__":
    asyncio.run(main())