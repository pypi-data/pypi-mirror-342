# -*- coding: utf-8 -*-

# Copyright (c) 2021, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import calendar
import time

from attotime import compat


def get_format_fields(format):
    # Return a list of format fields
    component_accumulator = ""
    format_components = []

    for field_char in format:
        if component_accumulator.startswith("%") and len(component_accumulator) == 2:
            # Field complete, reset accumulator
            format_components.append(component_accumulator)
            component_accumulator = ""
        elif (
            field_char == "%"
            and len(component_accumulator) > 0
            and not component_accumulator.startswith("%")
        ):
            # Starting new field, reset accumulator
            format_components.append(component_accumulator)
            component_accumulator = ""

        component_accumulator += field_char

    if component_accumulator != "":
        # Grab whatever was in the accumulator
        format_components.append(component_accumulator)

    return format_components


def expand_format_fields(format_fields):
    # Expands %c, %x, %X into their component fields
    # Taken from the Python implementation
    # https://github.com/python/cpython/blob/master/Lib/_strptime.py#L107
    expanded_format_fields = []

    # First we need timezone strings
    # https://github.com/python/cpython/blob/master/Lib/_strptime.py#L152
    tzname = time.tzname
    daylight = time.daylight
    no_saving = frozenset({"utc", "gmt", tzname[0].lower()})

    if daylight:
        has_saving = frozenset({tzname[1].lower()})
    else:
        has_saving = frozenset()

    timezone_tuple = (no_saving, has_saving)

    # Day and month strings
    a_string = calendar.day_abbr[2].lower()
    A_string = calendar.day_name[2].lower()

    b_string = calendar.month_abbr[3].lower()
    B_string = calendar.month_name[3].lower()

    # AM/PM string
    pm_time_tuple = time.struct_time((1999, 3, 17, 22, 44, 55, 2, 76, 0))
    pm_string = time.strftime("%p", pm_time_tuple).lower()

    # Now calculate the expansions
    time_tuple = time.struct_time((1999, 3, 17, 22, 44, 55, 2, 76, 0))

    expansions = [None, None, None]
    expansions[0] = time.strftime("%c", time_tuple).lower()
    expansions[1] = time.strftime("%x", time_tuple).lower()
    expansions[2] = time.strftime("%X", time_tuple).lower()

    replacement_pairs = [
        ("%", "%%"),
        (A_string, "%A"),
        (B_string, "%B"),
        (a_string, "%a"),
        (b_string, "%b"),
        (pm_string, "%p"),
        ("1999", "%Y"),
        ("99", "%y"),
        ("22", "%H"),
        ("44", "%M"),
        ("55", "%S"),
        ("76", "%j"),
        ("17", "%d"),
        ("03", "%m"),
        ("3", "%m"),
        ("2", "%w"),
        ("10", "%I"),
    ]

    replacement_pairs.extend(
        [(tz, "%Z") for tz_values in timezone_tuple for tz in tz_values]
    )

    for offset, directive in ((0, "%c"), (1, "%x"), (2, "%X")):
        current_format = expansions[offset]

        for old, new in replacement_pairs:
            current_format = current_format.replace(old, new)

        time_tuple = time.struct_time((1999, 1, 3, 1, 1, 1, 6, 3, 0))

        if "00" in time.strftime(directive, time_tuple):
            U_W = "%W"
        else:
            U_W = "%U"

        expansions[offset] = current_format.replace("11", U_W)

    c_expansion = get_format_fields(expansions[0])
    x_expansion = get_format_fields(expansions[1])
    X_expansion = get_format_fields(expansions[2])

    # Finally, perform the expansion
    for format_field in format_fields:
        if format_field == "%c":
            expanded_format_fields += c_expansion
        elif format_field == "%x":
            expanded_format_fields += x_expansion
        elif format_field == "%X":
            expanded_format_fields += X_expansion
        else:
            expanded_format_fields.append(format_field)

    return expanded_format_fields


def get_field_size(date_string, field_members, range_start, range_end):
    # Given the date string, a list of field members, and the range to start
    # in, find the member in the range, and return its size
    max_field_size = 0

    for field in field_members:
        if len(field) > max_field_size:
            max_field_size = len(field)

    for range_index in compat.range(range_start, range_end + max_field_size):
        for field_member in field_members:
            if date_string.lower()[range_index:].startswith(field_member.lower()):
                return len(field_member)

    # Field not found
    return -1
