#!/usr/bin/env python3
"""
Скрипт для инициализации git репо
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Выполнить команду с выводом"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"✅ {description} - успешно")
            if result.stdout.strip():
                print(f"   {result.stdout.strip()}")
        else:
            print(f"❌ {description} - ошибка")
            if result.stderr.strip():
                print(f"   {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} - исключение: {e}")
        return False
    return True

def main():
    """Основная функция"""
    print("🚀 Инициализация git репо для ML Product Classifier")
    
    # Проверяем, что мы в правильной директории
    if not Path("src/ml_model.py").exists():
        print("❌ Файл src/ml_model.py не найден. Запустите из корня проекта.")
        return
    
    # Инициализируем git
    if not run_command("git init", "Инициализация git"):
        return
    
    # Добавляем файлы
    if not run_command("git add .", "Добавление файлов"):
        return
    
    # Первый коммит
    if not run_command('git commit -m "Initial commit: ML Product Classifier"', "Первый коммит"):
        return
    
    print("\n✅ Git репо инициализирован!")
    print("\n📋 Следующие шаги:")
    print("1. Создайте репо на GitHub/GitLab")
    print("2. Добавьте remote:")
    print("   git remote add origin <your-repo-url>")
    print("3. Запушьте код:")
    print("   git push -u origin main")
    print("\n🔧 Для установки зависимостей:")
    print("   pip install -r requirements.txt")
    print("\n🚀 Для запуска:")
    print("   python run.py")

if __name__ == "__main__":
    main() 