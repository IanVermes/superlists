#!/usr/bin/env python3
# -*- coding: utf8 -*-
from django.test import TestCase

from lists.views import home_page

# Create your tests here.

"""Unittests for lists app.

Before you can design a unittest that works on progressing the functional test
you need to confirm the test runner will run the unittest.

functional_test.py was a programmer executed testrunner. The Django class
TestCase is more specialised than unittest.TestCase and even has a magic
testrunner.

Djano testrunner called:
python manage.py test
"""

class HomePageTest(TestCase):
    """ Unit test for '/' URL request and its resolution.

    Can we resolve the requested URL for the root of the site? Can the
    resolution take a view function I've made?
    """

    def test_uses_home_template(self):
        "Unit test for view resolution of '/' URL request."
        response = self.client.get('/')  # View func generetes a response.
        html = response.content.decode('utf8')
        self.assertTemplateUsed(response, 'home.html')
