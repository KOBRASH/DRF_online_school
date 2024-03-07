from django.shortcuts import redirect
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Course, Lesson, Payment, Subscription
from .services import create_product, create_price, create_session
from .validators import YoutubeValidator


class LessonSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview_image', 'video_link', 'course', 'user', 'product_id']
        validators = [YoutubeValidator(field='video_link')]
        read_only_fields = ('product_id', 'user')


    def create(self, validated_data):
        lesson = super().create(validated_data)
        lesson.product_id=create_product(lesson)
        lesson.save()
        return lesson


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'preview_image', 'description', 'lessons_count', 'lessons', 'user', 'product_id']
        read_only_fields=('product_id', 'user')


    def create(self, validated_data):
        course = super().create(validated_data)
        course.product_id=create_product(course)
        course.save()
        return course

    def get_lessons_count(self, obj):
        return obj.lessons.count()


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ['id', 'user', 'payment_date', 'course', 'lesson', 'amount', 'payment_method']


class PaymentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ['course', 'lesson', 'amount', 'payment_method', 'stripe_session_id']

    def create(self, validated_data):
        # Извлекаем данные из запроса
        amount = validated_data['amount']
        course = validated_data.get('course')
        lesson = validated_data.get('lesson')

        if course and not lesson:
            product = course
        elif lesson and not course:
            product = lesson
        else:
            raise ValidationError('Платеж создается только для курса или урока!')

        product_id = product.product_id
        if not product_id:
            product_id = create_product(product)
            product.product_id = product_id
            product.save()

        # Создаем цену в Stripe
        price_id = create_price(product_id, amount)

        # Создаем сессию в Stripe
        session_id = create_session(price_id)

        # Сохраняем информацию в базе данных
        payment = Payment.objects.create(
            user=self.context['request'].user,
            course=course,
            lesson=lesson,
            amount=amount,
            payment_method=validated_data['payment_method'],
            stripe_price_id=price_id,
            stripe_session_id=session_id
        )

        return payment



class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('user', 'course', 'subscribed_at')
