# -*- coding: utf-8 -*-

# Copyright (c) 2021, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import datetime
import sys

PY2 = sys.version_info[0] == 2

if PY2:  # pragma: no cover
    # pylint: disable=undefined-variable,import-error
    import mock

    # https://docs.python.org/2/library/datetime.html#tzinfo-objects
    ZERO = datetime.timedelta(0)

    class UTC(datetime.tzinfo):
        """UTC"""

        def utcoffset(self, dt):
            # dt isn't used, but the python stdlib typechecks
            if type(dt) != datetime.datetime:
                raise TypeError

            return ZERO

        def tzname(self, dt):
            if type(dt) != datetime.datetime:
                raise TypeError

            return "UTC"

        def dst(self, dt):
            if type(dt) != datetime.datetime:
                raise TypeError

            return ZERO

    utc = UTC()
else:
    from unittest import mock

    utc = datetime.timezone.utc
