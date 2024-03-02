from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, force_authenticate
from rest_framework import status
from .models import Course, Lesson, Subscription
from users.models import User

class SchoolTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email='test@example.com',
            password='testpassword',
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            user=self.user)

        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            course=self.course,
            user=self.user,
            description='Test Description',
            video_link='https://www.youtube.com/watch?v=your_video_id'
        )
    def test_list_lessons(self):
        response = self.client.get('/lesson/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_lesson(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            '/lesson/create/',
            {
                'title': 'Test Lesson',
                'course': self.course.id,
                'user': self.user.id,
                'description': 'Test Description',
                'video_link': 'https://www.youtube.com/watch?v=your_video_id'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Создаем новый урок для удаления
        lesson_to_delete = Lesson.objects.create(
            title='Lesson to Delete',
            course=self.course,
            user=self.user,
            description='Test Description',
            video_link='https://www.youtube.com/watch?v=delete_video_id'
        )

        # Получаем URL для удаления урока
        url = f'/lesson/delete/{lesson_to_delete.id}/'

        # Выполняем запрос DELETE
        response = self.client.delete(url)

        # Проверяем, что урок был успешно удален (HTTP_204_NO_CONTENT)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Проверяем, что урок больше не существует в базе данных
        with self.assertRaises(Lesson.DoesNotExist):
            Lesson.objects.get(pk=lesson_to_delete.id)

    def test_update_lesson(self):
        self.client.force_authenticate(user=self.user)
        create_url = '/lesson/create/'
        create_data = {
            'title': 'Lesson to Update',
            'course': self.course.id,
            'user': self.user.id,
            'description': 'Test Description',
            'video_link': 'https://www.youtube.com/watch?v=update_video_id'
        }
        response_create = self.client.post(create_url, create_data)

        # Проверяем, что урок был создан успешно
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)

        # Получаем URL для обновления урока
        update_url = f'/lesson/update/{response_create.data["id"]}/'

        # Отправляем запрос PATCH для обновления урока
        update_data = {'video_link': 'https://www.youtube.com/watch?v=delete_video_id'}
        response_update = self.client.patch(update_url, update_data)

        # Если ответ не 200, выведем содержимое ответа для дополнительной информации
        if response_update.status_code != status.HTTP_200_OK:
            print(response_update.content)

        # Проверяем, что урок был успешно обновлен (HTTP_200_OK)
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)

        # Проверяем, что урок был обновлен в базе данных
        updated_lesson = Lesson.objects.get(pk=response_create.data["id"])
        self.assertEqual(updated_lesson.video_link, 'https://www.youtube.com/watch?v=delete_video_id')

        # Удаляем урок после проверки
        updated_lesson.delete()

    def test_delete_lesson(self):
        self.client.force_authenticate(user=self.user)
        # Создаем новый урок для удаления
        lesson_to_delete = Lesson.objects.create(
            title='Lesson to Delete',
            course=self.course,
            user=self.user,
            description='Test Description',
            video_link='https://www.youtube.com/watch?v=delete_video_id'
        )

        # Получаем URL для удаления урока
        url = f'/lesson/delete/{lesson_to_delete.id}/'

        # Выполняем запрос DELETE
        response = self.client.delete(url)

        # Проверяем, что урок был успешно удален (HTTP_204_NO_CONTENT)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Проверяем, что урок больше не существует в базе данных
        with self.assertRaises(Lesson.DoesNotExist):
            Lesson.objects.get(pk=lesson_to_delete.id)

    def test_subscribe_to_course(self):
        self.client.force_authenticate(user=self.user)
        url = f'/courses/{self.course.id}/subscribe/'
        response = self.client.post(url)
        print(response.status_code)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.user.delete()
        self.course.delete()


    def test_unsubscribe_from_course(self):
        self.client.force_authenticate(user=self.user)
        subscription = Subscription.objects.create(user=self.user, course=self.course)
        url = f'/courses/{self.course.id}/unsubscribe/'
        response = self.client.post(url)
        print(response.status_code)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.delete()
        self.course.delete()






