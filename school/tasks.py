from celery import shared_task
from django.core.mail import send_mail
from school.models import Course, User
from django.utils import timezone
from datetime import timedelta


@shared_task
def send_course_update_email(course_id):
    course = Course.objects.get(pk=course_id)
    subject = 'Обновление материалов курса'
    message = f'{course.title} обновлен!'
    reciepen_list = course.subscription_set.values_list('user__email', flat=True)
    send_mail(subject, message, 'from@example.com', reciepen_list)


@shared_task
def check_inactive_users():
    threshold_date = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=threshold_date, is_active=True)
    inactive_users.update(is_active=False)
