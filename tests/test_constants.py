"""
test_constants.py

Test module for functions and classes in "constants".
"""

from datetime import datetime

from app.constants import RushHour


def test_rush_hour_contains_datetime_positive():
    """Test that contains_datetime method of rush hour class works with positive input."""
    rh = RushHour(day=0, hour_start=0, hour_end=1)
    dt = datetime.fromisoformat("2024-01-29T00:10:00Z")
    assert rh.contains_datetime(dt) is True


def test_rush_hour_contains_datetime_negative():
    """Test that contains_datetime method of rush hour class works with negative input."""
    rh = RushHour(day=0, hour_start=0, hour_end=1)
    dt = datetime.fromisoformat("2024-01-29T01:00:00Z")
    assert rh.contains_datetime(dt) is False
