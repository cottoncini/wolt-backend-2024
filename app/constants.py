"""
constants.py

Definition of constants and associated classes.
"""

from datetime import datetime, timezone
from typing import NamedTuple


class RushHour(NamedTuple):
    """
    Class that defines a time interval as rush hour.

    Takes as inputs day of the week (0 to 6), hours of start and end of the interval (0 to 24).
    """

    day: int
    hour_start: int
    hour_end: int

    def contains_datetime(self, dt: datetime) -> bool:
        """
        Check whether datetime is contained or not in rush hour interval.
        """
        dt_utc = dt.astimezone(tz=timezone.utc)
        return all(
            [
                dt_utc.weekday() == self.day,
                dt_utc.hour >= self.hour_start,
                dt_utc.hour < self.hour_end,
            ]
        )


RUSH_HOURS = [RushHour(day=4, hour_start=15, hour_end=19)]

# €c, minimum cart value for small order surcharge
CART_VALUE_MIN = 1000

# €c, maximum cart value for waving delivery fee
CART_VALUE_MAX = 20000

# m, minimum distance that charges FEE_DISTANCE_MIN
DISTANCE_MIN = 1000

# m, distance step that charges additional FEE_DISTANCE_STEP
DISTANCE_STEP = 500

# -, maximum number of items with no surcharge
ITEMS_MAX = 4

# -, maximum number of items before bulk surcharge
ITEMS_BULK = 12

# €c, minimum charge based on distance
FEE_DISTANCE_MIN = 200

# €c, additional charge based on DISTANCE_STEP
FEE_DISTANCE_STEP = 100

# €c, per-item surcharge
FEE_ITEM = 50

# €c, bulk order surcharge
FEE_BULK = 120

# €c, maximum total delivery fee
FEE_TOTAL_MAX = 1500

# -, multiplier of total delivery fee during rush hours
MULT_RUSH_HOUR = 1.2
