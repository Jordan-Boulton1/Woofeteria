from dataclasses import dataclass
@dataclass
class PriceConverter:
    @staticmethod
    def format_price(price: float):
        """
        Formats the price to 2 decimal places.
        """
        return "{0:.2f}".format(price)