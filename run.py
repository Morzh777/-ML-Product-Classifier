#!/usr/bin/env python3
"""
ML Product Classifier - Основной файл для запуска классификатора
by Morzh - Проект создан для развития валидатора товаров электроники
"""

import os
import sys
import json
import logging
import time
from pathlib import Path

# Настройка кодировки для Windows
if sys.platform == "win32":
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Добавляем путь к модулям
sys.path.append(str(Path(__file__).parent / "src"))

from ml_model import ProductClassifier

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)
logger = logging.getLogger(__name__)

def main():
    """Основная функция"""
    try:
        logger.info("🚀 Запуск ML Product Classifier")
        
        # Инициализируем классификатор
        logger.info("Инициализируем классификатор...")
        classifier = ProductClassifier()
        
        # Получаем информацию о модели
        model_info = classifier.get_model_info()
        logger.info(f"Информация о модели: {json.dumps(model_info, indent=2, ensure_ascii=False)}")
        
        # Загружаем модель
        logger.info("Загружаем модель через Ollama...")
        start_time = time.time()
        
        if not classifier.load_model():
            logger.error("❌ Не удалось загрузить модель")
            return
        
        load_time = time.time() - start_time
        logger.info(f"✅ Модель загружена за {load_time:.2f} секунд")
        
        # Тестируем модель
        logger.info("Тестируем модель...")
        test_products = [
            {
                'name': 'iPhone 15 Pro Max 256GB',
                'description': 'Смартфон Apple с процессором A17 Pro'
            },
            {
                'name': 'Intel Core i9-14900K',
                'description': 'Процессор Intel для настольных ПК'
            },
            {
                'name': 'NVIDIA RTX 4070 Ti',
                'description': 'Видеокарта NVIDIA с 12GB GDDR6X'
            }
        ]
        
        total_time = 0
        for i, product in enumerate(test_products, 1):
            logger.info(f"\n🧪 Тест {i}: {product['name']}")
            result = classifier.classify_product(product)
            
            if 'error' in result:
                logger.error(f"❌ Ошибка: {result['error']}")
            else:
                logger.info(f"✅ Результат: {json.dumps(result, indent=2, ensure_ascii=False)}")
                total_time += result.get('processing_time', 0)
        
        avg_time = total_time / len(test_products) if test_products else 0
        logger.info(f"\n📈 Итоги:")
        logger.info(f"   Общее время: {total_time:.2f} сек")
        logger.info(f"   Среднее время на продукт: {avg_time:.2f} сек")
        
        if avg_time < 10:
            logger.info("🚀 Отличная производительность!")
        elif avg_time < 20:
            logger.info("⚡ Хорошая производительность")
        else:
            logger.info("🐌 Медленная работа, нужна оптимизация")
        
        logger.info("✅ Тестирование завершено")
        
    except Exception as e:
        logger.error(f"❌ Ошибка в main: {str(e)}")
        raise

if __name__ == "__main__":
    main() 