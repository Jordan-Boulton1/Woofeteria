from dataclasses import dataclass

from entities.cafeteria_item import CafeteriaItem
from infrastructure.helpers.price_converter import PriceConverter


class CafeteriaItemService:
    def __init__(self):
        self.cafeteria_items = self.__populate_cafeteria_menu()
        self.price_converter = PriceConverter()

    def print_cafeteria_menu(self):
        for item in self.cafeteria_items:
            print(f"{item.Id}. {item.Name} - £{self.price_converter.format_price(item.Price)} | Stock - {item.Stock}")

    def get_cafeteria_menu(self):
        return self.cafeteria_items

    def __populate_cafeteria_menu(self):
        menu = [
            CafeteriaItem(1, "Woofin", 2.50, 10),
            CafeteriaItem(2, "Paw Cake", 3.20, 10),
            CafeteriaItem(3, "Cheeky Cheese Paws", 1.80, 10),
            CafeteriaItem(4, "Pup Cake", 2.00, 10)]
        return menu
