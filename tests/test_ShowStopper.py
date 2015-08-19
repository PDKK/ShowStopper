#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_ShowStopper
----------------------------------

Tests for `ShowStopper` module.
"""

import unittest
from gi.repository import Gtk

from ShowStopper import mainWindow


def refresh_gui():
    while gtk.events_pending():
        gtk.main_iteration_do(block=False)

class TestShowstopper(unittest.TestCase):

    def setUp(self):
        self.window = mainWindow.mainWindow()

    def test_something(self):
        pass

    def test_load(self):
        pass

    def tearDown(self):
        pass
