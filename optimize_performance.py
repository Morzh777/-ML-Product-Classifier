#!/usr/bin/env python3
"""
Скрипт для оптимизации производительности ML Product Classifier
by Morzh - Проект создан для развития валидатора товаров электроники
"""

import subprocess
import json
import time
import sys

def create_fast_modelfile():
    """Создать оптимизированный Modelfile для максимальной скорости"""
    
    modelfile_content = """FROM hf.co/t-tech/T-pro-it-2.0-GGUF:Q2_K

# Максимальная оптимизация для скорости
PARAMETER num_ctx 2048          # Уменьшаем контекст для скорости
PARAMETER num_gpu 40            # Больше слоев на GPU
PARAMETER num_thread 12         # Больше потоков CPU
PARAMETER temperature 0.1       # Низкая температура для точности
PARAMETER top_k 20              # Уменьшаем для скорости
PARAMETER top_p 0.8             # Оптимизируем
PARAMETER repeat_penalty 1.0    # Отключаем для скорости
PARAMETER seed 42               # Фиксированный seed

# Системный промпт для быстрых ответов
SYSTEM """Ты быстрый классификатор товаров. Отвечай только JSON без лишних слов.
Категории: iphone, processors, videocards, motherboards, playstation, nintendo-switch, steam-deck
Формат: {"category": "название", "confidence": 0.95, "reasoning": "краткое обоснование"}"""

# Шаблон для быстрых ответов
TEMPLATE """Классифицируй: {{.Input}}

JSON:"""
"""
    
    with open('Modelfile.fast', 'w', encoding='utf-8') as f:
        f.write(modelfile_content)
    
    print("✅ Создан Modelfile.fast для максимальной скорости")

def create_balanced_modelfile():
    """Создать сбалансированный Modelfile"""
    
    modelfile_content = """FROM hf.co/t-tech/T-pro-it-2.0-GGUF:Q2_K

# Сбалансированная оптимизация
PARAMETER num_ctx 3072          # Средний контекст
PARAMETER num_gpu 35            # Оптимальное количество слоев на GPU
PARAMETER num_thread 8          # Оптимальные потоки
PARAMETER temperature 0.2       # Немного выше для лучшего качества
PARAMETER top_k 30              # Сбалансированно
PARAMETER top_p 0.9             # Хорошее качество
PARAMETER repeat_penalty 1.05   # Легкий penalty
PARAMETER seed 42

SYSTEM """Ты классификатор товаров. Отвечай в JSON формате.
Категории: iphone, processors, videocards, motherboards, playstation, nintendo-switch, steam-deck
Формат: {"category": "название", "confidence": 0.95, "reasoning": "обоснование"}"""

TEMPLATE """Товар: {{.Input}}

Классификация:"""
"""
    
    with open('Modelfile.balanced', 'w', encoding='utf-8') as f:
        f.write(modelfile_content)
    
    print("✅ Создан Modelfile.balanced для баланса скорости и качества")

def benchmark_models():
    """Тестировать производительность разных моделей"""
    
    test_prompt = "iPhone 15 Pro Max 256GB - Смартфон Apple с процессором A17 Pro"
    
    models = [
        ("t-pro-it-2.0-optimized", "Текущая модель"),
        ("t-pro-it-2.0-fast", "Быстрая модель"),
        ("t-pro-it-2.0-balanced", "Сбалансированная модель")
    ]
    
    print("🏃‍♂️ Тестирование производительности моделей...")
    print("=" * 60)
    
    results = []
    
    for model_name, description in models:
        try:
            print(f"\n🔍 Тестируем {description} ({model_name})...")
            
            start_time = time.time()
            result = subprocess.run(
                ["ollama", "run", model_name, test_prompt],
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=30
            )
            elapsed_time = time.time() - start_time
            
            if result.returncode == 0:
                print(f"✅ Время: {elapsed_time:.2f} сек")
                print(f"📝 Ответ: {result.stdout.strip()[:100]}...")
                results.append((model_name, elapsed_time, "✅"))
            else:
                print(f"❌ Ошибка: {result.stderr}")
                results.append((model_name, 0, "❌"))
                
        except subprocess.TimeoutExpired:
            print(f"⏰ Таймаут (>30 сек)")
            results.append((model_name, 30, "⏰"))
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            results.append((model_name, 0, "❌"))
    
    # Итоги
    print("\n" + "=" * 60)
    print("📊 ИТОГИ ТЕСТИРОВАНИЯ:")
    print("=" * 60)
    
    for model_name, time_taken, status in results:
        print(f"{status} {model_name}: {time_taken:.2f} сек")
    
    # Рекомендации
    working_models = [r for r in results if r[2] == "✅"]
    if working_models:
        fastest = min(working_models, key=lambda x: x[1])
        print(f"\n🏆 Рекомендуемая модель: {fastest[0]} ({fastest[1]:.2f} сек)")

def main():
    """Основная функция"""
    print("🚀 Оптимизация производительности ML Product Classifier")
    print("=" * 60)
    
    # Создаем оптимизированные модели
    create_fast_modelfile()
    create_balanced_modelfile()
    
    print("\n📦 Создание оптимизированных моделей...")
    
    # Создаем быструю модель
    print("\n🔄 Создаем быструю модель...")
    result = subprocess.run(
        ["ollama", "create", "t-pro-it-2.0-fast", "-f", "Modelfile.fast"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("✅ Быстрая модель создана")
    else:
        print(f"❌ Ошибка создания быстрой модели: {result.stderr}")
    
    # Создаем сбалансированную модель
    print("\n🔄 Создаем сбалансированную модель...")
    result = subprocess.run(
        ["ollama", "create", "t-pro-it-2.0-balanced", "-f", "Modelfile.balanced"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("✅ Сбалансированная модель создана")
    else:
        print(f"❌ Ошибка создания сбалансированной модели: {result.stderr}")
    
    # Тестируем производительность
    print("\n🧪 Тестирование производительности...")
    benchmark_models()
    
    print("\n📋 Следующие шаги:")
    print("1. Выберите лучшую модель из тестов")
    print("2. Обновите model_name в src/ml_model.py")
    print("3. Протестируйте на реальных данных")
    print("4. Для дообучения используйте fine-tuning")

if __name__ == "__main__":
    main() 