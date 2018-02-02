#!/usr/bin/env python3
# -*- coding: utf8 -*-
from django.test import TestCase

from lists.views import home_page
from lists.models import Item, List

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

class ListAndItemModelTest(TestCase):
    """Unit tests for interacting with Django ORM.

    ORM is the abstraction for a database of tables.
        Classes map to tables.
        Attributes map to columns.
        An instance of a class is a row(s).
    """

    def test_saving_and_retrieving_items(self):
        """Unit test for ORM saving and retrieving objects."""
        _list = List()
        _list.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item.'
        first_item.list = _list
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = _list
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, _list)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item.')
        self.assertEqual(first_saved_item.list, _list)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, _list)


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        _list = List.objects.create()

        response = self.client.get(f'/lists/{_list.id}/')

        self.assertTemplateUsed(response, 'list.html')

    def test_display_only_items_for_that_list(self):
        _list_a = List.objects.create()
        _list_b = List.objects.create()
        string1a, string2a = 'itemey 1', 'itemey 2'
        string1b, string2b = 'other itemey 1', 'other itemey 2'
        Item.objects.create(text=string1a, list=_list_a)
        Item.objects.create(text=string2a, list=_list_a)
        Item.objects.create(text=string1b, list=_list_b)
        Item.objects.create(text=string2b, list=_list_b)

        response = self.client.get(f'/lists/{_list_a.id}/')

        self.assertContains(response, string1a)
        self.assertContains(response, string2a)
        self.assertNotContains(response, string1b)
        self.assertNotContains(response, string2b)


class NewListTest(TestCase):

    def test_can_save_a_POST_request_to_an_exisiting_list(self):
        new_item_txt = 'A new item for an existing list'
        prior_list = List.objects.create()  # Dummy list to prevent head/tail indexing.
        correct_list = List.objects.create()
        later_list = List.objects.create()  # Dummy list to prevent head/tail indexing.

        self.client.post(f'lists/{correct_list.id}/add_item',
                         data={'item_text': new_item_txt})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, new_item_txt)
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        new_item_txt = 'A new item for an existing list'
        prior_list = List.objects.create()  # Dummy list to prevent head/tail indexing.
        correct_list = List.objects.create()
        later_list = List.objects.create()  # Dummy list to prevent head/tail indexing.

        response = self.client.post(path=f'/lists/{correct_list.id}/add_item',
                                    data={'item_text': new_item_txt})

        self.assertRedirects(response, f'lists/{correct_list.id}')

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
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')
