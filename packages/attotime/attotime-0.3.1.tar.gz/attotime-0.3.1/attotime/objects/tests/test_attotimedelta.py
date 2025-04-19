# -*- coding: utf-8 -*-

# Copyright (c) 2021, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import datetime
import unittest
from decimal import Decimal

from attotime import constants
from attotime.objects.attotimedelta import attotimedelta


class TestAttoTimedeltaFunctions(unittest.TestCase):
    def test_init(self):
        result = attotimedelta(weeks=1)

        self.assertEqual(result._native_timedelta, datetime.timedelta(weeks=1))
        self.assertEqual(result._nanoseconds, 0)

        result = attotimedelta(weeks=1.5)

        self.assertEqual(result._native_timedelta, datetime.timedelta(weeks=1.5))
        self.assertEqual(result._nanoseconds, 0)

        result = attotimedelta(weeks=-1)

        self.assertEqual(result._native_timedelta, datetime.timedelta(weeks=-1))
        self.assertEqual(result._nanoseconds, 0)

        result = attotimedelta(weeks=-1.5)

        self.assertEqual(result._native_timedelta, datetime.timedelta(weeks=-1.5))
        self.assertEqual(result._nanoseconds, 0)

        result = attotimedelta(days=1)

        self.assertEqual(result._native_timedelta, datetime.timedelta(days=1))
        self.assertEqual(result._nanoseconds, 0)

        result = attotimedelta(days=1.5)

        self.assertEqual(result._native_timedelta, datetime.timedelta(days=1.5))
        self.assertEqual(result._nanoseconds, 0)

        result = attotimedelta(days=-1)

        self.assertEqual(result._native_timedelta, datetime.timedelta(days=-1))
        self.assertEqual(result._nanoseconds, 0)

        result = attotimedelta(days=-1.5)

        self.assertEqual(result._native_timedelta, datetime.timedelta(days=-1.5))
        self.assertEqual(result._nanoseconds, 0)

        result = attotimedelta(hours=1)

        self.assertEqual(result._native_timedelta, datetime.timedelta(hours=1))
        self.assertEqual(result._nanoseconds, 0)

        result = attotimedelta(hours=1.5)

        self.assertEqual(result._native_timedelta, datetime.timedelta(hours=1.5))
        self.assertEqual(result._nanoseconds, 0)

        result = attotimedelta(hours=-1)

        self.assertEqual(result._native_timedelta, datetime.timedelta(hours=-1))
        self.assertEqual(result._nanoseconds, 0)

        result = attotimedelta(hours=-1.5)

        self.assertEqual(result._native_timedelta, datetime.timedelta(hours=-1.5))
        self.assertEqual(result._nanoseconds, 0)

        result = attotimedelta(minutes=1)

        self.assertEqual(result._native_timedelta, datetime.timedelta(minutes=1))
        self.assertEqual(result._nanoseconds, 0)

        result = attotimedelta(minutes=1.5)

        self.assertEqual(result._native_timedelta, datetime.timedelta(minutes=1.5))
        self.assertEqual(result._nanoseconds, 0)

        result = attotimedelta(minutes=-1)

        self.assertEqual(result._native_timedelta, datetime.timedelta(minutes=-1))
        self.assertEqual(result._nanoseconds, 0)

        result = attotimedelta(minutes=-1.5)

        self.assertEqual(result._native_timedelta, datetime.timedelta(minutes=-1.5))
        self.assertEqual(result._nanoseconds, 0)

        result = attotimedelta(seconds=1)

        self.assertEqual(result._native_timedelta, datetime.timedelta(seconds=1))
        self.assertEqual(result._nanoseconds, 0)

        result = attotimedelta(seconds=1.5)

        self.assertEqual(result._native_timedelta, datetime.timedelta(seconds=1.5))
        self.assertEqual(result._nanoseconds, 0)

        result = attotimedelta(seconds=-1)

        self.assertEqual(result._native_timedelta, datetime.timedelta(seconds=-1))
        self.assertEqual(result._nanoseconds, 0)

        result = attotimedelta(seconds=-1.5)

        self.assertEqual(result._native_timedelta, datetime.timedelta(seconds=-1.5))
        self.assertEqual(result._nanoseconds, 0)

        result = attotimedelta(milliseconds=1)

        self.assertEqual(result._native_timedelta, datetime.timedelta(milliseconds=1))
        self.assertEqual(result._nanoseconds, 0)

        result = attotimedelta(milliseconds=1.5)

        self.assertEqual(result._native_timedelta, datetime.timedelta(milliseconds=1.5))
        self.assertEqual(result._nanoseconds, 0)

        result = attotimedelta(milliseconds=-1)

        self.assertEqual(result._native_timedelta, datetime.timedelta(milliseconds=-1))
        self.assertEqual(result._nanoseconds, 0)

        result = attotimedelta(milliseconds=-1.5)

        self.assertEqual(
            result._native_timedelta, datetime.timedelta(milliseconds=-1.5)
        )
        self.assertEqual(result._nanoseconds, 0)

        result = attotimedelta(microseconds=1)

        self.assertEqual(result._native_timedelta, datetime.timedelta(microseconds=1))
        self.assertEqual(result._nanoseconds, 0)

        result = attotimedelta(microseconds=1.5)

        self.assertEqual(result._native_timedelta, datetime.timedelta(microseconds=1))
        self.assertEqual(result._nanoseconds, 500)

        result = attotimedelta(microseconds=-1)

        self.assertEqual(result._native_timedelta, datetime.timedelta(microseconds=-1))
        self.assertEqual(result._nanoseconds, 0)

        result = attotimedelta(microseconds=-1.5)

        self.assertEqual(result._native_timedelta, datetime.timedelta(microseconds=-1))
        self.assertEqual(result._nanoseconds, -500)

        result = attotimedelta(nanoseconds=1)

        self.assertEqual(result._native_timedelta, datetime.timedelta())
        self.assertEqual(result._nanoseconds, 1)

        result = attotimedelta(nanoseconds=1.5)

        self.assertEqual(result._native_timedelta, datetime.timedelta())
        self.assertEqual(result._nanoseconds, 1.5)

        result = attotimedelta(nanoseconds=-1)

        self.assertEqual(result._native_timedelta, datetime.timedelta())
        self.assertEqual(result._nanoseconds, -1)

        result = attotimedelta(nanoseconds=-1.5)

        self.assertEqual(result._native_timedelta, datetime.timedelta())
        self.assertEqual(result._nanoseconds, -1.5)

        result = attotimedelta(
            days=1,
            seconds=2,
            microseconds=3,
            milliseconds=4,
            minutes=5,
            hours=6,
            weeks=7,
            nanoseconds=9,
        )

        self.assertEqual(
            result._native_timedelta,
            datetime.timedelta(
                days=1,
                seconds=2,
                microseconds=3,
                milliseconds=4,
                minutes=5,
                hours=6,
                weeks=7,
            ),
        )
        self.assertEqual(result._nanoseconds, 9)

        result = attotimedelta(
            nanoseconds=1 * constants.NANOSECONDS_PER_DAY
            + 2 * constants.NANOSECONDS_PER_SECOND
            + 3 * constants.NANOSECONDS_PER_MICROSECOND
            + 4 * constants.NANOSECONDS_PER_MILLISECOND
            + 5 * constants.NANOSECONDS_PER_MINUTE
            + 6 * constants.NANOSECONDS_PER_HOUR
            + 7 * constants.NANOSECONDS_PER_WEEK
            + 9
        )

        self.assertEqual(
            result._native_timedelta,
            datetime.timedelta(
                days=1,
                seconds=2,
                microseconds=3,
                milliseconds=4,
                minutes=5,
                hours=6,
                weeks=7,
            ),
        )
        self.assertEqual(result._nanoseconds, 9)

    def test_init_type_check(self):
        with self.assertRaises(TypeError):
            attotimedelta(days="1")

        with self.assertRaises(TypeError):
            attotimedelta(days=None)

        with self.assertRaises(TypeError):
            attotimedelta(seconds="1")

        with self.assertRaises(TypeError):
            attotimedelta(seconds=None)

        with self.assertRaises(TypeError):
            attotimedelta(microseconds="1")

        with self.assertRaises(TypeError):
            attotimedelta(microseconds=None)

        with self.assertRaises(TypeError):
            attotimedelta(milliseconds="1")

        with self.assertRaises(TypeError):
            attotimedelta(milliseconds=None)

        with self.assertRaises(TypeError):
            attotimedelta(minutes="1")

        with self.assertRaises(TypeError):
            attotimedelta(minutes=None)

        with self.assertRaises(TypeError):
            attotimedelta(hours="1")

        with self.assertRaises(TypeError):
            attotimedelta(hours=None)

        with self.assertRaises(TypeError):
            attotimedelta(weeks="1")

        with self.assertRaises(TypeError):
            attotimedelta(weeks=None)

        with self.assertRaises(TypeError):
            attotimedelta(nanoseconds="1")

        with self.assertRaises(TypeError):
            attotimedelta(nanoseconds=None)

    def test_days(self):
        dt = attotimedelta(days=3)
        self.assertEqual(dt.days, 3)

        dt = attotimedelta(weeks=1)
        self.assertEqual(dt.days, constants.DAYS_PER_WEEK)

    def test_seconds(self):
        dt = attotimedelta(seconds=3)
        self.assertEqual(dt.seconds, 3)

        dt = attotimedelta(minutes=1)
        self.assertEqual(dt.seconds, constants.SECONDS_PER_MINUTE)

        dt = attotimedelta(hours=1)
        self.assertEqual(dt.seconds, constants.SECONDS_PER_HOUR)

    def test_microseconds(self):
        dt = attotimedelta(microseconds=3)
        self.assertEqual(dt.microseconds, 3)

        dt = attotimedelta(milliseconds=1)
        self.assertEqual(dt.microseconds, constants.MICROSECONDS_PER_MILLISECOND)

    def test_nanoseconds(self):
        dt = attotimedelta(nanoseconds=Decimal("3.21"))
        self.assertEqual(dt.nanoseconds, Decimal("3.21"))

    def test_add(self):
        td1 = attotimedelta(days=1)
        td2 = attotimedelta(days=2)

        result = td1 + td2
        self.assertEqual(result, attotimedelta(days=3))

        td1 = attotimedelta(days=3, nanoseconds=Decimal(4))
        td2 = attotimedelta(days=5, nanoseconds=Decimal(6))

        result = td1 + td2
        self.assertEqual(result, attotimedelta(days=8, nanoseconds=Decimal(10)))

        td1 = attotimedelta(days=5, nanoseconds=Decimal(6))
        td2 = attotimedelta(days=-3, nanoseconds=Decimal(-4))

        result = td1 + td2
        self.assertEqual(result, attotimedelta(days=2, nanoseconds=Decimal(2)))

    def test_add_overflow(self):
        td1 = attotimedelta(days=3)
        td2 = attotimedelta(days=4)

        result = td1 + td2
        self.assertEqual(result, attotimedelta(weeks=1))

        td1 = attotimedelta(seconds=30)
        td2 = attotimedelta(seconds=30)

        result = td1 + td2
        self.assertEqual(result, attotimedelta(minutes=1))

        td1 = attotimedelta(microseconds=0.5e6)
        td2 = attotimedelta(microseconds=0.5e6)

        result = td1 + td2
        self.assertEqual(result, attotimedelta(seconds=1))

        td1 = attotimedelta(milliseconds=0.5e3)
        td2 = attotimedelta(milliseconds=0.5e3)

        result = td1 + td2
        self.assertEqual(result, attotimedelta(seconds=1))

        td1 = attotimedelta(minutes=30)
        td2 = attotimedelta(minutes=30)

        result = td1 + td2
        self.assertEqual(result, attotimedelta(hours=1))

        td1 = attotimedelta(hours=12)
        td2 = attotimedelta(hours=12)

        result = td1 + td2
        self.assertEqual(result, attotimedelta(days=1))

        td1 = attotimedelta(nanoseconds=0.5e9)
        td2 = attotimedelta(nanoseconds=0.5e9)

        result = td1 + td2
        self.assertEqual(result, attotimedelta(seconds=1))

    def test_sub(self):
        td1 = attotimedelta(days=2)
        td2 = attotimedelta(days=1)

        result = td1 - td2
        self.assertEqual(result, attotimedelta(days=1))

        td1 = attotimedelta(days=5, nanoseconds=Decimal(6))
        td2 = attotimedelta(days=3, nanoseconds=Decimal(4))

        result = td1 - td2
        self.assertEqual(result, attotimedelta(days=2, nanoseconds=Decimal(2)))

        td1 = attotimedelta(days=5, nanoseconds=Decimal(6))
        td2 = attotimedelta(days=-3, nanoseconds=Decimal(-4))

        result = td1 - td2
        self.assertEqual(result, attotimedelta(days=8, nanoseconds=Decimal(10)))

    def test_sub_underflow(self):
        td1 = attotimedelta(days=1)
        td2 = attotimedelta(hours=12)

        result = td1 - td2
        self.assertEqual(result, attotimedelta(hours=12))

        td1 = attotimedelta(seconds=1)
        td2 = attotimedelta(milliseconds=0.5e3)

        result = td1 - td2
        self.assertEqual(result, attotimedelta(milliseconds=0.5e3))

        td1 = attotimedelta(microseconds=1)
        td2 = attotimedelta(nanoseconds=0.5e3)

        result = td1 - td2
        self.assertEqual(result, attotimedelta(nanoseconds=0.5e3))

        td1 = attotimedelta(milliseconds=1)
        td2 = attotimedelta(microseconds=0.5e3)

        result = td1 - td2
        self.assertEqual(result, attotimedelta(microseconds=0.5e3))

        td1 = attotimedelta(minutes=1)
        td2 = attotimedelta(seconds=30)

        result = td1 - td2
        self.assertEqual(result, attotimedelta(seconds=30))

        td1 = attotimedelta(hours=1)
        td2 = attotimedelta(minutes=30)

        result = td1 - td2
        self.assertEqual(result, attotimedelta(minutes=30))

        td1 = attotimedelta(weeks=1)
        td2 = attotimedelta(days=3)

        result = td1 - td2
        self.assertEqual(result, attotimedelta(days=4))

        td1 = attotimedelta(nanoseconds=1)
        td2 = attotimedelta(nanoseconds=0.5)

        result = td1 - td2
        self.assertEqual(result, attotimedelta(nanoseconds=0.5))

    def test_mul(self):
        result = attotimedelta(days=2) * 3
        self.assertEqual(result, attotimedelta(days=6))

        result = attotimedelta(days=5, nanoseconds=Decimal(6)) * 3
        self.assertEqual(result, attotimedelta(days=15, nanoseconds=Decimal(18)))

        result = attotimedelta(days=5, nanoseconds=Decimal(6)) * -3
        self.assertEqual(result, attotimedelta(days=-15, nanoseconds=Decimal(-18)))

        result = attotimedelta(days=2) * 0.5
        self.assertEqual(result, attotimedelta(days=1))

        result = attotimedelta(days=4) * Decimal(0.25)
        self.assertEqual(result, attotimedelta(days=1))

        result = 3 * attotimedelta(days=2)
        self.assertEqual(result, attotimedelta(days=6))

        result = 3 * attotimedelta(days=5, nanoseconds=Decimal(6))
        self.assertEqual(result, attotimedelta(days=15, nanoseconds=Decimal(18)))

        result = -3 * attotimedelta(days=5, nanoseconds=Decimal(6))
        self.assertEqual(result, attotimedelta(days=-15, nanoseconds=Decimal(-18)))

        result = 0.5 * attotimedelta(days=2)
        self.assertEqual(result, attotimedelta(days=1))

        result = Decimal(0.25) * attotimedelta(days=4)
        self.assertEqual(result, attotimedelta(days=1))

    def test_mul_overflow(self):
        result = attotimedelta(days=1) * 7
        self.assertEqual(result, attotimedelta(weeks=1))

        result = attotimedelta(seconds=30) * 2
        self.assertEqual(result, attotimedelta(minutes=1))

        result = attotimedelta(microseconds=500) * 2
        self.assertEqual(result, attotimedelta(milliseconds=1))

        result = attotimedelta(milliseconds=500) * 2
        self.assertEqual(result, attotimedelta(seconds=1))

        result = attotimedelta(minutes=30) * 2
        self.assertEqual(result, attotimedelta(hours=1))

        result = attotimedelta(hours=12) * 2
        self.assertEqual(result, attotimedelta(days=1))

        result = attotimedelta(nanoseconds=500) * 2
        self.assertEqual(result, attotimedelta(microseconds=1))

    def test_mul_underflow(self):
        result = attotimedelta(days=1) * 0.5
        self.assertEqual(result, attotimedelta(hours=12))

        result = attotimedelta(seconds=1) * Decimal("0.1")
        self.assertEqual(result, attotimedelta(milliseconds=100))

        result = attotimedelta(microseconds=1) * Decimal("0.1")
        self.assertEqual(result, attotimedelta(nanoseconds=100))

        result = attotimedelta(milliseconds=1) * Decimal("0.1")
        self.assertEqual(result, attotimedelta(microseconds=100))

        result = attotimedelta(minutes=1) * 0.5
        self.assertEqual(result, attotimedelta(seconds=30))

        result = attotimedelta(hours=1) * 0.5
        self.assertEqual(result, attotimedelta(minutes=30))

        result = attotimedelta(nanoseconds=1) * 0.5
        self.assertEqual(result, attotimedelta(nanoseconds=0.5))

    def test_div(self):
        result = attotimedelta(days=2) / 2
        self.assertEqual(result, attotimedelta(days=1))

        result = attotimedelta(days=6, nanoseconds=Decimal(6)) / 3
        self.assertEqual(result, attotimedelta(days=2, nanoseconds=Decimal(2)))

        result = attotimedelta(days=6, nanoseconds=Decimal(6)) / -2
        self.assertEqual(result, attotimedelta(days=-3, nanoseconds=Decimal(-3)))

        result = attotimedelta(days=2) / 0.5
        self.assertEqual(result, attotimedelta(days=4))

        result = attotimedelta(days=4) / Decimal(0.25)
        self.assertEqual(result, attotimedelta(days=16))

        result = attotimedelta(nanoseconds=5) / 2
        self.assertEqual(result, attotimedelta(nanoseconds=Decimal(2.5)))

    def test_div_overflow(self):
        result = attotimedelta(days=4) / (Decimal(2) / Decimal(7))
        self.assertEqual(result, attotimedelta(weeks=2))

        result = attotimedelta(seconds=30) / Decimal(0.5)
        self.assertEqual(result, attotimedelta(minutes=1))

        result = attotimedelta(microseconds=500) / Decimal(0.5)
        self.assertEqual(result, attotimedelta(milliseconds=1))

        result = attotimedelta(milliseconds=500) / Decimal(0.5)
        self.assertEqual(result, attotimedelta(seconds=1))

        result = attotimedelta(minutes=30) / Decimal(0.5)
        self.assertEqual(result, attotimedelta(hours=1))

        result = attotimedelta(hours=12) / Decimal(0.5)
        self.assertEqual(result, attotimedelta(days=1))

        result = attotimedelta(nanoseconds=500) / Decimal(0.5)
        self.assertEqual(result, attotimedelta(microseconds=1))

    def test_div_underflow(self):
        result = attotimedelta(days=1) / 2
        self.assertEqual(result, attotimedelta(hours=12))

        result = attotimedelta(seconds=1) / 10
        self.assertEqual(result, attotimedelta(milliseconds=100))

        result = attotimedelta(microseconds=1) / 10
        self.assertEqual(result, attotimedelta(nanoseconds=100))

        result = attotimedelta(milliseconds=1) / 10
        self.assertEqual(result, attotimedelta(microseconds=100))

        result = attotimedelta(minutes=1) / 2
        self.assertEqual(result, attotimedelta(seconds=30))

        result = attotimedelta(hours=1) / 2
        self.assertEqual(result, attotimedelta(minutes=30))

    def test_floordiv(self):
        result = attotimedelta(days=2) // 2
        self.assertEqual(result, attotimedelta(days=1))

        result = attotimedelta(days=6, nanoseconds=Decimal(6)) // 3
        self.assertEqual(result, attotimedelta(days=2, nanoseconds=Decimal(2)))

        result = attotimedelta(days=6, nanoseconds=Decimal(6)) // -2
        self.assertEqual(result, attotimedelta(days=-3, nanoseconds=Decimal(-3)))

        result = attotimedelta(days=2) // 0.5
        self.assertEqual(result, attotimedelta(days=4))

        result = attotimedelta(days=4) // Decimal(0.25)
        self.assertEqual(result, attotimedelta(days=16))

        result = attotimedelta(nanoseconds=5) // 2
        self.assertEqual(result, attotimedelta(nanoseconds=2))

    def test_floordiv_overflow(self):
        result = attotimedelta(days=4) // (Decimal(2) / Decimal(7))
        self.assertEqual(result, attotimedelta(weeks=2))

        result = attotimedelta(seconds=30) // Decimal(0.5)
        self.assertEqual(result, attotimedelta(minutes=1))

        result = attotimedelta(microseconds=500) // Decimal(0.5)
        self.assertEqual(result, attotimedelta(milliseconds=1))

        result = attotimedelta(milliseconds=500) // Decimal(0.5)
        self.assertEqual(result, attotimedelta(seconds=1))

        result = attotimedelta(minutes=30) // Decimal(0.5)
        self.assertEqual(result, attotimedelta(hours=1))

        result = attotimedelta(hours=12) // Decimal(0.5)
        self.assertEqual(result, attotimedelta(days=1))

        result = attotimedelta(nanoseconds=500) // Decimal(0.5)
        self.assertEqual(result, attotimedelta(microseconds=1))

    def test_floordiv_underflow(self):
        result = attotimedelta(days=1) // 2
        self.assertEqual(result, attotimedelta(hours=12))

        result = attotimedelta(seconds=1) // 10
        self.assertEqual(result, attotimedelta(milliseconds=100))

        result = attotimedelta(microseconds=1) // 10
        self.assertEqual(result, attotimedelta(nanoseconds=100))

        result = attotimedelta(milliseconds=1) // 10
        self.assertEqual(result, attotimedelta(microseconds=100))

        result = attotimedelta(minutes=1) // 2
        self.assertEqual(result, attotimedelta(seconds=30))

        result = attotimedelta(hours=1) // 2
        self.assertEqual(result, attotimedelta(minutes=30))

    def test_eq(self):
        self.assertTrue(attotimedelta(days=1) == attotimedelta(days=1))
        self.assertTrue(attotimedelta(seconds=2) == attotimedelta(seconds=2))
        self.assertTrue(attotimedelta(microseconds=3) == attotimedelta(microseconds=3))
        self.assertTrue(attotimedelta(milliseconds=4) == attotimedelta(milliseconds=4))
        self.assertTrue(attotimedelta(minutes=5) == attotimedelta(minutes=5))
        self.assertTrue(attotimedelta(hours=6) == attotimedelta(hours=6))
        self.assertTrue(attotimedelta(weeks=7) == attotimedelta(weeks=7))
        self.assertTrue(
            attotimedelta(nanoseconds=Decimal(8))
            == attotimedelta(nanoseconds=Decimal(8))
        )
        self.assertTrue(
            attotimedelta(
                days=1,
                seconds=2,
                microseconds=3,
                milliseconds=4,
                minutes=5,
                hours=6,
                weeks=7,
                nanoseconds=Decimal(8),
            )
            == attotimedelta(
                days=1,
                seconds=2,
                microseconds=3,
                milliseconds=4,
                minutes=5,
                hours=6,
                weeks=7,
                nanoseconds=Decimal(8),
            )
        )

        # Test some equivalences
        # TODO: 1/7 of a week is not equal to 1 day due to rounding errors
        self.assertTrue(attotimedelta(days=7) == attotimedelta(weeks=1))
        self.assertTrue(attotimedelta(seconds=60) == attotimedelta(minutes=1))
        self.assertTrue(attotimedelta(microseconds=1 * 1e6) == attotimedelta(seconds=1))
        self.assertTrue(attotimedelta(milliseconds=1 * 1e3) == attotimedelta(seconds=1))
        self.assertTrue(attotimedelta(minutes=60) == attotimedelta(hours=1))
        self.assertTrue(attotimedelta(nanoseconds=1 * 1e9) == attotimedelta(seconds=1))

        # Not equals
        self.assertFalse(attotimedelta(days=1) == attotimedelta(days=2))
        self.assertFalse(attotimedelta(seconds=3) == attotimedelta(seconds=4))
        self.assertFalse(attotimedelta(microseconds=5) == attotimedelta(microseconds=6))
        self.assertFalse(attotimedelta(milliseconds=7) == attotimedelta(milliseconds=8))
        self.assertFalse(attotimedelta(minutes=9) == attotimedelta(minutes=10))
        self.assertFalse(attotimedelta(hours=11) == attotimedelta(hours=12))
        self.assertFalse(attotimedelta(weeks=13) == attotimedelta(weeks=14))
        self.assertFalse(
            attotimedelta(nanoseconds=Decimal(15))
            == attotimedelta(nanoseconds=Decimal(16))
        )
        self.assertFalse(
            attotimedelta(
                days=1,
                seconds=2,
                microseconds=3,
                milliseconds=4,
                minutes=5,
                hours=6,
                weeks=7,
                nanoseconds=Decimal(8),
            )
            == attotimedelta(
                days=9,
                seconds=10,
                microseconds=11,
                milliseconds=12,
                minutes=13,
                hours=14,
                weeks=15,
                nanoseconds=Decimal(16),
            )
        )

        # Class check
        self.assertFalse(attotimedelta(days=1) == datetime.timedelta(days=1))

    def test_ne(self):
        # Inverse of test_eq
        self.assertFalse(attotimedelta(days=1) != attotimedelta(days=1))
        self.assertFalse(attotimedelta(seconds=2) != attotimedelta(seconds=2))
        self.assertFalse(attotimedelta(microseconds=3) != attotimedelta(microseconds=3))
        self.assertFalse(attotimedelta(milliseconds=4) != attotimedelta(milliseconds=4))
        self.assertFalse(attotimedelta(minutes=5) != attotimedelta(minutes=5))
        self.assertFalse(attotimedelta(hours=6) != attotimedelta(hours=6))
        self.assertFalse(attotimedelta(weeks=7) != attotimedelta(weeks=7))
        self.assertFalse(
            attotimedelta(nanoseconds=Decimal(8))
            != attotimedelta(nanoseconds=Decimal(8))
        )
        self.assertFalse(
            attotimedelta(
                days=1,
                seconds=2,
                microseconds=3,
                milliseconds=4,
                minutes=5,
                hours=6,
                weeks=7,
                nanoseconds=Decimal(8),
            )
            != attotimedelta(
                days=1,
                seconds=2,
                microseconds=3,
                milliseconds=4,
                minutes=5,
                hours=6,
                weeks=7,
                nanoseconds=Decimal(8),
            )
        )

        # Test some equivalences
        # TODO: 1/7 of a week is not equal to 1 day due to rounding errors
        self.assertFalse(attotimedelta(days=7) != attotimedelta(weeks=1))
        self.assertFalse(attotimedelta(seconds=60) != attotimedelta(minutes=1))
        self.assertFalse(
            attotimedelta(microseconds=1 * 1e6) != attotimedelta(seconds=1)
        )
        self.assertFalse(
            attotimedelta(milliseconds=1 * 1e3) != attotimedelta(seconds=1)
        )
        self.assertFalse(attotimedelta(minutes=60) != attotimedelta(hours=1))
        self.assertFalse(attotimedelta(nanoseconds=1 * 1e9) != attotimedelta(seconds=1))

        # Not equals
        self.assertTrue(attotimedelta(days=1) != attotimedelta(days=2))
        self.assertTrue(attotimedelta(seconds=3) != attotimedelta(seconds=4))
        self.assertTrue(attotimedelta(microseconds=5) != attotimedelta(microseconds=6))
        self.assertTrue(attotimedelta(milliseconds=7) != attotimedelta(milliseconds=8))
        self.assertTrue(attotimedelta(minutes=9) != attotimedelta(minutes=10))
        self.assertTrue(attotimedelta(hours=11) != attotimedelta(hours=12))
        self.assertTrue(attotimedelta(weeks=13) != attotimedelta(weeks=14))
        self.assertTrue(
            attotimedelta(nanoseconds=Decimal(15))
            != attotimedelta(nanoseconds=Decimal(16))
        )
        self.assertTrue(
            attotimedelta(
                days=1,
                seconds=2,
                microseconds=3,
                milliseconds=4,
                minutes=5,
                hours=6,
                weeks=7,
                nanoseconds=Decimal(8),
            )
            != attotimedelta(
                days=9,
                seconds=10,
                microseconds=11,
                milliseconds=12,
                minutes=13,
                hours=14,
                weeks=15,
                nanoseconds=Decimal(16),
            )
        )

        # Class check
        self.assertTrue(attotimedelta(days=1) != datetime.timedelta(days=1))

    def test_gt(self):
        self.assertTrue(attotimedelta(days=2) > attotimedelta(days=1))
        self.assertTrue(attotimedelta(seconds=2) > attotimedelta(seconds=1))
        self.assertTrue(attotimedelta(microseconds=2) > attotimedelta(microseconds=1))
        self.assertTrue(attotimedelta(milliseconds=2) > attotimedelta(milliseconds=1))
        self.assertTrue(attotimedelta(minutes=2) > attotimedelta(minutes=1))
        self.assertTrue(attotimedelta(hours=2) > attotimedelta(hours=1))
        self.assertTrue(attotimedelta(weeks=2) > attotimedelta(weeks=1))
        self.assertTrue(
            attotimedelta(nanoseconds=Decimal(2))
            > attotimedelta(nanoseconds=Decimal(1))
        )
        self.assertTrue(
            attotimedelta(
                days=2,
                seconds=2,
                microseconds=2,
                milliseconds=2,
                minutes=2,
                hours=2,
                weeks=2,
                nanoseconds=Decimal(2),
            )
            > attotimedelta(
                days=1,
                seconds=1,
                microseconds=1,
                milliseconds=1,
                minutes=1,
                hours=1,
                weeks=1,
                nanoseconds=Decimal(1),
            )
        )

        # Test some equivalences
        self.assertFalse(attotimedelta(days=2) > attotimedelta(days=2))
        self.assertFalse(attotimedelta(seconds=2) > attotimedelta(seconds=2))
        self.assertFalse(attotimedelta(microseconds=2) > attotimedelta(microseconds=2))
        self.assertFalse(attotimedelta(milliseconds=2) > attotimedelta(milliseconds=2))
        self.assertFalse(attotimedelta(minutes=2) > attotimedelta(minutes=2))
        self.assertFalse(attotimedelta(hours=2) > attotimedelta(hours=2))
        self.assertFalse(attotimedelta(weeks=2) > attotimedelta(weeks=2))
        self.assertFalse(
            attotimedelta(nanoseconds=Decimal(2))
            > attotimedelta(nanoseconds=Decimal(2))
        )
        self.assertFalse(
            attotimedelta(
                days=2,
                seconds=2,
                microseconds=2,
                milliseconds=2,
                minutes=2,
                hours=2,
                weeks=2,
                nanoseconds=Decimal(2),
            )
            > attotimedelta(
                days=2,
                seconds=2,
                microseconds=2,
                milliseconds=2,
                minutes=2,
                hours=2,
                weeks=2,
                nanoseconds=Decimal(2),
            )
        )

        # Not greaters
        self.assertFalse(attotimedelta(days=1) > attotimedelta(days=2))
        self.assertFalse(attotimedelta(seconds=1) > attotimedelta(seconds=4))
        self.assertFalse(attotimedelta(microseconds=1) > attotimedelta(microseconds=6))
        self.assertFalse(attotimedelta(milliseconds=1) > attotimedelta(milliseconds=8))
        self.assertFalse(attotimedelta(minutes=1) > attotimedelta(minutes=10))
        self.assertFalse(attotimedelta(hours=1) > attotimedelta(hours=12))
        self.assertFalse(attotimedelta(weeks=1) > attotimedelta(weeks=14))
        self.assertFalse(
            attotimedelta(nanoseconds=Decimal(1))
            > attotimedelta(nanoseconds=Decimal(16))
        )
        self.assertFalse(
            attotimedelta(
                days=1,
                seconds=1,
                microseconds=1,
                milliseconds=1,
                minutes=1,
                hours=1,
                weeks=1,
                nanoseconds=Decimal(1),
            )
            > attotimedelta(
                days=2,
                seconds=2,
                microseconds=2,
                milliseconds=2,
                minutes=2,
                hours=2,
                weeks=2,
                nanoseconds=Decimal(2),
            )
        )

        # Class check
        with self.assertRaises(TypeError):
            attotimedelta(days=1) > 1

    def test_ge(self):
        self.assertTrue(attotimedelta(days=2) >= attotimedelta(days=1))
        self.assertTrue(attotimedelta(seconds=2) >= attotimedelta(seconds=1))
        self.assertTrue(attotimedelta(microseconds=2) >= attotimedelta(microseconds=1))
        self.assertTrue(attotimedelta(milliseconds=2) >= attotimedelta(milliseconds=1))
        self.assertTrue(attotimedelta(minutes=2) >= attotimedelta(minutes=1))
        self.assertTrue(attotimedelta(hours=2) >= attotimedelta(hours=1))
        self.assertTrue(attotimedelta(weeks=2) >= attotimedelta(weeks=1))
        self.assertTrue(
            attotimedelta(nanoseconds=Decimal(2))
            >= attotimedelta(nanoseconds=Decimal(1))
        )
        self.assertTrue(
            attotimedelta(
                days=2,
                seconds=2,
                microseconds=2,
                milliseconds=2,
                minutes=2,
                hours=2,
                weeks=2,
                nanoseconds=Decimal(2),
            )
            >= attotimedelta(
                days=1,
                seconds=1,
                microseconds=1,
                milliseconds=1,
                minutes=1,
                hours=1,
                weeks=1,
                nanoseconds=Decimal(1),
            )
        )

        # Test some equivalences
        self.assertTrue(attotimedelta(days=2) >= attotimedelta(days=2))
        self.assertTrue(attotimedelta(seconds=2) >= attotimedelta(seconds=2))
        self.assertTrue(attotimedelta(microseconds=2) >= attotimedelta(microseconds=2))
        self.assertTrue(attotimedelta(milliseconds=2) >= attotimedelta(milliseconds=2))
        self.assertTrue(attotimedelta(minutes=2) >= attotimedelta(minutes=2))
        self.assertTrue(attotimedelta(hours=2) >= attotimedelta(hours=2))
        self.assertTrue(attotimedelta(weeks=2) >= attotimedelta(weeks=2))
        self.assertTrue(
            attotimedelta(nanoseconds=Decimal(2))
            >= attotimedelta(nanoseconds=Decimal(2))
        )
        self.assertTrue(
            attotimedelta(
                days=2,
                seconds=2,
                microseconds=2,
                milliseconds=2,
                minutes=2,
                hours=2,
                weeks=2,
                nanoseconds=Decimal(2),
            )
            >= attotimedelta(
                days=2,
                seconds=2,
                microseconds=2,
                milliseconds=2,
                minutes=2,
                hours=2,
                weeks=2,
                nanoseconds=Decimal(2),
            )
        )

        # Not greaters
        self.assertFalse(attotimedelta(days=1) >= attotimedelta(days=2))
        self.assertFalse(attotimedelta(seconds=1) >= attotimedelta(seconds=4))
        self.assertFalse(attotimedelta(microseconds=1) >= attotimedelta(microseconds=6))
        self.assertFalse(attotimedelta(milliseconds=1) >= attotimedelta(milliseconds=8))
        self.assertFalse(attotimedelta(minutes=1) >= attotimedelta(minutes=10))
        self.assertFalse(attotimedelta(hours=1) >= attotimedelta(hours=12))
        self.assertFalse(attotimedelta(weeks=1) >= attotimedelta(weeks=14))
        self.assertFalse(
            attotimedelta(nanoseconds=Decimal(1))
            >= attotimedelta(nanoseconds=Decimal(16))
        )
        self.assertFalse(
            attotimedelta(
                days=1,
                seconds=1,
                microseconds=1,
                milliseconds=1,
                minutes=1,
                hours=1,
                weeks=1,
                nanoseconds=Decimal(1),
            )
            >= attotimedelta(
                days=2,
                seconds=2,
                microseconds=2,
                milliseconds=2,
                minutes=2,
                hours=2,
                weeks=2,
                nanoseconds=Decimal(2),
            )
        )

        # Class check
        with self.assertRaises(TypeError):
            attotimedelta(days=1) >= 1

    def test_lt(self):
        self.assertTrue(attotimedelta(days=1) < attotimedelta(days=2))
        self.assertTrue(attotimedelta(seconds=1) < attotimedelta(seconds=2))
        self.assertTrue(attotimedelta(microseconds=1) < attotimedelta(microseconds=2))
        self.assertTrue(attotimedelta(milliseconds=1) < attotimedelta(milliseconds=2))
        self.assertTrue(attotimedelta(minutes=1) < attotimedelta(minutes=2))
        self.assertTrue(attotimedelta(hours=1) < attotimedelta(hours=2))
        self.assertTrue(attotimedelta(weeks=1) < attotimedelta(weeks=2))
        self.assertTrue(
            attotimedelta(nanoseconds=Decimal(1))
            < attotimedelta(nanoseconds=Decimal(2))
        )
        self.assertTrue(
            attotimedelta(
                days=1,
                seconds=1,
                microseconds=1,
                milliseconds=1,
                minutes=1,
                hours=1,
                weeks=1,
                nanoseconds=Decimal(1),
            )
            < attotimedelta(
                days=2,
                seconds=2,
                microseconds=2,
                milliseconds=2,
                minutes=2,
                hours=2,
                weeks=2,
                nanoseconds=Decimal(2),
            )
        )

        # Test some equivalences
        self.assertFalse(attotimedelta(days=2) < attotimedelta(days=2))
        self.assertFalse(attotimedelta(seconds=2) < attotimedelta(seconds=2))
        self.assertFalse(attotimedelta(microseconds=2) < attotimedelta(microseconds=2))
        self.assertFalse(attotimedelta(milliseconds=2) < attotimedelta(milliseconds=2))
        self.assertFalse(attotimedelta(minutes=2) < attotimedelta(minutes=2))
        self.assertFalse(attotimedelta(hours=2) < attotimedelta(hours=2))
        self.assertFalse(attotimedelta(weeks=2) < attotimedelta(weeks=2))
        self.assertFalse(
            attotimedelta(nanoseconds=Decimal(2))
            < attotimedelta(nanoseconds=Decimal(2))
        )
        self.assertFalse(
            attotimedelta(
                days=2,
                seconds=2,
                microseconds=2,
                milliseconds=2,
                minutes=2,
                hours=2,
                weeks=2,
                nanoseconds=Decimal(2),
            )
            < attotimedelta(
                days=2,
                seconds=2,
                microseconds=2,
                milliseconds=2,
                minutes=2,
                hours=2,
                weeks=2,
                nanoseconds=Decimal(2),
            )
        )

        # Not greaters
        self.assertFalse(attotimedelta(days=2) < attotimedelta(days=1))
        self.assertFalse(attotimedelta(seconds=4) < attotimedelta(seconds=1))
        self.assertFalse(attotimedelta(microseconds=6) < attotimedelta(microseconds=1))
        self.assertFalse(attotimedelta(milliseconds=8) < attotimedelta(milliseconds=1))
        self.assertFalse(attotimedelta(minutes=10) < attotimedelta(minutes=1))
        self.assertFalse(attotimedelta(hours=12) < attotimedelta(hours=1))
        self.assertFalse(attotimedelta(weeks=14) < attotimedelta(weeks=1))
        self.assertFalse(
            attotimedelta(nanoseconds=Decimal(16))
            < attotimedelta(nanoseconds=Decimal(1))
        )
        self.assertFalse(
            attotimedelta(
                days=2,
                seconds=2,
                microseconds=2,
                milliseconds=2,
                minutes=2,
                hours=2,
                weeks=2,
                nanoseconds=Decimal(2),
            )
            < attotimedelta(
                days=1,
                seconds=1,
                microseconds=1,
                milliseconds=1,
                minutes=1,
                hours=1,
                weeks=1,
                nanoseconds=Decimal(1),
            )
        )

        # Class check
        with self.assertRaises(TypeError):
            attotimedelta(days=1) < 1

    def test_le(self):
        self.assertTrue(attotimedelta(days=1) <= attotimedelta(days=2))
        self.assertTrue(attotimedelta(seconds=1) <= attotimedelta(seconds=2))
        self.assertTrue(attotimedelta(microseconds=1) <= attotimedelta(microseconds=2))
        self.assertTrue(attotimedelta(milliseconds=1) <= attotimedelta(milliseconds=2))
        self.assertTrue(attotimedelta(minutes=1) <= attotimedelta(minutes=2))
        self.assertTrue(attotimedelta(hours=1) <= attotimedelta(hours=2))
        self.assertTrue(attotimedelta(weeks=1) <= attotimedelta(weeks=2))
        self.assertTrue(
            attotimedelta(nanoseconds=Decimal(1))
            <= attotimedelta(nanoseconds=Decimal(2))
        )
        self.assertTrue(
            attotimedelta(
                days=1,
                seconds=1,
                microseconds=1,
                milliseconds=1,
                minutes=1,
                hours=1,
                weeks=1,
                nanoseconds=Decimal(1),
            )
            <= attotimedelta(
                days=2,
                seconds=2,
                microseconds=2,
                milliseconds=2,
                minutes=2,
                hours=2,
                weeks=2,
                nanoseconds=Decimal(2),
            )
        )

        # Test some equivalences
        self.assertTrue(attotimedelta(days=2) <= attotimedelta(days=2))
        self.assertTrue(attotimedelta(seconds=2) <= attotimedelta(seconds=2))
        self.assertTrue(attotimedelta(microseconds=2) <= attotimedelta(microseconds=2))
        self.assertTrue(attotimedelta(milliseconds=2) <= attotimedelta(milliseconds=2))
        self.assertTrue(attotimedelta(minutes=2) <= attotimedelta(minutes=2))
        self.assertTrue(attotimedelta(hours=2) <= attotimedelta(hours=2))
        self.assertTrue(attotimedelta(weeks=2) <= attotimedelta(weeks=2))
        self.assertTrue(
            attotimedelta(nanoseconds=Decimal(2))
            <= attotimedelta(nanoseconds=Decimal(2))
        )
        self.assertTrue(
            attotimedelta(
                days=2,
                seconds=2,
                microseconds=2,
                milliseconds=2,
                minutes=2,
                hours=2,
                weeks=2,
                nanoseconds=Decimal(2),
            )
            <= attotimedelta(
                days=2,
                seconds=2,
                microseconds=2,
                milliseconds=2,
                minutes=2,
                hours=2,
                weeks=2,
                nanoseconds=Decimal(2),
            )
        )

        # Not greaters
        self.assertFalse(attotimedelta(days=2) <= attotimedelta(days=1))
        self.assertFalse(attotimedelta(seconds=4) <= attotimedelta(seconds=1))
        self.assertFalse(attotimedelta(microseconds=6) <= attotimedelta(microseconds=1))
        self.assertFalse(attotimedelta(milliseconds=8) <= attotimedelta(milliseconds=1))
        self.assertFalse(attotimedelta(minutes=10) <= attotimedelta(minutes=1))
        self.assertFalse(attotimedelta(hours=12) <= attotimedelta(hours=1))
        self.assertFalse(attotimedelta(weeks=14) <= attotimedelta(weeks=1))
        self.assertFalse(
            attotimedelta(nanoseconds=Decimal(16))
            <= attotimedelta(nanoseconds=Decimal(1))
        )
        self.assertFalse(
            attotimedelta(
                days=2,
                seconds=2,
                microseconds=2,
                milliseconds=2,
                minutes=2,
                hours=2,
                weeks=2,
                nanoseconds=Decimal(2),
            )
            <= attotimedelta(
                days=1,
                seconds=1,
                microseconds=1,
                milliseconds=1,
                minutes=1,
                hours=1,
                weeks=1,
                nanoseconds=Decimal(1),
            )
        )

        # Class check
        with self.assertRaises(TypeError):
            attotimedelta(days=1) <= 1

    def test_pos(self):
        td1 = attotimedelta(days=5, nanoseconds=Decimal(6))
        td2 = attotimedelta(days=-3, nanoseconds=Decimal(-4))
        # https://stackoverflow.com/questions/16819023/whats-the-purpose-of-the-pos-unary-operator-in-python
        td3 = attotimedelta(
            nanoseconds=Decimal("3.1415926535897932384626433832795028841971")
        )

        result = +td1
        self.assertEqual(result, td1)

        result = +td2
        self.assertEqual(result, td2)

        result = +td3
        self.assertEqual(
            result, attotimedelta(nanoseconds=Decimal("3.141592653589793238462643383"))
        )

    def test_neg(self):
        td1 = attotimedelta(days=5, nanoseconds=Decimal(6))
        td2 = attotimedelta(days=-3, nanoseconds=Decimal(-4))
        # https://stackoverflow.com/questions/16819023/whats-the-purpose-of-the-pos-unary-operator-in-python
        td3 = attotimedelta(
            nanoseconds=Decimal("3.1415926535897932384626433832795028841971")
        )

        result = -td1
        self.assertEqual(result, attotimedelta(days=-5, nanoseconds=Decimal(-6)))

        result = -td2
        self.assertEqual(result, attotimedelta(days=3, nanoseconds=Decimal(4)))

        result = -td3
        self.assertEqual(
            result, attotimedelta(nanoseconds=Decimal("-3.141592653589793238462643383"))
        )

    def test_abs(self):
        td1 = attotimedelta(days=5, nanoseconds=Decimal(6))
        td2 = attotimedelta(days=-3, nanoseconds=Decimal(-4))
        td3 = attotimedelta(days=-3, nanoseconds=Decimal(4))
        td4 = attotimedelta(days=3, nanoseconds=Decimal(-4))

        result = abs(td1)
        self.assertEqual(result, attotimedelta(days=5, nanoseconds=Decimal(6)))

        result = abs(td2)
        self.assertEqual(result, attotimedelta(days=3, nanoseconds=Decimal(4)))

        result = abs(td3)
        self.assertEqual(
            result, attotimedelta(days=3) - attotimedelta(nanoseconds=Decimal(4))
        )

        result = abs(td4)
        self.assertEqual(
            result, attotimedelta(days=3) - attotimedelta(nanoseconds=Decimal(4))
        )

    def test_str(self):
        result = str(attotimedelta(days=1))
        self.assertEqual(result, "1 day, 0:00:00")

        result = str(attotimedelta(days=5))
        self.assertEqual(result, "5 days, 0:00:00")

        result = str(attotimedelta(days=50))
        self.assertEqual(result, "50 days, 0:00:00")

        result = str(attotimedelta(days=-1))
        self.assertEqual(result, "-1 day, 0:00:00")

        result = str(attotimedelta(days=-5))
        self.assertEqual(result, "-5 days, 0:00:00")

        result = str(attotimedelta(days=-50))
        self.assertEqual(result, "-50 days, 0:00:00")

        result = str(attotimedelta(seconds=1))
        self.assertEqual(result, "0:00:01")

        result = str(attotimedelta(seconds=5))
        self.assertEqual(result, "0:00:05")

        result = str(attotimedelta(seconds=50))
        self.assertEqual(result, "0:00:50")

        result = str(attotimedelta(seconds=-1))
        self.assertEqual(result, "-1 day, 23:59:59")

        result = str(attotimedelta(seconds=-5))
        self.assertEqual(result, "-1 day, 23:59:55")

        result = str(attotimedelta(seconds=-50))
        self.assertEqual(result, "-1 day, 23:59:10")

        result = str(attotimedelta(microseconds=1))
        self.assertEqual(result, "0:00:00.000001")

        result = str(attotimedelta(microseconds=5))
        self.assertEqual(result, "0:00:00.000005")

        result = str(attotimedelta(microseconds=50))
        self.assertEqual(result, "0:00:00.00005")

        result = str(attotimedelta(microseconds=-1))
        self.assertEqual(result, "-1 day, 23:59:59.999999")

        result = str(attotimedelta(microseconds=-5))
        self.assertEqual(result, "-1 day, 23:59:59.999995")

        result = str(attotimedelta(microseconds=-50))
        self.assertEqual(result, "-1 day, 23:59:59.99995")

        result = str(attotimedelta(milliseconds=1))
        self.assertEqual(result, "0:00:00.001")

        result = str(attotimedelta(milliseconds=5))
        self.assertEqual(result, "0:00:00.005")

        result = str(attotimedelta(milliseconds=50))
        self.assertEqual(result, "0:00:00.05")

        result = str(attotimedelta(milliseconds=-1))
        self.assertEqual(result, "-1 day, 23:59:59.999")

        result = str(attotimedelta(milliseconds=-5))
        self.assertEqual(result, "-1 day, 23:59:59.995")

        result = str(attotimedelta(milliseconds=-50))
        self.assertEqual(result, "-1 day, 23:59:59.95")

        result = str(attotimedelta(minutes=1))
        self.assertEqual(result, "0:01:00")

        result = str(attotimedelta(minutes=5))
        self.assertEqual(result, "0:05:00")

        result = str(attotimedelta(minutes=50))
        self.assertEqual(result, "0:50:00")

        result = str(attotimedelta(minutes=-1))
        self.assertEqual(result, "-1 day, 23:59:00")

        result = str(attotimedelta(minutes=-5))
        self.assertEqual(result, "-1 day, 23:55:00")

        result = str(attotimedelta(minutes=-50))
        self.assertEqual(result, "-1 day, 23:10:00")

        result = str(attotimedelta(hours=1))
        self.assertEqual(result, "1:00:00")

        result = str(attotimedelta(hours=5))
        self.assertEqual(result, "5:00:00")

        result = str(attotimedelta(hours=12))
        self.assertEqual(result, "12:00:00")

        result = str(attotimedelta(hours=-1))
        self.assertEqual(result, "-1 day, 23:00:00")

        result = str(attotimedelta(hours=-5))
        self.assertEqual(result, "-1 day, 19:00:00")

        result = str(attotimedelta(hours=-12))
        self.assertEqual(result, "-1 day, 12:00:00")

        result = str(attotimedelta(weeks=1))
        self.assertEqual(result, "7 days, 0:00:00")

        result = str(attotimedelta(weeks=5))
        self.assertEqual(result, "35 days, 0:00:00")

        result = str(attotimedelta(weeks=50))
        self.assertEqual(result, "350 days, 0:00:00")

        result = str(attotimedelta(weeks=-1))
        self.assertEqual(result, "-7 days, 0:00:00")

        result = str(attotimedelta(weeks=-5))
        self.assertEqual(result, "-35 days, 0:00:00")

        result = str(attotimedelta(weeks=-50))
        self.assertEqual(result, "-350 days, 0:00:00")

        result = str(attotimedelta(nanoseconds=1))
        self.assertEqual(result, "0:00:00.000000001")

        result = str(attotimedelta(nanoseconds=5))
        self.assertEqual(result, "0:00:00.000000005")

        result = str(attotimedelta(nanoseconds=50))
        self.assertEqual(result, "0:00:00.00000005")

        result = str(attotimedelta(nanoseconds=Decimal("0.001")))
        self.assertEqual(result, "0:00:00.000000000001")

        result = str(attotimedelta(nanoseconds=-1))
        self.assertEqual(result, "-1 day, 23:59:59.999999999")

        result = str(attotimedelta(nanoseconds=-5))
        self.assertEqual(result, "-1 day, 23:59:59.999999995")

        result = str(attotimedelta(nanoseconds=-50))
        self.assertEqual(result, "-1 day, 23:59:59.99999995")

        result = str(attotimedelta(nanoseconds=Decimal("-0.001")))
        self.assertEqual(result, "-1 day, 23:59:59.999999999999")

        result = str(
            attotimedelta(
                days=1,
                seconds=5,
                microseconds=5,
                milliseconds=5,
                minutes=50,
                hours=5,
                weeks=1,
                nanoseconds=5,
            )
        )
        self.assertEqual(result, "8 days, 5:50:05.005005005")

        result = str(
            attotimedelta(
                days=-1,
                seconds=-5,
                microseconds=-5,
                milliseconds=-5,
                minutes=-50,
                hours=-5,
                weeks=-1,
                nanoseconds=-5,
            )
        )
        self.assertEqual(result, "-9 days, 18:09:54.994994995")

    def test_repr(self):
        result = repr(attotimedelta(days=1))
        self.assertEqual(result, "attotime.objects.attotimedelta(1)")

        result = repr(attotimedelta(days=5))
        self.assertEqual(result, "attotime.objects.attotimedelta(5)")

        result = repr(attotimedelta(days=50))
        self.assertEqual(result, "attotime.objects.attotimedelta(50)")

        result = repr(attotimedelta(days=-1))
        self.assertEqual(result, "attotime.objects.attotimedelta(-1)")

        result = repr(attotimedelta(days=-5))
        self.assertEqual(result, "attotime.objects.attotimedelta(-5)")

        result = repr(attotimedelta(days=-50))
        self.assertEqual(result, "attotime.objects.attotimedelta(-50)")

        result = repr(attotimedelta(seconds=1))
        self.assertEqual(result, "attotime.objects.attotimedelta(0, 1)")

        result = repr(attotimedelta(seconds=5))
        self.assertEqual(result, "attotime.objects.attotimedelta(0, 5)")

        result = repr(attotimedelta(seconds=50))
        self.assertEqual(result, "attotime.objects.attotimedelta(0, 50)")

        result = repr(attotimedelta(seconds=-1))
        self.assertEqual(result, "attotime.objects.attotimedelta(-1, 86399)")

        result = repr(attotimedelta(seconds=-5))
        self.assertEqual(result, "attotime.objects.attotimedelta(-1, 86395)")

        result = repr(attotimedelta(seconds=-50))
        self.assertEqual(result, "attotime.objects.attotimedelta(-1, 86350)")

        result = repr(attotimedelta(microseconds=1))
        self.assertEqual(result, "attotime.objects.attotimedelta(0, 0, 1)")

        result = repr(attotimedelta(microseconds=5))
        self.assertEqual(result, "attotime.objects.attotimedelta(0, 0, 5)")

        result = repr(attotimedelta(microseconds=50))
        self.assertEqual(result, "attotime.objects.attotimedelta(0, 0, 50)")

        result = repr(attotimedelta(microseconds=-1))
        self.assertEqual(result, "attotime.objects.attotimedelta(-1, 86399, 999999)")

        result = repr(attotimedelta(microseconds=-5))
        self.assertEqual(result, "attotime.objects.attotimedelta(-1, 86399, 999995)")

        result = repr(attotimedelta(microseconds=-50))
        self.assertEqual(result, "attotime.objects.attotimedelta(-1, 86399, 999950)")

        result = repr(attotimedelta(milliseconds=1))
        self.assertEqual(result, "attotime.objects.attotimedelta(0, 0, 1000)")

        result = repr(attotimedelta(milliseconds=5))
        self.assertEqual(result, "attotime.objects.attotimedelta(0, 0, 5000)")

        result = repr(attotimedelta(milliseconds=50))
        self.assertEqual(result, "attotime.objects.attotimedelta(0, 0, 50000)")

        result = repr(attotimedelta(milliseconds=-1))
        self.assertEqual(result, "attotime.objects.attotimedelta(-1, 86399, 999000)")

        result = repr(attotimedelta(milliseconds=-5))
        self.assertEqual(result, "attotime.objects.attotimedelta(-1, 86399, 995000)")

        result = repr(attotimedelta(milliseconds=-50))
        self.assertEqual(result, "attotime.objects.attotimedelta(-1, 86399, 950000)")

        result = repr(attotimedelta(minutes=1))
        self.assertEqual(result, "attotime.objects.attotimedelta(0, 60)")

        result = repr(attotimedelta(minutes=5))
        self.assertEqual(result, "attotime.objects.attotimedelta(0, 300)")

        result = repr(attotimedelta(minutes=50))
        self.assertEqual(result, "attotime.objects.attotimedelta(0, 3000)")

        result = repr(attotimedelta(minutes=-1))
        self.assertEqual(result, "attotime.objects.attotimedelta(-1, 86340)")

        result = repr(attotimedelta(minutes=-5))
        self.assertEqual(result, "attotime.objects.attotimedelta(-1, 86100)")

        result = repr(attotimedelta(minutes=-50))
        self.assertEqual(result, "attotime.objects.attotimedelta(-1, 83400)")

        result = repr(attotimedelta(hours=1))
        self.assertEqual(result, "attotime.objects.attotimedelta(0, 3600)")

        result = repr(attotimedelta(hours=5))
        self.assertEqual(result, "attotime.objects.attotimedelta(0, 18000)")

        result = repr(attotimedelta(hours=12))
        self.assertEqual(result, "attotime.objects.attotimedelta(0, 43200)")

        result = repr(attotimedelta(hours=-1))
        self.assertEqual(result, "attotime.objects.attotimedelta(-1, 82800)")

        result = repr(attotimedelta(hours=-5))
        self.assertEqual(result, "attotime.objects.attotimedelta(-1, 68400)")

        result = repr(attotimedelta(hours=-12))
        self.assertEqual(result, "attotime.objects.attotimedelta(-1, 43200)")

        result = repr(attotimedelta(weeks=1))
        self.assertEqual(result, "attotime.objects.attotimedelta(7)")

        result = repr(attotimedelta(weeks=5))
        self.assertEqual(result, "attotime.objects.attotimedelta(35)")

        result = repr(attotimedelta(weeks=50))
        self.assertEqual(result, "attotime.objects.attotimedelta(350)")

        result = repr(attotimedelta(weeks=-1))
        self.assertEqual(result, "attotime.objects.attotimedelta(-7)")

        result = repr(attotimedelta(weeks=-5))
        self.assertEqual(result, "attotime.objects.attotimedelta(-35)")

        result = repr(attotimedelta(weeks=-50))
        self.assertEqual(result, "attotime.objects.attotimedelta(-350)")

        result = repr(attotimedelta(nanoseconds=1))
        self.assertEqual(result, "attotime.objects.attotimedelta(0, 0, 0, 1)")

        result = repr(attotimedelta(nanoseconds=5))
        self.assertEqual(result, "attotime.objects.attotimedelta(0, 0, 0, 5)")

        result = repr(attotimedelta(nanoseconds=50))
        self.assertEqual(result, "attotime.objects.attotimedelta(0, 0, 0, 50)")

        result = repr(attotimedelta(nanoseconds=Decimal("0.001")))
        self.assertEqual(result, "attotime.objects.attotimedelta(0, 0, 0, 0.001)")

        result = repr(attotimedelta(nanoseconds=-1))
        self.assertEqual(
            result, "attotime.objects.attotimedelta(-1, 86399, 999999, 999)"
        )

        result = repr(attotimedelta(nanoseconds=-5))
        self.assertEqual(
            result, "attotime.objects.attotimedelta(-1, 86399, 999999, 995)"
        )

        result = repr(attotimedelta(nanoseconds=-50))
        self.assertEqual(
            result, "attotime.objects.attotimedelta(-1, 86399, 999999, 950)"
        )

        result = repr(attotimedelta(nanoseconds=Decimal("-0.001")))
        self.assertEqual(
            result, "attotime.objects.attotimedelta(-1, 86399, 999999, 999.999)"
        )

        result = repr(
            attotimedelta(
                days=1,
                seconds=5,
                microseconds=5,
                milliseconds=5,
                minutes=50,
                hours=5,
                weeks=1,
                nanoseconds=5,
            )
        )
        self.assertEqual(result, "attotime.objects.attotimedelta(8, 21005, 5005, 5)")

        result = repr(
            attotimedelta(
                days=-1,
                seconds=-5,
                microseconds=-5,
                milliseconds=-5,
                minutes=-50,
                hours=-5,
                weeks=-1,
                nanoseconds=-5,
            )
        )
        self.assertEqual(
            result, "attotime.objects.attotimedelta(-9, 65394, 994994, 995)"
        )

    def test_total_seconds(self):
        result = attotimedelta(days=1).total_seconds()
        self.assertEqual(result, constants.SECONDS_PER_DAY)

        result = attotimedelta(seconds=1).total_seconds()
        self.assertEqual(result, 1)

        result = attotimedelta(microseconds=1).total_seconds()
        self.assertEqual(result, Decimal("1e-6"))

        result = attotimedelta(milliseconds=1).total_seconds()
        self.assertEqual(result, Decimal("1e-3"))

        result = attotimedelta(minutes=1).total_seconds()
        self.assertEqual(result, constants.SECONDS_PER_MINUTE)

        result = attotimedelta(hours=1).total_seconds()
        self.assertEqual(result, constants.SECONDS_PER_HOUR)

        result = attotimedelta(weeks=1).total_seconds()
        self.assertEqual(result, constants.SECONDS_PER_WEEK)

        result = attotimedelta(nanoseconds=1).total_seconds()
        self.assertEqual(result, Decimal("1e-9"))

        result = attotimedelta(days=-1).total_seconds()
        self.assertEqual(result, -constants.SECONDS_PER_DAY)

        result = attotimedelta(seconds=-1).total_seconds()
        self.assertEqual(result, -1)

        result = attotimedelta(microseconds=-1).total_seconds()
        self.assertEqual(result, -Decimal("1e-6"))

        result = attotimedelta(milliseconds=-1).total_seconds()
        self.assertEqual(result, -Decimal("1e-3"))

        result = attotimedelta(minutes=-1).total_seconds()
        self.assertEqual(result, -constants.SECONDS_PER_MINUTE)

        result = attotimedelta(hours=-1).total_seconds()
        self.assertEqual(result, -constants.SECONDS_PER_HOUR)

        result = attotimedelta(weeks=-1).total_seconds()
        self.assertEqual(result, -constants.SECONDS_PER_WEEK)

        result = attotimedelta(nanoseconds=-1).total_seconds()
        self.assertEqual(result, -Decimal("1e-9"))

        result = attotimedelta(
            days=1,
            seconds=1,
            microseconds=1,
            milliseconds=1,
            minutes=1,
            hours=1,
            weeks=1,
            nanoseconds=Decimal(3.14159),
        ).total_seconds()
        self.assertEqual(
            result,
            constants.SECONDS_PER_DAY
            + 1
            + Decimal("1e-6")
            + Decimal("1e-3")
            + constants.SECONDS_PER_MINUTE
            + constants.SECONDS_PER_HOUR
            + constants.SECONDS_PER_WEEK
            + (Decimal(3.14159) / constants.NANOSECONDS_PER_SECOND),
        )

        result = attotimedelta(
            days=1,
            seconds=-1,
            microseconds=1,
            milliseconds=-1,
            minutes=1,
            hours=-1,
            weeks=1,
            nanoseconds=Decimal(3.14159),
        ).total_seconds()
        self.assertEqual(
            result,
            constants.SECONDS_PER_DAY
            - 1
            + Decimal("1e-6")
            - Decimal("1e-3")
            + constants.SECONDS_PER_MINUTE
            - constants.SECONDS_PER_HOUR
            + constants.SECONDS_PER_WEEK
            + (Decimal(3.14159) / constants.NANOSECONDS_PER_SECOND),
        )

    def test_total_nanoseconds(self):
        result = attotimedelta(days=1).total_nanoseconds()
        self.assertEqual(result, constants.NANOSECONDS_PER_DAY)

        result = attotimedelta(seconds=1).total_nanoseconds()
        self.assertEqual(result, constants.NANOSECONDS_PER_SECOND)

        result = attotimedelta(microseconds=1).total_nanoseconds()
        self.assertEqual(result, constants.NANOSECONDS_PER_MICROSECOND)

        result = attotimedelta(milliseconds=1).total_nanoseconds()
        self.assertEqual(result, constants.NANOSECONDS_PER_MILLISECOND)

        result = attotimedelta(minutes=1).total_nanoseconds()
        self.assertEqual(result, constants.NANOSECONDS_PER_MINUTE)

        result = attotimedelta(hours=1).total_nanoseconds()
        self.assertEqual(result, constants.NANOSECONDS_PER_HOUR)

        result = attotimedelta(weeks=1).total_nanoseconds()
        self.assertEqual(result, constants.NANOSECONDS_PER_WEEK)

        result = attotimedelta(nanoseconds=1).total_nanoseconds()
        self.assertEqual(result, 1)

        result = attotimedelta(days=-1).total_nanoseconds()
        self.assertEqual(result, -constants.NANOSECONDS_PER_DAY)

        result = attotimedelta(seconds=-1).total_nanoseconds()
        self.assertEqual(result, -constants.NANOSECONDS_PER_SECOND)

        result = attotimedelta(microseconds=-1).total_nanoseconds()
        self.assertEqual(result, -constants.NANOSECONDS_PER_MICROSECOND)

        result = attotimedelta(milliseconds=-1).total_nanoseconds()
        self.assertEqual(result, -constants.NANOSECONDS_PER_MILLISECOND)

        result = attotimedelta(minutes=-1).total_nanoseconds()
        self.assertEqual(result, -constants.NANOSECONDS_PER_MINUTE)

        result = attotimedelta(hours=-1).total_nanoseconds()
        self.assertEqual(result, -constants.NANOSECONDS_PER_HOUR)

        result = attotimedelta(weeks=-1).total_nanoseconds()
        self.assertEqual(result, -constants.NANOSECONDS_PER_WEEK)

        result = attotimedelta(nanoseconds=-1).total_nanoseconds()
        self.assertEqual(result, -1)

        result = attotimedelta(
            days=1,
            seconds=1,
            microseconds=1,
            milliseconds=1,
            minutes=1,
            hours=1,
            weeks=1,
            nanoseconds=Decimal(3.14159),
        ).total_nanoseconds()
        self.assertEqual(
            result,
            constants.NANOSECONDS_PER_DAY
            + constants.NANOSECONDS_PER_SECOND
            + constants.NANOSECONDS_PER_MICROSECOND
            + constants.NANOSECONDS_PER_MILLISECOND
            + constants.NANOSECONDS_PER_MINUTE
            + constants.NANOSECONDS_PER_HOUR
            + constants.NANOSECONDS_PER_WEEK
            + Decimal(3.14159),
        )

        result = attotimedelta(
            days=1,
            seconds=-1,
            microseconds=1,
            milliseconds=-1,
            minutes=1,
            hours=-1,
            weeks=1,
            nanoseconds=Decimal(3.14159),
        ).total_nanoseconds()
        self.assertEqual(
            result,
            constants.NANOSECONDS_PER_DAY
            - constants.NANOSECONDS_PER_SECOND
            + constants.NANOSECONDS_PER_MICROSECOND
            - constants.NANOSECONDS_PER_MILLISECOND
            + constants.NANOSECONDS_PER_MINUTE
            - constants.NANOSECONDS_PER_HOUR
            + constants.NANOSECONDS_PER_WEEK
            + Decimal(3.14159),
        )

    def test_as_nanoseconds(self):
        result = attotimedelta._as_nanoseconds(days=1)
        self.assertEqual(result, constants.NANOSECONDS_PER_DAY)

        result = attotimedelta._as_nanoseconds(seconds=1)
        self.assertEqual(result, constants.NANOSECONDS_PER_SECOND)

        result = attotimedelta._as_nanoseconds(microseconds=1)
        self.assertEqual(result, constants.NANOSECONDS_PER_MICROSECOND)

        result = attotimedelta._as_nanoseconds(milliseconds=1)
        self.assertEqual(result, constants.NANOSECONDS_PER_MILLISECOND)

        result = attotimedelta._as_nanoseconds(minutes=1)
        self.assertEqual(result, constants.NANOSECONDS_PER_MINUTE)

        result = attotimedelta._as_nanoseconds(hours=1)
        self.assertEqual(result, constants.NANOSECONDS_PER_HOUR)

        result = attotimedelta._as_nanoseconds(weeks=1)
        self.assertEqual(result, constants.NANOSECONDS_PER_WEEK)

        result = attotimedelta._as_nanoseconds(nanoseconds=1)
        self.assertEqual(result, 1)

        result = attotimedelta._as_nanoseconds(days=-1)
        self.assertEqual(result, -constants.NANOSECONDS_PER_DAY)

        result = attotimedelta._as_nanoseconds(seconds=-1)
        self.assertEqual(result, -constants.NANOSECONDS_PER_SECOND)

        result = attotimedelta._as_nanoseconds(microseconds=-1)
        self.assertEqual(result, -constants.NANOSECONDS_PER_MICROSECOND)

        result = attotimedelta._as_nanoseconds(milliseconds=-1)
        self.assertEqual(result, -constants.NANOSECONDS_PER_MILLISECOND)

        result = attotimedelta._as_nanoseconds(minutes=-1)
        self.assertEqual(result, -constants.NANOSECONDS_PER_MINUTE)

        result = attotimedelta._as_nanoseconds(hours=-1)
        self.assertEqual(result, -constants.NANOSECONDS_PER_HOUR)

        result = attotimedelta._as_nanoseconds(weeks=-1)
        self.assertEqual(result, -constants.NANOSECONDS_PER_WEEK)

        result = attotimedelta._as_nanoseconds(nanoseconds=-1)
        self.assertEqual(result, -1)

        result = attotimedelta._as_nanoseconds(
            days=1,
            seconds=2,
            microseconds=3,
            milliseconds=4,
            minutes=5,
            hours=6,
            weeks=7,
            nanoseconds=8,
        )
        self.assertEqual(
            result,
            constants.NANOSECONDS_PER_DAY
            + 2 * constants.NANOSECONDS_PER_SECOND
            + 3 * constants.NANOSECONDS_PER_MICROSECOND
            + 4 * constants.NANOSECONDS_PER_MILLISECOND
            + 5 * constants.NANOSECONDS_PER_MINUTE
            + 6 * constants.NANOSECONDS_PER_HOUR
            + 7 * constants.NANOSECONDS_PER_WEEK
            + 8,
        )

        result = attotimedelta._as_nanoseconds(
            days=-1,
            seconds=-2,
            microseconds=-3,
            milliseconds=-4,
            minutes=-5,
            hours=-6,
            weeks=-7,
            nanoseconds=-8,
        )
        self.assertEqual(
            result,
            -(
                constants.NANOSECONDS_PER_DAY
                + 2 * constants.NANOSECONDS_PER_SECOND
                + 3 * constants.NANOSECONDS_PER_MICROSECOND
                + 4 * constants.NANOSECONDS_PER_MILLISECOND
                + 5 * constants.NANOSECONDS_PER_MINUTE
                + 6 * constants.NANOSECONDS_PER_HOUR
                + 7 * constants.NANOSECONDS_PER_WEEK
                + 8
            ),
        )

    def test_reduce_nanoseconds_int(self):
        result = attotimedelta._reduce_nanoseconds(1)
        self.assertEqual(result, (0, 0, 0, 0, 0, 0, 0, 1))

        # One microsecond
        result = attotimedelta._reduce_nanoseconds(1 * Decimal("1e3"))
        self.assertEqual(result, (0, 0, 1, 0, 0, 0, 0, 0))

        # One millisecond
        result = attotimedelta._reduce_nanoseconds(1 * Decimal("1e6"))
        self.assertEqual(result, (0, 0, 0, 1, 0, 0, 0, 0))

        # One second
        result = attotimedelta._reduce_nanoseconds(1 * Decimal("1e9"))
        self.assertEqual(result, (0, 1, 0, 0, 0, 0, 0, 0))

        # One minute
        result = attotimedelta._reduce_nanoseconds(1 * Decimal("1e9") * 60)
        self.assertEqual(result, (0, 0, 0, 0, 1, 0, 0, 0))

        # One hour
        result = attotimedelta._reduce_nanoseconds(1 * Decimal("1e9") * 60 * 60)
        self.assertEqual(result, (0, 0, 0, 0, 0, 1, 0, 0))

        # One day
        result = attotimedelta._reduce_nanoseconds(1 * Decimal("1e9") * 60 * 60 * 24)
        self.assertEqual(result, (1, 0, 0, 0, 0, 0, 0, 0))

        # One week
        result = attotimedelta._reduce_nanoseconds(
            1 * Decimal("1e9") * 60 * 60 * 24 * 7
        )
        self.assertEqual(result, (0, 0, 0, 0, 0, 0, 1, 0))

        result = attotimedelta._reduce_nanoseconds(-1)
        self.assertEqual(result, (0, 0, 0, 0, 0, 0, 0, -1))

        # One microsecond
        result = attotimedelta._reduce_nanoseconds(-1 * Decimal("1e3"))
        self.assertEqual(result, (0, 0, -1, 0, 0, 0, 0, 0))

        # One millisecond
        result = attotimedelta._reduce_nanoseconds(-1 * Decimal("1e6"))
        self.assertEqual(result, (0, 0, 0, -1, 0, 0, 0, 0))

        # One second
        result = attotimedelta._reduce_nanoseconds(-1 * Decimal("1e9"))
        self.assertEqual(result, (0, -1, 0, 0, 0, 0, 0, 0))

        # One minute
        result = attotimedelta._reduce_nanoseconds(-1 * Decimal("1e9") * 60)
        self.assertEqual(result, (0, 0, 0, 0, -1, 0, 0, 0))

        # One hour
        result = attotimedelta._reduce_nanoseconds(-1 * Decimal("1e9") * 60 * 60)
        self.assertEqual(result, (0, 0, 0, 0, 0, -1, 0, 0))

        # One day
        result = attotimedelta._reduce_nanoseconds(-1 * Decimal("1e9") * 60 * 60 * 24)
        self.assertEqual(result, (-1, 0, 0, 0, 0, 0, 0, 0))

        # One week
        result = attotimedelta._reduce_nanoseconds(
            -1 * Decimal("1e9") * 60 * 60 * 24 * 7
        )
        self.assertEqual(result, (0, 0, 0, 0, 0, 0, -1, 0))

    def test_reduce_nanoseconds_decimal(self):
        result = attotimedelta._reduce_nanoseconds(Decimal("1.123456789"))
        self.assertEqual(result, (0, 0, 0, 0, 0, 0, 0, Decimal("1.123456789")))

        result = attotimedelta._reduce_nanoseconds(Decimal("-1.123456789"))
        self.assertEqual(result, (0, 0, 0, 0, 0, 0, 0, Decimal("-1.123456789")))
