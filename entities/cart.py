from dataclasses import dataclass

from entities.cafeteria_item import CafeteriaItem


@dataclass
class Cart:
    Items: list[CafeteriaItem]
    TotalQuantity: int
    TotalPrice: float
