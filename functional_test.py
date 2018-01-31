#!/usr/bin/env python3
# -*- coding: utf8 -*-
from selenium import webdriver

import unittest

class NewVisitorTest(unittest.TestCase):
    """Container for user orientated test conditions. My first unittest!

    Methods starting with test will be invoked by the test runner.

    self.setUp() and self.tearDown() are special methods which get run before and
    afer each test.

    https://docs.python.org/3/library/unittest.html#unittest.TestCase
    This class inherits from TestCase. TestCase provides some helpful methods that replace things like assert.
    e.g. assertIn(a, b) or assertEquals(a, b) or assertLess(a, b)

    """

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        """User story: User visits site, adds items to list and checks they persist.

        What is a USER STORY? By framing a coherent story as comments we always test
        from the point of view of the user."""

        # Edith has heard about a cool new online to-do app. She goes to check it out
        # its homepage.
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention to-do lists
        self.assertIn('To-do', self.browser.title)
        self.fail("Finish coding your test!")

        # She is invited to enter a to-do item straight away.

        # She types "Buy peacock feathers" into the a text box (Edith likes to make
        # fishing lures with feathers).

        # When she hits enter, the page updates, and now the page lists:
        # "1: Buy peacock feathers" as an item in a to-do list.

        # There is still a text box inviting her to add another item.

        # She enters "Use peacock feathers to make a fly".

        # The page updates again and shows both items on her list.

        # Edith wonders whether the site will remember her list. Then she sees that the
        # site has generate a unique URL for her -- there is some explanatory text to
        # that effect.

        # She visits that URL - her to-do list is still there.

        # Satisified she goes back to sleep.


if __name__ == "__main__":
    unittest.main(warnings='ignore')
