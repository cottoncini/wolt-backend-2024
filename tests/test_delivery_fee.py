"""
test_main.py

Test module for functions in "main".
"""

from datetime import datetime

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.routers.delivery_fee import (
    Cart,
    compute_cart_value_fee,
    compute_distance_fee,
    compute_items_fee,
    compute_multiplier_rush_hour,
    compute_total_fee,
)

client = TestClient(app)

cart_good = {
    "cart_value": 790,
    "delivery_distance": 2235,
    "number_of_items": 4,
    "time": "2024-01-15T13:00:00Z",
}
response_cart_good = {"delivery_fee": 710}


def test_cart_good():
    """Test for known good cart."""
    response = client.post("/delivery-fee", json=cart_good)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == response_cart_good


@pytest.mark.parametrize("field", cart_good.keys())
def test_cart_missing_field(field):
    """Test for missing fields in cart model."""
    data = cart_good.copy()
    del data[field]
    response = client.post("/delivery-fee", json=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "field", ["cart_value", "delivery_distance", "number_of_items"]
)
@pytest.mark.parametrize("value", [0, -1])
def test_cart_invalid_value(field, value):
    """Test for invalid values in cart model."""
    data = cart_good.copy()
    data.update({field: value})
    response = client.post("/delivery-fee", json=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_cart_invalid_time():
    """Test for invalid time in cart model."""
    data = cart_good.copy()
    data.update({"time": "2024-01-15"})
    response = client.post("/delivery-fee", json=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "function", [compute_cart_value_fee, compute_distance_fee, compute_items_fee]
)
@pytest.mark.parametrize("input_value", [-1, 0])
def test_nonpositive_input(function, input_value):
    """Test for non positive input values to functions."""
    with pytest.raises(ValueError):
        function(input_value)


@pytest.mark.parametrize(
    "cart_value,expected", [(890, 110), (999, 1), (1000, 0), (1001, 0)]
)
def test_compute_cart_value_fee(cart_value, expected):
    """Test for cart value component of delivery fee."""
    assert compute_cart_value_fee(cart_value) == expected


@pytest.mark.parametrize(
    "distance,expected",
    [(999, 200), (1000, 200), (1499, 300), (1500, 300), (1501, 400)],
)
def test_compute_distance_fee(distance, expected):
    """Test for distance component of delivery fee."""
    assert compute_distance_fee(distance) == expected


@pytest.mark.parametrize(
    "items,expected", [(4, 0), (5, 50), (10, 300), (13, 570), (14, 620)]
)
def test_compute_items_fee(items, expected):
    """Test for items component of delivery fee."""
    assert compute_items_fee(items) == expected


@pytest.mark.parametrize(
    "time,expected",
    [
        ("2024-01-26T14:59:59+00:00", 1.0),
        ("2024-01-26T15:00:00+00:00", 1.2),
        ("2024-01-26T18:59:59+00:00", 1.2),
        ("2024-01-26T19:00:00+00:00", 1.0),
        ("2024-01-26T19:00:00+01:00", 1.2),
    ],
)
def test_compute_multiplier_rush_hour(time, expected):
    """Test for rush hour multiplier."""
    dt = datetime.fromisoformat(time)
    assert compute_multiplier_rush_hour(dt) == expected


@pytest.mark.parametrize(
    "cart,expected",
    [
        (
            Cart(
                cart_value=20000,
                delivery_distance=1000,
                number_of_items=10,
                time="2024-01-15T13:00:00Z",
            ),
            0,
        ),
        (
            Cart(
                cart_value=100,
                delivery_distance=10000,
                number_of_items=20,
                time="2024-01-26T18:00:00Z",
            ),
            1500,
        ),
    ],
)
def test_compute_total_fee(cart, expected):
    """Test for total delivery fee."""
    assert compute_total_fee(cart) == expected
