#!/usr/bin/env python3
# -*- coding: utf8 -*-
from django.test import TestCase

from lists.views import home_page
from lists.models import Item

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
        self.assertTemplateUsed(response, 'home.html')

class ItemModelTest(TestCase):
    """Unit tests for interacting with Django ORM.

    ORM is the abstraction for a database of tables.
        Classes map to tables.
        Attributes map to columns.
        An instance of a class is a row(s).
    """

    def test_saving_and_retrieving_items(self):
        """Unit test for ORM saving and retrieving objects."""
        first_item = Item()
        first_item.text = 'The first (ever) list item.'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item.')
        self.assertEqual(second_saved_item.text, 'Item the second')


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')

    def test_display_all_items(self):
        string1, string2 = 'itemey 1', 'itemey 2'
        Item.objects.create(text=string1)
        Item.objects.create(text=string2)

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, string1)
        self.assertContains(response, string2)


class NewListsTest(TestCase):
        def test_can_save_a_POST_request(self):
            "Unit test for view function checking POST value is added to DB."
            self.client.post('/lists/new', data={'item_text': 'A new list item'})
            self.assertEqual(Item.objects.count(), 1)

            new_item = Item.objects.first()

            self.assertEqual(new_item.text, 'A new list item')

        def test_redirects_after_POST(self):
            "Unit test that checks view function redirects after POST"
            response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
            self.assertRedirects(response, '/lists/the-only-list-in-the-world/')
