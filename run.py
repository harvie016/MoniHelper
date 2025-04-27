# run.py
import asyncio
from monitoring import run_cpu_stress
from connect import main as analyze_results
import platform

async def full_test():
    try:
        # Проверка ОС
        if platform.system() != "Windows":
            print("❗ Тест поддерживается только на Windows")
            return

        # Шаг 1: Запуск стресс-теста
        print("🚀 Запуск комплексного тестирования системы\n")
        max_values = await run_cpu_stress(60)
        
        # Шаг 2: Анализ результатов
        print("\n🔍 Анализ результатов...")
        await analyze_results()
        
    except Exception as e:
        print(f"❌ Ошибка выполнения: {str(e)}")
    finally:
        print("\n✅ Тестирование завершено")

if __name__ == "__main__":
    # Проверка зависимостей
    try:
        import psutil
        import wmi
        from g4f.client import Client
    except ImportError as e:
        print(f"❌ Установите недостающие зависимости: {e.name}")
        print("Выполните: pip install psutil wmi g4f")
        exit(1)
    
    # Запуск главного процесса
    asyncio.run(full_test())