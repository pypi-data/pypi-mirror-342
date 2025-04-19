# -*- coding: utf-8 -*-

# Copyright (c) 2021, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import time
import unittest

from attotime.tests.compat import mock
from attotime.util import strptime

# Used for forcing a locale
LOCALE_DAY_ABBRS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
LOCALE_DAY_NAMES = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

LOCALE_MONTH_ABBRS = [
    "",
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
LOCALE_MONTH_NAMES = [
    "",
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def _mock_strftime(format, timetuple):
    if timetuple == time.struct_time((1999, 3, 17, 22, 44, 55, 2, 76, 0)):
        if format == "%p":
            return "PM"
        elif format == "%c":
            return "Wed Mar 17 22:44:55 1999"
        elif format == "%x":
            return "03/17/99"
        elif format == "%X":
            return "22:44:55"
    elif timetuple == time.struct_time((1999, 1, 3, 1, 1, 1, 6, 3, 0)):
        if format == "%c":
            return "Sun Jan 3 01:01:01 1999"
        elif format == "%x":
            return "01/03/99"
        elif format == "%X":
            return "01:01:01"


class TestStrptimeFunctions(unittest.TestCase):
    def test_get_format_fields(self):
        self.assertEqual(
            strptime.get_format_fields(
                "%a%A%w%d%b%B%m%y%Y%H%I%p%M%S%f%z%Z%j%U%W%c%x%X%%"
            ),
            [
                "%a",
                "%A",
                "%w",
                "%d",
                "%b",
                "%B",
                "%m",
                "%y",
                "%Y",
                "%H",
                "%I",
                "%p",
                "%M",
                "%S",
                "%f",
                "%z",
                "%Z",
                "%j",
                "%U",
                "%W",
                "%c",
                "%x",
                "%X",
                "%%",
            ],
        )
        self.assertEqual(strptime.get_format_fields("%o%q%v"), ["%o", "%q", "%v"])
        self.assertEqual(strptime.get_format_fields("abcd"), ["abcd"])
        self.assertEqual(
            strptime.get_format_fields("%a abcd %X"), ["%a", " abcd ", "%X"]
        )

        self.assertEqual(strptime.get_format_fields(""), [])

    @mock.patch(
        "attotime.util.strptime.calendar.day_abbr",
        new_callable=mock.PropertyMock(return_value=LOCALE_DAY_ABBRS),
    )
    @mock.patch(
        "attotime.util.strptime.calendar.day_name",
        new_callable=mock.PropertyMock(return_value=LOCALE_DAY_NAMES),
    )
    @mock.patch(
        "attotime.util.strptime.calendar.month_abbr",
        new_callable=mock.PropertyMock(return_value=LOCALE_MONTH_ABBRS),
    )
    @mock.patch(
        "attotime.util.strptime.calendar.month_name",
        new_callable=mock.PropertyMock(return_value=LOCALE_MONTH_NAMES),
    )
    @mock.patch("attotime.util.strptime.time.strftime")
    def test_expand_format_fields(
        self, mockStrftime, mockMonthName, mockMonthAbbr, mockDayName, mockDayAbbr
    ):
        self.assertEqual(
            strptime.expand_format_fields(
                [
                    "%a",
                    "%A",
                    "%w",
                    "%d",
                    "%b",
                    "%B",
                    "%m",
                    "%y",
                    "%Y",
                    "%H",
                    "%I",
                    "%p",
                    "%M",
                    "%S",
                    "%f",
                    "%z",
                    "%Z",
                    "%j",
                    "%U",
                    "%W",
                    "%%",
                ]
            ),
            [
                "%a",
                "%A",
                "%w",
                "%d",
                "%b",
                "%B",
                "%m",
                "%y",
                "%Y",
                "%H",
                "%I",
                "%p",
                "%M",
                "%S",
                "%f",
                "%z",
                "%Z",
                "%j",
                "%U",
                "%W",
                "%%",
            ],
        )
        self.assertEqual(
            strptime.expand_format_fields(["%o", "%q", "%v"]), ["%o", "%q", "%v"]
        )

        mockStrftime.side_effect = _mock_strftime

        self.assertEqual(
            strptime.expand_format_fields(["%c"]),
            [
                "%a",
                " ",
                "%b",
                " ",
                "%d",
                " ",
                "%H",
                ":",
                "%M",
                ":",
                "%S",
                " ",
                "%Y",
            ],
        )
        self.assertEqual(
            strptime.expand_format_fields(["%x"]),
            ["%m", "/", "%d", "/", "%y"],
        )
        self.assertEqual(
            strptime.expand_format_fields(["%X"]),
            ["%H", ":", "%M", ":", "%S"],
        )
        self.assertEqual(
            strptime.expand_format_fields(["%c", " ", "%o", "%q", "%v"]),
            [
                "%a",
                " ",
                "%b",
                " ",
                "%d",
                " ",
                "%H",
                ":",
                "%M",
                ":",
                "%S",
                " ",
                "%Y",
                " ",
                "%o",
                "%q",
                "%v",
            ],
        )

    @mock.patch(
        "attotime.util.strptime.calendar.day_abbr",
        new_callable=mock.PropertyMock(return_value=LOCALE_DAY_ABBRS),
    )
    @mock.patch(
        "attotime.util.strptime.calendar.day_name",
        new_callable=mock.PropertyMock(return_value=LOCALE_DAY_NAMES),
    )
    @mock.patch(
        "attotime.util.strptime.calendar.month_abbr",
        new_callable=mock.PropertyMock(return_value=LOCALE_MONTH_ABBRS),
    )
    @mock.patch(
        "attotime.util.strptime.calendar.month_name",
        new_callable=mock.PropertyMock(return_value=LOCALE_MONTH_NAMES),
    )
    @mock.patch(
        "attotime.util.strptime.time.daylight",
        new_callable=mock.PropertyMock(return_value=False),
    )
    @mock.patch("attotime.util.strptime.time.strftime")
    def test_expand_format_fields_daylight(
        self,
        mockStrftime,
        mockDaylight,
        mockMonthName,
        mockMonthAbbr,
        mockDayName,
        mockDayAbbr,
    ):
        mockStrftime.side_effect = _mock_strftime

        self.assertEqual(
            strptime.expand_format_fields(["%c"]),
            [
                "%a",
                " ",
                "%b",
                " ",
                "%d",
                " ",
                "%H",
                ":",
                "%M",
                ":",
                "%S",
                " ",
                "%Y",
            ],
        )
        self.assertEqual(
            strptime.expand_format_fields(["%x"]),
            ["%m", "/", "%d", "/", "%y"],
        )
        self.assertEqual(
            strptime.expand_format_fields(["%X"]),
            ["%H", ":", "%M", ":", "%S"],
        )
        self.assertEqual(
            strptime.expand_format_fields(["%c", " ", "%o", "%q", "%v"]),
            [
                "%a",
                " ",
                "%b",
                " ",
                "%d",
                " ",
                "%H",
                ":",
                "%M",
                ":",
                "%S",
                " ",
                "%Y",
                " ",
                "%o",
                "%q",
                "%v",
            ],
        )

    @mock.patch(
        "attotime.util.strptime.calendar.day_abbr",
        new_callable=mock.PropertyMock(return_value=LOCALE_DAY_ABBRS),
    )
    @mock.patch(
        "attotime.util.strptime.calendar.day_name",
        new_callable=mock.PropertyMock(return_value=LOCALE_DAY_NAMES),
    )
    @mock.patch(
        "attotime.util.strptime.calendar.month_abbr",
        new_callable=mock.PropertyMock(return_value=LOCALE_MONTH_ABBRS),
    )
    @mock.patch(
        "attotime.util.strptime.calendar.month_name",
        new_callable=mock.PropertyMock(return_value=LOCALE_MONTH_NAMES),
    )
    @mock.patch("attotime.util.strptime.time.strftime")
    def test_expand_format_fields_weeknumber(
        self, mockStrftime, mockMonthName, mockMonthAbbr, mockDayName, mockDayAbbr
    ):
        def _mock_strftime_weeknumber(format, timetuple):
            if timetuple == time.struct_time((1999, 3, 17, 22, 44, 55, 2, 76, 0)):
                if format == "%p":
                    return "PM"
                elif format == "%c":
                    return "Wed Mar 17 22:44:55 1999"
                elif format == "%x":
                    return "03/17/99"
                elif format == "%X":
                    return "22:44:55"
            elif timetuple == time.struct_time((1999, 1, 3, 1, 1, 1, 6, 3, 0)):
                if format == "%c":
                    return "00 0 01:01:01 1999"
                elif format == "%x":
                    return "01/03/99"
                elif format == "%X":
                    return "01:01:01"

        mockStrftime.side_effect = _mock_strftime_weeknumber

        self.assertEqual(
            strptime.expand_format_fields(["%c"]),
            [
                "%a",
                " ",
                "%b",
                " ",
                "%d",
                " ",
                "%H",
                ":",
                "%M",
                ":",
                "%S",
                " ",
                "%Y",
            ],
        )
        self.assertEqual(
            strptime.expand_format_fields(["%x"]),
            ["%m", "/", "%d", "/", "%y"],
        )
        self.assertEqual(
            strptime.expand_format_fields(["%X"]),
            ["%H", ":", "%M", ":", "%S"],
        )
        self.assertEqual(
            strptime.expand_format_fields(["%c", " ", "%o", "%q", "%v"]),
            [
                "%a",
                " ",
                "%b",
                " ",
                "%d",
                " ",
                "%H",
                ":",
                "%M",
                ":",
                "%S",
                " ",
                "%Y",
                " ",
                "%o",
                "%q",
                "%v",
            ],
        )

    def test_get_field_size(self):
        self.assertEqual(strptime.get_field_size("2001", ["2001"], 0, 1), 4)
        self.assertEqual(strptime.get_field_size("abcd2001", ["2001"], 0, 7), 4)
        self.assertEqual(strptime.get_field_size("abcd2001", ["2001"], 0, 5), 4)

        self.assertEqual(strptime.get_field_size("abcd2001", ["BC"], 0, 7), 2)
        self.assertEqual(strptime.get_field_size("abcd2001", ["BC"], 0, 2), 2)

        self.assertEqual(
            strptime.get_field_size("2001", ["a", "b", "c", "d"], 0, 2), -1
        )
        self.assertEqual(strptime.get_field_size("2001", ["2001"], 1, 2), -1)
