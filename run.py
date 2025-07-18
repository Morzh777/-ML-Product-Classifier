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
            # PlayStation 5 - основная приставка
            {
                'name': 'PlayStation 5',
                'description': 'Игровая приставка Sony PlayStation 5'
            },
            {
                'name': 'PlayStation 5 Slim',
                'description': 'Компактная игровая приставка Sony PS5'
            },
            {
                'name': 'PlayStation 5 Pro',
                'description': 'Мощная игровая приставка Sony PS5 Pro'
            },
            
            # Аксессуары к PlayStation (должны быть unknown)
            {
                'name': 'DualSense Controller',
                'description': 'Беспроводной геймпад для PlayStation 5'
            },
            {
                'name': 'PlayStation VR2',
                'description': 'VR гарнитура для PlayStation 5'
            },
            {
                'name': 'DualSense Edge',
                'description': 'Профессиональный геймпад для PS5'
            },
            {
                'name': 'PlayStation 5 Stand',
                'description': 'Подставка для вертикальной установки PS5'
            },
            {
                'name': 'PlayStation 5 SSD',
                'description': 'Внутренний SSD для расширения памяти PS5'
            },
            
            # Nintendo Switch - основная приставка
            {
                'name': 'Nintendo Switch OLED',
                'description': 'Портативная игровая приставка Nintendo Switch'
            },
            {
                'name': 'Nintendo Switch Lite',
                'description': 'Компактная портативная приставка Nintendo'
            },
            
            # Аксессуары к Nintendo (должны быть unknown)
            {
                'name': 'Joy-Con Controllers',
                'description': 'Беспроводные контроллеры для Nintendo Switch'
            },
            {
                'name': 'Nintendo Switch Pro Controller',
                'description': 'Профессиональный геймпад для Switch'
            },
            {
                'name': 'Nintendo Switch Dock',
                'description': 'Док-станция для подключения к TV'
            },
            
            # Steam Deck - основная приставка
            {
                'name': 'Steam Deck OLED',
                'description': 'Портативная игровая приставка Valve Steam Deck'
            },
            {
                'name': 'Steam Deck LCD',
                'description': 'Портативная игровая приставка Valve'
            },
            
            # Аксессуары к Steam Deck (должны быть unknown)
            {
                'name': 'Steam Deck Dock',
                'description': 'Док-станция для Steam Deck'
            },
            {
                'name': 'Steam Deck Case',
                'description': 'Защитный чехол для Steam Deck'
            },
            
            # iPhone - основные смартфоны
            {
                'name': 'iPhone 15 Pro Max 256GB',
                'description': 'Смартфон Apple iPhone 15 Pro Max'
            },
            {
                'name': 'iPhone 15 Pro 128GB',
                'description': 'Смартфон Apple iPhone 15 Pro'
            },
            {
                'name': 'iPhone 14 128GB',
                'description': 'Смартфон Apple iPhone 14'
            },
            
            # Аксессуары к iPhone (должны быть unknown)
            {
                'name': 'AirPods Pro 2',
                'description': 'Беспроводные наушники Apple для iPhone'
            },
            {
                'name': 'Apple Watch Series 9',
                'description': 'Умные часы Apple для iPhone'
            },
            {
                'name': 'iPhone 15 Pro Case',
                'description': 'Защитный чехол для iPhone 15 Pro'
            },
            {
                'name': 'MagSafe Charger',
                'description': 'Беспроводная зарядка для iPhone'
            },
            
            # Процессоры - основные компоненты
            {
                'name': 'Intel Core i9-14900K',
                'description': 'Процессор Intel Core i9 для настольных ПК'
            },
            {
                'name': 'AMD Ryzen 9 7950X',
                'description': 'Процессор AMD Ryzen 9 для настольных ПК'
            },
            
            # Аксессуары к процессорам (должны быть unknown)
            {
                'name': 'Noctua NH-D15',
                'description': 'Кулер для процессора Intel/AMD'
            },
            {
                'name': 'Thermal Grizzly Kryonaut',
                'description': 'Термопаста для процессора'
            },
            
            # Видеокарты - основные компоненты
            {
                'name': 'NVIDIA RTX 4070 Ti',
                'description': 'Видеокарта NVIDIA GeForce RTX 4070 Ti'
            },
            {
                'name': 'AMD RX 7900 XTX',
                'description': 'Видеокарта AMD Radeon RX 7900 XTX'
            },
            
            # Аксессуары к видеокартам (должны быть unknown)
            {
                'name': 'Corsair RM850x',
                'description': 'Блок питания для видеокарты'
            },
            {
                'name': 'GPU Support Bracket',
                'description': 'Поддержка для тяжелой видеокарты'
            }
        ]
        
        # Тест батчинга (только первые 10 товаров для стабильности)
        test_batch = test_products[:10]
        logger.info(f"\n🚀 Тест батч классификации ({len(test_batch)} товаров)")
        batch_results = classifier.classify_products_batch(test_batch)
        
        batch_time = 0
        for i, result in enumerate(batch_results, 1):
            if 'error' in result:
                logger.error(f"❌ Ошибка товар {i}: {result['error']}")
            else:
                product_name = result.get('product_name', f'Товар {i}')
                category = result.get('predicted_category', 'unknown')
                confidence = result.get('confidence', 0.0)
                logger.info(f"✅ Товар {i}: {product_name} → {category} ({confidence:.2f})")
                batch_time += result.get('processing_time', 0)
        
        avg_batch_time = batch_time / len(test_batch) if test_batch else 0
        
        # Статистика по категориям
        category_stats = {}
        for result in batch_results:
            if 'error' not in result:
                category = result.get('predicted_category', 'unknown')
                if category not in category_stats:
                    category_stats[category] = {'count': 0, 'confidence_sum': 0}
                category_stats[category]['count'] += 1
                category_stats[category]['confidence_sum'] += result.get('confidence', 0)
        
        logger.info(f"\n📈 Батч результаты:")
        logger.info(f"   Общее время: {batch_time:.2f} сек")
        logger.info(f"   Среднее время на продукт: {avg_batch_time:.2f} сек")
        logger.info(f"   Всего товаров: {len(test_batch)}")
        
        logger.info(f"\n📊 Статистика по категориям:")
        for category, stats in category_stats.items():
            avg_conf = stats['confidence_sum'] / stats['count'] if stats['count'] > 0 else 0
            logger.info(f"   {category}: {stats['count']} товаров (средняя уверенность: {avg_conf:.2f})")
        
        # Тест по одному для сравнения
        logger.info(f"\n🔍 Тест классификации по одному")
        single_total_time = 0
        test_count = 0
        for i, product in enumerate(test_products[:5], 1):  # Первые 5 товаров
            logger.info(f"🧪 Тест {i}: {product['name']}")
            result = classifier.classify_product(product)
            
            if 'error' in result:
                logger.error(f"❌ Ошибка: {result['error']}")
            else:
                logger.info(f"✅ Результат: {result['predicted_category']} ({result['confidence']:.2f})")
                single_total_time += result.get('processing_time', 0)
                test_count += 1
        
        avg_single_time = single_total_time / test_count if test_count > 0 else 0
        logger.info(f"\n📊 Сравнение:")
        logger.info(f"   Батч: {avg_batch_time:.2f} сек/товар")
        logger.info(f"   По одному: {avg_single_time:.2f} сек/товар")
        
        if avg_batch_time > 0 and avg_single_time > 0:
            if avg_batch_time < avg_single_time:
                speedup = avg_single_time / avg_batch_time
                logger.info(f"🚀 Батч быстрее в {speedup:.1f}x раз!")
            else:
                speedup = avg_batch_time / avg_single_time
                logger.info(f"⚡ Одиночная классификация быстрее в {speedup:.1f}x раз!")
        else:
            logger.info("⚠️ Не удалось сравнить производительность")
        
        logger.info("✅ Тестирование завершено")
        
    except Exception as e:
        logger.error(f"❌ Ошибка в main: {str(e)}")
        raise

if __name__ == "__main__":
    main() 