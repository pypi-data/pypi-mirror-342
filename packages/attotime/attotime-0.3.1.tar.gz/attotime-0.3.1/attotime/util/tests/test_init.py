# -*- coding: utf-8 -*-

# Copyright (c) 2021, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import datetime
import time
import unittest
from decimal import Decimal

from attotime import util
from attotime.tests.compat import mock


class TestInitFunctions(unittest.TestCase):
    def test_decimal_stringify(self):
        result = util.decimal_stringify(Decimal(0))
        self.assertEqual(result, "0")

        result = util.decimal_stringify(Decimal(1.0))
        self.assertEqual(result, "1")

        result = util.decimal_stringify(Decimal(-1.0))
        self.assertEqual(result, "-1")

        result = util.decimal_stringify(Decimal(25))
        self.assertEqual(result, "25")

        result = util.decimal_stringify(Decimal(-25))
        self.assertEqual(result, "-25")

        result = util.decimal_stringify(Decimal("2567.8"))
        self.assertEqual(result, "2567.8")

        result = util.decimal_stringify(Decimal("-2567.8"))
        self.assertEqual(result, "-2567.8")

        result = util.decimal_stringify(Decimal(1500))
        self.assertEqual(result, "1500")

        result = util.decimal_stringify(Decimal(-1500))
        self.assertEqual(result, "-1500")

        result = util.decimal_stringify(Decimal("1E16"))
        self.assertEqual(result, "10000000000000000")

        result = util.decimal_stringify(Decimal("-1E16"))
        self.assertEqual(result, "-10000000000000000")

        result = util.decimal_stringify(Decimal("1E-16"))
        self.assertEqual(result, "0.0000000000000001")

        result = util.decimal_stringify(Decimal("-1E-16"))
        self.assertEqual(result, "-0.0000000000000001")

        result = util.decimal_stringify(Decimal("1E-9"))
        self.assertEqual(result, "0.000000001")

        result = util.decimal_stringify(Decimal("-1E-9"))
        self.assertEqual(result, "-0.000000001")

    def test_multiple_replace(self):
        result = util.multiple_replace("replace me", {"replace ": "", "me": "replaced"})
        self.assertEqual(result, "replaced")

        result = util.multiple_replace("hey abc", {"ab": "AB", "abc": "ABC"})
        self.assertEqual(result, "hey ABC")


class TestLocalTimezone(unittest.TestCase):
    @mock.patch(
        "attotime.util.time.timezone", new_callable=mock.PropertyMock(return_value=1800)
    )
    @mock.patch(
        "attotime.util.time.altzone", new_callable=mock.PropertyMock(return_value=1900)
    )
    @mock.patch(
        "attotime.util.time.daylight",
        new_callable=mock.PropertyMock(return_value=False),
    )
    def test_setup(self, mockDaylight, mockAltzone, mockTimezone):
        self.assertEqual(
            util.LocalTimezone().STDOFFSET,
            datetime.timedelta(seconds=-1800),
        )
        self.assertEqual(
            util.LocalTimezone().DSTOFFSET,
            datetime.timedelta(seconds=-1800),
        )
        self.assertEqual(util.LocalTimezone().DSTDIFF, datetime.timedelta(seconds=0))

    @mock.patch(
        "attotime.util.time.timezone", new_callable=mock.PropertyMock(return_value=1800)
    )
    @mock.patch(
        "attotime.util.time.altzone", new_callable=mock.PropertyMock(return_value=1900)
    )
    @mock.patch(
        "attotime.util.time.daylight", new_callable=mock.PropertyMock(return_value=True)
    )
    def test_setup_daylight(self, mockDaylight, mockAltzone, mockTimezone):
        self.assertEqual(
            util.LocalTimezone().STDOFFSET,
            datetime.timedelta(seconds=-1800),
        )
        self.assertEqual(
            util.LocalTimezone().DSTOFFSET,
            datetime.timedelta(seconds=-1900),
        )
        self.assertEqual(util.LocalTimezone().DSTDIFF, datetime.timedelta(seconds=-100))

    def test_utcoffset(self):
        def _returnOne(*args, **kwargs):
            return 1

        def _returnZero(*args, **kwargs):
            return 0

        localTimezoneObject = util.LocalTimezone()
        localTimezoneObject.DSTOFFSET = mock.Mock()
        localTimezoneObject.STDOFFSET = mock.Mock()
        localTimezoneObject._isdst = _returnZero

        result = localTimezoneObject.utcoffset(datetime.datetime.now())

        self.assertEqual(result, localTimezoneObject.STDOFFSET)

        localTimezoneObject._isdst = _returnOne

        result = localTimezoneObject.utcoffset(datetime.datetime.now())

        self.assertEqual(result, localTimezoneObject.DSTOFFSET)

    def test_dst(self):
        def _returnOne(*args, **kwargs):
            return 1

        def _returnZero(*args, **kwargs):
            return 0

        localTimezoneObject = util.LocalTimezone()
        localTimezoneObject._isdst = _returnZero

        result = localTimezoneObject.dst(datetime.datetime.now())

        self.assertEqual(result, datetime.timedelta(0))

        localTimezoneObject = util.LocalTimezone()
        localTimezoneObject.DSTDIFF = mock.Mock()
        localTimezoneObject._isdst = _returnOne

        result = localTimezoneObject.dst(datetime.datetime.now())

        self.assertEqual(result, localTimezoneObject.DSTDIFF)

    @mock.patch(
        "attotime.util.time.tzname",
        new_callable=mock.PropertyMock(return_value=["notdst", "dst"]),
    )
    def test_tzname(self, mockTZName):
        def _returnOne(*args, **kwargs):
            return 1

        def _returnZero(*args, **kwargs):
            return 0

        localTimezoneObject = util.LocalTimezone()
        localTimezoneObject._isdst = _returnZero

        result = localTimezoneObject.tzname(datetime.datetime.now())

        self.assertEqual(result, "notdst")

        localTimezoneObject = util.LocalTimezone()
        localTimezoneObject._isdst = _returnOne

        result = localTimezoneObject.tzname(datetime.datetime.now())

        self.assertEqual(result, "dst")

    @mock.patch("attotime.util.time.localtime")
    def test_isdst(self, mockLocalTime):
        mockTimeObject = mock.Mock()
        mockTimeObject.tm_isdst = False

        mockLocalTime.return_value = mockTimeObject

        testTime = datetime.datetime.now()

        self.assertFalse(util.LocalTimezone()._isdst(testTime))

        mockLocalTime.assert_called_once_with(
            time.mktime(
                (
                    testTime.year,
                    testTime.month,
                    testTime.day,
                    testTime.hour,
                    testTime.minute,
                    testTime.second,
                    testTime.weekday(),
                    0,
                    0,
                )
            )
        )

        mockLocalTime.reset_mock()

        mockTimeObject = mock.Mock()
        mockTimeObject.tm_isdst = True

        mockLocalTime.return_value = mockTimeObject

        testTime = datetime.datetime.now()

        self.assertTrue(util.LocalTimezone()._isdst(testTime))

        mockLocalTime.assert_called_once_with(
            time.mktime(
                (
                    testTime.year,
                    testTime.month,
                    testTime.day,
                    testTime.hour,
                    testTime.minute,
                    testTime.second,
                    testTime.weekday(),
                    0,
                    0,
                )
            )
        )
