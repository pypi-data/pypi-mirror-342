# -*- coding: utf-8 -*-

# Copyright (c) 2021, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import datetime


class FixedOffset(datetime.tzinfo):
    def __init__(self, offset, name):
        self.__offset = datetime.timedelta(hours=offset)
        self.__name = name

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return self.__name

    def dst(self, dt):
        return datetime.timedelta(0)

    def __eq__(self, y):
        # Return the result of x == y, where self is x
        return (
            self.__class__ == y.__class__
            and self.__offset == y.__offset
            and self.__name == y.__name
        )

    def __str__(self):
        return self.__name


class DSTOffset(datetime.tzinfo):
    def __init__(self, offset, name):
        self.__offset = datetime.timedelta(hours=offset)
        self.__name = name

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return self.__name

    def dst(self, dt):
        # DST starts in month 6, moves clocks ahead one hour
        if dt is None:
            return datetime.timedelta(0)

        if dt.month >= 6:
            return datetime.timedelta(hours=1)

        return datetime.timedelta(0)

    def __eq__(self, y):
        # Return the result of x == y, where self is x
        return (
            self.__class__ == y.__class__
            and self.__offset == y.__offset
            and self.__name == y.__name
        )

    def __str__(self):
        return self.__name
