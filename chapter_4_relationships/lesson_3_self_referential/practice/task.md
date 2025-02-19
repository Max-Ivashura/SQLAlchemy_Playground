# Task: Работа с селф-референциальными отношениями

**Задача:** Создайте модель `Category` с селф-референциальным отношением для представления иерархии категорий (например, категория может иметь родительскую категорию).

**Шаги:**
1. Создайте модель `Category` с полем `parent_id`, которое ссылается на ту же таблицу.
2. Добавьте отношения `parent` (родительская категория) и `subcategories` (дочерние категории).
3. Добавьте несколько категорий с иерархией.
4. Реализуйте следующие запросы:
   - Получите все подкатегории для конкретной категории.
   - Найдите родительскую категорию для конкретной подкатегории.

**Дополнительное задание (для продвинутых):**
Добавьте возможность вывода всей иерархии категорий (например, "Электроника -> Гаджеты -> Телефоны").