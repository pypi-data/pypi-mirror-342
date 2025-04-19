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
from attotime.objects.attotime import attotime
from attotime.tests.common import DSTOffset, FixedOffset


class TestAttoTimeFunctions(unittest.TestCase):
    def test_init(self):
        result = attotime(
            hour=1,
            minute=2,
            second=3,
            microsecond=4,
            nanosecond=Decimal("5.67"),
        )

        self.assertEqual(
            result._native_time,
            datetime.time(hour=1, minute=2, second=3, microsecond=4),
        )
        self.assertEqual(result._nanosecond, Decimal("5.67"))
        self.assertEqual(result._tzinfo, None)

        result = attotime(
            hour=1,
            minute=2,
            second=3,
            microsecond=4,
            nanosecond=5,
            tzinfo=FixedOffset(1, name="+1"),
        )

        self.assertEqual(
            result._native_time,
            datetime.time(hour=1, minute=2, second=3, microsecond=4),
        )
        self.assertEqual(result._nanosecond, 5)
        self.assertEqual(result._tzinfo, FixedOffset(1, name="+1"))

    def test_native_time(self):
        result = attotime(hour=1)
        self.assertEqual(result._native_time, datetime.time(hour=1))

        result = attotime(minute=1)
        self.assertEqual(result._native_time, datetime.time(minute=1))

        result = attotime(second=1)
        self.assertEqual(result._native_time, datetime.time(second=1))

        result = attotime(microsecond=1)
        self.assertEqual(result._native_time, datetime.time(microsecond=1))

    def test_init_type_check(self):
        with self.assertRaises(TypeError):
            attotime(hour=1.2)

        with self.assertRaises(TypeError):
            attotime(minute=1.2)

        with self.assertRaises(TypeError):
            attotime(second=1.2)

        with self.assertRaises(TypeError):
            attotime(microsecond=1.2)

        with self.assertRaises(TypeError):
            attotime(nanosecond="1.2")

    def test_init_range_check(self):
        with self.assertRaises(ValueError):
            attotime(nanosecond=-1)

        with self.assertRaises(ValueError):
            attotime(nanosecond=constants.NANOSECONDS_PER_MICROSECOND)

    def test_hour(self):
        t = attotime(hour=1)
        self.assertEqual(t.hour, 1)

    def test_minute(self):
        t = attotime(minute=2)
        self.assertEqual(t.minute, 2)

    def test_second(self):
        t = attotime(second=3)
        self.assertEqual(t.second, 3)

    def test_microsecond(self):
        t = attotime(microsecond=4)
        self.assertEqual(t.microsecond, 4)

    def test_nanosecond(self):
        t = attotime(nanosecond=5.678)
        self.assertEqual(t.nanosecond, 5.678)

    def test_tzinfo(self):
        t = attotime(tzinfo=FixedOffset(1, name="+1"))
        self.assertEqual(t.tzinfo, FixedOffset(1, name="+1"))
        self.assertIs(t.tzinfo, t._tzinfo)

    def test_replace(self):
        t = attotime(hour=1, minute=2, second=3, microsecond=4, nanosecond=5.678)
        result = t.replace(hour=2)

        self.assertEqual(
            result,
            attotime(hour=2, minute=2, second=3, microsecond=4, nanosecond=5.678),
        )
        self.assertIsNot(result, t)

        t = attotime(hour=1, minute=2, second=3, microsecond=4, nanosecond=5.678)
        result = t.replace(minute=3)

        self.assertEqual(
            result,
            attotime(hour=1, minute=3, second=3, microsecond=4, nanosecond=5.678),
        )
        self.assertIsNot(result, t)

        t = attotime(hour=1, minute=2, second=3, microsecond=4, nanosecond=5.678)
        result = t.replace(second=4)

        self.assertEqual(
            result,
            attotime(hour=1, minute=2, second=4, microsecond=4, nanosecond=5.678),
        )
        self.assertIsNot(result, t)

        t = attotime(hour=1, minute=2, second=3, microsecond=4, nanosecond=5.678)
        result = t.replace(microsecond=5)

        self.assertEqual(
            result,
            attotime(hour=1, minute=2, second=3, microsecond=5, nanosecond=5.678),
        )
        self.assertIsNot(result, t)

        t = attotime(hour=1, minute=2, second=3, microsecond=4, nanosecond=5.678)
        result = t.replace(nanosecond=6.789)

        self.assertEqual(
            result,
            attotime(hour=1, minute=2, second=3, microsecond=4, nanosecond=6.789),
        )
        self.assertIsNot(result, t)

        t = attotime(hour=1, minute=2, second=3, microsecond=4, nanosecond=5.678)
        result = t.replace(tzinfo=FixedOffset(1, name="+1"))

        self.assertEqual(
            result,
            attotime(
                hour=1,
                minute=2,
                second=3,
                microsecond=4,
                nanosecond=5.678,
                tzinfo=FixedOffset(1, name="+1"),
            ),
        )
        self.assertIsNot(result, t)

        t = attotime(
            hour=1,
            minute=2,
            second=3,
            microsecond=4,
            nanosecond=5.678,
            tzinfo=FixedOffset(1, name="+1"),
        )
        result = t.replace(tzinfo=None)

        self.assertEqual(
            result,
            attotime(hour=1, minute=2, second=3, microsecond=4, nanosecond=5.678),
        )
        self.assertIsNot(result, t)

    def test_isoformat(self):
        self.assertEqual(attotime(hour=1).isoformat(), "01:00:00")
        self.assertEqual(attotime(hour=1, minute=2).isoformat(), "01:02:00")
        self.assertEqual(attotime(hour=1, minute=2, second=3).isoformat(), "01:02:03")
        self.assertEqual(attotime(hour=1, minute=2, second=34).isoformat(), "01:02:34")
        self.assertEqual(
            attotime(hour=1, minute=2, second=3, microsecond=4).isoformat(),
            "01:02:03.000004",
        )
        self.assertEqual(
            attotime(
                hour=1, minute=2, second=3, microsecond=4, nanosecond=6
            ).isoformat(),
            "01:02:03.000004006",
        )
        self.assertEqual(
            attotime(
                hour=1, minute=2, second=3, microsecond=4, nanosecond=Decimal("0.006")
            ).isoformat(),
            "01:02:03.000004000006",
        )
        self.assertEqual(
            attotime(
                hour=1,
                minute=2,
                second=3,
                microsecond=4,
                nanosecond=Decimal("0.006"),
                tzinfo=FixedOffset(1, name="+1"),
            ).isoformat(),
            "01:02:03.000004000006+01:00",
        )
        self.assertEqual(
            attotime(
                hour=1,
                minute=2,
                second=3,
                microsecond=4,
                nanosecond=Decimal("0.006"),
                tzinfo=FixedOffset(-1, name="-1"),
            ).isoformat(),
            "01:02:03.000004000006-01:00",
        )
        self.assertEqual(
            attotime(
                hour=1,
                minute=2,
                second=3,
                microsecond=4,
                nanosecond=Decimal("0.006"),
                tzinfo=FixedOffset(0.025, name="0.025"),
            ).isoformat(),
            "01:02:03.000004000006+00:01:30",
        )

    def test_strftime(self):
        self.assertEqual(attotime().strftime("%w"), "1")
        self.assertEqual(attotime().strftime("%d"), "01")
        self.assertEqual(attotime().strftime("%m"), "01")
        self.assertEqual(attotime().strftime("%y"), "00")
        self.assertEqual(attotime().strftime("%Y"), "1900")
        self.assertEqual(attotime().strftime("%j"), "001")
        self.assertEqual(attotime().strftime("%U"), "00")
        self.assertEqual(attotime().strftime("%W"), "01")

        self.assertEqual(
            attotime(hour=14, minute=25, second=36, microsecond=789123).strftime("%H"),
            "14",
        )
        self.assertEqual(
            attotime(hour=14, minute=25, second=36, microsecond=789123).strftime("%I"),
            "02",
        )
        self.assertEqual(
            attotime(hour=14, minute=25, second=36, microsecond=789123).strftime("%M"),
            "25",
        )
        self.assertEqual(
            attotime(hour=14, minute=25, second=36, microsecond=789123).strftime("%S"),
            "36",
        )
        self.assertEqual(
            attotime(hour=14, minute=25, second=36, microsecond=789123).strftime("%f"),
            "789123",
        )
        self.assertEqual(
            attotime(hour=14, minute=25, second=36, microsecond=789123).strftime("%z"),
            "",
        )
        self.assertEqual(
            attotime(hour=14, minute=25, second=36, microsecond=789123).strftime("%Z"),
            "",
        )
        self.assertEqual(
            attotime(hour=14, minute=25, second=36, microsecond=789123).strftime("%%"),
            "%",
        )

        self.assertEqual(
            attotime(nanosecond=Decimal("0.0001")).strftime("%o"), "000000"
        )
        self.assertEqual(attotime(nanosecond=Decimal("0.001")).strftime("%o"), "000001")
        self.assertEqual(attotime(nanosecond=Decimal("0.01")).strftime("%o"), "000010")
        self.assertEqual(attotime(nanosecond=Decimal("0.1")).strftime("%o"), "000100")
        self.assertEqual(attotime(nanosecond=1).strftime("%o"), "001000")
        self.assertEqual(attotime(nanosecond=10).strftime("%o"), "010000")
        self.assertEqual(attotime(nanosecond=100).strftime("%o"), "100000")

        self.assertEqual(
            attotime(nanosecond=Decimal("0.0000000001")).strftime("%q"), "000000"
        )
        self.assertEqual(
            attotime(nanosecond=Decimal("0.000000001")).strftime("%q"), "000001"
        )
        self.assertEqual(
            attotime(nanosecond=Decimal("0.00000001")).strftime("%q"), "000010"
        )
        self.assertEqual(
            attotime(nanosecond=Decimal("0.0000001")).strftime("%q"), "000100"
        )
        self.assertEqual(
            attotime(nanosecond=Decimal("0.000001")).strftime("%q"), "001000"
        )
        self.assertEqual(
            attotime(nanosecond=Decimal("0.00001")).strftime("%q"), "010000"
        )
        self.assertEqual(
            attotime(nanosecond=Decimal("0.0001")).strftime("%q"), "100000"
        )

        self.assertEqual(
            attotime(nanosecond=Decimal("0.0000000000000001")).strftime("%v"), "000000"
        )
        self.assertEqual(
            attotime(nanosecond=Decimal("0.000000000000001")).strftime("%v"), "000001"
        )
        self.assertEqual(
            attotime(nanosecond=Decimal("0.00000000000001")).strftime("%v"), "000010"
        )
        self.assertEqual(
            attotime(nanosecond=Decimal("0.0000000000001")).strftime("%v"), "000100"
        )
        self.assertEqual(
            attotime(nanosecond=Decimal("0.000000000001")).strftime("%v"), "001000"
        )
        self.assertEqual(
            attotime(nanosecond=Decimal("0.00000000001")).strftime("%v"), "010000"
        )
        self.assertEqual(
            attotime(nanosecond=Decimal("0.0000000001")).strftime("%v"), "100000"
        )

        # Note truncation of sub-yoctosecond precision
        self.assertEqual(
            attotime(
                second=12,
                microsecond=345678,
                nanosecond=Decimal("912.3456789123456789"),
            ).strftime("%S.%f%o%q%v"),
            "12.345678912345678912345678",
        )

        # Timezone tests
        self.assertEqual(
            attotime(tzinfo=DSTOffset(1, name="+1")).strftime("%z"), "+0100"
        )
        self.assertEqual(
            attotime(tzinfo=DSTOffset(10, name="+10")).strftime("%z"), "+1000"
        )
        self.assertEqual(attotime(tzinfo=DSTOffset(1, name="+1")).strftime("%Z"), "+1")

        self.assertEqual(
            attotime(tzinfo=DSTOffset(-1, name="-1")).strftime("%z"), "-0100"
        )
        self.assertEqual(
            attotime(tzinfo=DSTOffset(-10, name="-10")).strftime("%z"), "-1000"
        )
        self.assertEqual(attotime(tzinfo=DSTOffset(-1, name="-1")).strftime("%Z"), "-1")

        # Locale specific
        self.assertEqual(attotime().strftime("%a"), datetime.time().strftime("%a"))
        self.assertEqual(attotime().strftime("%A"), datetime.time().strftime("%A"))
        self.assertEqual(attotime().strftime("%b"), datetime.time().strftime("%b"))
        self.assertEqual(attotime().strftime("%B"), datetime.time().strftime("%B"))
        self.assertEqual(
            attotime(hour=14, minute=25, second=36, microsecond=789123).strftime("%p"),
            datetime.time(hour=14, minute=25, second=36, microsecond=789123).strftime(
                "%p"
            ),
        )
        self.assertEqual(
            attotime(hour=14, minute=25, second=36, microsecond=789123).strftime("%c"),
            datetime.time(hour=14, minute=25, second=36, microsecond=789123).strftime(
                "%c"
            ),
        )
        self.assertEqual(
            attotime(hour=14, minute=25, second=36, microsecond=789123).strftime("%x"),
            datetime.time(hour=14, minute=25, second=36, microsecond=789123).strftime(
                "%x"
            ),
        )
        self.assertEqual(
            attotime(hour=14, minute=25, second=36, microsecond=789123).strftime("%X"),
            datetime.time(hour=14, minute=25, second=36, microsecond=789123).strftime(
                "%X"
            ),
        )

    def test_utcoffset(self):
        t = attotime()
        self.assertIsNone(t.utcoffset())

        t = attotime(tzinfo=FixedOffset(1, name="+1"))
        self.assertEqual(t.utcoffset(), datetime.timedelta(hours=1))

        t = attotime(tzinfo=FixedOffset(-1, name="-1"))
        self.assertEqual(t.utcoffset(), datetime.timedelta(hours=-1))

    def test_dst(self):
        t = attotime()
        self.assertIsNone(t.dst())

        # DSTOffset is 0 when no datetime is provided
        t = attotime(tzinfo=DSTOffset(1, name="+1"))
        self.assertEqual(t.dst(), datetime.timedelta(hours=0))

        t = attotime(tzinfo=DSTOffset(-1, name="-1"))
        self.assertEqual(t.dst(), datetime.timedelta(hours=0))

    def test_tzname(self):
        t = attotime()
        self.assertIsNone(t.tzname())

        t = attotime(tzinfo=FixedOffset(1, name="+1"))
        self.assertEqual(t.tzname(), "+1")

    def test_eq(self):
        self.assertTrue(attotime(hour=1) == attotime(hour=1))
        self.assertTrue(attotime(minute=1) == attotime(minute=1))
        self.assertTrue(attotime(second=1) == attotime(second=1))
        self.assertTrue(attotime(microsecond=1) == attotime(microsecond=1))
        self.assertTrue(attotime(nanosecond=1) == attotime(nanosecond=1))

        self.assertTrue(
            attotime(hour=2, tzinfo=FixedOffset(1, name="+1"))
            == attotime(hour=3, tzinfo=FixedOffset(2, name="+2"))
        )
        self.assertTrue(
            attotime(hour=2, nanosecond=1, tzinfo=FixedOffset(1, name="+1"))
            == attotime(hour=3, nanosecond=1, tzinfo=FixedOffset(2, name="+2"))
        )

        # Not equals
        self.assertFalse(attotime(hour=1) == attotime(hour=2))
        self.assertFalse(attotime(minute=3) == attotime(minute=4))
        self.assertFalse(attotime(second=5) == attotime(second=6))
        self.assertFalse(attotime(microsecond=7) == attotime(microsecond=8))
        self.assertFalse(attotime(nanosecond=9) == attotime(nanosecond=10))

        self.assertFalse(
            attotime(hour=1, tzinfo=FixedOffset(1, name="+1"))
            == attotime(hour=1, tzinfo=FixedOffset(2, name="+2"))
        )
        self.assertFalse(
            attotime(hour=1, nanosecond=1, tzinfo=FixedOffset(1, name="+1"))
            == attotime(hour=1, nanosecond=1, tzinfo=FixedOffset(2, name="+2"))
        )

        self.assertFalse(attotime(hour=1) == datetime.time(hour=1))

        with self.assertRaises(TypeError):
            attotime(nanosecond=1, tzinfo=FixedOffset(1, name="+1")) == attotime(
                nanosecond=1
            )

    def test_ne(self):
        # Inverse of test_eq
        self.assertFalse(attotime(hour=1) != attotime(hour=1))
        self.assertFalse(attotime(minute=1) != attotime(minute=1))
        self.assertFalse(attotime(second=1) != attotime(second=1))
        self.assertFalse(attotime(microsecond=1) != attotime(microsecond=1))
        self.assertFalse(attotime(nanosecond=1) != attotime(nanosecond=1))

        self.assertFalse(
            attotime(hour=2, tzinfo=FixedOffset(1, name="+1"))
            != attotime(hour=3, tzinfo=FixedOffset(2, name="+2"))
        )
        self.assertFalse(
            attotime(hour=2, nanosecond=1, tzinfo=FixedOffset(1, name="+1"))
            != attotime(hour=3, nanosecond=1, tzinfo=FixedOffset(2, name="+2"))
        )

        # Not equals
        self.assertTrue(attotime(hour=1) != attotime(hour=2))
        self.assertTrue(attotime(minute=3) != attotime(minute=4))
        self.assertTrue(attotime(second=5) != attotime(second=6))
        self.assertTrue(attotime(microsecond=7) != attotime(microsecond=8))
        self.assertTrue(attotime(nanosecond=9) != attotime(nanosecond=10))

        self.assertTrue(
            attotime(hour=1, tzinfo=FixedOffset(1, name="+1"))
            != attotime(hour=1, tzinfo=FixedOffset(2, name="+2"))
        )
        self.assertTrue(
            attotime(hour=1, nanosecond=1, tzinfo=FixedOffset(1, name="+1"))
            != attotime(hour=1, nanosecond=1, tzinfo=FixedOffset(2, name="+2"))
        )

        with self.assertRaises(TypeError):
            attotime(nanosecond=1, tzinfo=FixedOffset(1, name="+1")) != attotime(
                nanosecond=1
            )

    def test_gt(self):
        self.assertTrue(attotime(hour=2) > attotime(hour=1))
        self.assertTrue(attotime(minute=2) > attotime(minute=1))
        self.assertTrue(attotime(second=2) > attotime(second=1))
        self.assertTrue(attotime(microsecond=2) > attotime(microsecond=1))
        self.assertTrue(attotime(nanosecond=2) > attotime(nanosecond=1))
        self.assertTrue(attotime(hour=2, nanosecond=1) > attotime(hour=2))
        self.assertTrue(attotime(hour=3) > attotime(hour=2, nanosecond=1))

        self.assertTrue(
            attotime(hour=3, tzinfo=FixedOffset(1, name="+1"))
            > attotime(hour=3, tzinfo=FixedOffset(2, name="+2"))
        )
        self.assertTrue(
            attotime(hour=3, nanosecond=1, tzinfo=FixedOffset(1, name="+1"))
            > attotime(hour=3, nanosecond=1, tzinfo=FixedOffset(2, name="+2"))
        )

        # Equals
        self.assertFalse(attotime(hour=1) > attotime(hour=1))
        self.assertFalse(attotime(minute=1) > attotime(minute=1))
        self.assertFalse(attotime(second=1) > attotime(second=1))
        self.assertFalse(attotime(microsecond=1) > attotime(microsecond=1))
        self.assertFalse(attotime(nanosecond=1) > attotime(nanosecond=1))

        self.assertFalse(
            attotime(hour=2, tzinfo=FixedOffset(1, name="+1"))
            > attotime(hour=3, tzinfo=FixedOffset(2, name="+2"))
        )
        self.assertFalse(
            attotime(hour=2, nanosecond=1, tzinfo=FixedOffset(1, name="+1"))
            > attotime(hour=3, nanosecond=1, tzinfo=FixedOffset(2, name="+2"))
        )

        # Not greaters
        self.assertFalse(attotime(hour=2) > attotime(hour=3))
        self.assertFalse(attotime(minute=2) > attotime(minute=3))
        self.assertFalse(attotime(second=2) > attotime(second=3))
        self.assertFalse(attotime(microsecond=2) > attotime(microsecond=3))
        self.assertFalse(attotime(nanosecond=2) > attotime(nanosecond=3))
        self.assertFalse(attotime(hour=2, nanosecond=1) > attotime(hour=3))
        self.assertFalse(attotime(hour=2) > attotime(hour=3, nanosecond=1))

        self.assertFalse(
            attotime(hour=1, tzinfo=FixedOffset(1, name="+1"))
            > attotime(hour=3, tzinfo=FixedOffset(2, name="+2"))
        )
        self.assertFalse(
            attotime(hour=1, nanosecond=1, tzinfo=FixedOffset(1, name="+1"))
            > attotime(hour=3, nanosecond=1, tzinfo=FixedOffset(2, name="+2"))
        )

        with self.assertRaises(TypeError):
            attotime(nanosecond=1, tzinfo=FixedOffset(1, name="+1")) > attotime(
                nanosecond=1
            )

        with self.assertRaises(TypeError):
            attotime(nanosecond=1) > 1

    def test_ge(self):
        self.assertTrue(attotime(hour=2) >= attotime(hour=1))
        self.assertTrue(attotime(minute=2) >= attotime(minute=1))
        self.assertTrue(attotime(second=2) >= attotime(second=1))
        self.assertTrue(attotime(microsecond=2) >= attotime(microsecond=1))
        self.assertTrue(attotime(nanosecond=2) >= attotime(nanosecond=1))
        self.assertTrue(attotime(hour=2, nanosecond=1) >= attotime(hour=2))
        self.assertTrue(attotime(hour=3) >= attotime(hour=2, nanosecond=1))

        self.assertTrue(
            attotime(hour=3, tzinfo=FixedOffset(1, name="+1"))
            >= attotime(hour=3, tzinfo=FixedOffset(2, name="+2"))
        )
        self.assertTrue(
            attotime(hour=3, nanosecond=1, tzinfo=FixedOffset(1, name="+1"))
            >= attotime(hour=3, nanosecond=1, tzinfo=FixedOffset(2, name="+2"))
        )

        # Equals
        self.assertTrue(attotime(hour=1) >= attotime(hour=1))
        self.assertTrue(attotime(minute=1) >= attotime(minute=1))
        self.assertTrue(attotime(second=1) >= attotime(second=1))
        self.assertTrue(attotime(microsecond=1) >= attotime(microsecond=1))
        self.assertTrue(attotime(nanosecond=1) >= attotime(nanosecond=1))

        self.assertTrue(
            attotime(hour=2, tzinfo=FixedOffset(1, name="+1"))
            >= attotime(hour=3, tzinfo=FixedOffset(2, name="+2"))
        )
        self.assertTrue(
            attotime(hour=2, nanosecond=1, tzinfo=FixedOffset(1, name="+1"))
            >= attotime(hour=3, nanosecond=1, tzinfo=FixedOffset(2, name="+2"))
        )

        # Not greaters
        self.assertFalse(attotime(hour=2) >= attotime(hour=3))
        self.assertFalse(attotime(minute=2) >= attotime(minute=3))
        self.assertFalse(attotime(second=2) >= attotime(second=3))
        self.assertFalse(attotime(microsecond=2) >= attotime(microsecond=3))
        self.assertFalse(attotime(nanosecond=2) >= attotime(nanosecond=3))
        self.assertFalse(attotime(hour=2, nanosecond=1) >= attotime(hour=3))
        self.assertFalse(attotime(hour=2) >= attotime(hour=3, nanosecond=1))

        self.assertFalse(
            attotime(hour=1, tzinfo=FixedOffset(1, name="+1"))
            >= attotime(hour=3, tzinfo=FixedOffset(2, name="+2"))
        )
        self.assertFalse(
            attotime(hour=1, nanosecond=1, tzinfo=FixedOffset(1, name="+1"))
            >= attotime(hour=3, nanosecond=1, tzinfo=FixedOffset(2, name="+2"))
        )

        with self.assertRaises(TypeError):
            attotime(nanosecond=1, tzinfo=FixedOffset(1, name="+1")) >= attotime(
                nanosecond=1
            )

        with self.assertRaises(TypeError):
            attotime(nanosecond=1) >= 1

    def test_lt(self):
        self.assertTrue(attotime(hour=2) < attotime(hour=3))
        self.assertTrue(attotime(minute=2) < attotime(minute=3))
        self.assertTrue(attotime(second=2) < attotime(second=3))
        self.assertTrue(attotime(microsecond=2) < attotime(microsecond=3))
        self.assertTrue(attotime(nanosecond=2) < attotime(nanosecond=3))
        self.assertTrue(attotime(hour=2, nanosecond=1) < attotime(hour=3))
        self.assertTrue(attotime(hour=2) < attotime(hour=3, nanosecond=1))

        self.assertTrue(
            attotime(hour=1, tzinfo=FixedOffset(1, name="+1"))
            < attotime(hour=3, tzinfo=FixedOffset(2, name="+2"))
        )
        self.assertTrue(
            attotime(hour=1, nanosecond=1, tzinfo=FixedOffset(1, name="+1"))
            < attotime(hour=3, nanosecond=1, tzinfo=FixedOffset(2, name="+2"))
        )

        # Equals
        self.assertFalse(attotime(hour=1) < attotime(hour=1))
        self.assertFalse(attotime(minute=1) < attotime(minute=1))
        self.assertFalse(attotime(second=1) < attotime(second=1))
        self.assertFalse(attotime(microsecond=1) < attotime(microsecond=1))
        self.assertFalse(attotime(nanosecond=1) < attotime(nanosecond=1))

        self.assertFalse(
            attotime(hour=2, tzinfo=FixedOffset(1, name="+1"))
            < attotime(hour=3, tzinfo=FixedOffset(2, name="+2"))
        )
        self.assertFalse(
            attotime(hour=2, nanosecond=1, tzinfo=FixedOffset(1, name="+1"))
            < attotime(hour=3, nanosecond=1, tzinfo=FixedOffset(2, name="+2"))
        )

        # Not lessers
        self.assertFalse(attotime(hour=2) < attotime(hour=1))
        self.assertFalse(attotime(minute=2) < attotime(minute=1))
        self.assertFalse(attotime(second=2) < attotime(second=1))
        self.assertFalse(attotime(microsecond=2) < attotime(microsecond=1))
        self.assertFalse(attotime(nanosecond=2) < attotime(nanosecond=1))
        self.assertFalse(attotime(hour=2, nanosecond=1) < attotime(hour=1))
        self.assertFalse(attotime(hour=2) < attotime(hour=1, nanosecond=1))

        self.assertFalse(
            attotime(hour=3, tzinfo=FixedOffset(1, name="+1"))
            < attotime(hour=3, tzinfo=FixedOffset(2, name="+2"))
        )
        self.assertFalse(
            attotime(hour=3, nanosecond=1, tzinfo=FixedOffset(1, name="+1"))
            < attotime(hour=3, nanosecond=1, tzinfo=FixedOffset(2, name="+2"))
        )

        with self.assertRaises(TypeError):
            attotime(nanosecond=1, tzinfo=FixedOffset(1, name="+1")) < attotime(
                nanosecond=1
            )

        with self.assertRaises(TypeError):
            attotime(nanosecond=1) < 1

    def test_le(self):
        self.assertTrue(attotime(hour=2) <= attotime(hour=3))
        self.assertTrue(attotime(minute=2) <= attotime(minute=3))
        self.assertTrue(attotime(second=2) <= attotime(second=3))
        self.assertTrue(attotime(microsecond=2) <= attotime(microsecond=3))
        self.assertTrue(attotime(nanosecond=2) <= attotime(nanosecond=3))
        self.assertTrue(attotime(hour=2, nanosecond=1) <= attotime(hour=3))
        self.assertTrue(attotime(hour=2) <= attotime(hour=3, nanosecond=1))

        self.assertTrue(
            attotime(hour=1, tzinfo=FixedOffset(1, name="+1"))
            <= attotime(hour=3, tzinfo=FixedOffset(2, name="+2"))
        )
        self.assertTrue(
            attotime(hour=1, nanosecond=1, tzinfo=FixedOffset(1, name="+1"))
            <= attotime(hour=3, nanosecond=1, tzinfo=FixedOffset(2, name="+2"))
        )

        # Equals
        self.assertTrue(attotime(hour=1) <= attotime(hour=1))
        self.assertTrue(attotime(minute=1) <= attotime(minute=1))
        self.assertTrue(attotime(second=1) <= attotime(second=1))
        self.assertTrue(attotime(microsecond=1) <= attotime(microsecond=1))
        self.assertTrue(attotime(nanosecond=1) <= attotime(nanosecond=1))

        self.assertTrue(
            attotime(hour=2, tzinfo=FixedOffset(1, name="+1"))
            <= attotime(hour=3, tzinfo=FixedOffset(2, name="+2"))
        )
        self.assertTrue(
            attotime(hour=2, nanosecond=1, tzinfo=FixedOffset(1, name="+1"))
            <= attotime(hour=3, nanosecond=1, tzinfo=FixedOffset(2, name="+2"))
        )

        # Not lessers
        self.assertFalse(attotime(hour=2) <= attotime(hour=1))
        self.assertFalse(attotime(minute=2) <= attotime(minute=1))
        self.assertFalse(attotime(second=2) <= attotime(second=1))
        self.assertFalse(attotime(microsecond=2) <= attotime(microsecond=1))
        self.assertFalse(attotime(nanosecond=2) <= attotime(nanosecond=1))
        self.assertFalse(attotime(hour=2, nanosecond=1) <= attotime(hour=1))
        self.assertFalse(attotime(hour=2) <= attotime(hour=1, nanosecond=1))

        self.assertFalse(
            attotime(hour=3, tzinfo=FixedOffset(1, name="+1"))
            <= attotime(hour=3, tzinfo=FixedOffset(2, name="+2"))
        )
        self.assertFalse(
            attotime(hour=3, nanosecond=1, tzinfo=FixedOffset(1, name="+1"))
            <= attotime(hour=3, nanosecond=1, tzinfo=FixedOffset(2, name="+2"))
        )

        with self.assertRaises(TypeError):
            attotime(nanosecond=1, tzinfo=FixedOffset(1, name="+1")) <= attotime(
                nanosecond=1
            )

        with self.assertRaises(TypeError):
            attotime(nanosecond=1) <= 1

    def test_str(self):
        self.assertEqual(str(attotime(hour=1)), "01:00:00")
        self.assertEqual(str(attotime(hour=1, minute=2)), "01:02:00")
        self.assertEqual(str(attotime(hour=1, minute=2, second=3)), "01:02:03")
        self.assertEqual(
            str(attotime(hour=1, minute=2, second=3, microsecond=4)), "01:02:03.000004"
        )
        self.assertEqual(
            str(attotime(hour=1, minute=2, second=3, microsecond=4, nanosecond=6)),
            "01:02:03.000004006",
        )
        self.assertEqual(
            str(
                attotime(
                    hour=1,
                    minute=2,
                    second=3,
                    microsecond=4,
                    nanosecond=Decimal("0.006"),
                )
            ),
            "01:02:03.000004000006",
        )
        self.assertEqual(
            str(
                attotime(
                    hour=1,
                    minute=2,
                    second=3,
                    microsecond=4,
                    nanosecond=Decimal("0.006"),
                    tzinfo=FixedOffset(1, name="+1"),
                )
            ),
            "01:02:03.000004000006+01:00",
        )
        self.assertEqual(
            str(
                attotime(
                    hour=1,
                    minute=2,
                    second=3,
                    microsecond=4,
                    nanosecond=Decimal("0.006"),
                    tzinfo=FixedOffset(-1, name="-1"),
                )
            ),
            "01:02:03.000004000006-01:00",
        )

    def test_repr(self):
        self.assertEqual(
            attotime(hour=1).__repr__(), "attotime.objects.attotime(1, 0, 0, 0, 0)"
        )
        self.assertEqual(
            attotime(hour=1, minute=2).__repr__(),
            "attotime.objects.attotime(1, 2, 0, 0, 0)",
        )
        self.assertEqual(
            attotime(hour=1, minute=2, second=3).__repr__(),
            "attotime.objects.attotime(1, 2, 3, 0, 0)",
        )
        self.assertEqual(
            attotime(hour=1, minute=2, second=3, microsecond=4).__repr__(),
            "attotime.objects.attotime(1, 2, 3, 4, 0)",
        )
        self.assertEqual(
            attotime(
                hour=1, minute=2, second=3, microsecond=4, nanosecond=6
            ).__repr__(),
            "attotime.objects.attotime(1, 2, 3, 4, 6)",
        )
        self.assertEqual(
            attotime(
                hour=1, minute=2, second=3, microsecond=4, nanosecond=Decimal("0.006")
            ).__repr__(),
            "attotime.objects.attotime(1, 2, 3, 4, 0.006)",
        )
        self.assertEqual(
            attotime(
                hour=1,
                minute=2,
                second=3,
                microsecond=4,
                nanosecond=Decimal("0.006"),
                tzinfo=FixedOffset(1, name="+1"),
            ).__repr__(),
            "attotime.objects.attotime(1, 2, 3, 4, 0.006, +1)",
        )
        self.assertEqual(
            attotime(
                hour=1,
                minute=2,
                second=3,
                microsecond=4,
                nanosecond=Decimal("0.006"),
                tzinfo=FixedOffset(-1, name="-1"),
            ).__repr__(),
            "attotime.objects.attotime(1, 2, 3, 4, 0.006, -1)",
        )

    def test_format(self):
        self.assertEqual("{0:%w}".format(attotime()), "1")
        self.assertEqual("{0:%d}".format(attotime()), "01")
        self.assertEqual("{0:%m}".format(attotime()), "01")
        self.assertEqual("{0:%y}".format(attotime()), "00")
        self.assertEqual("{0:%Y}".format(attotime()), "1900")
        self.assertEqual("{0:%j}".format(attotime()), "001")
        self.assertEqual("{0:%U}".format(attotime()), "00")
        self.assertEqual("{0:%W}".format(attotime()), "01")

        self.assertEqual(
            "{0:%H}".format(
                attotime(hour=14, minute=25, second=36, microsecond=789123)
            ),
            "14",
        )
        self.assertEqual(
            "{0:%I}".format(
                attotime(hour=14, minute=25, second=36, microsecond=789123)
            ),
            "02",
        )
        self.assertEqual(
            "{0:%M}".format(
                attotime(hour=14, minute=25, second=36, microsecond=789123)
            ),
            "25",
        )
        self.assertEqual(
            "{0:%S}".format(
                attotime(hour=14, minute=25, second=36, microsecond=789123)
            ),
            "36",
        )
        self.assertEqual(
            "{0:%f}".format(
                attotime(hour=14, minute=25, second=36, microsecond=789123)
            ),
            "789123",
        )
        self.assertEqual(
            "{0:%z}".format(
                attotime(hour=14, minute=25, second=36, microsecond=789123)
            ),
            "",
        )
        self.assertEqual(
            "{0:%Z}".format(
                attotime(hour=14, minute=25, second=36, microsecond=789123)
            ),
            "",
        )
        self.assertEqual(
            "{0:%%}".format(
                attotime(hour=14, minute=25, second=36, microsecond=789123)
            ),
            "%",
        )

        self.assertEqual(
            "{0:%o}".format(attotime(nanosecond=Decimal("0.0001"))), "000000"
        )
        self.assertEqual(
            "{0:%o}".format(attotime(nanosecond=Decimal("0.001"))), "000001"
        )
        self.assertEqual(
            "{0:%o}".format(attotime(nanosecond=Decimal("0.01"))), "000010"
        )
        self.assertEqual("{0:%o}".format(attotime(nanosecond=Decimal("0.1"))), "000100")
        self.assertEqual("{0:%o}".format(attotime(nanosecond=1)), "001000")
        self.assertEqual("{0:%o}".format(attotime(nanosecond=10)), "010000")
        self.assertEqual("{0:%o}".format(attotime(nanosecond=100)), "100000")

        self.assertEqual(
            "{0:%q}".format(attotime(nanosecond=Decimal("0.0000000001"))), "000000"
        )
        self.assertEqual(
            "{0:%q}".format(attotime(nanosecond=Decimal("0.000000001"))), "000001"
        )
        self.assertEqual(
            "{0:%q}".format(attotime(nanosecond=Decimal("0.00000001"))), "000010"
        )
        self.assertEqual(
            "{0:%q}".format(attotime(nanosecond=Decimal("0.0000001"))), "000100"
        )
        self.assertEqual(
            "{0:%q}".format(attotime(nanosecond=Decimal("0.000001"))), "001000"
        )
        self.assertEqual(
            "{0:%q}".format(attotime(nanosecond=Decimal("0.00001"))), "010000"
        )
        self.assertEqual(
            "{0:%q}".format(attotime(nanosecond=Decimal("0.0001"))), "100000"
        )

        self.assertEqual(
            "{0:%v}".format(attotime(nanosecond=Decimal("0.0000000000000001"))),
            "000000",
        )
        self.assertEqual(
            "{0:%v}".format(attotime(nanosecond=Decimal("0.000000000000001"))), "000001"
        )
        self.assertEqual(
            "{0:%v}".format(attotime(nanosecond=Decimal("0.00000000000001"))), "000010"
        )
        self.assertEqual(
            "{0:%v}".format(attotime(nanosecond=Decimal("0.0000000000001"))), "000100"
        )
        self.assertEqual(
            "{0:%v}".format(attotime(nanosecond=Decimal("0.000000000001"))), "001000"
        )
        self.assertEqual(
            "{0:%v}".format(attotime(nanosecond=Decimal("0.00000000001"))), "010000"
        )
        self.assertEqual(
            "{0:%v}".format(attotime(nanosecond=Decimal("0.0000000001"))), "100000"
        )

        # Note truncation of sub-yoctosecond precision
        self.assertEqual(
            "{0:%S.%f%o%q%v}".format(
                attotime(
                    second=12,
                    microsecond=345678,
                    nanosecond=Decimal("912.3456789123456789"),
                )
            ),
            "12.345678912345678912345678",
        )

        # Timezone tests
        self.assertEqual(
            "{0:%z}".format(attotime(tzinfo=DSTOffset(1, name="+1"))), "+0100"
        )
        self.assertEqual(
            "{0:%z}".format(attotime(tzinfo=DSTOffset(10, name="+10"))), "+1000"
        )
        self.assertEqual(
            "{0:%Z}".format(attotime(tzinfo=DSTOffset(1, name="+1"))), "+1"
        )

        self.assertEqual(
            "{0:%z}".format(attotime(tzinfo=DSTOffset(-1, name="-1"))), "-0100"
        )
        self.assertEqual(
            "{0:%z}".format(attotime(tzinfo=DSTOffset(-10, name="-10"))), "-1000"
        )
        self.assertEqual(
            "{0:%Z}".format(attotime(tzinfo=DSTOffset(-1, name="-1"))), "-1"
        )

        # Locale specific
        self.assertEqual("{0:%a}".format(attotime()), datetime.time().strftime("%a"))
        self.assertEqual("{0:%A}".format(attotime()), datetime.time().strftime("%A"))
        self.assertEqual("{0:%b}".format(attotime()), datetime.time().strftime("%b"))
        self.assertEqual("{0:%B}".format(attotime()), datetime.time().strftime("%B"))
        self.assertEqual(
            "{0:%p}".format(
                attotime(hour=14, minute=25, second=36, microsecond=789123)
            ),
            datetime.time(hour=14, minute=25, second=36, microsecond=789123).strftime(
                "%p"
            ),
        )
        self.assertEqual(
            "{0:%c}".format(
                attotime(hour=14, minute=25, second=36, microsecond=789123)
            ),
            datetime.time(hour=14, minute=25, second=36, microsecond=789123).strftime(
                "%c"
            ),
        )
        self.assertEqual(
            "{0:%x}".format(
                attotime(hour=14, minute=25, second=36, microsecond=789123)
            ),
            datetime.time(hour=14, minute=25, second=36, microsecond=789123).strftime(
                "%x"
            ),
        )
        self.assertEqual(
            "{0:%X}".format(
                attotime(hour=14, minute=25, second=36, microsecond=789123)
            ),
            datetime.time(hour=14, minute=25, second=36, microsecond=789123).strftime(
                "%X"
            ),
        )
