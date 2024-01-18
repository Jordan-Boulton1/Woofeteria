from dataclasses import dataclass

from entities.cafeteria_item import CafeteriaItem


@dataclass
class Cart:
    """
    Represents a shopping cart in a cafeteria application.

    Attributes:
        Items (List[CafeteriaItem]): A list of CafeteriaItem objects
         representing items in the cart.
        TotalQuantity (int): The total quantity of items in the cart.
        TotalPrice (float): The total price of all items in the cart.
    """
    Items: list[CafeteriaItem]
    TotalQuantity: int
    TotalPrice: float
