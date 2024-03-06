from django.shortcuts import redirect
from rest_framework import serializers
from .models import Course, Lesson, Payment, Subscription
from .services import create_product, create_price, create_session
from .validators import YoutubeValidator


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview_image', 'video_link', 'course', 'user']
        validators = [YoutubeValidator(field='video_link')]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'preview_image', 'description', 'lessons_count', 'lessons', 'user']

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
        course = validated_data['course']

        # Создаем продукт в Stripe
        product_id = create_product(course)

        # Создаем цену в Stripe
        price_id = create_price(product_id, amount)

        # Создаем сессию в Stripe
        session_id = create_session(price_id)

        # Сохраняем информацию в базе данных
        payment = Payment.objects.create(
            user=self.context['request'].user,
            course=validated_data.get('course'),
            lesson=validated_data.get('lesson'),
            amount=amount,
            payment_method=validated_data.get('payment_method'),
            stripe_product_id=product_id,
            stripe_price_id=price_id,
            stripe_session_id=session_id
        )

        return payment



class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('user', 'course', 'subscribed_at')
