from dataclasses import dataclass


@dataclass
class CafeteriaItem:
    """
    Represents a cafeteria item with unique identifier, name, price, and stock.

    Attributes:
        Id (int): A unique identifier for the cafeteria item.
        Name (str): The name of the cafeteria item.
        Price (float): The price of the cafeteria item.
        Stock (int): The available stock or quantity of the cafeteria item.
    """
    Id: int
    Name: str
    Price: float
    Stock: int
