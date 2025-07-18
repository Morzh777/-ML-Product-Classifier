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
import subprocess
import threading
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

def parse_validation_response(response: str, products: list, elapsed_time: float) -> list:
    """Парсить ответ валидации"""
    try:
        start = response.find('{')
        end = response.rfind('}') + 1
        
        if start != -1 and end != 0:
            json_str = response[start:end]
            parsed = json.loads(json_str)
            
            results = []
            for i, product in enumerate(products):
                # Ищем результат по индексу
                product_result = None
                for result in parsed.get('results', []):
                    if result.get('index') == i + 1:
                        product_result = result
                        break
                
                if product_result:
                    results.append({
                        "product_name": product.get("name", ""),
                        "is_valid": product_result.get("is_valid", False),
                        "reason": product_result.get("reason", ""),
                        "processing_time": elapsed_time / len(products)
                    })
                else:
                    results.append({
                        "product_name": product.get("name", ""),
                        "is_valid": False,
                        "reason": "Не найден в ответе",
                        "processing_time": elapsed_time / len(products)
                    })
            
            return results
        else:
            # Fallback
            return [{"error": "Не удалось распарсить ответ"}] * len(products)
            
    except json.JSONDecodeError:
        return [{"error": "Ошибка парсинга JSON"}] * len(products)

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
            # Смешанные товары для валидации "playstation 5"
            # Валидные PlayStation товары
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
            
            # Невалидные аксессуары к PlayStation
            {
                'name': 'DualSense Controller',
                'description': 'Беспроводной геймпад для PlayStation 5'
            },
            {
                'name': 'PlayStation VR2',
                'description': 'VR гарнитура для PlayStation 5'
            },
            
            # Невалидные товары других брендов
            {
                'name': 'Nintendo Switch OLED',
                'description': 'Портативная игровая приставка Nintendo Switch'
            },
            {
                'name': 'Xbox Series X',
                'description': 'Игровая приставка Microsoft Xbox Series X'
            },
            {
                'name': 'iPhone 15 Pro Max',
                'description': 'Смартфон Apple iPhone 15 Pro Max'
            },
            {
                'name': 'NVIDIA RTX 4070 Ti',
                'description': 'Видеокарта NVIDIA GeForce RTX 4070 Ti'
            },
            {
                'name': 'Intel Core i9-14900K',
                'description': 'Процессор Intel Core i9 для настольных ПК'
            }
        ]
        
        # Тест валидации с запросом "playstation 5"
        query = "playstation 5"
        test_batch = test_products[:10]  # Смешанные товары
        logger.info(f"\n🔍 ВАЛИДАЦИЯ: Запрос '{query}' vs {len(test_batch)} товаров")
        logger.info(f"   Ожидаем: PlayStation товары = валидны, остальные = невалидны")
        
        # Создаем промпт для валидации
        validation_prompt = f"""
Запрос пользователя: "{query}"

Проверь каждый товар - подходит ли он под этот запрос?

Товары:
"""
        
        for i, product in enumerate(test_batch, 1):
            validation_prompt += f"""
{i}. {product['name']}
   Описание: {product['description']}
"""
        
        validation_prompt += f"""

Ответ в формате JSON:
{{
  "query": "{query}",
  "results": [
    {{
      "index": 1,
      "product_name": "название товара",
      "is_valid": true/false,
      "reason": "обоснование"
    }}
  ]
}}

Валидными считаются только основные товары PlayStation 5, аксессуары - невалидны.
"""
        
        # Отправляем запрос модели
        logger.info(f"⏳ Отправляем запрос модели...")
        
        # ASCII-арт анимация
        loading_frames = ["8uu==3", "8==uu3"]
        current_frame = 0
        animation_running = True
        
        def animate():
            nonlocal current_frame
            while animation_running:
                frame = loading_frames[current_frame % len(loading_frames)]
                sys.stdout.write(f"\r⏳ {frame} Валидация запроса '{query}'...")
                sys.stdout.flush()
                current_frame += 1
                time.sleep(0.3)
        
        animation_thread = threading.Thread(target=animate, daemon=True)
        animation_thread.start()
        
        start_time = time.time()
        
        result = subprocess.run(
            ["ollama", "run", "t-pro-it-2.0-optimized", validation_prompt],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=300
        )
        
        animation_running = False
        sys.stdout.write("\r" + " " * 80 + "\r")
        sys.stdout.flush()
        
        elapsed_time = time.time() - start_time
        
        if result.returncode != 0:
            logger.error(f"❌ Ошибка валидации: {result.stderr}")
            batch_results = [{"error": "Ошибка валидации"}] * len(test_batch)
        else:
            response = result.stdout.strip()
            logger.info(f"✅ Валидация готова! Время: {elapsed_time:.2f} сек")
            batch_results = parse_validation_response(response, test_batch, elapsed_time)
        
        batch_time = 0
        for i, result in enumerate(batch_results, 1):
            if 'error' in result:
                logger.error(f"❌ Ошибка товар {i}: {result['error']}")
            else:
                product_name = result.get('product_name', f'Товар {i}')
                is_valid = result.get('is_valid', False)
                reason = result.get('reason', '')
                status = "✅ ВАЛИДЕН" if is_valid else "❌ НЕВАЛИДЕН"
                logger.info(f"{status} {i}: {product_name}")
                if reason:
                    logger.info(f"   Причина: {reason}")
                batch_time += result.get('processing_time', 0)
        
        avg_batch_time = batch_time / len(test_batch) if test_batch else 0
        
        # Статистика валидации
        valid_count = 0
        invalid_count = 0
        for result in batch_results:
            if 'error' not in result:
                if result.get('is_valid', False):
                    valid_count += 1
                else:
                    invalid_count += 1
        
        logger.info(f"\n📈 РЕЗУЛЬТАТЫ ВАЛИДАЦИИ:")
        logger.info(f"   Общее время: {batch_time:.2f} сек")
        logger.info(f"   Среднее время на продукт: {avg_batch_time:.2f} сек")
        logger.info(f"   Всего товаров: {len(test_batch)}")
        logger.info(f"   ✅ Валидных: {valid_count}")
        logger.info(f"   ❌ Невалидных: {invalid_count}")
        
        # Детальная валидация
        logger.info(f"\n🔍 ДЕТАЛЬНАЯ ВАЛИДАЦИЯ:")
        logger.info(f"   Ожидаемые категории vs Фактические:")
        
        expected_validation = {
            'PlayStation 5': True,
            'PlayStation 5 Slim': True, 
            'PlayStation 5 Pro': True,
            'DualSense Controller': False,
            'PlayStation VR2': False,
            'Nintendo Switch OLED': False,
            'Xbox Series X': False,
            'iPhone 15 Pro Max': False,
            'NVIDIA RTX 4070 Ti': False,
            'Intel Core i9-14900K': False
        }
        
        correct = 0
        total = 0
        
        for i, result in enumerate(batch_results):
            if 'error' not in result:
                product_name = result.get('product_name', '')
                is_valid = result.get('is_valid', False)
                expected = expected_validation.get(product_name, False)
                
                is_correct = is_valid == expected
                if is_correct:
                    correct += 1
                total += 1
                
                status = "✅" if is_correct else "❌"
                expected_text = "валиден" if expected else "невалиден"
                actual_text = "валиден" if is_valid else "невалиден"
                logger.info(f"   {status} {product_name}")
                logger.info(f"      Ожидалось: {expected_text} | Получено: {actual_text}")
        
        accuracy = (correct / total * 100) if total > 0 else 0
        logger.info(f"\n📈 ТОЧНОСТЬ ВАЛИДАЦИИ: {accuracy:.1f}% ({correct}/{total})")
        
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