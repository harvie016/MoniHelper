# monitoring.py
import psutil
import multiprocessing
import time
from datetime import datetime
import wmi
import asyncio

def cpu_stress():
    while True:
        987654321 * 123456789  # Интенсивные вычисления

async def get_cpu_temperature():
    try:
        w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
        sensors = w.Sensor()
        for sensor in sensors:
            if sensor.SensorType == "Temperature" and "CPU" in sensor.Name:
                return float(sensor.Value)
        return 0.0
    except Exception:
        return 0.0

async def monitor_system(duration_sec):
    max_cpu = 0.0
    max_temp = 0.0
    max_mem = 0.0
    max_freq = 0.0
    
    print("\nМониторинг системы во время стресс-теста:")
    print("Время   | CPU % | Темп.°C | Память % | Частота MHz")
    print("--------|-------|---------|----------|------------")
    
    start_time = time.time()
    while time.time() - start_time < duration_sec:
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            mem_percent = psutil.virtual_memory().percent
            freq = psutil.cpu_freq().current if hasattr(psutil, "cpu_freq") else 0.0
            cpu_temp = await get_cpu_temperature()
            
            max_cpu = max(max_cpu, cpu_percent)
            max_temp = max(max_temp, cpu_temp)
            max_mem = max(max_mem, mem_percent)
            max_freq = max(max_freq, freq)
            
            now = datetime.now().strftime("%H:%M:%S")
            print(f"{now} | {cpu_percent:5.1f} | {cpu_temp:7.1f} | {mem_percent:8.1f} | {freq:10.1f}")
            
        except KeyboardInterrupt:
            break
    
    return max_cpu, max_temp, max_mem, max_freq

async def run_cpu_stress(duration_sec=10):
    processes = []
    cpu_count = multiprocessing.cpu_count()

    print(f"Запуск стресс-теста CPU на {duration_sec} секунд...")
    print(f"Используется ядер: {cpu_count}")
    
    for _ in range(cpu_count):
        p = multiprocessing.Process(target=cpu_stress)
        p.start()
        processes.append(p)
    
    max_values = await monitor_system(duration_sec)
    
    for p in processes:
        p.terminate()
    
    print("\nМаксимальные показатели во время теста:")
    print(f"- Загрузка CPU: {max_values[0]:.1f}%")
    print(f"- Температура CPU: {max_values[1]:.1f}°C")
    print(f"- Использование памяти: {max_values[2]:.1f}%")
    print(f"- Максимальная частота CPU: {max_values[3]:.1f} MHz")
    print("\nСтресс-тест завершен.")
    
    return max_values

if __name__ == "__main__":
    try:
        import wmi
    except ImportError:
        print("Установите библиотеку wmi: pip install wmi")
        exit(1)
    
    asyncio.run(run_cpu_stress(60))