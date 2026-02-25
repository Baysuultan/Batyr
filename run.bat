@echo off
REM Запуск CourseHub локально

echo.
echo ========================
echo   CourseHub Local Server
echo ========================
echo.

REM Проверяем если .venv существует
if not exist ".venv" (
    echo Создаю виртуальное окружение...
    python -m venv .venv
)

REM Активируем окружение
echo Активирую окружение...
call .venv\Scripts\activate.bat

REM Проверяем если зависимости установлены
if not exist ".venv\Lib\site-packages\django" (
    echo Устанавливаю зависимости...
    pip install -r requirements.txt
)

REM Применяем миграции
echo Применяю миграции...
python manage.py migrate

REM Собираем статические файлы
echo Собираю статические файлы...
python manage.py collectstatic --noinput

REM Проверяем если БД пуста
if not exist "db.sqlite3" (
    echo Заполняю БД данными...
    python populate_db.py > nul 2>&1
)

REM Запускаем сервер
echo.
echo ✅ Запускаю сервер...
echo.
echo 🌐 Откройте браузер: http://localhost:8000
echo.
echo 🔴 Чтобы остановить: нажми CTRL+C
echo.

python manage.py runserver
