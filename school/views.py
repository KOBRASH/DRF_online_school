import django_filters
from rest_framework import viewsets, generics, permissions
from rest_framework.permissions import IsAuthenticated
from .models import Course, Lesson, Payment
from .permissions import IsModerator, IsOwner
from .serializers import CourseSerializer, LessonSerializer, PaymentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

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
            'course_or_lesson': ['exact'],
            'payment_method': ['exact'],
        }


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = PaymentFilter
    permission_classes = [IsAuthenticated]
