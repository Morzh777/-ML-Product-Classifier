#!/usr/bin/env python3
"""
Скрипт для проверки установки ML Product Classifier
"""

import subprocess
import sys
import json

def check_command(command, description):
    """Проверить команду"""
    print(f"🔍 Проверяем {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"✅ {description} - OK")
            return True
        else:
            print(f"❌ {description} - НЕ НАЙДЕН")
            return False
    except Exception as e:
        print(f"❌ {description} - ОШИБКА: {e}")
        return False

def main():
    """Основная функция"""
    print("🔧 Проверка установки ML Product Classifier")
    print("=" * 50)
    
    # Проверяем Python
    python_ok = check_command("python --version", "Python")
    
    # Проверяем pip
    pip_ok = check_command("pip --version", "pip")
    
    # Проверяем Ollama
    ollama_ok = check_command("ollama --version", "Ollama")
    
    # Проверяем модели Ollama
    print("\n🔍 Проверяем модели Ollama...")
    try:
        result = subprocess.run("ollama list", shell=True, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            models = result.stdout.strip()
            if "t-pro-it-2.0-optimized" in models:
                print("✅ Модель t-pro-it-2.0-optimized - НАЙДЕНА")
                model_ok = True
            else:
                print("❌ Модель t-pro-it-2.0-optimized - НЕ НАЙДЕНА")
                print("   Запустите: ollama create t-pro-it-2.0-optimized -f Modelfile.optimized")
                model_ok = False
        else:
            print("❌ Не удалось получить список моделей")
            model_ok = False
    except Exception as e:
        print(f"❌ Ошибка проверки моделей: {e}")
        model_ok = False
    
    # Проверяем зависимости Python
    print("\n🔍 Проверяем Python зависимости...")
    try:
        import psutil
        print("✅ psutil - OK")
        psutil_ok = True
    except ImportError:
        print("❌ psutil - НЕ УСТАНОВЛЕН")
        print("   Запустите: pip install -r requirements.txt")
        psutil_ok = False
    
    try:
        import tqdm
        print("✅ tqdm - OK")
        tqdm_ok = True
    except ImportError:
        print("❌ tqdm - НЕ УСТАНОВЛЕН")
        print("   Запустите: pip install -r requirements.txt")
        tqdm_ok = False
    
    # Итоги
    print("\n" + "=" * 50)
    print("📊 ИТОГИ ПРОВЕРКИ:")
    
    all_ok = python_ok and pip_ok and ollama_ok and model_ok and psutil_ok and tqdm_ok
    
    if all_ok:
        print("✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ!")
        print("🚀 Можете запускать: python run.py")
    else:
        print("❌ ЕСТЬ ПРОБЛЕМЫ:")
        if not python_ok:
            print("   - Установите Python 3.8+")
        if not pip_ok:
            print("   - Установите pip")
        if not ollama_ok:
            print("   - Установите Ollama: https://ollama.ai")
        if not model_ok:
            print("   - Создайте модель: ollama create t-pro-it-2.0-optimized -f Modelfile.optimized")
        if not psutil_ok or not tqdm_ok:
            print("   - Установите зависимости: pip install -r requirements.txt")

if __name__ == "__main__":
    main() 