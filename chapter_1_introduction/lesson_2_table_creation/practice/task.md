# Task: Создание таблицы employees

**Задача:** Создайте таблицу `employees` с помощью SQLAlchemy Core. Таблица должна содержать следующие столбцы:
- `id`: Целое число, первичный ключ.
- `first_name`: Строка длиной до 50 символов, обязательное поле.
- `last_name`: Строка длиной до 50 символов, обязательное поле.
- `email`: Строка длиной до 100 символов, уникальное значение, обязательное поле.
- `salary`: Число с плавающей точкой.
- `hire_date`: Дата приема на работу.
- `is_manager`: Логическое значение, по умолчанию `False`.

Добавьте индекс для столбца `email`.

**Шаги:**
1. Используйте код из лекции как основу.
2. Создайте таблицу `employees`.
3. Добавьте индекс для столбца `email`.

**Дополнительное задание (для продвинутых):**
Создайте составной индекс для столбцов `first_name` и `last_name`.