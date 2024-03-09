from celery import shared_task
from django.core.mail import send_mail
from school.models import Course


@shared_task
def send_course_update_email(course_id):
    course = Course.objects.get(pk=course_id)
    subject = 'Обновление материалов курса'
    message = f'{course.title} обновлен!'
    reciepen_list = course.subscription_set.values_list('user__email', flat=True)
    send_mail(subject, message, 'from@example.com', reciepen_list)