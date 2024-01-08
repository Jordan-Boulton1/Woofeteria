from dataclasses import dataclass
@dataclass
class PriceConverter:
    def format_price(self, price: float):
        """
        Formats the price to 2 decimal places.
        """
        return "{0:.2f}".format(price)