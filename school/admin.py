from django.contrib import admin
from .models import Course, Lesson, Payment, Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'subscribed_at')
    search_fields = ('user__email', 'course__title')  # Предполагая, что у пользователя есть поле email


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_user_username', 'preview_image', 'description')
    search_fields = ('title', 'user__username')

    def get_user_username(self, obj):
        return obj.user.username

    get_user_username.short_description = 'User'


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_user_username', 'preview_image', 'course', 'video_link')
    search_fields = ('title', 'user__username', 'course__title')

    def get_user_username(self, obj):
        return obj.user.username

    get_user_username.short_description = 'User'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_date', 'course', 'amount', 'payment_method')
    search_fields = ('user__username', 'course__title')
