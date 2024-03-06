from django.urls import path
from school.apps import SchoolConfig
from rest_framework.routers import DefaultRouter
from school.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PaymentListView, SubscriptionViewSet, PaymentCreateView

app_name = SchoolConfig.name


router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscriptions')





urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-get'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-delete'),
    path('payments/', PaymentListView.as_view(), name='payment-list'),
    path('payments/create/', PaymentCreateView.as_view(), name='payment-create'),
    path('courses/<int:pk>/subscribe/', SubscriptionViewSet.as_view({'post': 'subscribe'}), name='course-subscribe'),
    path('courses/<int:pk>/unsubscribe/', SubscriptionViewSet.as_view({'post': 'unsubscribe'}), name='course-unsubscribe'),
]

urlpatterns += router.urls
urlpatterns += [
    path('courses/<int:pk>/subscribe/', SubscriptionViewSet.as_view({'post': 'subscribe'}), name='course-subscribe'),
    path('courses/<int:pk>/unsubscribe/', SubscriptionViewSet.as_view({'post': 'unsubscribe'}), name='course-unsubscribe'),
]