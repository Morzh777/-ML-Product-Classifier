# ML Product Classifier

Классификатор продуктов с использованием модели от Т-Банка T-pro-it-2.0.

## Возможности

- 🚀 Классификация продуктов (9-10 секунд на запрос)
- 🎮 Поддержка GPU (NVIDIA)
- 📊 Мониторинг ресурсов в реальном времени
- ⏳ Анимированный индикатор прогресса
- 🔧 Простая настройка и использование

## Категории

- iPhone
- Processors (процессоры)
- Videocards (видеокарты)
- Motherboards (материнские платы)
- PlayStation
- Nintendo Switch
- Steam Deck

## Требования

- Python 3.8+
- Ollama
- NVIDIA GPU (опционально)
- 12GB+ VRAM для оптимальной работы

## Платформы

### Mac Pro с Intel i9
- Оптимизированная конфигурация для CPU
- 16 потоков обработки
- Время отклика: 5-8 секунд
- Файл конфигурации: `Modelfile.mac-pro-i9`
- Скрипт настройки: `setup_mac_pro_i9.py`

### Mac с M1 Pro/M2
- Использование Neural Engine
- Оптимизация для Apple Silicon
- Время отклика: 3-6 секунд
- Файл конфигурации: `Modelfile.m1pro`

### Windows с NVIDIA GPU
- Использование CUDA
- Оптимизация для RTX 4070 Ti
- Время отклика: 3-5 секунд
- Файл конфигурации: `Modelfile.optimized`

## Установка

1. Клонируйте репозиторий:
```bash
git clone <your-repo-url>
cd ml-product-classifier
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Установите Ollama:
```bash
# Windows
winget install Ollama.Ollama

# macOS (Intel)
curl -fsSL https://ollama.ai/install.sh | sh

# macOS (M1/M2)
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh
```

4. Скачайте модель:
```bash
ollama pull t-pro-it-2.0:q2_k
```

5. Создайте оптимизированную модель под ваше железо:
```bash
# Для Mac Pro с Intel i9
ollama create product-classifier -f Modelfile.mac-pro-i9

# Для Mac с M1 Pro
ollama create product-classifier -f Modelfile.m1pro

# Для других систем
ollama create t-pro-it-2.0-optimized -f Modelfile.optimized
```

6. Проверьте установку:
```bash
ollama list
```

7. Проверьте готовность системы:
```bash
# Для Mac Pro с Intel i9
python setup_mac_pro_i9.py

# Для других систем
python check_setup.py
```

## Использование

### Базовый запуск
```bash
python run.py
```

### Программное использование
```python
from src.ml_model import ProductClassifier

# Инициализация
classifier = ProductClassifier()
classifier.load_model()

# Классификация
product = {
    'name': 'iPhone 15 Pro Max 256GB',
    'description': 'Смартфон Apple с процессором A17 Pro'
}

result = classifier.classify_product(product)
print(result)
```

## Структура проекта

```
ml-product-classifier/
├── src/
│   └── ml_model.py          # Основной классификатор
├── data/
│   └── example_raw_data.json # Пример данных
├── Modelfile.optimized      # Конфигурация модели
├── run.py                   # Основной скрипт
├── requirements.txt         # Зависимости
└── README.md               # Документация
```

## Производительность

- **Время классификации**: 9-13 секунд (базовая модель)
- **Цель**: 3-5 секунд (оптимизированная модель)
- **Использование VRAM**: ~8-10GB
- **Точность**: 85-95% в зависимости от категории

## 🚀 Оптимизация производительности

### Быстрая оптимизация:
```bash
python optimize_performance.py
```

Этот скрипт создаст:
- `t-pro-it-2.0-fast` - максимальная скорость (3-5 сек)
- `t-pro-it-2.0-balanced` - баланс скорости и качества (5-8 сек)

### Дообучение модели:
```bash
python fine_tune.py
```

Создаст `t-pro-it-2.0-finetuned` с улучшенной точностью на ваших данных.

## Мониторинг ресурсов

Система автоматически отслеживает:
- Загрузку CPU
- Использование RAM
- Загрузку GPU (если доступен)
- Время обработки

## Лицензия

MIT License

---

## Автор

**by Morzh**

Проект создан для развития валидатора товаров электроники. Классификатор продуктов помогает автоматически определять категории товаров для улучшения качества валидации и структурирования данных. 