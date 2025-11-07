# Инструкция по использованию

## Установка зависимостей

```bash
pip install -r requirements.txt
```

## Запуск программы

```bash
python main.py
```

Программа автоматически:
1. Инициализирует базу данных с тестовыми данными
2. Создаст извещения на оплату для всех лицевых счетов
3. Сохранит Excel-файлы в текущей директории

## Структура файлов

- `main.py` - Главный модуль программы
- `models.py` - Модели данных
- `database.py` - Класс для работы с базой данных
- `date_time_utils.py` - Утилиты для работы с датой и временем
- `chain_of_responsibility.py` - Реализация паттерна Chain of Responsibility
- `excel_generator.py` - Генератор Excel-файлов
- `requirements.txt` - Зависимости проекта
- `README.md` - Описание проекта
- `context_diagram.txt` - Контекстная диаграмма

## Пример использования в коде

```python
from database import Database
from main import init_database, create_payment_notice
from chain_of_responsibility import ChargeProcessor
from excel_generator import ExcelGenerator
from date_time_utils import DateTimeHandler

# Инициализация
db = init_database()
processor = ChargeProcessor()
excel_gen = ExcelGenerator()
date_handler = DateTimeHandler()

# Получение текущего периода
current_date = date_handler.get_current_date()
period_month = current_date.month
period_year = current_date.year

# Создание извещения
notice = create_payment_notice(db, account_code=1, period_month=period_month, period_year=period_year)

# Обработка начислений через Chain of Responsibility
notice = processor.process_notice(notice)

# Генерация Excel-файла
excel_gen.generate_payment_notice(notice, "извещение.xlsx")
```

## Паттерн Chain of Responsibility

Цепочка обработчиков начислений:
1. **ValidationChargeHandler** - проверяет корректность данных
2. **DiscountChargeHandler** - применяет скидку 5% при сумме > 5000 руб.
3. **StandardChargeHandler** - стандартный расчет стоимости

Каждый обработчик может передать обработку следующему звену цепи.

