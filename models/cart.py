from dataclasses import dataclass
@dataclass
class Cart:
    items: list
    quantity: int
    total_price: float
