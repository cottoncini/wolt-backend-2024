"""
delivery_fee.py

Delivery fee router module. Contains POST endpoint and functions to compute and 
return delivery fee.
"""

from datetime import datetime
from math import ceil

from fastapi import APIRouter
from pydantic import BaseModel, NonNegativeInt, PositiveInt

from app import constants


class Cart(BaseModel):
    """Cart model."""

    cart_value: PositiveInt
    delivery_distance: PositiveInt
    number_of_items: PositiveInt
    time: datetime


class DeliveryFee(BaseModel):
    """Delivery fee model."""

    delivery_fee: NonNegativeInt


def compute_cart_value_fee(cart_value: int) -> int:
    """
    Computes component of delivery fee based on cart value.

    Carts with value lower than CART_VALUE_MIN are charged a fee corresponding to
    the difference between cart value and CART_VALUE_MIN.
    Input 'cart_value' must be positive.
    """
    if cart_value <= 0:
        raise ValueError("input cart value must be positive")
    return max(0, constants.CART_VALUE_MIN - cart_value)


def compute_distance_fee(delivery_distance: int) -> int:
    """
    Computes component of delivery fee based on distance.

    The fee is made of a fixed rate FEE_DISTANCE_MIN for the first DISTANCE_MIN meters,
    and a piecewise constant component FEE_DISTANCE_STEP for each step DISTANCE_STEP after that.
    Input "delivery_distance" must be positive.
    """
    if delivery_distance <= 0:
        raise ValueError("input delivery distance must be positive")
    n_distance_steps = ceil(
        (delivery_distance - constants.DISTANCE_MIN) / constants.DISTANCE_STEP
    )
    return constants.FEE_DISTANCE_MIN + n_distance_steps * constants.FEE_DISTANCE_STEP


def compute_items_fee(number_of_items: int) -> int:
    """
    Computes component of delivery fee based on number of items in cart.

    Items above ITEMS_MAX are charged FEE_ITEM per piece. A surcharge of FEE_BULK is added for carts
    with more than ITEMS_BULK items.
    Input "number_of_items" must be positive.
    """
    if number_of_items <= 0:
        raise ValueError("input number of items must be positive")
    bulk_surcharge = constants.FEE_BULK if number_of_items > constants.ITEMS_BULK else 0
    per_item_surcharge = constants.FEE_ITEM * max(
        0, number_of_items - constants.ITEMS_MAX
    )
    return bulk_surcharge + per_item_surcharge


def compute_multiplier_rush_hour(time: datetime) -> float:
    """
    Computes multiplier of delivery fee depending on order time and rush hours.

    The multiplier is set to MULT_RUSH_HOUR if the order time is included in any of the rush hours.
    """
    is_rush_hour = any(
        rush_hour.contains_datetime(time) for rush_hour in constants.RUSH_HOURS
    )
    return constants.MULT_RUSH_HOUR if is_rush_hour else 1.0


def compute_total_fee(cart: Cart) -> int:
    """
    Computes total delivery fee for a given cart.

    Delivery fee is made of three components: fee on cart value, fee on distance, fee on no. of
    items. A multiplier for rush our orders is used. The delivery fee is clamped to FEE_TOTAL_MAX
    and waived completely for orders higher than CART_VALUE_MAX.
    """
    if cart.cart_value >= constants.CART_VALUE_MAX:
        return 0
    total_delivery_fee = (
        compute_cart_value_fee(cart.cart_value)
        + compute_distance_fee(cart.delivery_distance)
        + compute_items_fee(cart.number_of_items)
    )
    multiplier = compute_multiplier_rush_hour(cart.time)
    return min(constants.FEE_TOTAL_MAX, int(multiplier * total_delivery_fee))


router = APIRouter()


@router.post("/delivery-fee")
async def get_delivery_fee(cart: Cart) -> DeliveryFee:
    """Return delivery fee model for a given cart."""
    return DeliveryFee(delivery_fee=compute_total_fee(cart))
