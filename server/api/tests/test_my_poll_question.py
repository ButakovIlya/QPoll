from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from ..models import Poll, PollQuestion, AnswerOption, Profile, UserRole, PollType
from admin_api.models import Settings
from django.contrib.auth.models import User
from unittest.mock import patch
from api.utils import get_object_or_404

import logging
logger = logging.getLogger('django.test')

class MyPollQuestionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        role = UserRole.objects.create(role='Админ')
        poll_type = PollType.objects.create(name='Опрос')
        self.profile = Profile.objects.create(user=self.user, role=role)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.profile = get_object_or_404(Profile, user=self.user)
        self.poll = Poll.objects.create(author=self.profile, poll_id=1, is_in_production=False)
        self.poll.poll_type = poll_type
        self.question = PollQuestion.objects.create(poll=self.poll, order_id=1, name='Sample question')
        self.answer_option = AnswerOption.objects.create(question=self.question, name='Sample answer', order_id=1)
        self.settings = Settings.objects.create(max_questions_quantity=50)


    def tearDown(self):
        self.client.logout()
        logger.info('Tear down complete')

    def test_get_poll_questions(self):
        url = reverse('my_poll_question')
        response = self.client.get(url, {'poll_id': self.poll.poll_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_poll_question_with_id(self):
        url = reverse('my_poll_question')
        response = self.client.get(url, {'poll_id': self.poll.poll_id, 'id': self.question.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], self.question.id)

    def test_create_poll_question(self):
        url = reverse('my_poll_question')
        data = {
            'poll': self.poll.id,
            'name': 'New question'
        }
        response = self.client.post(url, data, format='json')
        print(self.poll.poll_type.name)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PollQuestion.objects.count(), 2)



class MyPollQuestionTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        self.client.logout()
        logger.info('Tear down complete')

    def test_get_poll_questions(self):
        url = reverse('my_poll_question')
        response = self.client.get(url, {'poll_id': self.poll.poll_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)