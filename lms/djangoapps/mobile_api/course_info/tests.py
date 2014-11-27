"""
Tests for course_info
"""
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase

from courseware.tests.factories import UserFactory
from courseware.tests.modulestore_config import TEST_DATA_MOCK_MODULESTORE
from xmodule.modulestore.tests.factories import CourseFactory
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase


@override_settings(MODULESTORE=TEST_DATA_MOCK_MODULESTORE)
class TestVideoOutline(ModuleStoreTestCase, APITestCase):
    """
    Tests for /api/mobile/v0.5/course_info/...
    """
    def setUp(self):
        super(TestVideoOutline, self).setUp()
        self.user = UserFactory.create()
        self.course = CourseFactory.create(mobile_available=True)
        self.client.login(username=self.user.username, password='test')

    def test_about(self):
        url = reverse('course-about-detail', kwargs={'course_id': unicode(self.course.id)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('overview' in response.data)  # pylint: disable=E1103

    def test_handouts(self):
        url = reverse('course-handouts-list', kwargs={'course_id': unicode(self.course.id)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_updates(self):
        url = reverse('course-updates-list', kwargs={'course_id': unicode(self.course.id)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])  # pylint: disable=E1103
        # TODO: add handouts and updates, somehow
