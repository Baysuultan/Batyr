# 🚀 CourseHub - Быстрый старт

## Системные требования

- **Python:** 3.10+
- **Git:** установленный git
- **OS:** Windows, macOS, Linux

## Установка и запуск (локально)

### 1️⃣ Клонируй репозиторий

```bash
git clone https://github.com/YOUR_USERNAME/coursehub.git
cd coursehub
```

### 2️⃣ Создай виртуальное окружение

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3️⃣ Установи зависимости

```bash
pip install -r requirements.txt
```

### 4️⃣ Примени миграции БД

```bash
python manage.py migrate
```

### 5️⃣ Создай суперпользователя (администратора)

```bash
python manage.py createsuperuser
```

Введи:
- Username: `admin`
- Email: `admin@example.com`
- Password: придумай пароль

### 6️⃣ Заполни БД тестовыми данными

```bash
python manage.py populate_db.py
```

Это создаст:
- ✅ 5+ курсов
- ✅ 36+ уроков
- ✅ 4 инструктора
- ✅ 20+ студентов с отзывами
- ✅ YouTube видео в каждом уроке

### 7️⃣ Запусти сервер

```bash
python manage.py runserver
```

Откроется на: **http://localhost:8000** 🌐

### 8️⃣ Вход в админку

- URL: `http://localhost:8000/admin/`
- Username: `admin`
- Password: тот, что ты ввел выше

---

## 📋 Полный набор команд

```bash
# Активировать виртуальное окружение
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Установить зависимости
pip install -r requirements.txt

# Применить миграции
python manage.py migrate

# Создать администратора
python manage.py createsuperuser

# Заполнить данные
python manage.py populate_db.py

# Создать статические страницы
python manage.py create_static_pages.py

# Запустить сервер
python manage.py runserver

# Запустить на другом порту (если 8000 занят)
python manage.py runserver 8001

# Запустить на всех интерфейсах
python manage.py runserver 0.0.0.0:8000

# Собрать статические файлы
python manage.py collectstatic --noinput

# Проверить конфигурацию
python manage.py check

# Запустить тесты
python manage.py test

# Проверить проект на безопасность
python manage.py check --deploy

# Аудит сайта (поиск ошибок)
python manage.py audit_site.py
```

---

## 🌍 Структура проекта

```
coursehub/
├── accounts/          # Профили пользователей
├── api/              # REST API
├── categories/       # Категории курсов
├── courses/          # Курсы
├── coursehub/        # Основные настройки
├── enrollments/      # Записи на курсы
├── lessons/          # Уроки и видео
├── notifications/    # Уведомления
├── pages/            # Статические страницы
├── reviews/          # Отзывы
├── users/            # Модель пользователя
├── static/           # CSS, JS, изображения
├── templates/        # HTML шаблоны
├── media/            # Загруженные файлы
├── logs/             # Логи приложения
├── manage.py         # Django управление
├── requirements.txt  # Зависимости
└── db.sqlite3        # База данных
```

---

## 📄 Основные URL

| URL | Описание |
|-----|---------|
| `/` | Главная страница |
| `/courses/` | Список всех курсов |
| `/courses/<slug>/` | Страница курса |
| `/courses/<slug>/lessons/` | Уроки курса |
| `/courses/<slug>/lessons/<lesson_slug>/` | Просмотр урока с видео |
| `/about/` | О проекте |
| `/terms/` | Условия использования |
| `/privacy/` | Политика конфиденциальности |
| `/accounts/login/` | Вход |
| `/accounts/register/` | Регистрация |
| `/accounts/profile/` | Профиль пользователя |
| `/admin/` | Панель администратора |
| `/api/courses/` | API - Все курсы (JSON) |
| `/api/lessons/` | API - Все уроки (JSON) |

---

## 🔧 Полезные скрипты

### Заполнить БД курсами
```bash
python manage.py populate_db.py
```

### Создать статические страницы
```bash
python manage.py create_static_pages.py
```

### Проверить видео
```bash
python manage.py check_videos.py
```

### Исправить слаги уроков
```bash
python manage.py fix_slugs.py
```

### Аудит всего сайта
```bash
python manage.py audit_site.py
```

---

## 🐛 Решение проблем

### Ошибка: "No module named 'django'"
```bash
pip install -r requirements.txt
```

### Ошибка: "ModuleNotFoundError"
```bash
.venv\Scripts\activate  # Убедись что виртуальное окружение активировано
pip install -r requirements.txt
```

### Порт 8000 уже занят
```bash
python manage.py runserver 8001
```

### БД повреждена
```bash
# Удалить и пересоздать
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
python manage.py populate_db.py
```

### Статические файлы не загружаются
```bash
python manage.py collectstatic --noinput
```

---

## 🌐 Развертывание на Render.com

### 1. Отправь на GitHub

```bash
git add .
git commit -m "Deploy to Render"
git push origin main
```

### 2. Создай аккаунт на Render.com

https://render.com

### 3. Создай Web Service

- Выбери "Web Service"
- Подключи GitHub репозиторий
- Build command: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
- Start command: `gunicorn coursehub.wsgi:application`

### 4. Добавь Environment Variables

```
DEBUG=False
ALLOWED_HOSTS=yourdomain.onrender.com
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://...
```

---

## 📚 Документация

- [Django документация](https://docs.djangoproject.com/en/4.2/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Bootstrap 5](https://getbootstrap.com/docs/5.3/)
- [Font Awesome](https://fontawesome.com/icons)

---

## ✨ Функциональность

✅ **Backend:**
- Django 4.2
- REST API с фильтрацией
- Аутентификация пользователей
- Управление курсами и уроками
- Система отзывов
- Отслеживание прогресса

✅ **Frontend:**
- Bootstrap 5 дизайн
- Адаптивный интерфейс (мобильный, планшет, десктоп)
- YouTube видеоплеер
- JavaScript интерактивность
- Гладкие анимации

✅ **Функции:**
- Просмотр курсов по категориям
- Просмотр видео уроков
- Запись на курсы
- Система рейтинга и отзывов
- Профиль пользователя
- Отслеживание прогресса обучения
- Сертификаты

---

## 📞 Поддержка

Если у тебя есть вопросы или проблемы:
1. Проверь логи: `python manage.py check`
2. Запусти аудит: `python manage.py audit_site.py`
3. Посмотри в консоль при запуске сервера

---

**Happy Learning! 🎓**
