from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
class UserTestClass(TestCase):

    # Set up method
    def setUp(self):
        self.testuser = User(username="user", email="test@mail.com")

    def test_instance(self):
        self.assertIsInstance(self.testuser, User)

    def test_save_user(self):
        self.assertFalse(self.testuser in User.objects.all())
        self.testuser.save()
        self.assertTrue(self.testuser in User.objects.all())
        self.testuser.delete()

    def test_delete_user(self):
        self.testuser.save()
        self.assertTrue(self.testuser in User.objects.all())
        self.testuser.delete()
        self.assertFalse(self.testuser in User.objects.all())
