#!/bin/bash

# Запуск CourseHub локально

echo ""
echo "========================"
echo "  CourseHub Local Server"
echo "========================"
echo ""

# Проверяем если .venv существует
if [ ! -d ".venv" ]; then
    echo "Создаю виртуальное окружение..."
    python3 -m venv .venv
fi

# Активируем окружение
echo "Активирую окружение..."
source .venv/bin/activate

# Проверяем если зависимости установлены
if ! python -c "import django" 2>/dev/null; then
    echo "Устанавливаю зависимости..."
    pip install -r requirements.txt > /dev/null 2>&1
fi

# Применяем миграции
echo "Применяю миграции..."
python manage.py migrate > /dev/null 2>&1

# Проверяем если БД пуста
if [ ! -f "db.sqlite3" ]; then
    echo "Заполняю БД данными..."
    python populate_db.py > /dev/null 2>&1
fi

# Запускаем сервер
echo ""
echo "✅ Запускаю сервер..."
echo ""
echo "🌐 Откройте браузер: http://localhost:8000"
echo ""
echo "🔴 Чтобы остановить: нажми CTRL+C"
echo ""

python manage.py runserver
