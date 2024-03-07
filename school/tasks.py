from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string

@shared_task
def send_course_update_email(user_email, course_title):
    subject = 'Обновление материалов курса'
    message = render_to_string('course_update_email.html', {'course_title': course_title})
    send_mail(subject, message, 'from@example.com', [user_email])