from dataclasses import dataclass


@dataclass
class PriceConverter:
    """
    A utility class for formatting prices.
    This class provides methods to format prices to a specific decimal
    precision.
    """
    @staticmethod
    def format_price(price: float):
        """
        Format the given price to two decimal places.
        Args:
            price (float): The price value to be formatted.
        Returns:
            str: The formatted price as a string with two decimal places.
        """
        return "{0:.2f}".format(price)
