import re
from decimal import Decimal


def validate_name(name: str) -> None:
    if re.search(r"^[A-Za-z0-9\s,.-]*$", name) is None:
        raise ValueError(f"Name {name} contains non-english letters")


def validate_price(price: Decimal) -> None:
    if price < 0:
        raise ValueError(f"Price cannot be negative")


def validate_inventory(inventory: int) -> None:
    if inventory < 0:
        raise ValueError(f"Inventory cannot be negative")