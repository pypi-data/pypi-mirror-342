# -*- coding: utf-8 -*-

# Copyright (c) 2021, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import datetime
import re
import time
from decimal import getcontext


def decimal_stringify(decimal):
    # https://stackoverflow.com/questions/11227620/drop-trailing-zeros-from-decimal
    decimal_string = str(decimal)

    if "E" in decimal_string:
        # Arbitrarily force 16 place fixed point
        decimal_string = "{0:16f}".format(decimal)

    if "." in decimal_string:
        decimal_string = decimal_string.rstrip("0").rstrip(".")

    return decimal_string.strip()


def multiple_replace(string, replacements):
    # https://gist.github.com/bgusach/a967e0587d6e01e889fd1d776c5f3729
    # Place longer ones first to keep shorter substrings from matching where the longer ones should take place
    # For instance given the replacements {'ab': 'AB', 'abc': 'ABC'} against the string 'hey abc', it should produce
    #'hey ABC' and not 'hey ABc'
    substrs = sorted(replacements, key=len, reverse=True)

    # Create a big OR regex that matches any of the substrings to replace
    regexp = re.compile("|".join(map(re.escape, substrs)))

    # For each match, look up the new string in the replacements
    return regexp.sub(lambda match: replacements[match.group(0)], string)


class LocalTimezone(datetime.tzinfo):
    # https://docs.python.org/2/library/datetime.html#tzinfo-objects
    def __init__(self):
        self.STDOFFSET = datetime.timedelta(seconds=-time.timezone)

        if time.daylight:
            self.DSTOFFSET = datetime.timedelta(seconds=-time.altzone)
        else:
            self.DSTOFFSET = self.STDOFFSET

        self.DSTDIFF = self.DSTOFFSET - self.STDOFFSET

    def utcoffset(self, dt):
        if self._isdst(dt):
            return self.DSTOFFSET
        else:
            return self.STDOFFSET

    def dst(self, dt):
        if self._isdst(dt):
            return self.DSTDIFF
        else:
            return datetime.timedelta(0)

    def tzname(self, dt):
        return time.tzname[self._isdst(dt)]

    def _isdst(self, dt):
        tt = (
            dt.year,
            dt.month,
            dt.day,
            dt.hour,
            dt.minute,
            dt.second,
            dt.weekday(),
            0,
            0,
        )
        stamp = time.mktime(tt)
        tt = time.localtime(stamp)
        return tt.tm_isdst > 0
