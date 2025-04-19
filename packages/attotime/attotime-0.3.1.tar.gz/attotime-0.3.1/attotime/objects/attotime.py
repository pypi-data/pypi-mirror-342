# -*- coding: utf-8 -*-

# Copyright (c) 2021, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

from __future__ import absolute_import

import datetime
from decimal import Decimal, getcontext

from attotime import constants, util


class attotime(object):
    def __init__(
        self, hour=0, minute=0, second=0, microsecond=0, nanosecond=0, tzinfo=None
    ):
        # Everything is stored as an integer, except for nanoseconds, which is stored as a Decimal
        if not isinstance(hour, int):
            raise TypeError("hour must be int")

        if not isinstance(minute, int):
            raise TypeError("minute must be int")

        if not isinstance(second, int):
            raise TypeError("second must be int")

        if not isinstance(microsecond, int):
            raise TypeError("microsecond must be int")

        if type(nanosecond) not in (int, float, Decimal):
            raise TypeError("nanosecond must be int, float, or Decimal")

        if nanosecond < 0 or nanosecond >= constants.NANOSECONDS_PER_MICROSECOND:
            raise ValueError(
                "nanosecond must be in 0..{0}".format(
                    constants.NANOSECONDS_PER_MICROSECOND
                )
            )

        # Create the native time object
        self._native_time = datetime.time(
            hour=hour,
            minute=minute,
            second=second,
            microsecond=microsecond,
        )

        self._nanosecond = nanosecond

        self._tzinfo = tzinfo

    @property
    def hour(self):
        return self._native_time.hour

    @property
    def minute(self):
        return self._native_time.minute

    @property
    def second(self):
        return self._native_time.second

    @property
    def microsecond(self):
        return self._native_time.microsecond

    @property
    def nanosecond(self):
        return self._nanosecond

    @property
    def tzinfo(self):
        return self._tzinfo

    def replace(
        self,
        hour=None,
        minute=None,
        second=None,
        microsecond=None,
        nanosecond=None,
        tzinfo=True,
    ):
        if hour is None:
            hour = self.hour

        if minute is None:
            minute = self.minute

        if second is None:
            second = self.second

        if microsecond is None:
            microsecond = self.microsecond

        if nanosecond is None:
            nanosecond = self.nanosecond

        # Use True to support clearing tzinfo by setting tzinfo=None
        # https://github.com/python/cpython/blob/master/Lib/datetime.py#L1315
        if tzinfo is True:
            tzinfo = self.tzinfo

        return attotime(
            hour=hour,
            minute=minute,
            second=second,
            microsecond=microsecond,
            nanosecond=nanosecond,
            tzinfo=tzinfo,
        )

    def isoformat(self):
        # Returns a string of the form HH:MM:SS[.mmmmmm][+HH:MM]
        combined_seconds = (
            self.second
            + (self.microsecond / constants.MICROSECONDS_PER_SECOND)
            + (self.nanosecond / constants.NANOSECONDS_PER_SECOND)
        )

        if combined_seconds == 0:
            time_str = "{0:02d}:{1:02d}:00".format(self.hour, self.minute)
        elif combined_seconds < 10:
            time_str = "{0:02d}:{1:02d}:0{2}".format(
                self.hour, self.minute, util.decimal_stringify(combined_seconds)
            )
        else:
            time_str = "{0:02d}:{1:02d}:{2}".format(
                self.hour, self.minute, util.decimal_stringify(combined_seconds)
            )

        if self.utcoffset() is not None:
            offset = self.utcoffset()

            # Build a +HH:MM string
            if offset.days < 0:
                sign_str = "-"
                offset = -offset  # pylint: disable=invalid-unary-operand-type
            else:
                sign_str = "+"

            offset_hours, remaining_seconds = getcontext().divmod(
                Decimal(offset.total_seconds()), constants.SECONDS_PER_HOUR
            )
            offset_minutes, offset_seconds = getcontext().divmod(
                remaining_seconds, constants.SECONDS_PER_MINUTE
            )

            if offset_seconds == 0:
                offset_str = "{0}{1:02d}:{2:02d}".format(
                    sign_str, int(offset_hours), int(offset_minutes)
                )
            else:
                offset_str = "{0}{1:02d}:{2:02d}:{3:02d}".format(
                    sign_str,
                    int(offset_hours),
                    int(offset_minutes),
                    int(offset_seconds),
                )

            time_str += offset_str

        return time_str

    def strftime(self, formatstr):
        replacement_dict = {}

        # Build the dictionary of replacements
        for directive in [
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
        ]:
            replacement_dict[directive] = self._native_time.strftime(directive)

        # Build a native datetime with tzinfo so we can get timezone replacements
        if self._tzinfo is not None:
            tz_datetime = datetime.datetime(1900, 1, 1, tzinfo=self._tzinfo)

            replacement_dict["%z"] = tz_datetime.strftime("%z")
            replacement_dict["%Z"] = tz_datetime.strftime("%Z")
        else:
            replacement_dict["%z"] = ""
            replacement_dict["%Z"] = ""

        # Build the picosecond, attosecond, and yoctosecond replacements
        nanosecond_string = util.decimal_stringify(self._nanosecond)

        if "." in nanosecond_string:
            stop_index = nanosecond_string.index(".")

            left_padding = 3 - stop_index
            right_padding = 18 - len(nanosecond_string[stop_index:])
        else:
            left_padding = 3 - len(nanosecond_string)
            right_padding = 18 - left_padding - len(nanosecond_string)

        nanosecond_string = "0" * left_padding + nanosecond_string + "0" * right_padding
        nanosecond_string = nanosecond_string.replace(".", "")

        replacement_dict["%o"] = nanosecond_string[0:6]  # picoseconds
        replacement_dict["%q"] = nanosecond_string[6:12]  # attoseconds
        replacement_dict["%v"] = nanosecond_string[12:18]  # yoctoseconds

        replacement_dict["%%"] = "%"

        return util.multiple_replace(formatstr, replacement_dict)

    def utcoffset(self):
        if self.tzinfo is None:
            return None

        return self.tzinfo.utcoffset(None)

    def dst(self):
        if self.tzinfo is None:
            return None

        return self.tzinfo.dst(None)

    def tzname(self):
        if self.tzinfo is None:
            return None

        return self.tzinfo.tzname(self.tzinfo)

    def __eq__(self, y):
        # Return the result of x == y, where self is x
        if isinstance(y, self.__class__):
            if self.tzinfo is None and y.tzinfo is None:
                # Do a naive comparison
                return (
                    self._native_time == y._native_time
                    and self._nanosecond == y._nanosecond
                )
            elif self.tzinfo is not None and y.tzinfo is not None:
                # Do a tz aware comparison, since there is currently not a nanosecond aware
                # tzinfo implementation, just compare each part separately
                return (
                    self._native_time.replace(tzinfo=self.tzinfo)
                    == y._native_time.replace(tzinfo=y.tzinfo)
                    and self._nanosecond == y._nanosecond
                )
            else:
                raise TypeError("can't compare offset-naive and offset-aware times")

        return False

    def __ne__(self, y):
        # Return the result of x != y, where self is x
        return not self.__eq__(y)

    def __gt__(self, y):
        # Return the result of x > y, where self is x
        if isinstance(y, self.__class__):
            if self.tzinfo is None and y.tzinfo is None:
                # Do a naive comparison
                return (self._native_time > y._native_time) or (
                    self._native_time == y._native_time
                    and self._nanosecond > y._nanosecond
                )
            elif self.tzinfo is not None and y.tzinfo is not None:
                # Do a tz aware comparison, since there is currently not a nanosecond aware
                # tzinfo implementation, just compare each part separately
                return (
                    self._native_time.replace(tzinfo=self.tzinfo)
                    > y._native_time.replace(tzinfo=y.tzinfo)
                    and self._nanosecond == y._nanosecond
                ) or (
                    self._native_time.replace(tzinfo=self.tzinfo)
                    == y._native_time.replace(tzinfo=y.tzinfo)
                    and self._nanosecond > y._nanosecond
                )
            else:
                raise TypeError("can't compare offset-naive and offset-aware times")
        else:
            raise TypeError(
                "can't compare {0} to {1}".format(type(self).__name__, type(y).__name__)
            )

    def __ge__(self, y):
        # Return the result of x >= y, where self is x
        if isinstance(y, self.__class__):
            return (self > y) or (self == y)
        else:
            raise TypeError(
                "can't compare {0} to {1}".format(type(self).__name__, type(y).__name__)
            )

    def __lt__(self, y):
        # Return the result of x < y, where self is x
        if isinstance(y, self.__class__):
            if self.tzinfo is None and y.tzinfo is None:
                # Do a naive comparison
                return (self._native_time < y._native_time) or (
                    self._native_time == y._native_time
                    and self._nanosecond < y._nanosecond
                )
            elif self.tzinfo is not None and y.tzinfo is not None:
                # Do a tz aware comparison, since there is currently not a nanosecond aware
                # tzinfo implementation, just compare each part separately
                return (
                    self._native_time.replace(tzinfo=self.tzinfo)
                    < y._native_time.replace(tzinfo=y.tzinfo)
                    and self._nanosecond == y._nanosecond
                ) or (
                    self._native_time.replace(tzinfo=self.tzinfo)
                    == y._native_time.replace(tzinfo=y.tzinfo)
                    and self._nanosecond < y._nanosecond
                )
            else:
                raise TypeError("can't compare offset-naive and offset-aware times")
        else:
            raise TypeError(
                "can't compare {0} to {1}".format(type(self).__name__, type(y).__name__)
            )

    def __le__(self, y):
        # Return the result of x <= y, where self is x
        if isinstance(y, self.__class__):
            return (self < y) or (self == y)
        else:
            raise TypeError(
                "can't compare {0} to {1}".format(type(self).__name__, type(y).__name__)
            )

    def __str__(self):
        return self.isoformat()

    def __repr__(self):
        if self._tzinfo is None:
            return "{0}({1}, {2}, {3}, {4}, {5})".format(
                self.__class__.__module__,
                self.hour,
                self.minute,
                self.second,
                self.microsecond,
                str(self.nanosecond),
            )

        return "{0}({1}, {2}, {3}, {4}, {5}, {6})".format(
            self.__class__.__module__,
            self.hour,
            self.minute,
            self.second,
            self.microsecond,
            str(self.nanosecond),
            str(self._tzinfo),
        )

    def __format__(self, formatstr):
        return self.strftime(formatstr)
