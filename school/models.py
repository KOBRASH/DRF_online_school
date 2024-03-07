from django.db import models
from users.models import User


class Product(models.Model):
    title = models.CharField(max_length=255)
    product_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True


class Course(Product):

    preview_image = models.ImageField(upload_to='course_previews/', blank=True, null=True)
    description = models.TextField()
    user = models.ForeignKey(User, related_name='courses', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(Product):

    description = models.TextField()
    preview_image = models.ImageField(upload_to='lesson_previews/', blank=True, null=True)
    video_link = models.URLField()

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lessons')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, blank=True, null=True)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=[('cash', 'Наличные'), ('transfer', 'Перевод')])
    stripe_price_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_session_id = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.payment_date}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'




class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'

