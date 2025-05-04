from django.test import TestCase
from core.utils import add

class AddTest(TestCase):
    def test_add(self):
        self.assertEqual(add(1, 2), 3)
# Create your tests here.
