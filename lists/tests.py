from django.test import TestCase

# Create your tests here.

""" Unittests for lists app.

Before you can design a unittest that works on progressing the functional test
you need to confirm the test runner will run the unittest.

functional_test.py was a programmer executed testrunner. The Django class
TestCase is more specialised than unittest.TestCase and even has a magic
testrunner.

Djano testrunner called:
python manage.py test
"""

class SmokeTest(TestCase):

    def test_bad_math(self):
        """Deliberate failing unittest to inspect Django functionality."""
        self.assertEqual(1 + 1, 3)
