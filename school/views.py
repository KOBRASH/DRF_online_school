import django_filters
from django.shortcuts import redirect
from rest_framework import viewsets, generics, permissions, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Course, Lesson, Payment, Subscription
from .paginators import CourseLessonPaginator
from .permissions import IsModerator, IsOwner
from .serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer, \
    PaymentCreateSerializer
from school.tasks import send_course_update_email


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CourseLessonPaginator

    def get_permissions(self):

        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, ~IsModerator]

        elif self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]

        elif self.action in ['update', 'partial_update', 'retrieve']:
            permission_classes = [IsAuthenticated, IsModerator | IsOwner]

        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsOwner]

        return [permission() for permission in permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CourseLessonPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class PaymentFilter(django_filters.FilterSet):
    class Meta:
        model = Payment
        fields = {
            'payment_date': ['exact', 'gt', 'lt'],
            'course': ['exact'],
            'payment_method': ['exact'],
        }


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = PaymentFilter
    permission_classes = [IsAuthenticated]


class PaymentCreateView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentCreateSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def subscribe(self, request, pk=None):
        course = Course.objects.get(pk=pk)
        user = request.user

        if not Subscription.objects.filter(user=user, course=course).exists():
            Subscription.objects.create(user=user, course=course)

            send_course_update_email.delay(user.email, course.title)

            return Response({'detail': 'Подписка успешно установлена.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'Подписка уже установлена.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def unsubscribe(self, request, pk=None):
        course = Course.objects.get(pk=pk)
        user = request.user

        subscription = Subscription.objects.filter(user=user, course=course).first()
        if subscription:
            subscription.delete()
            return Response({'detail': 'Подписка успешно отменена.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Подписка не найдена.'}, status=status.HTTP_404_NOT_FOUND)
