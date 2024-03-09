from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Установка переменной окружения для настроек проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создание экземпляра объекта Celery
app = Celery('config')

# Загрузка настроек из файла Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение и регистрация задач из файлов tasks.py в приложениях Django
app.autodiscover_tasks()


# Регистрируйте периодическую задачу для проверки неактивных пользователей (один раз в день, например)
app.conf.beat_schedule = {
    'check-inactive-users': {
        'task': 'your_app.tasks.check_inactive_users',
        'schedule': crontab(hour=0, minute=0),  # ежедневно в полночь
    },
}