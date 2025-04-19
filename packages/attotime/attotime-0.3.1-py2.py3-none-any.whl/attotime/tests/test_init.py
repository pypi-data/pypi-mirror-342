# -*- coding: utf-8 -*-

# Copyright (c) 2021, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import unittest

import attotime


class TestInitFunctions(unittest.TestCase):
    def test_import(self):
        self.assertEqual(
            attotime.attodatetime, attotime.objects.attodatetime.attodatetime
        )
        self.assertEqual(attotime.attotime, attotime.objects.attotime.attotime)
        self.assertEqual(
            attotime.attotimedelta, attotime.objects.attotimedelta.attotimedelta
        )
