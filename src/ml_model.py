#!/usr/bin/env python3
"""
ML Model - Классификатор продуктов с использованием Ollama
by Morzh - Проект создан для развития валидатора товаров электроники
"""

import json
import logging
import time
import subprocess
import sys
import psutil
import threading
from typing import Dict, Any

# Настройка кодировки для Windows
if sys.platform == "win32":
    import os
    os.environ['PYTHONIOENCODING'] = 'utf-8'

logger = logging.getLogger(__name__)

class ResourceMonitor:
    """Мониторинг ресурсов системы"""
    
    def __init__(self):
        self.monitoring = False
        self.stats = {}
    
    def start_monitoring(self):
        """Начать мониторинг ресурсов"""
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Остановить мониторинг"""
        self.monitoring = False
    
    def _monitor_loop(self):
        """Цикл мониторинга"""
        while self.monitoring:
            try:
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                gpu_info = self._get_gpu_info()
                
                self.stats = {
                    'cpu_percent': cpu_percent,
                    'ram_percent': memory.percent,
                    'ram_used_gb': memory.used / (1024**3),
                    'ram_total_gb': memory.total / (1024**3),
                    'gpu_info': gpu_info,
                    'timestamp': time.time()
                }
                
                time.sleep(1)
            except Exception as e:
                logger.warning(f"Ошибка мониторинга: {e}")
                time.sleep(2)
    
    def _get_gpu_info(self) -> Dict[str, Any]:
        """Получить информацию о GPU"""
        try:
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=name,memory.used,memory.total,utilization.gpu', 
                 '--format=csv,noheader,nounits'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                gpu_info = []
                
                for line in lines:
                    if line.strip():
                        parts = line.split(', ')
                        if len(parts) >= 4:
                            gpu_info.append({
                                'name': parts[0],
                                'memory_used_mb': int(parts[1]),
                                'memory_total_mb': int(parts[2]),
                                'utilization_percent': int(parts[3])
                            })
                
                return gpu_info
            else:
                return []
                
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            return []
    
    def get_current_stats(self) -> Dict[str, Any]:
        """Получить текущую статистику"""
        return self.stats.copy()

class ProductClassifier:
    """Классификатор продуктов с использованием модели T-pro-it-2.0"""
    
    def __init__(self):
        self.model_name = "t-pro-it-2.0-optimized"
        self.is_loaded = False
        self.categories = [
            "iphone", "processors", "videocards", "motherboards", 
            "playstation", "nintendo-switch", "steam-deck"
        ]
        self.resource_monitor = ResourceMonitor()
    
    def get_model_info(self) -> Dict[str, Any]:
        """Получить информацию о модели"""
        return {
            "model_name": self.model_name,
            "is_loaded": self.is_loaded,
            "method": "t_pro_it_2_0",
            "categories": self.categories,
            "platform": sys.platform,
            "model_size_gb": 12.3
        }
    
    def load_model(self) -> bool:
        """Загрузить модель T-pro-it-2.0"""
        try:
            logger.info(f"Загружаем модель {self.model_name} (T-pro-it-2.0)...")
            
            self.resource_monitor.start_monitoring()
            
            result = subprocess.run(
                ["ollama", "list"], 
                capture_output=True, 
                text=True, 
                encoding='utf-8'
            )
            
            if result.returncode != 0:
                logger.error("Модель не найдена")
                return False
            
            if self.model_name not in result.stdout:
                logger.error(f"Модель {self.model_name} (T-pro-it-2.0) не найдена")
                return False
            
            self.is_loaded = True
            logger.info("✅ Модель загружена успешно")
            
            stats = self.resource_monitor.get_current_stats()
            logger.info(f"📊 Ресурсы: CPU {stats.get('cpu_percent', 0):.1f}%, RAM {stats.get('ram_percent', 0):.1f}%")
            
            return True
            
        except Exception as e:
            logger.error(f"Ошибка загрузки модели: {str(e)}")
            return False
    
    def classify_products_batch(self, products: list) -> list:
        """Классифицировать несколько продуктов одним запросом"""
        if not self.is_loaded:
            return [{"error": "Модель не загружена"}] * len(products)
        
        try:
            prompt = self._create_batch_prompt(products)
            
            logger.info(f"🔍 Батч классификация: {len(products)} товаров")
            
            # ASCII-арт анимация для батча
            loading_frames = ["8uu==3", "8==uu3"]
            current_frame = 0
            animation_running = True
            
            def animate():
                nonlocal current_frame
                while animation_running:
                    frame = loading_frames[current_frame % len(loading_frames)]
                    sys.stdout.write(f"\r⏳ {frame} Батч классификация {len(products)} товаров...")
                    sys.stdout.flush()
                    current_frame += 1
                    time.sleep(0.3)
            
            animation_thread = threading.Thread(target=animate, daemon=True)
            animation_thread.start()
            
            start_time = time.time()
            result = subprocess.run(
                ["ollama", "run", self.model_name, prompt],
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=300  # Больше времени для батча
            )
            
            animation_running = False
            sys.stdout.write("\r" + " " * 80 + "\r")
            sys.stdout.flush()
            
            elapsed_time = time.time() - start_time
            
            if result.returncode != 0:
                return [{"error": f"Ошибка модели: {result.stderr}"}] * len(products)
            
            response = result.stdout.strip()
            stats = self.resource_monitor.get_current_stats()
            
            logger.info(f"✅ Батч готов! Время: {elapsed_time:.2f} сек ({elapsed_time/len(products):.2f} сек/товар)")
            logger.debug(f"Ответ модели: {response[:500]}...")
            
            return self._parse_batch_response(response, products, elapsed_time, stats)
            
        except subprocess.TimeoutExpired:
            animation_running = False
            sys.stdout.write("\r" + " " * 80 + "\r")
            sys.stdout.flush()
            return [{"error": "Таймаут при батч классификации"}] * len(products)
        except Exception as e:
            animation_running = False
            sys.stdout.write("\r" + " " * 80 + "\r")
            sys.stdout.flush()
            return [{"error": f"Ошибка батч классификации: {str(e)}"}] * len(products)

    def classify_product(self, product: Dict[str, str]) -> Dict[str, Any]:
        """Классифицировать продукт"""
        if not self.is_loaded:
            return {"error": "Модель не загружена"}
        
        try:
            prompt = self._create_classification_prompt(product)
            
            stats = self.resource_monitor.get_current_stats()
            logger.info(f"🔍 Классификация: {product.get('name', '')[:30]}...")
            
            # ASCII-арт анимация
            loading_frames = ["8uu==3", "8==uu3"]
            current_frame = 0
            animation_running = True
            
            def animate():
                nonlocal current_frame
                while animation_running:
                    frame = loading_frames[current_frame % len(loading_frames)]
                    sys.stdout.write(f"\r⏳ {frame} {product.get('name', '')[:30]}...")
                    sys.stdout.flush()
                    current_frame += 1
                    time.sleep(0.3)
            
            animation_thread = threading.Thread(target=animate, daemon=True)
            animation_thread.start()
            
            start_time = time.time()
            result = subprocess.run(
                ["ollama", "run", self.model_name, prompt],
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=120
            )
            
            animation_running = False
            sys.stdout.write("\r" + " " * 80 + "\r")
            sys.stdout.flush()
            
            elapsed_time = time.time() - start_time
            
            if result.returncode != 0:
                return {"error": f"Ошибка Ollama: {result.stderr}"}
            
            response = result.stdout.strip()
            
            stats = self.resource_monitor.get_current_stats()
            logger.info(f"✅ Готово! Время: {elapsed_time:.2f} сек")
            
            parsed_response = self._parse_classification_response(response)
            
            return {
                "product_name": product.get("name", ""),
                "predicted_category": parsed_response.get("category", "unknown"),
                "confidence": parsed_response.get("confidence", 0.0),
                "full_response": response,
                "method": "ollama",
                "processing_time": elapsed_time,
                "resources": stats
            }
            
        except subprocess.TimeoutExpired:
            animation_running = False
            sys.stdout.write("\r" + " " * 80 + "\r")
            sys.stdout.flush()
            return {"error": "Таймаут при классификации"}
        except Exception as e:
            animation_running = False
            sys.stdout.write("\r" + " " * 80 + "\r")
            sys.stdout.flush()
            return {"error": f"Ошибка классификации: {str(e)}"}
    
    def _create_batch_prompt(self, products: list) -> str:
        """Создать промпт для батч классификации"""
        categories_str = ", ".join(self.categories)
        
        products_text = ""
        for i, product in enumerate(products, 1):
            products_text += f"""
{i}. Товар: {product.get('name', '')}
   Описание: {product.get('description', '')}
