#!/usr/bin/env python3
"""
Скрипт для дообучения модели на специфичных данных
by Morzh - Проект создан для развития валидатора товаров электроники
"""

import json
import subprocess
import os
from pathlib import Path

def create_training_data():
    """Создать данные для дообучения"""
    
    training_data = [
        # iPhone
        {"input": "iPhone 15 Pro Max 256GB", "output": "{\"category\": \"iphone\", \"confidence\": 0.98, \"reasoning\": \"iPhone 15 Pro Max - флагманский смартфон Apple\"}"},
        {"input": "iPhone 14 128GB", "output": "{\"category\": \"iphone\", \"confidence\": 0.98, \"reasoning\": \"iPhone 14 - смартфон Apple\"}"},
        {"input": "iPhone SE 2022", "output": "{\"category\": \"iphone\", \"confidence\": 0.98, \"reasoning\": \"iPhone SE - компактный смартфон Apple\"}"},
        
        # Processors
        {"input": "Intel Core i9-14900K", "output": "{\"category\": \"processors\", \"confidence\": 0.98, \"reasoning\": \"Intel Core i9 - процессор для настольных ПК\"}"},
        {"input": "AMD Ryzen 9 7950X", "output": "{\"category\": \"processors\", \"confidence\": 0.98, \"reasoning\": \"AMD Ryzen 9 - процессор для настольных ПК\"}"},
        {"input": "Intel Core i7-13700K", "output": "{\"category\": \"processors\", \"confidence\": 0.98, \"reasoning\": \"Intel Core i7 - процессор для настольных ПК\"}"},
        
        # Videocards
        {"input": "NVIDIA RTX 4070 Ti", "output": "{\"category\": \"videocards\", \"confidence\": 0.98, \"reasoning\": \"NVIDIA RTX - видеокарта для игр\"}"},
        {"input": "AMD RX 7900 XTX", "output": "{\"category\": \"videocards\", \"confidence\": 0.98, \"reasoning\": \"AMD RX - видеокарта для игр\"}"},
        {"input": "NVIDIA RTX 4090", "output": "{\"category\": \"videocards\", \"confidence\": 0.98, \"reasoning\": \"NVIDIA RTX - флагманская видеокарта\"}"},
        
        # Motherboards
        {"input": "ASUS ROG STRIX Z790-E", "output": "{\"category\": \"motherboards\", \"confidence\": 0.98, \"reasoning\": \"ASUS ROG - материнская плата для Intel\"}"},
        {"input": "MSI MPG B650", "output": "{\"category\": \"motherboards\", \"confidence\": 0.98, \"reasoning\": \"MSI MPG - материнская плата для AMD\"}"},
        {"input": "Gigabyte AORUS X670E", "output": "{\"category\": \"motherboards\", \"confidence\": 0.98, \"reasoning\": \"Gigabyte AORUS - материнская плата для AMD\"}"},
        
        # PlayStation
        {"input": "PlayStation 5", "output": "{\"category\": \"playstation\", \"confidence\": 0.98, \"reasoning\": \"PlayStation 5 - игровая консоль Sony\"}"},
        {"input": "PS5 Digital Edition", "output": "{\"category\": \"playstation\", \"confidence\": 0.98, \"reasoning\": \"PS5 Digital - цифровая версия консоли Sony\"}"},
        {"input": "PlayStation 4 Pro", "output": "{\"category\": \"playstation\", \"confidence\": 0.98, \"reasoning\": \"PlayStation 4 Pro - игровая консоль Sony\"}"},
        
        # Nintendo Switch
        {"input": "Nintendo Switch OLED", "output": "{\"category\": \"nintendo-switch\", \"confidence\": 0.98, \"reasoning\": \"Nintendo Switch OLED - гибридная консоль Nintendo\"}"},
        {"input": "Nintendo Switch Lite", "output": "{\"category\": \"nintendo-switch\", \"confidence\": 0.98, \"reasoning\": \"Nintendo Switch Lite - портативная консоль Nintendo\"}"},
        {"input": "Nintendo Switch", "output": "{\"category\": \"nintendo-switch\", \"confidence\": 0.98, \"reasoning\": \"Nintendo Switch - гибридная консоль Nintendo\"}"},
        
        # Steam Deck
        {"input": "Steam Deck 512GB", "output": "{\"category\": \"steam-deck\", \"confidence\": 0.98, \"reasoning\": \"Steam Deck - портативная игровая консоль Valve\"}"},
        {"input": "Steam Deck 256GB", "output": "{\"category\": \"steam-deck\", \"confidence\": 0.98, \"reasoning\": \"Steam Deck - портативная игровая консоль Valve\"}"},
        {"input": "Steam Deck 64GB", "output": "{\"category\": \"steam-deck\", \"confidence\": 0.98, \"reasoning\": \"Steam Deck - портативная игровая консоль Valve\"}"},
    ]
    
    # Сохраняем в JSON
    with open('training_data.json', 'w', encoding='utf-8') as f:
        json.dump(training_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Создано {len(training_data)} примеров для обучения")
    return training_data

def create_finetune_modelfile():
    """Создать Modelfile для дообучения"""
    
    modelfile_content = """FROM t-pro-it-2.0-optimized

# Параметры для дообучения
PARAMETER num_ctx 4096
PARAMETER num_gpu 35
PARAMETER num_thread 8
PARAMETER temperature 0.1
PARAMETER top_k 40
PARAMETER top_p 0.9
PARAMETER repeat_penalty 1.1

# Системный промпт для классификации
SYSTEM """Ты точный классификатор товаров электроники. Отвечай только в JSON формате.
Категории: iphone, processors, videocards, motherboards, playstation, nintendo-switch, steam-deck
Формат ответа: {"category": "название_категории", "confidence": 0.95, "reasoning": "краткое обоснование"}"""

# Шаблон для обучения
TEMPLATE """Товар: {{.Input}}

Классификация: {{.Response}}"""

# Данные для обучения
{{range .Data}}
{{.Input}}
{{.Output}}
{{end}}
"""
    
    with open('Modelfile.finetune', 'w', encoding='utf-8') as f:
        f.write(modelfile_content)
    
    print("✅ Создан Modelfile.finetune для дообучения")

def prepare_training_data():
    """Подготовить данные в формате для Ollama"""
    
    # Загружаем данные
    with open('training_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Создаем файл в формате Ollama
    with open('training_data.txt', 'w', encoding='utf-8') as f:
        for item in data:
            f.write(f"Товар: {item['input']}\n")
            f.write(f"Классификация: {item['output']}\n\n")
    
    print("✅ Данные подготовлены для обучения")

def main():
    """Основная функция"""
    print("🎓 Дообучение модели ML Product Classifier")
    print("=" * 50)
    
    # Создаем данные для обучения
    print("📝 Создание данных для обучения...")
    create_training_data()
    
    # Подготавливаем данные
    print("🔧 Подготовка данных...")
    prepare_training_data()
    
    # Создаем Modelfile для дообучения
    print("📋 Создание Modelfile для дообучения...")
    create_finetune_modelfile()
    
    print("\n📋 Инструкции для дообучения:")
    print("1. Убедитесь, что базовая модель t-pro-it-2.0-optimized создана")
    print("2. Запустите команду:")
    print("   ollama create t-pro-it-2.0-finetuned -f Modelfile.finetune")
    print("3. Протестируйте новую модель:")
    print("   ollama run t-pro-it-2.0-finetuned 'iPhone 15 Pro'")
    print("4. Обновите model_name в src/ml_model.py на t-pro-it-2.0-finetuned")
    
    print("\n💡 Дополнительные советы:")
    print("- Добавьте больше примеров в training_data.json")
    print("- Используйте реальные данные из вашего проекта")
    print("- Тестируйте на edge cases (неоднозначные товары)")
    print("- Мониторьте точность классификации")

if __name__ == "__main__":
    main() 