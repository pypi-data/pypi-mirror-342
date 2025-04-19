# -*- coding: utf-8 -*-

# Copyright (c) 2021, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

from __future__ import absolute_import

import calendar
import datetime
import time
from decimal import Decimal, getcontext

from attotime import compat, constants, util
from attotime.objects.attotime import attotime
from attotime.objects.attotimedelta import attotimedelta
from attotime.util.strptime import (
    expand_format_fields,
    get_field_size,
    get_format_fields,
)


class attodatetime(object):
    def __init__(
        self,
        year,
        month,
        day,
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
        nanosecond=0,
        tzinfo=None,
    ):
        if not isinstance(year, int):
            raise TypeError("year must be int")

        if not isinstance(month, int):
            raise TypeError("month must be int")

        if not isinstance(day, int):
            raise TypeError("day must be int")

        # Create the native date object
        self._native_date = datetime.date(year=year, month=month, day=day)

        # Create the attotime time object
        self._attotime = attotime(
            hour=hour,
            minute=minute,
            second=second,
            microsecond=microsecond,
            nanosecond=nanosecond,
            tzinfo=tzinfo,
        )

    @classmethod
    def today(cls):
        return cls.fromtimestamp(time.time())

    @classmethod
    def now(cls, tz=None):
        if tz is None:
            return cls.today()

        return cls.fromtimestamp(time.time(), tz)

    @classmethod
    def utcnow(cls):
        return cls.utcfromtimestamp(time.time())

    @classmethod
    def fromtimestamp(cls, timestamp, tz=None):
        utc_datetime = cls.utcfromtimestamp(timestamp)

        if tz is None:
            # Apply the local timezone, return as naive
            tz_delta = attotimedelta(
                seconds=util.LocalTimezone().utcoffset(utc_datetime).total_seconds()
            )
            return utc_datetime + tz_delta

        # Apply the timezone
        tz_delta = attotimedelta(
            seconds=tz.utcoffset(utc_datetime._as_datetime()).total_seconds()
        )
        return (utc_datetime + tz_delta).replace(tzinfo=tz)

    @classmethod
    def utcfromtimestamp(cls, timestamp):
        epoch_struct = time.gmtime(0)
        epoch_datetime = cls(
            year=epoch_struct[0],
            month=epoch_struct[1],
            day=epoch_struct[2],
            hour=epoch_struct[3],
            minute=epoch_struct[4],
            second=epoch_struct[5],
        )

        timestamp_delta = attotimedelta(seconds=timestamp)

        return epoch_datetime + timestamp_delta

    @classmethod
    def fromordinal(cls, ordinal):
        date = datetime.datetime.fromordinal(ordinal)

        return cls(year=date.year, month=date.month, day=date.day)

    @classmethod
    def combine(cls, date, time):
        result = cls(year=1, month=1, day=1)

        # Now replace the instance objects
        result._native_date = datetime.date(
            year=date.year, month=date.month, day=date.day
        )
        result._attotime = time

        return result

    @classmethod
    def strptime(cls, date_string, format):
        FIXED_LENGTH_FIELDS = [
            "%a",
            "%A",
            "%w",
            "%b",
            "%B",
            "%y",
            "%Y",
            "%p",
            "%x",
            "%X",
            "%%",
        ]

        if "%o" in format or "%q" in format or "%v" in format:
            # We have to process the sub-microsecond fields
            format_fields = expand_format_fields(get_format_fields(format))
            string_index = 0
            format_span_sizes = []

            for field_index in compat.range(0, len(format_fields)):
                format_field = format_fields[field_index]

                format_span_search_start = 0
                format_span_search_end = 0

                for span_size in format_span_sizes:
                    if isinstance(span_size, tuple):
                        # Search in a range
                        format_span_search_start += span_size[0]
                        format_span_search_end += span_size[1]
                    else:
                        # Exact span size is known
                        format_span_search_start += span_size
                        format_span_search_end += span_size

                if not format_field.startswith("%"):
                    # Span is fixed
                    format_span_sizes.append(len(format_field))
                elif format_field in FIXED_LENGTH_FIELDS:
                    # Span is fixed, but needs to be determined
                    span_size = -1

                    if format_field == "%a":
                        # Flip through all available weekday abbreviations
                        day_abbrs = []

                        for day_index in compat.range(0, 7):
                            day_abbrs.append(calendar.day_abbr[day_index])

                        span_size = get_field_size(
                            date_string,
                            day_abbrs,
                            format_span_search_start,
                            format_span_search_end,
                        )
                    elif format_field == "%A":
                        # Flip through all available weekdays
                        day_names = []

                        for day_index in compat.range(0, 7):
                            day_names.append(calendar.day_name[day_index])

                        span_size = get_field_size(
                            date_string,
                            day_names,
                            format_span_search_start,
                            format_span_search_end,
                        )
                    elif format_field == "%w":
                        span_size = 1
                    elif format_field == "%b":
                        # Check all available month abbreviations
                        month_abbrs = []

                        for month_index in compat.range(1, 13):
                            month_abbrs.append(calendar.month_abbr[month_index])

                        span_size = get_field_size(
                            date_string,
                            month_abbrs,
                            format_span_search_start,
                            format_span_search_end,
                        )
                    elif format_field == "%B":
                        # Check all available month names
                        month_names = []

                        for month_index in compat.range(1, 13):
                            month_names.append(calendar.month_name[month_index])

                        span_size = get_field_size(
                            date_string,
                            month_names,
                            format_span_search_start,
                            format_span_search_end,
                        )
                    elif format_field == "%y":
                        span_size = 2
                    elif format_field == "%Y":
                        span_size = 4
                    elif format_field == "%p":
                        # Taken from the Python strptime implementation
                        # https://github.com/python/cpython/blob/master/Lib/_strptime.py#L95
                        am_pm = []

                        for hour in (1, 22):
                            time_tuple = time.struct_time(
                                (1999, 3, 17, hour, 44, 55, 2, 76, 0)
                            )
                            am_pm.append(time.strftime("%p", time_tuple).lower())

                        if "" in am_pm:
                            # Some locales don't have am/pm designator
                            span_size = 0
                        else:
                            span_size = get_field_size(
                                date_string,
                                am_pm,
                                format_span_search_start,
                                format_span_search_end,
                            )
                    else:
                        # %%
                        span_size = 1

                    if span_size == -1:
                        raise ValueError("Span {0} not found".format(format_field))

                    format_span_sizes.append(span_size)
                else:
                    # Span is a range
                    if format_field in ["%d", "%m", "%H", "%I", "%M", "%S", "%U", "%W"]:
                        # Could be 1 or 2 characters
                        format_span_sizes.append((1, 2))
                    elif format_field in ["%f", "%o", "%q", "%v"]:
                        format_span_sizes.append((1, 6))
                    elif format_field == "%j":
                        format_span_sizes.append((1, 3))

            # Now calculate the size of the range spans
            used_length = 0
            unknown_span_ranges = []
            unknown_spans = []

            for span_index in compat.range(0, len(format_span_sizes)):
                span_size = format_span_sizes[span_index]

                if isinstance(span_size, tuple):
                    unknown_span_ranges.append(span_size)
                    unknown_spans.append(span_index)
                else:
                    used_length += span_size

            # Distribute remaining length
            remaining_length = len(date_string) - used_length
            unknown_span_index = 0

            for unknown_span_index in unknown_spans:
                format_span_sizes[unknown_span_index] = 0

            unknown_span_index = 0
            length_distributed = 0

            while remaining_length > 0:
                current_span_size = format_span_sizes[unknown_spans[unknown_span_index]]

                if current_span_size + 1 <= max(
                    unknown_span_ranges[unknown_span_index]
                ):
                    format_span_sizes[unknown_spans[unknown_span_index]] += 1
                    remaining_length -= 1
                    length_distributed += 1

                unknown_span_index += 1

                if unknown_span_index == len(unknown_spans):
                    if length_distributed == 0:
                        break

                    unknown_span_index = 0
                    length_distributed = 0

            # Now that we know all the lengths we can split up the date string
            python_date_string = ""
            python_format_fields = ""

            atto_date_string = ""
            atto_format_fields = ""

            string_index = 0

            for span_index in compat.range(0, len(format_span_sizes)):
                format_field = format_fields[span_index]
                span_size = format_span_sizes[span_index]

                if format_field in ["%o", "%q", "%v"]:
                    atto_date_string += date_string[
                        string_index : string_index + span_size
                    ]
                    atto_format_fields += format_field
                else:
                    python_date_string += date_string[
                        string_index : string_index + span_size
                    ]
                    python_format_fields += format_field

                string_index += span_size

            # Build the python datetime
            python_datetime = datetime.datetime.strptime(
                python_date_string, python_format_fields
            )
            atto_datetime = attodatetime(
                python_datetime.year,
                python_datetime.month,
                python_datetime.day,
                hour=python_datetime.hour,
                minute=python_datetime.minute,
                second=python_datetime.second,
                microsecond=python_datetime.microsecond,
                tzinfo=python_datetime.tzinfo,
            )

            # Build the attotimedelta
            nanoseconds_accumulator = Decimal(0)

            string_index = 0

            for span_index in compat.range(0, len(format_span_sizes)):
                format_field = format_fields[span_index]
                span_size = format_span_sizes[span_index]

                date_component = atto_date_string[
                    string_index : string_index + span_size
                ]

                if format_field == "%o":
                    nanoseconds_accumulator += (
                        Decimal(date_component) / constants.PICOSECONDS_PER_NANOSECOND
                    )
                    string_index += span_size
                elif format_field == "%q":
                    nanoseconds_accumulator += (
                        Decimal(date_component) / constants.ATTOSECONDS_PER_NANOSECOND
                    )
                    string_index += span_size
                elif format_field == "%v":
                    nanoseconds_accumulator += (
                        Decimal(date_component) / constants.YOCTOSECONDS_PER_NANOSECOND
                    )
                    string_index += span_size

            atto_delta = attotimedelta(nanoseconds=nanoseconds_accumulator)

            return atto_datetime + atto_delta
        else:
            # We can simply call the Python implementation
            python_datetime = datetime.datetime.strptime(date_string, format)

            return attodatetime(
                python_datetime.year,
                python_datetime.month,
                python_datetime.day,
                hour=python_datetime.hour,
                minute=python_datetime.minute,
                second=python_datetime.second,
                microsecond=python_datetime.microsecond,
                tzinfo=python_datetime.tzinfo,
            )

    @property
    def year(self):
        return self._native_date.year

    @property
    def month(self):
        return self._native_date.month

    @property
    def day(self):
        return self._native_date.day

    @property
    def hour(self):
        return self._attotime.hour

    @property
    def minute(self):
        return self._attotime.minute

    @property
    def second(self):
        return self._attotime.second

    @property
    def microsecond(self):
        return self._attotime.microsecond

    @property
    def nanosecond(self):
        return self._attotime.nanosecond

    @property
    def tzinfo(self):
        return self._attotime.tzinfo

    def date(self):
        return self._as_datetime().date()

    def time(self):
        return attotime(
            hour=self.hour,
            minute=self.minute,
            second=self.second,
            microsecond=self.microsecond,
            nanosecond=self.nanosecond,
        )

    def timetz(self):
        return attotime(
            hour=self.hour,
            minute=self.minute,
            second=self.second,
            microsecond=self.microsecond,
            nanosecond=self.nanosecond,
            tzinfo=self.tzinfo,
        )

    def replace(
        self,
        year=None,
        month=None,
        day=None,
        hour=None,
        minute=None,
        second=None,
        microsecond=None,
        nanosecond=None,
        tzinfo=True,
    ):
        if year is None:
            year = self.year

        if month is None:
            month = self.month

        if day is None:
            day = self.day

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
        # https://github.com/python/cpython/blob/master/Lib/datetime.py#L1596
        if tzinfo is True:
            tzinfo = self.tzinfo

        return attodatetime(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=second,
            microsecond=microsecond,
            nanosecond=nanosecond,
            tzinfo=tzinfo,
        )

    def astimezone(self, tz):
        if self.tzinfo is None:
            raise ValueError("astimezone() cannot be applied to a naive datetime")

        if self.tzinfo is tz:
            return self

        # Convert to UTC, remove timezone info
        utc_datetime = (self - self.utcoffset()).replace(tzinfo=None)

        # Apply the timezone
        tz_delta = attotimedelta(
            seconds=tz.utcoffset(utc_datetime._as_datetime()).total_seconds()
        )
        return (utc_datetime + tz_delta).replace(tzinfo=tz)

    def utcoffset(self):
        # Offsets don't have nanosecond resolution, so build a native datetime
        native_datetime = self._as_datetime()

        native_timedelta = native_datetime.utcoffset()

        if native_timedelta is None:
            return None

        # Convert the native timedelta to an attotimedelta
        return attotimedelta(
            days=native_timedelta.days,
            seconds=native_timedelta.seconds,
            microseconds=native_timedelta.microseconds,
            nanoseconds=0,
        )

    def dst(self):
        if self.tzinfo is None:
            return None

        # Offsets don't have nanosecond resolution, so build a native datetime
        native_datetime = self._as_datetime()

        native_timedelta = native_datetime.tzinfo.dst(native_datetime)

        # Convert the native timedelta to an attotimedelta
        return attotimedelta(
            days=native_timedelta.days,
            seconds=native_timedelta.seconds,
            microseconds=native_timedelta.microseconds,
            nanoseconds=0,
        )

    def tzname(self):
        if self.tzinfo is None:
            return None

        return self.tzinfo.tzname(self.tzinfo)

    def timetuple(self):
        return self._as_datetime().timetuple()

    def utctimetuple(self):
        return self._as_datetime().utctimetuple()

    def toordinal(self):
        return self._as_datetime().toordinal()

    def weekday(self):
        return self._as_datetime().weekday()

    def isoweekday(self):
        return self._as_datetime().isoweekday()

    def isocalendar(self):
        return self._as_datetime().isocalendar()

    def isoformat(self, separator="T"):
        return separator.join(
            [self._as_datetime().date().isoformat(), self._attotime.isoformat()]
        )

    def ctime(self):
        return self._as_datetime().ctime()

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
            "%j",
            "%U",
            "%W",
            "%x",
        ]:
            replacement_dict[directive] = self._native_date.strftime(directive)

        native_time = self._attotime._native_time

        for directive in ["%H", "%I", "%p", "%M", "%S", "%f", "%z", "%Z", "%X"]:
            replacement_dict[directive] = native_time.strftime(directive)

        # Build a native datetime with tzinfo so we can get timezone replacements
        if self._attotime.tzinfo is not None:
            tz_datetime = datetime.datetime(1900, 1, 1, tzinfo=self._attotime.tzinfo)

            replacement_dict["%z"] = tz_datetime.strftime("%z")
            replacement_dict["%Z"] = tz_datetime.strftime("%Z")
        else:
            replacement_dict["%z"] = ""
            replacement_dict["%Z"] = ""

        # Hack together a "Locale's appropriate date and time representation."
        replacement_dict["%c"] = self._native_date.strftime("%c").replace(
            "00:00:00", native_time.strftime("%X")
        )

        # Build the picosecond, attosecond, and yoctosecond replacements
        nanosecond_string = util.decimal_stringify(self._attotime._nanosecond)

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

    def __add__(self, y):
        # Return the result of x + y, where self is x and y is an attotimedelta
        if not isinstance(y, attotimedelta):
            return NotImplemented

        delta = attotimedelta(
            days=self._native_date.toordinal(),
            hours=self.hour,
            minutes=self.minute,
            seconds=self.second,
            microseconds=self.microsecond,
            nanoseconds=self.nanosecond,
        )

        delta += y

        hour, remaining_seconds = getcontext().divmod(
            delta.seconds, constants.SECONDS_PER_HOUR
        )
        minute, second = getcontext().divmod(
            remaining_seconds, constants.SECONDS_PER_MINUTE
        )

        if delta.days > 0 and delta.days < datetime.date.max.toordinal():
            return self.combine(
                datetime.date.fromordinal(delta.days),
                attotime(
                    int(hour),
                    int(minute),
                    int(second),
                    delta.microseconds,
                    delta.nanoseconds,
                    tzinfo=self.tzinfo,
                ),
            )

        raise OverflowError("result out of range")

    def __sub__(self, y):
        # Returns the result of x - y, where self ix x, and y is
        # an attodatetime or attotimedelta, when y is an attodatetime,
        # the result is an attotimedelta, when y is an attotimedelta,
        # the result is an attodatetime
        if not isinstance(y, attodatetime):
            if isinstance(y, attotimedelta):
                # y is an attotimedelta
                return self + -y

            return NotImplemented

        # y is an attodatetime, build an attotimedelta
        daysx = self._native_date.toordinal()
        daysy = y._native_date.toordinal()

        secondsx = (
            self.second
            + self.minute * constants.SECONDS_PER_MINUTE
            + self.hour * constants.SECONDS_PER_HOUR
        )
        secondsy = (
            y.second
            + y.minute * constants.SECONDS_PER_MINUTE
            + y.hour * constants.SECONDS_PER_HOUR
        )

        microsecondsx = self.microsecond
        microsecondsy = y.microsecond

        nanosecondsx = self.nanosecond
        nanosecondsy = y.nanosecond

        base = attotimedelta(
            days=daysx - daysy,
            seconds=secondsx - secondsy,
            microseconds=microsecondsx - microsecondsy,
            nanoseconds=nanosecondsx - nanosecondsy,
        )

        if self.tzinfo is y.tzinfo:
            return base

        offsetx = self.utcoffset()
        offsety = y.utcoffset()

        if offsetx == offsety:
            return base

        if offsetx is None or offsety is None:
            raise TypeError("cannot mix naive and timezone-aware time")

        return base + offsety - offsetx

    def __eq__(self, y):
        # Return the result of x == y, where self is x
        if isinstance(y, self.__class__):
            return self._native_date == y._native_date and self._attotime == y._attotime

        return False

    def __ne__(self, y):
        # Return the result of x != y, where self is x
        return not self.__eq__(y)

    def __gt__(self, y):
        # Return the result of x > y, where self is x
        if isinstance(y, self.__class__):
            return self._native_date > y._native_date or (
                self._native_date == y._native_date and self._attotime > y._attotime
            )
        else:
            raise TypeError(
                "can't compare {0} to {1}".format(type(self).__name__, type(y).__name__)
            )

    def __ge__(self, y):
        # Return the result of x >= y, where self is x
        if isinstance(y, self.__class__):
            return self._native_date > y._native_date or (
                self._native_date == y._native_date and self._attotime >= y._attotime
            )
        else:
            raise TypeError(
                "can't compare {0} to {1}".format(type(self).__name__, type(y).__name__)
            )

    def __lt__(self, y):
        # Return the result of x < y, where self is x
        if isinstance(y, self.__class__):
            return self._native_date < y._native_date or (
                self._native_date == y._native_date and self._attotime < y._attotime
            )
        else:
            raise TypeError(
                "can't compare {0} to {1}".format(type(self).__name__, type(y).__name__)
            )

    def __le__(self, y):
        # Return the result of x <= y, where self is x
        if isinstance(y, self.__class__):
            return self._native_date < y._native_date or (
                self._native_date == y._native_date and self._attotime <= y._attotime
            )
        else:
            raise TypeError(
                "can't compare {0} to {1}".format(type(self).__name__, type(y).__name__)
            )

    def __str__(self):
        return self.isoformat(separator=" ")

    def __repr__(self):
        if self._attotime.tzinfo is None:
            return "{0}({1}, {2}, {3}, {4}, {5}, {6}, {7}, {8})".format(
                self.__class__.__module__,
                self._native_date.year,
                self._native_date.month,
                self._native_date.day,
                self._attotime.hour,
                self._attotime.minute,
                self._attotime.second,
                self._attotime.microsecond,
                str(self._attotime.nanosecond),
            )

        return "{0}({1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9})".format(
            self.__class__.__module__,
            self._native_date.year,
            self._native_date.month,
            self._native_date.day,
            self._attotime.hour,
            self._attotime.minute,
            self._attotime.second,
            self._attotime.microsecond,
            str(self._attotime.nanosecond),
            str(self._attotime.tzinfo),
        )

    def __format__(self, formatstr):
        return self.strftime(formatstr)

    def _as_datetime(self):
        # Returns the attodatetime as a native datetime, losing nanosecond resolution
        return datetime.datetime(
            year=self.year,
            month=self.month,
            day=self.day,
            hour=self.hour,
            minute=self.minute,
            second=self.second,
            microsecond=self.microsecond,
            tzinfo=self.tzinfo,
        )