"""
        
        prompt = f"""
Классифицируй все товары по одной из категорий: {categories_str}

{products_text}

Ответ в формате JSON массив:
[
  {{
    "index": 1,
    "category": "название_категории",
    "confidence": 0.95,
    "reasoning": "обоснование выбора"
  }},
  {{
    "index": 2,
    "category": "название_категории", 
    "confidence": 0.95,
    "reasoning": "обоснование выбора"
  }}
]

Если не можешь определить категорию, используй "unknown" с confidence 0.0.
"""
        return prompt.strip()

    def _create_classification_prompt(self, product: Dict[str, str]) -> str:
        """Создать промпт для классификации"""
        categories_str = ", ".join(self.categories)
        
        prompt = f"""
Классифицируй товар по одной из категорий: {categories_str}

Товар: {product.get('name', '')}
Описание: {product.get('description', '')}

Ответ в формате JSON:
{{
  "category": "название_категории",
  "confidence": 0.95,
  "reasoning": "обоснование выбора"
}}

Если не можешь определить категорию, используй "unknown" с confidence 0.0.
"""
        return prompt.strip()
    
    def _parse_batch_response(self, response: str, products: list, elapsed_time: float, stats: dict) -> list:
        """Парсить батч ответ от модели"""
        try:
            start = response.find('[')
            end = response.rfind(']') + 1
            
            if start != -1 and end != 0:
                json_str = response[start:end]
                parsed_results = json.loads(json_str)
                
                results = []
                for i, product in enumerate(products):
                    # Ищем результат по индексу
                    product_result = None
                    for result in parsed_results:
                        if result.get('index') == i + 1:
                            product_result = result
                            break
                    
                    if product_result:
                        results.append({
                            "product_name": product.get("name", ""),
                            "predicted_category": product_result.get("category", "unknown"),
                            "confidence": product_result.get("confidence", 0.0),
                            "full_response": response,
                            "method": "ollama_batch",
                            "processing_time": elapsed_time / len(products),
                            "resources": stats
                        })
                    else:
                        results.append({
                            "product_name": product.get("name", ""),
                            "predicted_category": "unknown",
                            "confidence": 0.0,
                            "full_response": response,
                            "method": "ollama_batch",
                            "processing_time": elapsed_time / len(products),
                            "resources": stats
                        })
                
                return results
            else:
                # Fallback - создаем базовые результаты
                results = []
                for product in products:
                    # Пытаемся найти категорию в тексте
                    category = "unknown"
                    confidence = 0.0
                    
                    for cat in self.categories:
                        if cat.lower() in response.lower():
                            category = cat
                            confidence = 0.6
                            break
                    
                    results.append({
                        "product_name": product.get("name", ""),
                        "predicted_category": category,
                        "confidence": confidence,
                        "full_response": response,
                        "method": "ollama_batch_fallback",
                        "processing_time": elapsed_time / len(products),
                        "resources": stats
                    })
                
                return results
                
        except json.JSONDecodeError:
            # Fallback - создаем базовые результаты
            results = []
            for product in products:
                # Пытаемся найти категорию в тексте
                category = "unknown"
                confidence = 0.0
                
                for cat in self.categories:
                    if cat.lower() in response.lower():
                        category = cat
                        confidence = 0.6
                        break
                
                results.append({
                    "product_name": product.get("name", ""),
                    "predicted_category": category,
                    "confidence": confidence,
                    "full_response": response,
                    "method": "ollama_batch_fallback",
                    "processing_time": elapsed_time / len(products),
                    "resources": stats
                })
            
            return results

    def _parse_classification_response(self, response: str) -> Dict[str, Any]:
        """Парсить ответ от модели"""
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            
            if start != -1 and end != 0:
                json_str = response[start:end]
                parsed = json.loads(json_str)
                return parsed
            else:
                for category in self.categories:
                    if category.lower() in response.lower():
                        return {
                            "category": category,
                            "confidence": 0.7,
                            "reasoning": "Извлечено из текста"
                        }
                
                return {"category": "unknown", "confidence": 0.0}
                
        except json.JSONDecodeError:
            for category in self.categories:
                if category.lower() in response.lower():
                    return {
                        "category": category,
                        "confidence": 0.6,
                        "reasoning": "Извлечено из текста"
                    }
            
            return {"category": "unknown", "confidence": 0.0}
    
    def __del__(self):
        """Очистка при удалении объекта"""
        self.resource_monitor.stop_monitoring() 