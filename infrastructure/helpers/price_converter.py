from dataclasses import dataclass
@dataclass
class PriceConverter:
    def format_price(self, price: float):
        return "{0:.2f}".format(price)