# -*- coding: utf-8 -*-

# Copyright (c) 2021, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import datetime
import time
import unittest
from decimal import Decimal, localcontext

from attotime import constants
from attotime.objects.attodatetime import attodatetime
from attotime.objects.attotime import attotime
from attotime.objects.attotimedelta import attotimedelta
from attotime.tests.common import DSTOffset, FixedOffset
from attotime.tests.compat import mock, utc


class TestAttoDateTimeFunctions(unittest.TestCase):
    def test_init(self):
        result = attodatetime(2001, 2, 3)

        self.assertEqual(result._native_date, datetime.date(2001, 2, 3))
        self.assertEqual(
            result._attotime,
            attotime(hour=0, minute=0, second=0, microsecond=0, nanosecond=0),
        )

        result = attodatetime(
            2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5
        )

        self.assertEqual(result._native_date, datetime.date(2001, 2, 3))
        self.assertEqual(
            result._attotime,
            attotime(hour=1, minute=2, second=3, microsecond=4, nanosecond=5),
        )

        result = attodatetime(
            2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5.6
        )

        self.assertEqual(result._native_date, datetime.date(2001, 2, 3))
        self.assertEqual(
            result._attotime,
            attotime(hour=1, minute=2, second=3, microsecond=4, nanosecond=5.6),
        )

        result = attodatetime(
            2001,
            2,
            3,
            hour=1,
            minute=2,
            second=3,
            microsecond=4,
            nanosecond=Decimal("5.67"),
        )

        self.assertEqual(result._native_date, datetime.date(2001, 2, 3))
        self.assertEqual(
            result._attotime,
            attotime(
                hour=1, minute=2, second=3, microsecond=4, nanosecond=Decimal("5.67")
            ),
        )

        result = attodatetime(
            2001,
            2,
            3,
            hour=1,
            minute=2,
            second=3,
            microsecond=4,
            nanosecond=5,
            tzinfo=FixedOffset(1, name="+1"),
        )

        self.assertEqual(result._native_date, datetime.date(2001, 2, 3))
        self.assertEqual(
            result._attotime,
            attotime(
                hour=1,
                minute=2,
                second=3,
                microsecond=4,
                nanosecond=5,
                tzinfo=FixedOffset(1, name="+1"),
            ),
        )

    def test_init_type_check(self):
        with self.assertRaises(TypeError):
            attodatetime(2001.5, 2, 3)

        with self.assertRaises(TypeError):
            attodatetime(2001, 2.5, 3)

        with self.assertRaises(TypeError):
            attodatetime(2001, 2, 3.5)

        with self.assertRaises(TypeError):
            attodatetime(2001, 2, 3, hour=4.5)

        with self.assertRaises(TypeError):
            attodatetime(2001, 2, 3, minute=4.5)

        with self.assertRaises(TypeError):
            attodatetime(2001, 2, 3, second=4.5)

        with self.assertRaises(TypeError):
            attodatetime(2001, 2, 3, microsecond=4.5)

    def test_year(self):
        dt = attodatetime(2006, 7, 8)
        self.assertEqual(dt.year, 2006)

    def test_month(self):
        dt = attodatetime(2006, 7, 8)
        self.assertEqual(dt.month, 7)

    def test_day(self):
        dt = attodatetime(2006, 7, 8)
        self.assertEqual(dt.day, 8)

    def test_hour(self):
        dt = attodatetime(2006, 7, 8, hour=9)
        self.assertEqual(dt.hour, 9)

    def test_minute(self):
        dt = attodatetime(2006, 7, 8, minute=10)
        self.assertEqual(dt.minute, 10)

    def test_second(self):
        dt = attodatetime(2006, 7, 8, second=11)
        self.assertEqual(dt.second, 11)

    def test_microsecond(self):
        dt = attodatetime(2006, 7, 8, microsecond=12)
        self.assertEqual(dt.microsecond, 12)

    def test_nanosecond(self):
        dt = attodatetime(2006, 7, 8, nanosecond=13.1415)
        self.assertEqual(dt.nanosecond, 13.1415)

    def test_tzinfo(self):
        dt = attodatetime(2006, 7, 8, tzinfo=FixedOffset(2, name="+2"))
        self.assertEqual(dt.tzinfo, FixedOffset(2, name="+2"))
        self.assertIs(dt.tzinfo, dt._attotime._tzinfo)

    @mock.patch("attotime.objects.attodatetime.attodatetime.fromtimestamp")
    @mock.patch("attotime.objects.attodatetime.time.time")
    def test_today(self, mockTime, mockFromTimestamp):
        result = attodatetime.today()

        self.assertEqual(result, mockFromTimestamp.return_value)

        mockTime.assert_called_once_with()
        mockFromTimestamp.assert_called_once_with(mockTime.return_value)

    @mock.patch("attotime.objects.attodatetime.attodatetime.today")
    @mock.patch("attotime.objects.attodatetime.attodatetime.fromtimestamp")
    @mock.patch("attotime.objects.attodatetime.time.time")
    def test_now(self, mockTime, mockFromTimestamp, mockToday):
        result = attodatetime.now()

        self.assertEqual(result, mockToday.return_value)

        mockToday.assert_called_once_with()

        dummyTZ = mock.Mock()

        result = attodatetime.now(tz=dummyTZ)

        self.assertEqual(result, mockFromTimestamp.return_value)

        mockTime.assert_called_once_with()
        mockFromTimestamp.assert_called_once_with(mockTime.return_value, dummyTZ)

    @mock.patch("attotime.objects.attodatetime.attodatetime.utcfromtimestamp")
    @mock.patch("attotime.objects.attodatetime.time.time")
    def test_utcnow(self, mockTime, mockUTCFromTimestamp):
        result = attodatetime.utcnow()

        self.assertEqual(result, mockUTCFromTimestamp.return_value)

        mockTime.assert_called_once_with()
        mockUTCFromTimestamp.assert_called_once_with(mockTime.return_value)

    @mock.patch("attotime.util.LocalTimezone._isdst")
    @mock.patch("attotime.util.time")
    @mock.patch("attotime.objects.attodatetime.time.gmtime")
    def test_fromtimestamp(self, mockObjectGMTime, mockUtilTime, mockIsDST):
        UNIX_EPOCH_STRUCT = time.struct_time((1970, 1, 1, 0, 0, 0, 3, 1, 0))

        mockIsDST.return_value = False
        mockUtilTime.daylight = False
        mockUtilTime.timezone = 0

        mockObjectGMTime.return_value = UNIX_EPOCH_STRUCT

        # Run tests assuming the Unix epoch
        dt = attodatetime.fromtimestamp(0)
        self.assertEqual(dt, attodatetime(1970, 1, 1))

        dt = attodatetime.fromtimestamp(1)
        self.assertEqual(dt, attodatetime(1970, 1, 1, second=1))

        dt = attodatetime.fromtimestamp(Decimal(1) / constants.NANOSECONDS_PER_SECOND)
        self.assertEqual(dt, attodatetime(1970, 1, 1, nanosecond=1))

        dt = attodatetime.fromtimestamp(
            Decimal("0.1") / constants.NANOSECONDS_PER_SECOND
        )
        self.assertEqual(
            dt,
            attodatetime(1970, 1, 1, nanosecond=Decimal("0.1")),
        )

        dt = attodatetime.fromtimestamp(Decimal(1) / constants.MICROSECONDS_PER_SECOND)
        self.assertEqual(dt, attodatetime(1970, 1, 1, microsecond=1))

        dt = attodatetime.fromtimestamp(constants.SECONDS_PER_MINUTE)
        self.assertEqual(dt, attodatetime(1970, 1, 1, minute=1))

        dt = attodatetime.fromtimestamp(constants.SECONDS_PER_HOUR)
        self.assertEqual(dt, attodatetime(1970, 1, 1, hour=1))

        dt = attodatetime.fromtimestamp(constants.SECONDS_PER_DAY)
        self.assertEqual(dt, attodatetime(1970, 1, 2))

        dt = attodatetime.fromtimestamp(constants.SECONDS_PER_DAY * 31)
        self.assertEqual(dt, attodatetime(1970, 2, 1))

        dt = attodatetime.fromtimestamp(constants.SECONDS_PER_DAY * 365)
        self.assertEqual(dt, attodatetime(1971, 1, 1))

        # Test with Python timezone
        utc_timezone = utc

        dt = attodatetime.fromtimestamp(0, tz=utc_timezone)
        self.assertEqual(dt, attodatetime(1970, 1, 1, tzinfo=utc_timezone))

        dt = attodatetime.fromtimestamp(1, tz=utc_timezone)
        self.assertEqual(dt, attodatetime(1970, 1, 1, second=1, tzinfo=utc_timezone))

        dt = attodatetime.fromtimestamp(
            Decimal(1) / constants.NANOSECONDS_PER_SECOND, tz=utc_timezone
        )
        self.assertEqual(
            dt, attodatetime(1970, 1, 1, nanosecond=1, tzinfo=utc_timezone)
        )

        dt = attodatetime.fromtimestamp(
            Decimal("0.1") / constants.NANOSECONDS_PER_SECOND, tz=utc_timezone
        )
        self.assertEqual(
            dt,
            attodatetime(1970, 1, 1, nanosecond=Decimal("0.1"), tzinfo=utc_timezone),
        )

        dt = attodatetime.fromtimestamp(
            Decimal(1) / constants.MICROSECONDS_PER_SECOND, tz=utc_timezone
        )
        self.assertEqual(
            dt, attodatetime(1970, 1, 1, microsecond=1, tzinfo=utc_timezone)
        )

        dt = attodatetime.fromtimestamp(constants.SECONDS_PER_MINUTE, tz=utc_timezone)
        self.assertEqual(dt, attodatetime(1970, 1, 1, minute=1, tzinfo=utc_timezone))

        dt = attodatetime.fromtimestamp(constants.SECONDS_PER_HOUR, tz=utc_timezone)
        self.assertEqual(dt, attodatetime(1970, 1, 1, hour=1, tzinfo=utc_timezone))

        dt = attodatetime.fromtimestamp(constants.SECONDS_PER_DAY, tz=utc_timezone)
        self.assertEqual(dt, attodatetime(1970, 1, 2, tzinfo=utc_timezone))

        dt = attodatetime.fromtimestamp(constants.SECONDS_PER_DAY * 31, tz=utc_timezone)
        self.assertEqual(dt, attodatetime(1970, 2, 1, tzinfo=utc_timezone))

        dt = attodatetime.fromtimestamp(
            constants.SECONDS_PER_DAY * 365, tz=utc_timezone
        )
        self.assertEqual(dt, attodatetime(1971, 1, 1, tzinfo=utc_timezone))

        # Test again with specific timezones
        fixed_timezone = FixedOffset(-6, name="-6")
        fixed_timezone_delta = attotimedelta(hours=-6)

        dt = attodatetime.fromtimestamp(0, tz=fixed_timezone)
        self.assertEqual(
            dt,
            attodatetime(1970, 1, 1, tzinfo=fixed_timezone) + fixed_timezone_delta,
        )

        dt = attodatetime.fromtimestamp(1, tz=fixed_timezone)
        self.assertEqual(
            dt,
            attodatetime(1970, 1, 1, second=1, tzinfo=fixed_timezone)
            + fixed_timezone_delta,
        )

        dt = attodatetime.fromtimestamp(
            Decimal(1) / constants.NANOSECONDS_PER_SECOND, tz=fixed_timezone
        )
        self.assertEqual(
            dt,
            attodatetime(1970, 1, 1, nanosecond=1, tzinfo=fixed_timezone)
            + fixed_timezone_delta,
        )

        dt = attodatetime.fromtimestamp(
            Decimal("0.1") / constants.NANOSECONDS_PER_SECOND, tz=fixed_timezone
        )
        self.assertEqual(
            dt,
            attodatetime(1970, 1, 1, nanosecond=Decimal("0.1"), tzinfo=fixed_timezone)
            + fixed_timezone_delta,
        )

        dt = attodatetime.fromtimestamp(
            Decimal(1) / constants.MICROSECONDS_PER_SECOND, tz=fixed_timezone
        )
        self.assertEqual(
            dt,
            attodatetime(1970, 1, 1, microsecond=1, tzinfo=fixed_timezone)
            + fixed_timezone_delta,
        )

        dt = attodatetime.fromtimestamp(constants.SECONDS_PER_MINUTE, tz=fixed_timezone)
        self.assertEqual(
            dt,
            attodatetime(1970, 1, 1, minute=1, tzinfo=fixed_timezone)
            + fixed_timezone_delta,
        )

        dt = attodatetime.fromtimestamp(constants.SECONDS_PER_HOUR, tz=fixed_timezone)
        self.assertEqual(
            dt,
            attodatetime(1970, 1, 1, hour=1, tzinfo=fixed_timezone)
            + fixed_timezone_delta,
        )

        dt = attodatetime.fromtimestamp(constants.SECONDS_PER_DAY, tz=fixed_timezone)
        self.assertEqual(
            dt,
            attodatetime(1970, 1, 2, tzinfo=fixed_timezone) + fixed_timezone_delta,
        )

        dt = attodatetime.fromtimestamp(
            constants.SECONDS_PER_DAY * 31, tz=fixed_timezone
        )
        self.assertEqual(
            dt,
            attodatetime(1970, 2, 1, tzinfo=fixed_timezone) + fixed_timezone_delta,
        )

        dt = attodatetime.fromtimestamp(
            constants.SECONDS_PER_DAY * 365, tz=fixed_timezone
        )
        self.assertEqual(
            dt,
            attodatetime(1971, 1, 1, tzinfo=fixed_timezone) + fixed_timezone_delta,
        )

        fixed_timezone = FixedOffset(6, name="+6")
        fixed_timezone_delta = attotimedelta(hours=6)

        dt = attodatetime.fromtimestamp(0, tz=fixed_timezone)
        self.assertEqual(
            dt,
            attodatetime(1970, 1, 1, tzinfo=fixed_timezone) + fixed_timezone_delta,
        )

        dt = attodatetime.fromtimestamp(1, tz=fixed_timezone)
        self.assertEqual(
            dt,
            attodatetime(1970, 1, 1, second=1, tzinfo=fixed_timezone)
            + fixed_timezone_delta,
        )

        dt = attodatetime.fromtimestamp(
            Decimal(1) / constants.NANOSECONDS_PER_SECOND, tz=fixed_timezone
        )
        self.assertEqual(
            dt,
            attodatetime(1970, 1, 1, nanosecond=1, tzinfo=fixed_timezone)
            + fixed_timezone_delta,
        )

        dt = attodatetime.fromtimestamp(
            Decimal("0.1") / constants.NANOSECONDS_PER_SECOND, tz=fixed_timezone
        )
        self.assertEqual(
            dt,
            attodatetime(1970, 1, 1, nanosecond=Decimal("0.1"), tzinfo=fixed_timezone)
            + fixed_timezone_delta,
        )

        dt = attodatetime.fromtimestamp(
            Decimal(1) / constants.MICROSECONDS_PER_SECOND, tz=fixed_timezone
        )
        self.assertEqual(
            dt,
            attodatetime(1970, 1, 1, microsecond=1, tzinfo=fixed_timezone)
            + fixed_timezone_delta,
        )

        dt = attodatetime.fromtimestamp(constants.SECONDS_PER_MINUTE, tz=fixed_timezone)
        self.assertEqual(
            dt,
            attodatetime(1970, 1, 1, minute=1, tzinfo=fixed_timezone)
            + fixed_timezone_delta,
        )

        dt = attodatetime.fromtimestamp(constants.SECONDS_PER_HOUR, tz=fixed_timezone)
        self.assertEqual(
            dt,
            attodatetime(1970, 1, 1, hour=1, tzinfo=fixed_timezone)
            + fixed_timezone_delta,
        )

        dt = attodatetime.fromtimestamp(constants.SECONDS_PER_DAY, tz=fixed_timezone)
        self.assertEqual(
            dt,
            attodatetime(1970, 1, 2, tzinfo=fixed_timezone) + fixed_timezone_delta,
        )

        dt = attodatetime.fromtimestamp(
            constants.SECONDS_PER_DAY * 31, tz=fixed_timezone
        )
        self.assertEqual(
            dt,
            attodatetime(1970, 2, 1, tzinfo=fixed_timezone) + fixed_timezone_delta,
        )

        dt = attodatetime.fromtimestamp(
            constants.SECONDS_PER_DAY * 365, tz=fixed_timezone
        )
        self.assertEqual(
            dt,
            attodatetime(1971, 1, 1, tzinfo=fixed_timezone) + fixed_timezone_delta,
        )

    @mock.patch("attotime.objects.attodatetime.time.gmtime")
    def test_utcfromtimestamp(self, mockObjectGMTime):
        UNIX_EPOCH_STRUCT = time.struct_time((1970, 1, 1, 0, 0, 0, 3, 1, 0))

        mockObjectGMTime.return_value = UNIX_EPOCH_STRUCT

        dt = attodatetime.utcfromtimestamp(0)
        self.assertEqual(dt, attodatetime(1970, 1, 1))

        dt = attodatetime.utcfromtimestamp(1)
        self.assertEqual(dt, attodatetime(1970, 1, 1, second=1))

        dt = attodatetime.utcfromtimestamp(
            Decimal(1) / constants.NANOSECONDS_PER_SECOND
        )
        self.assertEqual(dt, attodatetime(1970, 1, 1, nanosecond=1))

        dt = attodatetime.utcfromtimestamp(
            Decimal("0.1") / constants.NANOSECONDS_PER_SECOND
        )
        self.assertEqual(dt, attodatetime(1970, 1, 1, nanosecond=Decimal("0.1")))

        dt = attodatetime.utcfromtimestamp(
            Decimal(1) / constants.MICROSECONDS_PER_SECOND
        )
        self.assertEqual(dt, attodatetime(1970, 1, 1, microsecond=1))

        dt = attodatetime.utcfromtimestamp(constants.SECONDS_PER_MINUTE)
        self.assertEqual(dt, attodatetime(1970, 1, 1, minute=1))

        dt = attodatetime.utcfromtimestamp(constants.SECONDS_PER_HOUR)
        self.assertEqual(dt, attodatetime(1970, 1, 1, hour=1))

        dt = attodatetime.utcfromtimestamp(constants.SECONDS_PER_DAY)
        self.assertEqual(dt, attodatetime(1970, 1, 2))

        dt = attodatetime.utcfromtimestamp(constants.SECONDS_PER_DAY * 31)
        self.assertEqual(dt, attodatetime(1970, 2, 1))

        dt = attodatetime.utcfromtimestamp(constants.SECONDS_PER_DAY * 365)
        self.assertEqual(dt, attodatetime(1971, 1, 1))

    def test_fromordinal(self):
        result = attodatetime.fromordinal(1)

        self.assertEqual(result._as_datetime(), datetime.datetime.fromordinal(1))
        self.assertEqual(result.nanosecond, 0)

        result = attodatetime.fromordinal(128)

        self.assertEqual(result._as_datetime(), datetime.datetime.fromordinal(128))
        self.assertEqual(result.nanosecond, 0)

    def test_combine(self):
        d = datetime.date(2006, 7, 8)
        t = attotime(
            hour=9,
            minute=10,
            second=11,
            microsecond=12,
            nanosecond=13.1415,
            tzinfo=FixedOffset(1, name="+1"),
        )

        result = attodatetime.combine(d, t)

        self.assertEqual(
            result,
            attodatetime(
                2006,
                7,
                8,
                hour=9,
                minute=10,
                second=11,
                microsecond=12,
                nanosecond=13.1415,
                tzinfo=FixedOffset(1, name="+1"),
            ),
        )

        # Make sure the time part of a datetime is ignored
        dt = attodatetime(
            2008,
            9,
            10,
            hour=11,
            minute=12,
            second=13,
            microsecond=14,
            nanosecond=15.1617,
        )
        t = attotime(hour=18, minute=19, second=20, microsecond=21, nanosecond=22.2324)

        result = attodatetime.combine(dt, t)

        self.assertEqual(
            result,
            attodatetime(
                2008,
                9,
                10,
                hour=18,
                minute=19,
                second=20,
                microsecond=21,
                nanosecond=22.2324,
            ),
        )

    def test_strptime(self):
        self.assertEqual(
            attodatetime.strptime("000000", "%o"), attodatetime(1900, 1, 1)
        )
        self.assertEqual(
            attodatetime.strptime("000001", "%o"),
            attodatetime(1900, 1, 1, nanosecond=Decimal("0.001")),
        )
        self.assertEqual(
            attodatetime.strptime("000010", "%o"),
            attodatetime(1900, 1, 1, nanosecond=Decimal("0.01")),
        )
        self.assertEqual(
            attodatetime.strptime("000100", "%o"),
            attodatetime(1900, 1, 1, nanosecond=Decimal("0.1")),
        )
        self.assertEqual(
            attodatetime.strptime("001000", "%o"),
            attodatetime(1900, 1, 1, nanosecond=1),
        )
        self.assertEqual(
            attodatetime.strptime("010000", "%o"),
            attodatetime(1900, 1, 1, nanosecond=10),
        )
        self.assertEqual(
            attodatetime.strptime("100000", "%o"),
            attodatetime(1900, 1, 1, nanosecond=100),
        )

        with localcontext() as context:
            context.prec = 29

            self.assertEqual(
                attodatetime.strptime("000000", "%q"), attodatetime(1900, 1, 1)
            )
            self.assertEqual(
                attodatetime.strptime("000001", "%q"),
                attodatetime(1900, 1, 1, nanosecond=Decimal("0.000000001")),
            )
            self.assertEqual(
                attodatetime.strptime("000010", "%q"),
                attodatetime(1900, 1, 1, nanosecond=Decimal("0.00000001")),
            )
            self.assertEqual(
                attodatetime.strptime("000100", "%q"),
                attodatetime(1900, 1, 1, nanosecond=Decimal("0.0000001")),
            )
            self.assertEqual(
                attodatetime.strptime("001000", "%q"),
                attodatetime(1900, 1, 1, nanosecond=Decimal("0.000001")),
            )
            self.assertEqual(
                attodatetime.strptime("010000", "%q"),
                attodatetime(1900, 1, 1, nanosecond=Decimal("0.00001")),
            )
            self.assertEqual(
                attodatetime.strptime("100000", "%q"),
                attodatetime(1900, 1, 1, nanosecond=Decimal("0.0001")),
            )

        with localcontext() as context:
            context.prec = 35

            self.assertEqual(
                attodatetime.strptime("000000", "%v"), attodatetime(1900, 1, 1)
            )
            self.assertEqual(
                attodatetime.strptime("000001", "%v"),
                attodatetime(1900, 1, 1, nanosecond=Decimal("0.000000000000001")),
            )
            self.assertEqual(
                attodatetime.strptime("000010", "%v"),
                attodatetime(1900, 1, 1, nanosecond=Decimal("0.00000000000001")),
            )
            self.assertEqual(
                attodatetime.strptime("000100", "%v"),
                attodatetime(1900, 1, 1, nanosecond=Decimal("0.0000000000001")),
            )
            self.assertEqual(
                attodatetime.strptime("001000", "%v"),
                attodatetime(1900, 1, 1, nanosecond=Decimal("0.000000000001")),
            )
            self.assertEqual(
                attodatetime.strptime("010000", "%v"),
                attodatetime(1900, 1, 1, nanosecond=Decimal("0.00000000001")),
            )
            self.assertEqual(
                attodatetime.strptime("100000", "%v"),
                attodatetime(1900, 1, 1, nanosecond=Decimal("0.0000000001")),
            )

        with localcontext() as context:
            context.prec = 35

            self.assertEqual(
                attodatetime.strptime("12.345678912345678912345678", "%S.%f%o%q%v"),
                attodatetime(
                    1900,
                    1,
                    1,
                    second=12,
                    microsecond=345678,
                    nanosecond=Decimal("912.345678912345678"),
                ),
            )

        # Combinations
        with localcontext() as context:
            context.prec = 35

            self.assertEqual(
                attodatetime.strptime(
                    "20010203 14:25:12.345678912345678912345678",
                    "%Y%m%d %H:%M:%S.%f%o%q%v",
                ),
                attodatetime(
                    2001,
                    2,
                    3,
                    hour=14,
                    minute=25,
                    second=12,
                    microsecond=345678,
                    nanosecond=Decimal("912.345678912345678"),
                ),
            )

        with localcontext() as context:
            context.prec = 29

            self.assertEqual(
                attodatetime.strptime(
                    "20010203 14:25:12.345678912345678912", "%Y%m%d %H:%M:%S.%f%o%q"
                ),
                attodatetime(
                    2001,
                    2,
                    3,
                    hour=14,
                    minute=25,
                    second=12,
                    microsecond=345678,
                    nanosecond=Decimal("912.345678912"),
                ),
            )

        self.assertEqual(
            attodatetime.strptime(
                "20010203 14:25:12.345678912345", "%Y%m%d %H:%M:%S.%f%o"
            ),
            attodatetime(
                2001,
                2,
                3,
                hour=14,
                minute=25,
                second=12,
                microsecond=345678,
                nanosecond=Decimal("912.345"),
            ),
        )

        self.assertEqual(
            attodatetime.strptime(
                "2021-10-Thursday 14:25:12.345678912345", "%Y-%W-%A %H:%M:%S.%f%o"
            ),
            attodatetime(
                2021,
                3,
                11,
                hour=14,
                minute=25,
                second=12,
                microsecond=345678,
                nanosecond=Decimal("912.345"),
            ),
        )

        self.assertEqual(
            attodatetime.strptime(
                "2021 10 4 14:25:12.345678912345", "%Y %W %w %H:%M:%S.%f%o"
            ),
            attodatetime(
                2021,
                3,
                11,
                hour=14,
                minute=25,
                second=12,
                microsecond=345678,
                nanosecond=Decimal("912.345"),
            ),
        )

        self.assertEqual(
            attodatetime.strptime(
                "2021 March 11 14:25:12.345678912345", "%Y %B %d %H:%M:%S.%f%o"
            ),
            attodatetime(
                2021,
                3,
                11,
                hour=14,
                minute=25,
                second=12,
                microsecond=345678,
                nanosecond=Decimal("912.345"),
            ),
        )

        self.assertEqual(
            attodatetime.strptime(
                "2021-03-11 02:25:12.345678912345 PM", "%Y-%m-%d %I:%M:%S.%f%o %p"
            ),
            attodatetime(
                2021,
                3,
                11,
                hour=14,
                minute=25,
                second=12,
                microsecond=345678,
                nanosecond=Decimal("912.345"),
            ),
        )

        self.assertEqual(
            attodatetime.strptime(
                "2021 321 14:25:12.345678912345", "%Y %j %H:%M:%S.%f%o"
            ),
            attodatetime(
                2021,
                11,
                17,
                hour=14,
                minute=25,
                second=12,
                microsecond=345678,
                nanosecond=Decimal("912.345"),
            ),
        )

        # Klunky test for empty %p
        from datetime import datetime

        def _mock_strftime(format, timetuple):
            if format == "%p":
                return ""

        with mock.patch("attotime.objects.attodatetime.time") as mockTime:
            with mock.patch(
                "attotime.objects.attodatetime.datetime.datetime"
            ) as mockDatetime:
                mockTime.strftime.side_effect = _mock_strftime
                mockDatetime.strptime.return_value = datetime(
                    2021, 3, 11, hour=2, minute=25, second=12, microsecond=345678
                )

                self.assertEqual(
                    attodatetime.strptime(
                        "2021-03-11 02:25:12.345678912345 ", "%Y-%m-%d %H:%M:%S.%f%o %p"
                    ),
                    attodatetime(
                        2021,
                        3,
                        11,
                        hour=2,
                        minute=25,
                        second=12,
                        microsecond=345678,
                        nanosecond=Decimal("912.345"),
                    ),
                )

        self.assertEqual(
            attodatetime.strptime(
                "2021-03-11%02:25:12.345678912345", "%Y-%m-%d%%%H:%M:%S.%f%o"
            ),
            attodatetime(
                2021,
                3,
                11,
                hour=2,
                minute=25,
                second=12,
                microsecond=345678,
                nanosecond=Decimal("912.345"),
            ),
        )

        test_attodatetime = attodatetime.utcnow()

        self.assertEqual(
            attodatetime.strptime(test_attodatetime.strftime("%c") + "912345", "%c%o"),
            attodatetime(
                test_attodatetime.year,
                test_attodatetime.month,
                test_attodatetime.day,
                hour=test_attodatetime.hour,
                minute=test_attodatetime.minute,
                second=test_attodatetime.second,
                nanosecond=Decimal("912.345"),
            ),
        )
        self.assertEqual(
            attodatetime.strptime(
                test_attodatetime.strftime("%x %X") + " " + "912345", "%x %X %o"
            ),
            attodatetime(
                test_attodatetime.year,
                test_attodatetime.month,
                test_attodatetime.day,
                hour=test_attodatetime.hour,
                minute=test_attodatetime.minute,
                second=test_attodatetime.second,
                nanosecond=Decimal("912.345"),
            ),
        )

        test_attodatetime = attodatetime(
            2001,
            2,
            3,
            hour=14,
            minute=25,
            second=12,
            microsecond=345678,
            nanosecond=Decimal("912.345"),
        )

        self.assertEqual(
            attodatetime.strptime(
                test_attodatetime.strftime("%a %b %d %H:%M:%S.%f%o%q %Y"),
                "%a %b %d %H:%M:%S.%f%o%q %Y",
            ),
            test_attodatetime,
        )
        self.assertEqual(
            attodatetime.strptime(
                test_attodatetime.strftime("%Y %H:%M:%S.%f%o%q %a %b %d"),
                "%Y %H:%M:%S.%f%o%q %a %b %d",
            ),
            test_attodatetime,
        )

        # Make sure we correctly call the Python implementation
        self.assertEqual(attodatetime.strptime("03", "%d"), attodatetime(1900, 1, 3))
        self.assertEqual(attodatetime.strptime("02", "%m"), attodatetime(1900, 2, 1))
        self.assertEqual(attodatetime.strptime("01", "%y"), attodatetime(2001, 1, 1))
        self.assertEqual(attodatetime.strptime("2001", "%Y"), attodatetime(2001, 1, 1))

        self.assertEqual(
            attodatetime.strptime("14", "%H"), attodatetime(1900, 1, 1, hour=14)
        )
        self.assertEqual(
            attodatetime.strptime("02", "%I"), attodatetime(1900, 1, 1, hour=2)
        )
        self.assertEqual(
            attodatetime.strptime("25", "%M"), attodatetime(1900, 1, 1, minute=25)
        )
        self.assertEqual(
            attodatetime.strptime("36", "%S"), attodatetime(1900, 1, 1, second=36)
        )
        self.assertEqual(
            attodatetime.strptime("789123", "%f"),
            attodatetime(1900, 1, 1, microsecond=789123),
        )
        self.assertEqual(attodatetime.strptime("034", "%j"), attodatetime(1900, 2, 3))

        self.assertEqual(
            attodatetime.strptime("2001205", "%Y%w%U"), attodatetime(2001, 2, 6)
        )
        self.assertEqual(
            attodatetime.strptime("2001205", "%Y%w%W"), attodatetime(2001, 1, 30)
        )

        # Locale specific
        test_attodatetime = attodatetime.utcnow()

        # Note no sub-microsecond precision
        self.assertEqual(
            attodatetime.strptime(
                test_attodatetime.strftime("%a %b %d %H:%M:%S %Y"),
                "%a %b %d %H:%M:%S %Y",
            ),
            attodatetime(
                test_attodatetime.year,
                test_attodatetime.month,
                test_attodatetime.day,
                hour=test_attodatetime.hour,
                minute=test_attodatetime.minute,
                second=test_attodatetime.second,
            ),
        )
        self.assertEqual(
            attodatetime.strptime(
                test_attodatetime.strftime("%Y %H:%M:%S %a %b %d"),
                "%Y %H:%M:%S %a %b %d",
            ),
            attodatetime(
                test_attodatetime.year,
                test_attodatetime.month,
                test_attodatetime.day,
                hour=test_attodatetime.hour,
                minute=test_attodatetime.minute,
                second=test_attodatetime.second,
            ),
        )
        self.assertEqual(
            attodatetime.strptime(test_attodatetime.strftime("%c"), "%c"),
            attodatetime(
                test_attodatetime.year,
                test_attodatetime.month,
                test_attodatetime.day,
                hour=test_attodatetime.hour,
                minute=test_attodatetime.minute,
                second=test_attodatetime.second,
            ),
        )
        self.assertEqual(
            attodatetime.strptime(test_attodatetime.strftime("%x"), "%x"),
            attodatetime(
                test_attodatetime.year, test_attodatetime.month, test_attodatetime.day
            ),
        )
        self.assertEqual(
            attodatetime.strptime(test_attodatetime.strftime("%x %X"), "%x %X"),
            attodatetime(
                test_attodatetime.year,
                test_attodatetime.month,
                test_attodatetime.day,
                hour=test_attodatetime.hour,
                minute=test_attodatetime.minute,
                second=test_attodatetime.second,
            ),
        )

    def test_strptime_span_not_found(self):
        with self.assertRaises(ValueError):
            attodatetime.strptime(
                "2021 11 14:25:12.345678912345", "%Y %B %d %H:%M:%S.%f%o"
            )

    def test_strptime_invalid_field(self):
        with self.assertRaises(ValueError):
            attodatetime.strptime(
                "2021-03-11 02:25:12.345678912345", "%Y-%m-%d%K%H:%M:%S.%f%o"
            )

    def test_date(self):
        dt = attodatetime(2001, 2, 3)
        self.assertEqual(dt.date(), datetime.date(2001, 2, 3))
        self.assertIsNot(dt.date(), dt._native_date)

    def test_time(self):
        dt = attodatetime(
            2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5.678
        )
        result = dt.time()

        self.assertEqual(
            result,
            attotime(hour=1, minute=2, second=3, microsecond=4, nanosecond=5.678),
        )
        self.assertIsNot(result, dt._attotime)

        dt = attodatetime(
            2001,
            2,
            3,
            hour=1,
            minute=2,
            second=3,
            microsecond=4,
            nanosecond=5.678,
            tzinfo=FixedOffset(1, name="+1"),
        )
        result = dt.time()

        self.assertEqual(
            result,
            attotime(hour=1, minute=2, second=3, microsecond=4, nanosecond=5.678),
        )
        self.assertIsNot(result, dt._attotime)

    def test_timetz(self):
        dt = attodatetime(
            2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5.678
        )
        result = dt.timetz()

        self.assertEqual(
            result,
            attotime(hour=1, minute=2, second=3, microsecond=4, nanosecond=5.678),
        )
        self.assertIsNot(result, dt._attotime)

        dt = attodatetime(
            2001,
            2,
            3,
            hour=1,
            minute=2,
            second=3,
            microsecond=4,
            nanosecond=5.678,
            tzinfo=FixedOffset(1, name="+1"),
        )
        result = dt.timetz()

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
        self.assertIsNot(result, dt._attotime)

    def test_replace(self):
        dt = attodatetime(
            2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5.678
        )
        result = dt.replace(year=2002)

        self.assertEqual(
            result,
            attodatetime(
                2002, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5.678
            ),
        )

        dt = attodatetime(
            2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5.678
        )
        result = dt.replace(month=3)

        self.assertEqual(
            result,
            attodatetime(
                2001, 3, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5.678
            ),
        )

        dt = attodatetime(
            2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5.678
        )
        result = dt.replace(day=4)

        self.assertEqual(
            result,
            attodatetime(
                2001, 2, 4, hour=1, minute=2, second=3, microsecond=4, nanosecond=5.678
            ),
        )

        dt = attodatetime(
            2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5.678
        )
        result = dt.replace(hour=2)

        self.assertEqual(
            result,
            attodatetime(
                2001, 2, 3, hour=2, minute=2, second=3, microsecond=4, nanosecond=5.678
            ),
        )

        dt = attodatetime(
            2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5.678
        )
        result = dt.replace(minute=3)

        self.assertEqual(
            result,
            attodatetime(
                2001, 2, 3, hour=1, minute=3, second=3, microsecond=4, nanosecond=5.678
            ),
        )

        dt = attodatetime(
            2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5.678
        )
        result = dt.replace(second=4)

        self.assertEqual(
            result,
            attodatetime(
                2001, 2, 3, hour=1, minute=2, second=4, microsecond=4, nanosecond=5.678
            ),
        )

        dt = attodatetime(
            2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5.678
        )
        result = dt.replace(microsecond=5)

        self.assertEqual(
            result,
            attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=5, nanosecond=5.678
            ),
        )

        dt = attodatetime(
            2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5.678
        )
        result = dt.replace(nanosecond=0.91011)

        self.assertEqual(
            result,
            attodatetime(
                2001,
                2,
                3,
                hour=1,
                minute=2,
                second=3,
                microsecond=4,
                nanosecond=0.91011,
            ),
        )

        dt = attodatetime(
            2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5.678
        )
        result = dt.replace(tzinfo=FixedOffset(1, name="+1"))

        self.assertEqual(
            result,
            attodatetime(
                2001,
                2,
                3,
                hour=1,
                minute=2,
                second=3,
                microsecond=4,
                nanosecond=5.678,
                tzinfo=FixedOffset(1, name="+1"),
            ),
        )

        dt = attodatetime(
            2001,
            2,
            3,
            hour=1,
            minute=2,
            second=3,
            microsecond=4,
            nanosecond=5.678,
            tzinfo=FixedOffset(1, name="+1"),
        )
        result = dt.replace(tzinfo=None)

        self.assertEqual(
            result,
            attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5.678
            ),
        )

    def test_astimezone(self):
        dt = attodatetime(2001, 2, 3, hour=1, tzinfo=FixedOffset(1, name="+1"))
        result = dt.astimezone(utc)

        self.assertEqual(result, attodatetime(2001, 2, 3, tzinfo=utc))

        dt = attodatetime(2001, 2, 3, hour=1, tzinfo=utc)
        result = dt.astimezone(FixedOffset(1, name="+1"))

        self.assertEqual(
            result, attodatetime(2001, 2, 3, hour=2, tzinfo=FixedOffset(1, name="+1"))
        )

        dt = attodatetime(2001, 2, 3, hour=1, tzinfo=FixedOffset(1, name="+1"))
        result = dt.astimezone(FixedOffset(0, name="UTC"))

        self.assertEqual(
            result, attodatetime(2001, 2, 3, tzinfo=FixedOffset(0, name="UTC"))
        )

        dt = attodatetime(2001, 2, 3, hour=23, tzinfo=FixedOffset(-1, name="-1"))
        result = dt.astimezone(FixedOffset(0, name="UTC"))

        self.assertEqual(
            result, attodatetime(2001, 2, 4, tzinfo=FixedOffset(0, name="UTC"))
        )

        dt = attodatetime(2001, 2, 3, hour=23, tzinfo=FixedOffset(0, name="UTC"))
        result = dt.astimezone(FixedOffset(1, name="+1"))

        self.assertEqual(
            result, attodatetime(2001, 2, 4, tzinfo=FixedOffset(1, name="+1"))
        )

        dt = attodatetime(2001, 2, 3, hour=1, tzinfo=FixedOffset(0, name="UTC"))
        result = dt.astimezone(FixedOffset(-1, name="-1"))

        self.assertEqual(
            result, attodatetime(2001, 2, 3, tzinfo=FixedOffset(-1, name="-1"))
        )

        dt = attodatetime(
            2001,
            2,
            3,
            hour=1,
            nanosecond=Decimal("1.234"),
            tzinfo=FixedOffset(1, name="+1"),
        )
        result = dt.astimezone(FixedOffset(0, name="UTC"))

        self.assertEqual(
            result,
            attodatetime(
                2001,
                2,
                3,
                nanosecond=Decimal("1.234"),
                tzinfo=FixedOffset(0, name="UTC"),
            ),
        )

        dt = attodatetime(
            2001,
            2,
            3,
            hour=23,
            nanosecond=Decimal("1.234"),
            tzinfo=FixedOffset(-1, name="-1"),
        )
        result = dt.astimezone(FixedOffset(0, name="UTC"))

        self.assertEqual(
            result,
            attodatetime(
                2001,
                2,
                4,
                nanosecond=Decimal("1.234"),
                tzinfo=FixedOffset(0, name="UTC"),
            ),
        )

        dt = attodatetime(
            2001,
            2,
            3,
            hour=23,
            nanosecond=Decimal("1.234"),
            tzinfo=FixedOffset(0, name="UTC"),
        )
        result = dt.astimezone(FixedOffset(1, name="+1"))

        self.assertEqual(
            result,
            attodatetime(
                2001,
                2,
                4,
                nanosecond=Decimal("1.234"),
                tzinfo=FixedOffset(1, name="+1"),
            ),
        )

        dt = attodatetime(
            2001,
            2,
            3,
            hour=1,
            nanosecond=Decimal("1.234"),
            tzinfo=FixedOffset(0, name="UTC"),
        )
        result = dt.astimezone(FixedOffset(-1, name="-1"))

        self.assertEqual(
            result,
            attodatetime(
                2001,
                2,
                3,
                nanosecond=Decimal("1.234"),
                tzinfo=FixedOffset(-1, name="-1"),
            ),
        )

        # Test same tz
        test_tz = FixedOffset(1, name="+1")

        dt = attodatetime(2001, 2, 3, hour=1, tzinfo=test_tz)
        result = dt.astimezone(test_tz)

        self.assertEqual(result, dt)

        with self.assertRaises(ValueError):
            dt = attodatetime(2001, 2, 3)
            dt.astimezone(FixedOffset(1, name="+1"))

    def test_utcoffset(self):
        dt = attodatetime(2001, 2, 3)
        self.assertIsNone(dt.utcoffset())

        dt = attodatetime(2001, 2, 3, tzinfo=FixedOffset(1, name="+1"))
        self.assertEqual(dt.utcoffset(), attotimedelta(hours=1))

        dt = attodatetime(2001, 2, 3, tzinfo=FixedOffset(-1, name="-1"))
        self.assertEqual(dt.utcoffset(), attotimedelta(hours=-1))

    def test_dst(self):
        dt = attodatetime(2001, 1, 1)
        self.assertIsNone(dt.dst())

        dt = attodatetime(2001, 1, 1, tzinfo=DSTOffset(1, name="+1"))
        self.assertEqual(dt.dst(), attotimedelta(hours=0))

        dt = attodatetime(2001, 12, 1, tzinfo=DSTOffset(1, name="+1"))
        self.assertEqual(dt.dst(), attotimedelta(hours=1))

        dt = attodatetime(2001, 1, 1, tzinfo=DSTOffset(-1, name="-1"))
        self.assertEqual(dt.dst(), attotimedelta(hours=0))

        dt = attodatetime(2001, 12, 1, tzinfo=DSTOffset(-1, name="-1"))
        self.assertEqual(dt.dst(), attotimedelta(hours=1))

    def test_tzname(self):
        dt = attodatetime(2001, 1, 1)
        self.assertIsNone(dt.tzname())

        dt = attodatetime(2001, 1, 1, tzinfo=DSTOffset(1, name="+1"))
        self.assertEqual(dt.tzname(), "+1")

    def test_timetuple(self):
        self.assertEqual(
            attodatetime(2001, 2, 3).timetuple(),
            datetime.datetime(2001, 2, 3).timetuple(),
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, hour=1).timetuple(),
            datetime.datetime(2001, 2, 3, hour=1).timetuple(),
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, hour=1, minute=2).timetuple(),
            datetime.datetime(2001, 2, 3, hour=1, minute=2).timetuple(),
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, hour=1, minute=2, second=3).timetuple(),
            datetime.datetime(2001, 2, 3, hour=1, minute=2, second=3).timetuple(),
        )
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4
            ).timetuple(),
            datetime.datetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4
            ).timetuple(),
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, tzinfo=FixedOffset(1, name="+1")).timetuple(),
            datetime.datetime(2001, 2, 3, tzinfo=FixedOffset(1, name="+1")).timetuple(),
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, tzinfo=DSTOffset(1, name="+1")).timetuple(),
            datetime.datetime(2001, 2, 3, tzinfo=DSTOffset(1, name="+1")).timetuple(),
        )

        # No support for nanoseconds
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5
            ).timetuple(),
            datetime.datetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4
            ).timetuple(),
        )

    def test_utctimetuple(self):
        self.assertEqual(
            attodatetime(2001, 2, 3).utctimetuple(),
            datetime.datetime(2001, 2, 3).utctimetuple(),
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, hour=1).utctimetuple(),
            datetime.datetime(2001, 2, 3, hour=1).utctimetuple(),
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, hour=1, minute=2).utctimetuple(),
            datetime.datetime(2001, 2, 3, hour=1, minute=2).utctimetuple(),
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, hour=1, minute=2, second=3).utctimetuple(),
            datetime.datetime(2001, 2, 3, hour=1, minute=2, second=3).utctimetuple(),
        )
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4
            ).utctimetuple(),
            datetime.datetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4
            ).utctimetuple(),
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, tzinfo=FixedOffset(1, name="+1")).utctimetuple(),
            datetime.datetime(
                2001, 2, 3, tzinfo=FixedOffset(1, name="+1")
            ).utctimetuple(),
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, tzinfo=DSTOffset(1, name="+1")).utctimetuple(),
            datetime.datetime(
                2001, 2, 3, tzinfo=DSTOffset(1, name="+1")
            ).utctimetuple(),
        )

        # No support for nanoseconds
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5
            ).utctimetuple(),
            datetime.datetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4
            ).utctimetuple(),
        )

    def test_toordinal(self):
        date = datetime.date(2001, 2, 3)

        self.assertEqual(attodatetime(2001, 2, 3).toordinal(), date.toordinal())

        # Additional resolution shouldn't matter
        self.assertEqual(attodatetime(2001, 2, 3, hour=1).toordinal(), date.toordinal())
        self.assertEqual(
            attodatetime(2001, 2, 3, hour=1, minute=2).toordinal(), date.toordinal()
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, hour=1, minute=2, second=3).toordinal(),
            date.toordinal(),
        )
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4
            ).toordinal(),
            date.toordinal(),
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, tzinfo=FixedOffset(1, name="+1")).toordinal(),
            date.toordinal(),
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, tzinfo=DSTOffset(1, name="+1")).toordinal(),
            date.toordinal(),
        )
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5
            ).toordinal(),
            date.toordinal(),
        )

    def test_weekday(self):
        date = datetime.date(2001, 2, 3)

        self.assertEqual(attodatetime(2001, 2, 3).weekday(), date.weekday())

        # Additional resolution shouldn't matter
        self.assertEqual(attodatetime(2001, 2, 3, hour=1).weekday(), date.weekday())
        self.assertEqual(
            attodatetime(2001, 2, 3, hour=1, minute=2).weekday(), date.weekday()
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, hour=1, minute=2, second=3).weekday(),
            date.weekday(),
        )
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4
            ).weekday(),
            date.weekday(),
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, tzinfo=FixedOffset(1, name="+1")).weekday(),
            date.weekday(),
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, tzinfo=DSTOffset(1, name="+1")).weekday(),
            date.weekday(),
        )
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5
            ).weekday(),
            date.weekday(),
        )

    def test_isoweekday(self):
        date = datetime.date(2001, 2, 3)

        self.assertEqual(attodatetime(2001, 2, 3).isoweekday(), date.isoweekday())

        # Additional resolution shouldn't matter
        self.assertEqual(
            attodatetime(2001, 2, 3, hour=1).isoweekday(), date.isoweekday()
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, hour=1, minute=2).isoweekday(), date.isoweekday()
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, hour=1, minute=2, second=3).isoweekday(),
            date.isoweekday(),
        )
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4
            ).isoweekday(),
            date.isoweekday(),
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, tzinfo=FixedOffset(1, name="+1")).isoweekday(),
            date.isoweekday(),
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, tzinfo=DSTOffset(1, name="+1")).isoweekday(),
            date.isoweekday(),
        )
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5
            ).isoweekday(),
            date.isoweekday(),
        )

    def test_isocalendar(self):
        date = datetime.date(2001, 2, 3)

        self.assertEqual(attodatetime(2001, 2, 3).isocalendar(), date.isocalendar())

        # Additional resolution shouldn't matter
        self.assertEqual(
            attodatetime(2001, 2, 3, hour=1).isocalendar(), date.isocalendar()
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, hour=1, minute=2).isocalendar(), date.isocalendar()
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, hour=1, minute=2, second=3).isocalendar(),
            date.isocalendar(),
        )
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4
            ).isocalendar(),
            date.isocalendar(),
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, tzinfo=FixedOffset(1, name="+1")).isocalendar(),
            date.isocalendar(),
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, tzinfo=DSTOffset(1, name="+1")).isocalendar(),
            date.isocalendar(),
        )
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5
            ).isocalendar(),
            date.isocalendar(),
        )

    def test_isoformat(self):
        self.assertEqual(attodatetime(2001, 2, 3).isoformat(), "2001-02-03T00:00:00")
        self.assertEqual(
            attodatetime(2001, 2, 3, hour=1).isoformat(), "2001-02-03T01:00:00"
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, hour=1, minute=2).isoformat(),
            "2001-02-03T01:02:00",
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, hour=1, minute=2, second=3).isoformat(),
            "2001-02-03T01:02:03",
        )
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4
            ).isoformat(),
            "2001-02-03T01:02:03.000004",
        )
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=6
            ).isoformat(),
            "2001-02-03T01:02:03.000004006",
        )
        self.assertEqual(
            attodatetime(
                2001,
                2,
                3,
                hour=1,
                minute=2,
                second=3,
                microsecond=4,
                nanosecond=Decimal("0.006"),
            ).isoformat(),
            "2001-02-03T01:02:03.000004000006",
        )
        self.assertEqual(
            attodatetime(
                2001,
                2,
                3,
                hour=1,
                minute=2,
                second=3,
                microsecond=4,
                nanosecond=Decimal("0.006"),
                tzinfo=DSTOffset(1, name="+1"),
            ).isoformat(),
            "2001-02-03T01:02:03.000004000006+01:00",
        )
        self.assertEqual(
            attodatetime(
                2001,
                2,
                3,
                hour=1,
                minute=2,
                second=3,
                microsecond=4,
                nanosecond=Decimal("0.006"),
                tzinfo=DSTOffset(-1, name="-1"),
            ).isoformat(),
            "2001-02-03T01:02:03.000004000006-01:00",
        )

        self.assertEqual(
            attodatetime(2001, 2, 3).isoformat(separator=" "), "2001-02-03 00:00:00"
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, hour=1).isoformat(separator=" "),
            "2001-02-03 01:00:00",
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, hour=1, minute=2).isoformat(separator=" "),
            "2001-02-03 01:02:00",
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, hour=1, minute=2, second=3).isoformat(
                separator=" "
            ),
            "2001-02-03 01:02:03",
        )
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4
            ).isoformat(separator=" "),
            "2001-02-03 01:02:03.000004",
        )
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=6
            ).isoformat(separator=" "),
            "2001-02-03 01:02:03.000004006",
        )
        self.assertEqual(
            attodatetime(
                2001,
                2,
                3,
                hour=1,
                minute=2,
                second=3,
                microsecond=4,
                nanosecond=Decimal("0.006"),
            ).isoformat(separator=" "),
            "2001-02-03 01:02:03.000004000006",
        )
        self.assertEqual(
            attodatetime(
                2001,
                2,
                3,
                hour=1,
                minute=2,
                second=3,
                microsecond=4,
                nanosecond=Decimal("0.006"),
                tzinfo=DSTOffset(1, name="+1"),
            ).isoformat(separator=" "),
            "2001-02-03 01:02:03.000004000006+01:00",
        )
        self.assertEqual(
            attodatetime(
                2001,
                2,
                3,
                hour=1,
                minute=2,
                second=3,
                microsecond=4,
                nanosecond=Decimal("0.006"),
                tzinfo=DSTOffset(-1, name="-1"),
            ).isoformat(separator=" "),
            "2001-02-03 01:02:03.000004000006-01:00",
        )

    def test_ctime(self):
        self.assertEqual(
            attodatetime(2001, 2, 3).ctime(), datetime.datetime(2001, 2, 3).ctime()
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, hour=1).ctime(),
            datetime.datetime(2001, 2, 3, hour=1).ctime(),
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, hour=1, minute=2).ctime(),
            datetime.datetime(2001, 2, 3, hour=1, minute=2).ctime(),
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, hour=1, minute=2, second=3).ctime(),
            datetime.datetime(2001, 2, 3, hour=1, minute=2, second=3).ctime(),
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, hour=1, minute=2, second=3, microsecond=4).ctime(),
            datetime.datetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4
            ).ctime(),
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, tzinfo=FixedOffset(1, name="+1")).ctime(),
            datetime.datetime(2001, 2, 3, tzinfo=FixedOffset(1, name="+1")).ctime(),
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, tzinfo=DSTOffset(1, name="+1")).ctime(),
            datetime.datetime(2001, 2, 3, tzinfo=DSTOffset(1, name="+1")).ctime(),
        )

        # No support for nanoseconds
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5
            ).ctime(),
            datetime.datetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4
            ).ctime(),
        )

    def test_strftime(self):
        self.assertEqual(attodatetime(2001, 2, 3).strftime("%w"), "6")
        self.assertEqual(attodatetime(2001, 2, 3).strftime("%d"), "03")
        self.assertEqual(attodatetime(2001, 2, 3).strftime("%m"), "02")
        self.assertEqual(attodatetime(2001, 2, 3).strftime("%y"), "01")
        self.assertEqual(attodatetime(2001, 2, 3).strftime("%Y"), "2001")

        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
            ).strftime("%H"),
            "14",
        )
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
            ).strftime("%I"),
            "02",
        )
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
            ).strftime("%M"),
            "25",
        )
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
            ).strftime("%S"),
            "36",
        )
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
            ).strftime("%f"),
            "789123",
        )
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
            ).strftime("%z"),
            "",
        )
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
            ).strftime("%Z"),
            "",
        )
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
            ).strftime("%j"),
            "034",
        )
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
            ).strftime("%U"),
            "04",
        )
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
            ).strftime("%W"),
            "05",
        )
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
            ).strftime("%%"),
            "%",
        )

        self.assertEqual(
            attodatetime(2001, 2, 3, nanosecond=Decimal("0.0001")).strftime("%o"),
            "000000",
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, nanosecond=Decimal("0.001")).strftime("%o"),
            "000001",
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, nanosecond=Decimal("0.01")).strftime("%o"),
            "000010",
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, nanosecond=Decimal("0.1")).strftime("%o"), "000100"
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, nanosecond=1).strftime("%o"), "001000"
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, nanosecond=10).strftime("%o"), "010000"
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, nanosecond=100).strftime("%o"), "100000"
        )

        self.assertEqual(
            attodatetime(2001, 2, 3, nanosecond=Decimal("0.0000000001")).strftime("%q"),
            "000000",
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, nanosecond=Decimal("0.000000001")).strftime("%q"),
            "000001",
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, nanosecond=Decimal("0.00000001")).strftime("%q"),
            "000010",
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, nanosecond=Decimal("0.0000001")).strftime("%q"),
            "000100",
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, nanosecond=Decimal("0.000001")).strftime("%q"),
            "001000",
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, nanosecond=Decimal("0.00001")).strftime("%q"),
            "010000",
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, nanosecond=Decimal("0.0001")).strftime("%q"),
            "100000",
        )

        self.assertEqual(
            attodatetime(2001, 2, 3, nanosecond=Decimal("0.0000000000000001")).strftime(
                "%v"
            ),
            "000000",
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, nanosecond=Decimal("0.000000000000001")).strftime(
                "%v"
            ),
            "000001",
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, nanosecond=Decimal("0.00000000000001")).strftime(
                "%v"
            ),
            "000010",
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, nanosecond=Decimal("0.0000000000001")).strftime(
                "%v"
            ),
            "000100",
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, nanosecond=Decimal("0.000000000001")).strftime(
                "%v"
            ),
            "001000",
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, nanosecond=Decimal("0.00000000001")).strftime(
                "%v"
            ),
            "010000",
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, nanosecond=Decimal("0.0000000001")).strftime("%v"),
            "100000",
        )

        # Note truncation of sub-yoctosecond precision
        self.assertEqual(
            attodatetime(
                2001,
                2,
                3,
                second=12,
                microsecond=345678,
                nanosecond=Decimal("912.3456789123456789"),
            ).strftime("%S.%f%o%q%v"),
            "12.345678912345678912345678",
        )

        # Timezone tests
        self.assertEqual(
            attodatetime(2001, 2, 3, tzinfo=DSTOffset(1, name="+1")).strftime("%z"),
            "+0100",
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, tzinfo=DSTOffset(10, name="+10")).strftime("%z"),
            "+1000",
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, tzinfo=DSTOffset(1, name="+1")).strftime("%Z"),
            "+1",
        )

        self.assertEqual(
            attodatetime(2001, 2, 3, tzinfo=DSTOffset(-1, name="-1")).strftime("%z"),
            "-0100",
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, tzinfo=DSTOffset(-10, name="-10")).strftime("%z"),
            "-1000",
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, tzinfo=DSTOffset(-1, name="-1")).strftime("%Z"),
            "-1",
        )

        # Locale specific
        self.assertEqual(
            attodatetime(2001, 2, 3).strftime("%a"),
            datetime.datetime(2001, 2, 3).strftime("%a"),
        )
        self.assertEqual(
            attodatetime(2001, 2, 3).strftime("%A"),
            datetime.datetime(2001, 2, 3).strftime("%A"),
        )
        self.assertEqual(
            attodatetime(2001, 2, 3).strftime("%b"),
            datetime.datetime(2001, 2, 3).strftime("%b"),
        )
        self.assertEqual(
            attodatetime(2001, 2, 3).strftime("%B"),
            datetime.datetime(2001, 2, 3).strftime("%B"),
        )
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
            ).strftime("%p"),
            datetime.datetime(
                2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
            ).strftime("%p"),
        )
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
            ).strftime("%c"),
            datetime.datetime(
                2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
            ).strftime("%c"),
        )
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
            ).strftime("%x"),
            datetime.datetime(
                2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
            ).strftime("%x"),
        )
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
            ).strftime("%X"),
            datetime.datetime(
                2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
            ).strftime("%X"),
        )

    def test_add(self):
        dt = attodatetime(2001, 2, 3)
        td = attotimedelta(days=1)

        result = dt + td
        self.assertEqual(result, attodatetime(2001, 2, 4))

        dt = attodatetime(2001, 2, 3)
        td = attotimedelta(seconds=1)

        result = dt + td
        self.assertEqual(result, attodatetime(2001, 2, 3, second=1))

        dt = attodatetime(2001, 2, 3)
        td = attotimedelta(microseconds=1)

        result = dt + td
        self.assertEqual(result, attodatetime(2001, 2, 3, microsecond=1))

        dt = attodatetime(2001, 2, 3)
        td = attotimedelta(milliseconds=1)

        result = dt + td
        self.assertEqual(
            result,
            attodatetime(
                2001, 2, 3, microsecond=int(constants.MICROSECONDS_PER_MILLISECOND)
            ),
        )

        dt = attodatetime(2001, 2, 3)
        td = attotimedelta(minutes=1)

        result = dt + td
        self.assertEqual(result, attodatetime(2001, 2, 3, minute=1))

        dt = attodatetime(2001, 2, 3)
        td = attotimedelta(hours=1)

        result = dt + td
        self.assertEqual(result, attodatetime(2001, 2, 3, hour=1))

        dt = attodatetime(2001, 2, 3)
        td = attotimedelta(weeks=1)

        result = dt + td
        self.assertEqual(result, attodatetime(2001, 2, 10))

        dt = attodatetime(2001, 2, 3)
        td = attotimedelta(nanoseconds=1)

        result = dt + td
        self.assertEqual(result, attodatetime(2001, 2, 3, nanosecond=1))

        with self.assertRaises(TypeError):
            attodatetime(2001, 2, 3) + datetime.timedelta(1)

        with self.assertRaises(OverflowError):
            attodatetime(2001, 2, 3) + attotimedelta(days=datetime.date.max.year * 365)

    def test_add_overflow(self):
        dt = attodatetime(2001, 2, 1)
        td = attotimedelta(days=365)

        result = dt + td
        self.assertEqual(result, attodatetime(2002, 2, 1))

        dt = attodatetime(2001, 2, 1)
        td = attotimedelta(seconds=constants.SECONDS_PER_MINUTE)

        result = dt + td
        self.assertEqual(result, attodatetime(2001, 2, 1, minute=1))

        dt = attodatetime(2001, 2, 1)
        td = attotimedelta(microseconds=constants.MICROSECONDS_PER_SECOND)

        result = dt + td
        self.assertEqual(result, attodatetime(2001, 2, 1, second=1))

        dt = attodatetime(2001, 2, 1)
        td = attotimedelta(milliseconds=constants.MILLISECONDS_PER_SECOND)

        result = dt + td
        self.assertEqual(result, attodatetime(2001, 2, 1, second=1))

        dt = attodatetime(2001, 2, 1)
        td = attotimedelta(minutes=constants.MINUTES_PER_HOUR)

        result = dt + td
        self.assertEqual(result, attodatetime(2001, 2, 1, hour=1))

        dt = attodatetime(2001, 2, 1)
        td = attotimedelta(hours=constants.HOURS_PER_DAY)

        result = dt + td
        self.assertEqual(result, attodatetime(2001, 2, 2))

        dt = attodatetime(2001, 2, 1)
        td = attotimedelta(weeks=4)

        result = dt + td
        self.assertEqual(result, attodatetime(2001, 3, 1))

        dt = attodatetime(2001, 2, 1)
        td = attotimedelta(nanoseconds=constants.NANOSECONDS_PER_SECOND)

        result = dt + td
        self.assertEqual(result, attodatetime(2001, 2, 1, second=1))

    def test_sub(self):
        dt = attodatetime(2001, 2, 2)
        td = attotimedelta(days=1)

        result = dt - td
        self.assertEqual(result, attodatetime(2001, 2, 1))

        dt = attodatetime(2001, 2, 1, hour=1)
        td = attotimedelta(hours=1)

        result = dt - td
        self.assertEqual(result, attodatetime(2001, 2, 1))

        dt = attodatetime(2001, 2, 1, minute=1)
        td = attotimedelta(minutes=1)

        result = dt - td
        self.assertEqual(result, attodatetime(2001, 2, 1))

        dt = attodatetime(2001, 2, 1, second=1)
        td = attotimedelta(seconds=1)

        result = dt - td
        self.assertEqual(result, attodatetime(2001, 2, 1))

        dt = attodatetime(2001, 2, 1, microsecond=1)
        td = attotimedelta(microseconds=1)

        result = dt - td
        self.assertEqual(result, attodatetime(2001, 2, 1))

        dt = attodatetime(
            2001, 2, 1, microsecond=int(constants.MICROSECONDS_PER_MILLISECOND)
        )
        td = attotimedelta(milliseconds=1)

        result = dt - td
        self.assertEqual(result, attodatetime(2001, 2, 1))

        dt = attodatetime(2001, 2, 1, nanosecond=0.121)
        td = attotimedelta(nanoseconds=0.121)

        result = dt - td
        self.assertEqual(result, attodatetime(2001, 2, 1))

        dt1 = attodatetime(2001, 2, 2, tzinfo=DSTOffset(1, name="+1"))
        dt2 = attodatetime(2001, 2, 3, tzinfo=DSTOffset(1, name="+1"))

        result = dt2 - dt1
        self.assertEqual(result, attotimedelta(days=1))

        with self.assertRaises(TypeError):
            attodatetime(2001, 2, 2) - datetime.timedelta(1)

    def test_sub_underflow(self):
        dt = attodatetime(2001, 1, 1)
        td = attotimedelta(days=1)

        result = dt - td
        self.assertEqual(result, attodatetime(2000, 12, 31))

        dt = attodatetime(2001, 2, 1)
        td = attotimedelta(days=1)

        result = dt - td
        self.assertEqual(result, attodatetime(2001, 1, 31))

        dt = attodatetime(2001, 2, 7)
        td = attotimedelta(weeks=1)

        result = dt - td
        self.assertEqual(result, attodatetime(2001, 1, 31))

        dt = attodatetime(2001, 1, 1, hour=1)
        td = attotimedelta(hours=2)

        result = dt - td
        self.assertEqual(result, attodatetime(2000, 12, 31, hour=23))

        dt = attodatetime(2001, 1, 1, minute=1)
        td = attotimedelta(minutes=2)

        result = dt - td
        self.assertEqual(result, attodatetime(2000, 12, 31, hour=23, minute=59))

        dt = attodatetime(2001, 1, 1, second=1)
        td = attotimedelta(seconds=2)

        result = dt - td
        self.assertEqual(
            result, attodatetime(2000, 12, 31, hour=23, minute=59, second=59)
        )

        dt = attodatetime(2001, 1, 1, microsecond=1)
        td = attotimedelta(microseconds=2)

        result = dt - td
        self.assertEqual(
            result,
            attodatetime(
                2000,
                12,
                31,
                hour=23,
                minute=59,
                second=59,
                microsecond=(int(constants.MICROSECONDS_PER_SECOND) - 1),
            ),
        )

        dt = attodatetime(
            2001, 1, 1, microsecond=(int(constants.MICROSECONDS_PER_MILLISECOND) - 1)
        )
        td = attotimedelta(milliseconds=1)

        result = dt - td
        self.assertEqual(
            result,
            attodatetime(
                2000,
                12,
                31,
                hour=23,
                minute=59,
                second=59,
                microsecond=(int(constants.MICROSECONDS_PER_SECOND) - 1),
            ),
        )

        dt = attodatetime(2001, 1, 1, nanosecond=1)
        td = attotimedelta(nanoseconds=2)

        result = dt - td
        self.assertEqual(
            result,
            attodatetime(
                2000,
                12,
                31,
                hour=23,
                minute=59,
                second=59,
                microsecond=(int(constants.MICROSECONDS_PER_SECOND) - 1),
                nanosecond=(constants.NANOSECONDS_PER_MICROSECOND - 1),
            ),
        )

        dt = attodatetime(2001, 1, 1)
        td = attotimedelta(nanoseconds=Decimal("0.00000001"))

        result = dt - td
        self.assertEqual(
            result,
            attodatetime(
                2000,
                12,
                31,
                hour=23,
                minute=59,
                second=59,
                microsecond=(int(constants.MICROSECONDS_PER_SECOND) - 1),
                nanosecond=(
                    constants.NANOSECONDS_PER_MICROSECOND - Decimal("0.00000001")
                ),
            ),
        )

    def test_sub_attotimedelta(self):
        dt1 = attodatetime(2001, 2, 2)
        dt2 = attodatetime(2001, 2, 1)

        result = dt1 - dt2
        self.assertEqual(result, attotimedelta(days=1))

        result = dt2 - dt1
        self.assertEqual(result, -attotimedelta(days=1))

        dt1 = attodatetime(2001, 2, 1, second=2)
        dt2 = attodatetime(2001, 2, 1, second=1)

        result = dt1 - dt2
        self.assertEqual(result, attotimedelta(seconds=1))

        result = dt2 - dt1
        self.assertEqual(result, -attotimedelta(seconds=1))

        dt1 = attodatetime(2001, 2, 1, microsecond=2)
        dt2 = attodatetime(2001, 2, 1, microsecond=1)

        result = dt1 - dt2
        self.assertEqual(result, attotimedelta(microseconds=1))

        result = dt2 - dt1
        self.assertEqual(result, -attotimedelta(microseconds=1))

        dt1 = attodatetime(
            2001, 2, 1, microsecond=(2 * int(constants.MICROSECONDS_PER_MILLISECOND))
        )
        dt2 = attodatetime(
            2001, 2, 1, microsecond=(1 * int(constants.MICROSECONDS_PER_MILLISECOND))
        )

        result = dt1 - dt2
        self.assertEqual(
            result,
            attotimedelta(microseconds=(1 * constants.MICROSECONDS_PER_MILLISECOND)),
        )

        result = dt2 - dt1
        self.assertEqual(
            result,
            -attotimedelta(microseconds=(1 * constants.MICROSECONDS_PER_MILLISECOND)),
        )

        dt1 = attodatetime(2001, 2, 1, minute=2)
        dt2 = attodatetime(2001, 2, 1, minute=1)

        result = dt1 - dt2
        self.assertEqual(result, attotimedelta(minutes=1))

        result = dt2 - dt1
        self.assertEqual(result, -attotimedelta(minutes=1))

        dt1 = attodatetime(2001, 2, 1, hour=2)
        dt2 = attodatetime(2001, 2, 1, hour=1)

        result = dt1 - dt2
        self.assertEqual(result, attotimedelta(hours=1))

        result = dt2 - dt1
        self.assertEqual(result, -attotimedelta(hours=1))

        dt1 = attodatetime(2001, 2, 8)
        dt2 = attodatetime(2001, 2, 1)

        result = dt1 - dt2
        self.assertEqual(result, attotimedelta(weeks=1))

        result = dt2 - dt1
        self.assertEqual(result, -attotimedelta(weeks=1))

        dt1 = attodatetime(2001, 2, 1, nanosecond=2)
        dt2 = attodatetime(2001, 2, 1, nanosecond=1)

        result = dt1 - dt2
        self.assertEqual(result, attotimedelta(nanoseconds=1))

        result = dt2 - dt1
        self.assertEqual(result, -attotimedelta(nanoseconds=1))

        dt1 = attodatetime(2001, 2, 1, tzinfo=FixedOffset(0, name="+0"))
        dt2 = attodatetime(2001, 2, 1, tzinfo=FixedOffset(1, name="+1"))

        result = dt1 - dt2
        self.assertEqual(result, attotimedelta(hours=1))

        result = dt2 - dt1
        self.assertEqual(result, -attotimedelta(hours=1))

        with self.assertRaises(TypeError):
            dt1 = attodatetime(2001, 2, 1, tzinfo=FixedOffset(0, name="+0"))
            dt2 = attodatetime(2001, 2, 1)

            dt1 - dt2

        with self.assertRaises(TypeError):
            dt1 = attodatetime(2001, 2, 1)
            dt2 = attodatetime(2001, 2, 1, tzinfo=FixedOffset(0, name="+0"))

            dt1 - dt2

    def test_eq(self):
        self.assertTrue(attodatetime(2001, 2, 3) == attodatetime(2001, 2, 3))
        self.assertTrue(
            attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5
            )
            == attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5
            )
        )
        self.assertTrue(
            attotime(
                hour=1,
                minute=2,
                second=3,
                microsecond=4,
                nanosecond=5,
                tzinfo=FixedOffset(1, name="+1"),
            )
            == attotime(
                hour=1,
                minute=2,
                second=3,
                microsecond=4,
                nanosecond=5,
                tzinfo=FixedOffset(1, name="+1"),
            )
        )

        # Not equals
        self.assertFalse(attodatetime(2001, 2, 3) == attodatetime(2002, 2, 3))
        self.assertFalse(
            attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5
            )
            == attodatetime(
                2001, 3, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5
            )
        )
        self.assertFalse(
            attotime(
                hour=1,
                minute=2,
                second=3,
                microsecond=4,
                nanosecond=5,
                tzinfo=FixedOffset(1, name="+1"),
            )
            == attotime(
                hour=1,
                minute=2,
                second=3,
                microsecond=4,
                nanosecond=5,
                tzinfo=FixedOffset(2, name="+2"),
            )
        )
        self.assertFalse(attodatetime(2001, 2, 3) == datetime.date(2002, 2, 3))

    def test_ne(self):
        # Inverse of test_eq
        self.assertFalse(attodatetime(2001, 2, 3) != attodatetime(2001, 2, 3))
        self.assertFalse(
            attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5
            )
            != attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5
            )
        )
        self.assertFalse(
            attotime(
                hour=1,
                minute=2,
                second=3,
                microsecond=4,
                nanosecond=5,
                tzinfo=FixedOffset(1, name="+1"),
            )
            != attotime(
                hour=1,
                minute=2,
                second=3,
                microsecond=4,
                nanosecond=5,
                tzinfo=FixedOffset(1, name="+1"),
            )
        )

        # Not equals
        self.assertTrue(attodatetime(2001, 2, 3) != attodatetime(2002, 2, 3))
        self.assertTrue(
            attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5
            )
            != attodatetime(
                2001, 3, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5
            )
        )
        self.assertTrue(
            attotime(
                hour=1,
                minute=2,
                second=3,
                microsecond=4,
                nanosecond=5,
                tzinfo=FixedOffset(1, name="+1"),
            )
            != attotime(
                hour=1,
                minute=2,
                second=3,
                microsecond=4,
                nanosecond=5,
                tzinfo=FixedOffset(2, name="+2"),
            )
        )

    def test_gt(self):
        self.assertTrue(attodatetime(2001, 2, 2) > attodatetime(2001, 2, 1))
        self.assertTrue(attodatetime(2001, 3, 1) > attodatetime(2001, 2, 1))
        self.assertTrue(attodatetime(2002, 2, 1) > attodatetime(2001, 2, 1))
        self.assertTrue(attodatetime(2001, 2, 2) > attodatetime(2001, 2, 1, hour=1))
        self.assertTrue(attodatetime(2001, 3, 1) > attodatetime(2001, 2, 1, hour=1))
        self.assertTrue(attodatetime(2002, 2, 1) > attodatetime(2001, 2, 1, hour=1))
        self.assertTrue(attodatetime(2001, 2, 2) > attodatetime(2001, 2, 1, minute=1))
        self.assertTrue(attodatetime(2001, 3, 1) > attodatetime(2001, 2, 1, minute=1))
        self.assertTrue(attodatetime(2002, 2, 1) > attodatetime(2001, 2, 1, minute=1))
        self.assertTrue(attodatetime(2001, 2, 2) > attodatetime(2001, 2, 1, second=1))
        self.assertTrue(attodatetime(2001, 3, 1) > attodatetime(2001, 2, 1, second=1))
        self.assertTrue(attodatetime(2002, 2, 1) > attodatetime(2001, 2, 1, second=1))
        self.assertTrue(
            attodatetime(2001, 2, 2) > attodatetime(2001, 2, 1, microsecond=1)
        )
        self.assertTrue(
            attodatetime(2001, 3, 1) > attodatetime(2001, 2, 1, microsecond=1)
        )
        self.assertTrue(
            attodatetime(2002, 2, 1) > attodatetime(2001, 2, 1, microsecond=1)
        )
        self.assertTrue(
            attodatetime(2001, 2, 2) > attodatetime(2001, 2, 1, nanosecond=0.1)
        )
        self.assertTrue(
            attodatetime(2001, 3, 1) > attodatetime(2001, 2, 1, nanosecond=0.1)
        )
        self.assertTrue(
            attodatetime(2002, 2, 1) > attodatetime(2001, 2, 1, nanosecond=0.1)
        )
        self.assertTrue(attodatetime(2001, 2, 1, hour=1) > attodatetime(2001, 2, 1))
        self.assertTrue(attodatetime(2001, 2, 1, minute=1) > attodatetime(2001, 2, 1))
        self.assertTrue(attodatetime(2001, 2, 1, second=1) > attodatetime(2001, 2, 1))
        self.assertTrue(
            attodatetime(2001, 2, 1, microsecond=1) > attodatetime(2001, 2, 1)
        )
        self.assertTrue(
            attodatetime(2001, 2, 1, nanosecond=0.1) > attodatetime(2001, 2, 1)
        )
        self.assertTrue(
            attodatetime(2001, 2, 2, tzinfo=FixedOffset(1, name="+1"))
            > attodatetime(2001, 2, 1, tzinfo=FixedOffset(1, name="+1"))
        )
        self.assertTrue(
            attodatetime(2001, 2, 1, tzinfo=FixedOffset(0, name="+0"))
            > attodatetime(2001, 2, 1, tzinfo=FixedOffset(1, name="+1"))
        )

        # Equivalances
        self.assertFalse(attodatetime(2001, 2, 3) > attodatetime(2001, 2, 3))
        self.assertFalse(
            attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5
            )
            > attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5
            )
        )
        self.assertFalse(
            attotime(
                hour=1,
                minute=2,
                second=3,
                microsecond=4,
                nanosecond=5,
                tzinfo=FixedOffset(1, name="+1"),
            )
            > attotime(
                hour=1,
                minute=2,
                second=3,
                microsecond=4,
                nanosecond=5,
                tzinfo=FixedOffset(1, name="+1"),
            )
        )

        # Not greaters
        self.assertFalse(attodatetime(2001, 2, 1) > attodatetime(2001, 2, 2))
        self.assertFalse(attodatetime(2001, 2, 1) > attodatetime(2001, 3, 1))
        self.assertFalse(attodatetime(2001, 2, 1) > attodatetime(2002, 2, 1))
        self.assertFalse(attodatetime(2001, 2, 1, hour=1) > attodatetime(2001, 2, 2))
        self.assertFalse(attodatetime(2001, 2, 1, hour=1) > attodatetime(2001, 3, 1))
        self.assertFalse(attodatetime(2001, 2, 1, hour=1) > attodatetime(2002, 2, 1))
        self.assertFalse(attodatetime(2001, 2, 1, minute=1) > attodatetime(2001, 2, 2))
        self.assertFalse(attodatetime(2001, 2, 1, minute=1) > attodatetime(2001, 3, 1))
        self.assertFalse(attodatetime(2001, 2, 1, minute=1) > attodatetime(2002, 2, 1))
        self.assertFalse(attodatetime(2001, 2, 1, second=1) > attodatetime(2001, 2, 2))
        self.assertFalse(attodatetime(2001, 2, 1, second=1) > attodatetime(2001, 3, 1))
        self.assertFalse(attodatetime(2001, 2, 1, second=1) > attodatetime(2002, 2, 1))
        self.assertFalse(
            attodatetime(2001, 2, 1, microsecond=1) > attodatetime(2001, 2, 2)
        )
        self.assertFalse(
            attodatetime(2001, 2, 1, microsecond=1) > attodatetime(2001, 3, 1)
        )
        self.assertFalse(
            attodatetime(2001, 2, 1, microsecond=1) > attodatetime(2002, 2, 1)
        )
        self.assertFalse(
            attodatetime(2001, 2, 1, nanosecond=0.1) > attodatetime(2001, 2, 2)
        )
        self.assertFalse(
            attodatetime(2001, 2, 1, nanosecond=0.1) > attodatetime(2001, 3, 1)
        )
        self.assertFalse(
            attodatetime(2001, 2, 1, nanosecond=0.1) > attodatetime(2002, 2, 1)
        )
        self.assertFalse(attodatetime(2001, 2, 1) > attodatetime(2001, 2, 1, hour=1))
        self.assertFalse(attodatetime(2001, 2, 1) > attodatetime(2001, 2, 1, minute=1))
        self.assertFalse(attodatetime(2001, 2, 1) > attodatetime(2001, 2, 1, second=1))
        self.assertFalse(
            attodatetime(2001, 2, 1) > attodatetime(2001, 2, 1, microsecond=1)
        )
        self.assertFalse(
            attodatetime(2001, 2, 1) > attodatetime(2001, 2, 1, nanosecond=0.1)
        )
        self.assertFalse(
            attodatetime(2001, 2, 1, tzinfo=FixedOffset(1, name="+1"))
            > attodatetime(2001, 2, 2, tzinfo=FixedOffset(1, name="+1"))
        )
        self.assertFalse(
            attodatetime(2001, 2, 1, tzinfo=FixedOffset(1, name="+1"))
            > attodatetime(2001, 2, 1, tzinfo=FixedOffset(0, name="+0"))
        )

        with self.assertRaises(TypeError):
            attodatetime(2001, 2, 1) > datetime.date(2001, 2, 2)

    def test_ge(self):
        self.assertTrue(attodatetime(2001, 2, 2) >= attodatetime(2001, 2, 1))
        self.assertTrue(attodatetime(2001, 3, 1) >= attodatetime(2001, 2, 1))
        self.assertTrue(attodatetime(2002, 2, 1) >= attodatetime(2001, 2, 1))
        self.assertTrue(attodatetime(2001, 2, 2) >= attodatetime(2001, 2, 1, hour=1))
        self.assertTrue(attodatetime(2001, 3, 1) >= attodatetime(2001, 2, 1, hour=1))
        self.assertTrue(attodatetime(2002, 2, 1) >= attodatetime(2001, 2, 1, hour=1))
        self.assertTrue(attodatetime(2001, 2, 2) >= attodatetime(2001, 2, 1, minute=1))
        self.assertTrue(attodatetime(2001, 3, 1) >= attodatetime(2001, 2, 1, minute=1))
        self.assertTrue(attodatetime(2002, 2, 1) >= attodatetime(2001, 2, 1, minute=1))
        self.assertTrue(attodatetime(2001, 2, 2) >= attodatetime(2001, 2, 1, second=1))
        self.assertTrue(attodatetime(2001, 3, 1) >= attodatetime(2001, 2, 1, second=1))
        self.assertTrue(attodatetime(2002, 2, 1) >= attodatetime(2001, 2, 1, second=1))
        self.assertTrue(
            attodatetime(2001, 2, 2) >= attodatetime(2001, 2, 1, microsecond=1)
        )
        self.assertTrue(
            attodatetime(2001, 3, 1) >= attodatetime(2001, 2, 1, microsecond=1)
        )
        self.assertTrue(
            attodatetime(2002, 2, 1) >= attodatetime(2001, 2, 1, microsecond=1)
        )
        self.assertTrue(
            attodatetime(2001, 2, 2) >= attodatetime(2001, 2, 1, nanosecond=0.1)
        )
        self.assertTrue(
            attodatetime(2001, 3, 1) >= attodatetime(2001, 2, 1, nanosecond=0.1)
        )
        self.assertTrue(
            attodatetime(2002, 2, 1) >= attodatetime(2001, 2, 1, nanosecond=0.1)
        )
        self.assertTrue(attodatetime(2001, 2, 1, hour=1) >= attodatetime(2001, 2, 1))
        self.assertTrue(attodatetime(2001, 2, 1, minute=1) >= attodatetime(2001, 2, 1))
        self.assertTrue(attodatetime(2001, 2, 1, second=1) >= attodatetime(2001, 2, 1))
        self.assertTrue(
            attodatetime(2001, 2, 1, microsecond=1) >= attodatetime(2001, 2, 1)
        )
        self.assertTrue(
            attodatetime(2001, 2, 1, nanosecond=0.1) >= attodatetime(2001, 2, 1)
        )
        self.assertTrue(
            attodatetime(2001, 2, 2, tzinfo=FixedOffset(1, name="+1"))
            >= attodatetime(2001, 2, 1, tzinfo=FixedOffset(1, name="+1"))
        )
        self.assertTrue(
            attodatetime(2001, 2, 1, tzinfo=FixedOffset(0, name="+0"))
            >= attodatetime(2001, 2, 1, tzinfo=FixedOffset(1, name="+1"))
        )

        # Equivalances
        self.assertTrue(attodatetime(2001, 2, 3) >= attodatetime(2001, 2, 3))
        self.assertTrue(
            attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5
            )
            >= attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5
            )
        )
        self.assertTrue(
            attotime(
                hour=1,
                minute=2,
                second=3,
                microsecond=4,
                nanosecond=5,
                tzinfo=FixedOffset(1, name="+1"),
            )
            >= attotime(
                hour=1,
                minute=2,
                second=3,
                microsecond=4,
                nanosecond=5,
                tzinfo=FixedOffset(1, name="+1"),
            )
        )

        # Not greaters
        self.assertFalse(attodatetime(2001, 2, 1) >= attodatetime(2001, 2, 2))
        self.assertFalse(attodatetime(2001, 2, 1) >= attodatetime(2001, 3, 1))
        self.assertFalse(attodatetime(2001, 2, 1) >= attodatetime(2002, 2, 1))
        self.assertFalse(attodatetime(2001, 2, 1, hour=1) >= attodatetime(2001, 2, 2))
        self.assertFalse(attodatetime(2001, 2, 1, hour=1) >= attodatetime(2001, 3, 1))
        self.assertFalse(attodatetime(2001, 2, 1, hour=1) >= attodatetime(2002, 2, 1))
        self.assertFalse(attodatetime(2001, 2, 1, minute=1) >= attodatetime(2001, 2, 2))
        self.assertFalse(attodatetime(2001, 2, 1, minute=1) >= attodatetime(2001, 3, 1))
        self.assertFalse(attodatetime(2001, 2, 1, minute=1) >= attodatetime(2002, 2, 1))
        self.assertFalse(attodatetime(2001, 2, 1, second=1) >= attodatetime(2001, 2, 2))
        self.assertFalse(attodatetime(2001, 2, 1, second=1) >= attodatetime(2001, 3, 1))
        self.assertFalse(attodatetime(2001, 2, 1, second=1) >= attodatetime(2002, 2, 1))
        self.assertFalse(
            attodatetime(2001, 2, 1, microsecond=1) >= attodatetime(2001, 2, 2)
        )
        self.assertFalse(
            attodatetime(2001, 2, 1, microsecond=1) >= attodatetime(2001, 3, 1)
        )
        self.assertFalse(
            attodatetime(2001, 2, 1, microsecond=1) >= attodatetime(2002, 2, 1)
        )
        self.assertFalse(
            attodatetime(2001, 2, 1, nanosecond=0.1) >= attodatetime(2001, 2, 2)
        )
        self.assertFalse(
            attodatetime(2001, 2, 1, nanosecond=0.1) >= attodatetime(2001, 3, 1)
        )
        self.assertFalse(
            attodatetime(2001, 2, 1, nanosecond=0.1) >= attodatetime(2002, 2, 1)
        )
        self.assertFalse(attodatetime(2001, 2, 1) >= attodatetime(2001, 2, 1, hour=1))
        self.assertFalse(attodatetime(2001, 2, 1) >= attodatetime(2001, 2, 1, minute=1))
        self.assertFalse(attodatetime(2001, 2, 1) >= attodatetime(2001, 2, 1, second=1))
        self.assertFalse(
            attodatetime(2001, 2, 1) >= attodatetime(2001, 2, 1, microsecond=1)
        )
        self.assertFalse(
            attodatetime(2001, 2, 1) >= attodatetime(2001, 2, 1, nanosecond=0.1)
        )
        self.assertFalse(
            attodatetime(2001, 2, 1, tzinfo=FixedOffset(1, name="+1"))
            >= attodatetime(2001, 2, 2, tzinfo=FixedOffset(1, name="+1"))
        )
        self.assertFalse(
            attodatetime(2001, 2, 1, tzinfo=FixedOffset(1, name="+1"))
            >= attodatetime(2001, 2, 1, tzinfo=FixedOffset(0, name="+0"))
        )

        with self.assertRaises(TypeError):
            attodatetime(2001, 2, 1) >= datetime.date(2001, 2, 2)

    def test_lt(self):
        self.assertTrue(attodatetime(2001, 2, 1) < attodatetime(2001, 2, 2))
        self.assertTrue(attodatetime(2001, 2, 1) < attodatetime(2001, 3, 1))
        self.assertTrue(attodatetime(2001, 2, 1) < attodatetime(2002, 2, 1))
        self.assertTrue(attodatetime(2001, 2, 1, hour=1) < attodatetime(2001, 2, 2))
        self.assertTrue(attodatetime(2001, 2, 1, hour=1) < attodatetime(2001, 3, 1))
        self.assertTrue(attodatetime(2001, 2, 1, hour=1) < attodatetime(2002, 2, 1))
        self.assertTrue(attodatetime(2001, 2, 1, minute=1) < attodatetime(2001, 2, 2))
        self.assertTrue(attodatetime(2001, 2, 1, minute=1) < attodatetime(2001, 3, 1))
        self.assertTrue(attodatetime(2001, 2, 1, minute=1) < attodatetime(2002, 2, 1))
        self.assertTrue(attodatetime(2001, 2, 1, second=1) < attodatetime(2001, 2, 2))
        self.assertTrue(attodatetime(2001, 2, 1, second=1) < attodatetime(2001, 3, 1))
        self.assertTrue(attodatetime(2001, 2, 1, second=1) < attodatetime(2002, 2, 1))
        self.assertTrue(
            attodatetime(2001, 2, 1, microsecond=1) < attodatetime(2001, 2, 2)
        )
        self.assertTrue(
            attodatetime(2001, 2, 1, microsecond=1) < attodatetime(2001, 3, 1)
        )
        self.assertTrue(
            attodatetime(2001, 2, 1, microsecond=1) < attodatetime(2002, 2, 1)
        )
        self.assertTrue(
            attodatetime(2001, 2, 1, nanosecond=0.1) < attodatetime(2001, 2, 2)
        )
        self.assertTrue(
            attodatetime(2001, 2, 1, nanosecond=0.1) < attodatetime(2001, 3, 1)
        )
        self.assertTrue(
            attodatetime(2001, 2, 1, nanosecond=0.1) < attodatetime(2002, 2, 1)
        )
        self.assertTrue(attodatetime(2001, 2, 1) < attodatetime(2001, 2, 1, hour=1))
        self.assertTrue(attodatetime(2001, 2, 1) < attodatetime(2001, 2, 1, minute=1))
        self.assertTrue(attodatetime(2001, 2, 1) < attodatetime(2001, 2, 1, second=1))
        self.assertTrue(
            attodatetime(2001, 2, 1) < attodatetime(2001, 2, 1, microsecond=1)
        )
        self.assertTrue(
            attodatetime(2001, 2, 1) < attodatetime(2001, 2, 1, nanosecond=0.1)
        )
        self.assertTrue(
            attodatetime(2001, 2, 1, tzinfo=FixedOffset(1, name="+1"))
            < attodatetime(2001, 2, 2, tzinfo=FixedOffset(1, name="+1"))
        )
        self.assertTrue(
            attodatetime(2001, 2, 1, tzinfo=FixedOffset(1, name="+1"))
            < attodatetime(2001, 2, 1, tzinfo=FixedOffset(0, name="+0"))
        )

        # Equivalances
        self.assertFalse(attodatetime(2001, 2, 3) < attodatetime(2001, 2, 3))
        self.assertFalse(
            attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5
            )
            < attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5
            )
        )
        self.assertFalse(
            attotime(
                hour=1,
                minute=2,
                second=3,
                microsecond=4,
                nanosecond=5,
                tzinfo=FixedOffset(1, name="+1"),
            )
            < attotime(
                hour=1,
                minute=2,
                second=3,
                microsecond=4,
                nanosecond=5,
                tzinfo=FixedOffset(1, name="+1"),
            )
        )

        # Not lessers
        self.assertFalse(attodatetime(2001, 2, 2) < attodatetime(2001, 2, 1))
        self.assertFalse(attodatetime(2001, 3, 1) < attodatetime(2001, 2, 1))
        self.assertFalse(attodatetime(2002, 2, 1) < attodatetime(2001, 2, 1))
        self.assertFalse(attodatetime(2001, 2, 2) < attodatetime(2001, 2, 1, hour=1))
        self.assertFalse(attodatetime(2001, 3, 1) < attodatetime(2001, 2, 1, hour=1))
        self.assertFalse(attodatetime(2002, 2, 1) < attodatetime(2001, 2, 1, hour=1))
        self.assertFalse(attodatetime(2001, 2, 2) < attodatetime(2001, 2, 1, minute=1))
        self.assertFalse(attodatetime(2001, 3, 1) < attodatetime(2001, 2, 1, minute=1))
        self.assertFalse(attodatetime(2002, 2, 1) < attodatetime(2001, 2, 1, minute=1))
        self.assertFalse(attodatetime(2001, 2, 2) < attodatetime(2001, 2, 1, second=1))
        self.assertFalse(attodatetime(2001, 3, 1) < attodatetime(2001, 2, 1, second=1))
        self.assertFalse(attodatetime(2002, 2, 1) < attodatetime(2001, 2, 1, second=1))
        self.assertFalse(
            attodatetime(2001, 2, 2) < attodatetime(2001, 2, 1, microsecond=1)
        )
        self.assertFalse(
            attodatetime(2001, 3, 1) < attodatetime(2001, 2, 1, microsecond=1)
        )
        self.assertFalse(
            attodatetime(2002, 2, 1) < attodatetime(2001, 2, 1, microsecond=1)
        )
        self.assertFalse(
            attodatetime(2001, 2, 2) < attodatetime(2001, 2, 1, nanosecond=0.1)
        )
        self.assertFalse(
            attodatetime(2001, 3, 1) < attodatetime(2001, 2, 1, nanosecond=0.1)
        )
        self.assertFalse(
            attodatetime(2002, 2, 1) < attodatetime(2001, 2, 1, nanosecond=0.1)
        )
        self.assertFalse(attodatetime(2001, 2, 1, hour=1) < attodatetime(2001, 2, 1))
        self.assertFalse(attodatetime(2001, 2, 1, minute=1) < attodatetime(2001, 2, 1))
        self.assertFalse(attodatetime(2001, 2, 1, second=1) < attodatetime(2001, 2, 1))
        self.assertFalse(
            attodatetime(2001, 2, 1, microsecond=1) < attodatetime(2001, 2, 1)
        )
        self.assertFalse(
            attodatetime(2001, 2, 1, nanosecond=0.1) < attodatetime(2001, 2, 1)
        )
        self.assertFalse(
            attodatetime(2001, 2, 2, tzinfo=FixedOffset(1, name="+1"))
            < attodatetime(2001, 2, 1, tzinfo=FixedOffset(1, name="+1"))
        )
        self.assertFalse(
            attodatetime(2001, 2, 1, tzinfo=FixedOffset(0, name="+0"))
            < attodatetime(2001, 2, 1, tzinfo=FixedOffset(1, name="+1"))
        )

        with self.assertRaises(TypeError):
            attodatetime(2001, 2, 2) < datetime.date(2001, 2, 1)

    def test_le(self):
        self.assertTrue(attodatetime(2001, 2, 1) <= attodatetime(2001, 2, 2))
        self.assertTrue(attodatetime(2001, 2, 1) <= attodatetime(2001, 3, 1))
        self.assertTrue(attodatetime(2001, 2, 1) <= attodatetime(2002, 2, 1))
        self.assertTrue(attodatetime(2001, 2, 1, hour=1) <= attodatetime(2001, 2, 2))
        self.assertTrue(attodatetime(2001, 2, 1, hour=1) <= attodatetime(2001, 3, 1))
        self.assertTrue(attodatetime(2001, 2, 1, hour=1) <= attodatetime(2002, 2, 1))
        self.assertTrue(attodatetime(2001, 2, 1, minute=1) <= attodatetime(2001, 2, 2))
        self.assertTrue(attodatetime(2001, 2, 1, minute=1) <= attodatetime(2001, 3, 1))
        self.assertTrue(attodatetime(2001, 2, 1, minute=1) <= attodatetime(2002, 2, 1))
        self.assertTrue(attodatetime(2001, 2, 1, second=1) <= attodatetime(2001, 2, 2))
        self.assertTrue(attodatetime(2001, 2, 1, second=1) <= attodatetime(2001, 3, 1))
        self.assertTrue(attodatetime(2001, 2, 1, second=1) <= attodatetime(2002, 2, 1))
        self.assertTrue(
            attodatetime(2001, 2, 1, microsecond=1) <= attodatetime(2001, 2, 2)
        )
        self.assertTrue(
            attodatetime(2001, 2, 1, microsecond=1) <= attodatetime(2001, 3, 1)
        )
        self.assertTrue(
            attodatetime(2001, 2, 1, microsecond=1) <= attodatetime(2002, 2, 1)
        )
        self.assertTrue(
            attodatetime(2001, 2, 1, nanosecond=0.1) <= attodatetime(2001, 2, 2)
        )
        self.assertTrue(
            attodatetime(2001, 2, 1, nanosecond=0.1) <= attodatetime(2001, 3, 1)
        )
        self.assertTrue(
            attodatetime(2001, 2, 1, nanosecond=0.1) <= attodatetime(2002, 2, 1)
        )
        self.assertTrue(attodatetime(2001, 2, 1) <= attodatetime(2001, 2, 1, hour=1))
        self.assertTrue(attodatetime(2001, 2, 1) <= attodatetime(2001, 2, 1, minute=1))
        self.assertTrue(attodatetime(2001, 2, 1) <= attodatetime(2001, 2, 1, second=1))
        self.assertTrue(
            attodatetime(2001, 2, 1) <= attodatetime(2001, 2, 1, microsecond=1)
        )
        self.assertTrue(
            attodatetime(2001, 2, 1) <= attodatetime(2001, 2, 1, nanosecond=0.1)
        )
        self.assertTrue(
            attodatetime(2001, 2, 1, tzinfo=FixedOffset(1, name="+1"))
            <= attodatetime(2001, 2, 2, tzinfo=FixedOffset(1, name="+1"))
        )
        self.assertTrue(
            attodatetime(2001, 2, 1, tzinfo=FixedOffset(1, name="+1"))
            <= attodatetime(2001, 2, 1, tzinfo=FixedOffset(0, name="+0"))
        )

        # Equivalances
        self.assertTrue(attodatetime(2001, 2, 3) <= attodatetime(2001, 2, 3))
        self.assertTrue(
            attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5
            )
            <= attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5
            )
        )
        self.assertTrue(
            attotime(
                hour=1,
                minute=2,
                second=3,
                microsecond=4,
                nanosecond=5,
                tzinfo=FixedOffset(1, name="+1"),
            )
            <= attotime(
                hour=1,
                minute=2,
                second=3,
                microsecond=4,
                nanosecond=5,
                tzinfo=FixedOffset(1, name="+1"),
            )
        )

        # Not lessers
        self.assertFalse(attodatetime(2001, 2, 2) <= attodatetime(2001, 2, 1))
        self.assertFalse(attodatetime(2001, 3, 1) <= attodatetime(2001, 2, 1))
        self.assertFalse(attodatetime(2002, 2, 1) <= attodatetime(2001, 2, 1))
        self.assertFalse(attodatetime(2001, 2, 2) <= attodatetime(2001, 2, 1, hour=1))
        self.assertFalse(attodatetime(2001, 3, 1) <= attodatetime(2001, 2, 1, hour=1))
        self.assertFalse(attodatetime(2002, 2, 1) <= attodatetime(2001, 2, 1, hour=1))
        self.assertFalse(attodatetime(2001, 2, 2) <= attodatetime(2001, 2, 1, minute=1))
        self.assertFalse(attodatetime(2001, 3, 1) <= attodatetime(2001, 2, 1, minute=1))
        self.assertFalse(attodatetime(2002, 2, 1) <= attodatetime(2001, 2, 1, minute=1))
        self.assertFalse(attodatetime(2001, 2, 2) <= attodatetime(2001, 2, 1, second=1))
        self.assertFalse(attodatetime(2001, 3, 1) <= attodatetime(2001, 2, 1, second=1))
        self.assertFalse(attodatetime(2002, 2, 1) <= attodatetime(2001, 2, 1, second=1))
        self.assertFalse(
            attodatetime(2001, 2, 2) <= attodatetime(2001, 2, 1, microsecond=1)
        )
        self.assertFalse(
            attodatetime(2001, 3, 1) <= attodatetime(2001, 2, 1, microsecond=1)
        )
        self.assertFalse(
            attodatetime(2002, 2, 1) <= attodatetime(2001, 2, 1, microsecond=1)
        )
        self.assertFalse(
            attodatetime(2001, 2, 2) <= attodatetime(2001, 2, 1, nanosecond=0.1)
        )
        self.assertFalse(
            attodatetime(2001, 3, 1) <= attodatetime(2001, 2, 1, nanosecond=0.1)
        )
        self.assertFalse(
            attodatetime(2002, 2, 1) <= attodatetime(2001, 2, 1, nanosecond=0.1)
        )
        self.assertFalse(attodatetime(2001, 2, 1, hour=1) <= attodatetime(2001, 2, 1))
        self.assertFalse(attodatetime(2001, 2, 1, minute=1) <= attodatetime(2001, 2, 1))
        self.assertFalse(attodatetime(2001, 2, 1, second=1) <= attodatetime(2001, 2, 1))
        self.assertFalse(
            attodatetime(2001, 2, 1, microsecond=1) <= attodatetime(2001, 2, 1)
        )
        self.assertFalse(
            attodatetime(2001, 2, 1, nanosecond=0.1) <= attodatetime(2001, 2, 1)
        )
        self.assertFalse(
            attodatetime(2001, 2, 2, tzinfo=FixedOffset(1, name="+1"))
            <= attodatetime(2001, 2, 1, tzinfo=FixedOffset(1, name="+1"))
        )
        self.assertFalse(
            attodatetime(2001, 2, 1, tzinfo=FixedOffset(0, name="+0"))
            <= attodatetime(2001, 2, 1, tzinfo=FixedOffset(1, name="+1"))
        )

        with self.assertRaises(TypeError):
            attodatetime(2001, 2, 2) <= datetime.date(2001, 2, 1)

    def test_str(self):
        self.assertEqual(str(attodatetime(2001, 2, 3)), "2001-02-03 00:00:00")
        self.assertEqual(str(attodatetime(2001, 2, 3, hour=1)), "2001-02-03 01:00:00")
        self.assertEqual(
            str(attodatetime(2001, 2, 3, hour=1, minute=2)), "2001-02-03 01:02:00"
        )
        self.assertEqual(
            str(attodatetime(2001, 2, 3, hour=1, minute=2, second=3)),
            "2001-02-03 01:02:03",
        )
        self.assertEqual(
            str(attodatetime(2001, 2, 3, hour=1, minute=2, second=3, microsecond=4)),
            "2001-02-03 01:02:03.000004",
        )
        self.assertEqual(
            str(
                attodatetime(
                    2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=6
                )
            ),
            "2001-02-03 01:02:03.000004006",
        )
        self.assertEqual(
            str(
                attodatetime(
                    2001,
                    2,
                    3,
                    hour=1,
                    minute=2,
                    second=3,
                    microsecond=4,
                    nanosecond=Decimal("0.006"),
                )
            ),
            "2001-02-03 01:02:03.000004000006",
        )
        self.assertEqual(
            str(
                attodatetime(
                    2001,
                    2,
                    3,
                    hour=1,
                    minute=2,
                    second=3,
                    microsecond=4,
                    nanosecond=Decimal("0.006"),
                    tzinfo=DSTOffset(1, name="+1"),
                )
            ),
            "2001-02-03 01:02:03.000004000006+01:00",
        )
        self.assertEqual(
            str(
                attodatetime(
                    2001,
                    2,
                    3,
                    hour=1,
                    minute=2,
                    second=3,
                    microsecond=4,
                    nanosecond=Decimal("0.006"),
                    tzinfo=DSTOffset(-1, name="-1"),
                )
            ),
            "2001-02-03 01:02:03.000004000006-01:00",
        )

    def test_repr(self):
        self.assertEqual(
            attodatetime(2001, 2, 3).__repr__(),
            "attotime.objects.attodatetime(2001, 2, 3, 0, 0, 0, 0, 0)",
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, hour=1).__repr__(),
            "attotime.objects.attodatetime(2001, 2, 3, 1, 0, 0, 0, 0)",
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, hour=1, minute=2).__repr__(),
            "attotime.objects.attodatetime(2001, 2, 3, 1, 2, 0, 0, 0)",
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, hour=1, minute=2, second=3).__repr__(),
            "attotime.objects.attodatetime(2001, 2, 3, 1, 2, 3, 0, 0)",
        )
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4
            ).__repr__(),
            "attotime.objects.attodatetime(2001, 2, 3, 1, 2, 3, 4, 0)",
        )
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=6
            ).__repr__(),
            "attotime.objects.attodatetime(2001, 2, 3, 1, 2, 3, 4, 6)",
        )
        self.assertEqual(
            attodatetime(
                2001,
                2,
                3,
                hour=1,
                minute=2,
                second=3,
                microsecond=4,
                nanosecond=Decimal("0.006"),
            ).__repr__(),
            "attotime.objects.attodatetime(2001, 2, 3, 1, 2, 3, 4, 0.006)",
        )
        self.assertEqual(
            attodatetime(
                2001,
                2,
                3,
                hour=1,
                minute=2,
                second=3,
                microsecond=4,
                nanosecond=Decimal("0.006"),
                tzinfo=DSTOffset(1, name="+1"),
            ).__repr__(),
            "attotime.objects.attodatetime(2001, 2, 3, 1, 2, 3, 4, 0.006, +1)",
        )
        self.assertEqual(
            attodatetime(
                2001,
                2,
                3,
                hour=1,
                minute=2,
                second=3,
                microsecond=4,
                nanosecond=Decimal("0.006"),
                tzinfo=DSTOffset(-1, name="-1"),
            ).__repr__(),
            "attotime.objects.attodatetime(2001, 2, 3, 1, 2, 3, 4, 0.006, -1)",
        )

    def test_format(self):
        self.assertEqual("{0:%w}".format(attodatetime(2001, 2, 3)), "6")
        self.assertEqual("{0:%d}".format(attodatetime(2001, 2, 3)), "03")
        self.assertEqual("{0:%m}".format(attodatetime(2001, 2, 3)), "02")
        self.assertEqual("{0:%y}".format(attodatetime(2001, 2, 3)), "01")
        self.assertEqual("{0:%Y}".format(attodatetime(2001, 2, 3)), "2001")

        self.assertEqual(
            "{0:%H}".format(
                attodatetime(
                    2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
                )
            ),
            "14",
        )
        self.assertEqual(
            "{0:%I}".format(
                attodatetime(
                    2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
                )
            ),
            "02",
        )
        self.assertEqual(
            "{0:%M}".format(
                attodatetime(
                    2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
                )
            ),
            "25",
        )
        self.assertEqual(
            "{0:%S}".format(
                attodatetime(
                    2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
                )
            ),
            "36",
        )
        self.assertEqual(
            "{0:%f}".format(
                attodatetime(
                    2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
                )
            ),
            "789123",
        )
        self.assertEqual(
            "{0:%z}".format(
                attodatetime(
                    2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
                )
            ),
            "",
        )
        self.assertEqual(
            "{0:%Z}".format(
                attodatetime(
                    2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
                )
            ),
            "",
        )
        self.assertEqual(
            "{0:%j}".format(
                attodatetime(
                    2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
                )
            ),
            "034",
        )
        self.assertEqual(
            "{0:%U}".format(
                attodatetime(
                    2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
                )
            ),
            "04",
        )
        self.assertEqual(
            "{0:%W}".format(
                attodatetime(
                    2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
                )
            ),
            "05",
        )
        self.assertEqual(
            "{0:%%}".format(
                attodatetime(
                    2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
                )
            ),
            "%",
        )

        self.assertEqual(
            "{0:%o}".format(attodatetime(2001, 2, 3, nanosecond=Decimal("0.0001"))),
            "000000",
        )
        self.assertEqual(
            "{0:%o}".format(attodatetime(2001, 2, 3, nanosecond=Decimal("0.001"))),
            "000001",
        )
        self.assertEqual(
            "{0:%o}".format(attodatetime(2001, 2, 3, nanosecond=Decimal("0.01"))),
            "000010",
        )
        self.assertEqual(
            "{0:%o}".format(attodatetime(2001, 2, 3, nanosecond=Decimal("0.1"))),
            "000100",
        )
        self.assertEqual(
            "{0:%o}".format(attodatetime(2001, 2, 3, nanosecond=1)), "001000"
        )
        self.assertEqual(
            "{0:%o}".format(attodatetime(2001, 2, 3, nanosecond=10)), "010000"
        )
        self.assertEqual(
            "{0:%o}".format(attodatetime(2001, 2, 3, nanosecond=100)), "100000"
        )

        self.assertEqual(
            "{0:%q}".format(
                attodatetime(2001, 2, 3, nanosecond=Decimal("0.0000000001"))
            ),
            "000000",
        )
        self.assertEqual(
            "{0:%q}".format(
                attodatetime(2001, 2, 3, nanosecond=Decimal("0.000000001"))
            ),
            "000001",
        )
        self.assertEqual(
            "{0:%q}".format(attodatetime(2001, 2, 3, nanosecond=Decimal("0.00000001"))),
            "000010",
        )
        self.assertEqual(
            "{0:%q}".format(attodatetime(2001, 2, 3, nanosecond=Decimal("0.0000001"))),
            "000100",
        )
        self.assertEqual(
            "{0:%q}".format(attodatetime(2001, 2, 3, nanosecond=Decimal("0.000001"))),
            "001000",
        )
        self.assertEqual(
            "{0:%q}".format(attodatetime(2001, 2, 3, nanosecond=Decimal("0.00001"))),
            "010000",
        )
        self.assertEqual(
            "{0:%q}".format(attodatetime(2001, 2, 3, nanosecond=Decimal("0.0001"))),
            "100000",
        )

        self.assertEqual(
            "{0:%v}".format(
                attodatetime(2001, 2, 3, nanosecond=Decimal("0.0000000000000001"))
            ),
            "000000",
        )
        self.assertEqual(
            "{0:%v}".format(
                attodatetime(2001, 2, 3, nanosecond=Decimal("0.000000000000001"))
            ),
            "000001",
        )
        self.assertEqual(
            "{0:%v}".format(
                attodatetime(2001, 2, 3, nanosecond=Decimal("0.00000000000001"))
            ),
            "000010",
        )
        self.assertEqual(
            "{0:%v}".format(
                attodatetime(2001, 2, 3, nanosecond=Decimal("0.0000000000001"))
            ),
            "000100",
        )
        self.assertEqual(
            "{0:%v}".format(
                attodatetime(2001, 2, 3, nanosecond=Decimal("0.000000000001"))
            ),
            "001000",
        )
        self.assertEqual(
            "{0:%v}".format(
                attodatetime(2001, 2, 3, nanosecond=Decimal("0.00000000001"))
            ),
            "010000",
        )
        self.assertEqual(
            "{0:%v}".format(
                attodatetime(2001, 2, 3, nanosecond=Decimal("0.0000000001"))
            ),
            "100000",
        )

        # Note truncation of sub-yoctosecond precision
        self.assertEqual(
            "{0:%S.%f%o%q%v}".format(
                attodatetime(
                    2001,
                    2,
                    3,
                    second=12,
                    microsecond=345678,
                    nanosecond=Decimal("912.3456789123456789"),
                )
            ),
            "12.345678912345678912345678",
        )

        # Timezone tests
        self.assertEqual(
            "{0:%z}".format(attodatetime(2001, 2, 3, tzinfo=DSTOffset(1, name="+1"))),
            "+0100",
        )
        self.assertEqual(
            "{0:%z}".format(attodatetime(2001, 2, 3, tzinfo=DSTOffset(10, name="+10"))),
            "+1000",
        )
        self.assertEqual(
            "{0:%Z}".format(attodatetime(2001, 2, 3, tzinfo=DSTOffset(1, name="+1"))),
            "+1",
        )

        self.assertEqual(
            "{0:%z}".format(attodatetime(2001, 2, 3, tzinfo=DSTOffset(-1, name="-1"))),
            "-0100",
        )
        self.assertEqual(
            "{0:%z}".format(
                attodatetime(2001, 2, 3, tzinfo=DSTOffset(-10, name="-10"))
            ),
            "-1000",
        )
        self.assertEqual(
            "{0:%Z}".format(attodatetime(2001, 2, 3, tzinfo=DSTOffset(-1, name="-1"))),
            "-1",
        )

        # Locale specific
        self.assertEqual(
            "{0:%a}".format(attodatetime(2001, 2, 3)),
            datetime.datetime(2001, 2, 3).strftime("%a"),
        )
        self.assertEqual(
            "{0:%A}".format(attodatetime(2001, 2, 3)),
            datetime.datetime(2001, 2, 3).strftime("%A"),
        )
        self.assertEqual(
            "{0:%b}".format(attodatetime(2001, 2, 3)),
            datetime.datetime(2001, 2, 3).strftime("%b"),
        )
        self.assertEqual(
            "{0:%B}".format(attodatetime(2001, 2, 3)),
            datetime.datetime(2001, 2, 3).strftime("%B"),
        )
        self.assertEqual(
            "{0:%p}".format(
                attodatetime(
                    2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
                )
            ),
            datetime.datetime(
                2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
            ).strftime("%p"),
        )
        self.assertEqual(
            "{0:%c}".format(
                attodatetime(
                    2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
                )
            ),
            datetime.datetime(
                2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
            ).strftime("%c"),
        )
        self.assertEqual(
            "{0:%x}".format(
                attodatetime(
                    2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
                )
            ),
            datetime.datetime(
                2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
            ).strftime("%x"),
        )
        self.assertEqual(
            "{0:%X}".format(
                attodatetime(
                    2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
                )
            ),
            datetime.datetime(
                2001, 2, 3, hour=14, minute=25, second=36, microsecond=789123
            ).strftime("%X"),
        )

    def test_as_datetime(self):
        self.assertEqual(
            attodatetime(2001, 2, 3)._as_datetime(), datetime.datetime(2001, 2, 3)
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, hour=1)._as_datetime(),
            datetime.datetime(2001, 2, 3, hour=1),
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, hour=1, minute=2)._as_datetime(),
            datetime.datetime(2001, 2, 3, hour=1, minute=2),
        )
        self.assertEqual(
            attodatetime(2001, 2, 3, hour=1, minute=2, second=3)._as_datetime(),
            datetime.datetime(2001, 2, 3, hour=1, minute=2, second=3),
        )
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4
            )._as_datetime(),
            datetime.datetime(2001, 2, 3, hour=1, minute=2, second=3, microsecond=4),
        )

        # Nanosecond precision is lost
        self.assertEqual(
            attodatetime(
                2001, 2, 3, hour=1, minute=2, second=3, microsecond=4, nanosecond=5
            )._as_datetime(),
            datetime.datetime(2001, 2, 3, hour=1, minute=2, second=3, microsecond=4),
        )
