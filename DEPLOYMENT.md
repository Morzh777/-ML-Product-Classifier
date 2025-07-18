# Инструкции по развертыванию

## Подготовка к загрузке в отдельное репо

### 1. Инициализация Git репо

```bash
# Инициализируем git репо
python init_repo.py
```

### 2. Создание репо на GitHub/GitLab

1. Создайте новый репозиторий на GitHub или GitLab
2. Не инициализируйте с README (у нас уже есть)
3. Скопируйте URL репозитория

### 3. Подключение к удаленному репо

```bash
# Добавляем remote
git remote add origin <URL_ВАШЕГО_РЕПО>

# Переименовываем ветку в main (если нужно)
git branch -M main

# Пушим код
git push -u origin main
```

### 4. Структура проекта

```
ml-product-classifier/
├── src/
│   └── ml_model.py          # Основной классификатор
├── data/
│   └── example_raw_data.json # Пример данных
├── Modelfile.optimized      # Конфигурация модели
├── run.py                   # Основной скрипт
├── check_setup.py           # Проверка установки
├── init_repo.py             # Инициализация git
├── requirements.txt         # Зависимости
├── .gitignore              # Исключения для git
├── README.md               # Документация
└── DEPLOYMENT.md           # Эти инструкции
```

### 5. Проверка готовности

```bash
# Проверяем, что все работает
python check_setup.py

# Тестируем классификатор
python run.py
```

### 6. Настройка CI/CD (опционально)

Создайте `.github/workflows/test.yml`:

```yaml
name: Test ML Classifier

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python check_setup.py
```

### 7. Обновление README

После загрузки в репо обновите в README.md:
- URL репозитория в инструкциях клонирования
- Добавьте информацию о лицензии
- Обновите контактную информацию

### 8. Теги и релизы

```bash
# Создаем тег для первого релиза
git tag -a v1.0.0 -m "First release: ML Product Classifier"

# Пушим тег
git push origin v1.0.0
```

### 9. Мониторинг

После развертывания отслеживайте:
- Количество звезд и форков
- Issues и Pull Requests
- Использование модели
- Производительность

## Готово! 🚀

Ваш ML Product Classifier готов к использованию в отдельном репозитории.

---

**by Morzh** - Проект создан для развития валидатора товаров электроники 