# Инструкция по развертыванию на Render.com

## Шаг 1: Подготовка проекта
1. Убедитесь, что у вас есть GitHub аккаунт
2. Загрузите проект на GitHub

```bash
git add -A
git commit -m "Final: CourseHub ready for deployment"
git push origin main
```

## Шаг 2: Создание Web Service на Render

1. Перейдите на https://render.com
2. Нажмите "New +" → "Web Service"
3. Выберите ваш GitHub репозиторий
4. Заполните форму:
   - **Name**: coursehub
   - **Environment**: Python 3
   - **Region**: Singapore
   - **Branch**: main
   - **Build Command**: `sh build.sh`
   - **Start Command**: `gunicorn coursehub.wsgi`

## Шаг 3: Окружение переменных

1. Нажмите "Environment"
2. Добавьте переменные:
   ```
   SECRET_KEY=ваш-секретный-ключ
   DEBUG=False
   ALLOWED_HOSTS=coursehub.render.com,coursehub.kz
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=coursehub
   DB_USER=postgres_user
   DB_PASSWORD=your_password
   DB_HOST=your-db.render.com
   DB_PORT=5432
   ```

## Шаг 4: Подключение базы данных PostgreSQL

1. Создайте PostgreSQL Database на Render
2. Скопируйте CONNECTION URL
3. Добавьте переменные окружения для БД

## Шаг 5: Домен

1. Перейдите в Settings Web Service
2. Найдите "Custom Domain"
3. Добавьте: coursehub.kz
4. Обновите DNS записи у вашего регистратора

## Шаг 6: SSL/TLS

Render автоматически предоставляет SSL сертификаты

## Логирование и мониторинг

- Logs доступны через панель Render
- Используйте `python manage.py tail_logs` для потокового просмотра

## Резервное копирование БД

```bash
# Экспорт БД
pg_dump -U postgres_user -h your-db.render.com coursehub > backup.sql

# Импорт БД
psql -U postgres_user -h your-db.render.com coursehub < backup.sql
```

---

**Готово!** Ваш сайт будет доступен по адресу: https://coursehub.render.com
