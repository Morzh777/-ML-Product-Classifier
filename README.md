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

# macOS
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
ollama create t-pro-it-2.0-optimized -f Modelfile.optimized
```

6. Проверьте установку:
```bash
ollama list
```

7. Проверьте готовность системы:
```bash
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

- **Время классификации**: 9-13 секунд
- **Использование VRAM**: ~8-10GB
- **Точность**: 85-95% в зависимости от категории

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