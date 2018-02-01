#!/usr/bin/env python3
# -*- coding: utf8 -*-

""" Collection of tests for superlists Django project.

As this is the first time I've been exposed to test driven development I'll
outline the workflow.
1) Write a functional test when I want to add new functionality.
    - The test should have verbose comments giving a user story ie. written from
      how the functionality will work from a users point of view.
    - The test should have an expected failure, as there is no production code.
2) Think about how to write code that may pass the FAILING functional test.
    - Write a unit test(s) to define how I want the code to behave.
    - Each line of production code should be tested by one of the unit tests.
3) Think about how to write code that may pass the FAILING unit test.
    - Write the smallest amount of code to pass the unit test.
    - Iterate between step 2 and 3 until the functional test will move beyond
      its current failure.
4) Rerurn the functional test and see if they either pass or get a little further.

In this way the functional test is driving development I do at a high level
while the unit tests drive the work at a low level.

THUS functional tests should help you build an application with the right
functionality and guarentee you will never break it. Unit tests should help you
to write code thats clean and bug free.
"""

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

import time

MAX_WAIT = 10  # seconds

class NewVisitorTest(LiveServerTestCase):
    """Container for user orientated test conditions.

    The class features both outside-in functional tests and inside-out unit tests.
    - Functional tests describe functionality from the user's point of view.
    - Unit tests define how we want code to behave. Passing unit tests thus pass functional tests.

    Methods starting with test will be invoked by the test runner.

    self.setUp() and self.tearDown() are special methods which get run before and
    afer each test.

    https://docs.python.org/3/library/unittest.html#unittest.TestCase
    This class inherits from TestCase. TestCase provides some helpful methods
    that replace things like assert. e.g. assertIn(a, b) or assertEquals(a, b)
    or assertLess(a, b)

    """

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def _wait_for_row_in_list_table(self, comparator_text):
        """Helper function for test_can_start_a_list_and_retrieve_it_later.

        Programatic explicit waits wait upto MAX_WAIT from the call.
        """
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(comparator_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as err:
                if time.time() - start_time > MAX_WAIT:
                    raise err
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        """User story: User visits site, adds items to list and checks they are there.

        What is a USER STORY? By framing a coherent story as comments we always test
        from the point of view of the user."""

        # Edith has heard about a cool new online to-do app. She goes to check it out
        # its homepage.
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do lists', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn("Your To-Do list", header_text)

        # She is invited to enter a to-do item straight away.
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter to-do item'
        )

        # She types "Buy peacock feathers" into the a text box (Edith likes to make
        # fishing lures with feathers).
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates, and now the page lists:
        # "1: Buy peacock feathers" as an item in a to-do list.
        inputbox.send_keys(Keys.ENTER)
        self._wait_for_row_in_list_table("1: Buy peacock feathers")

        # There is still a text box inviting her to add another item.
        inputbox = self.browser.find_element_by_id('id_new_item')

        # She enters "Use peacock feathers to make a fly".
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again and shows both items on her list.
        self._wait_for_row_in_list_table("1: Buy peacock feathers")
        self._wait_for_row_in_list_table("2: Use peacock feathers to make a fly")

        # Satisfied she goes back to sleep.

    def test_multiple_users_can_start_lists_at_different_urls(self):
        """Multiple users visit the site, each with a different URL and make lists."""
        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers.')
        inputbox.send_keys(Keys.ENTER)
        self._wait_for_row_in_list_table("1: Buy peacock feathers.")

        # She notices her list has a unique URL.
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # Now a new user, Francis, comes along to the site.

        ## We use a new browser session to make sure that no information of Edith's is coming through from the cookie etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the homepage. There is no sign of Eidth's lists
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('Make a fly', page_text)

        # Francis starts a new list by entering a new item.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self._wait_for_row_in_list_table('1: Buy milk')

        # Francis gets his own unique URL
        francis_list_url = self.browser.get_current_url
        self.assertRegex(francis_list_url, '/list/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again there is no trace of Edith's lists
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied she goes back to sleep.
