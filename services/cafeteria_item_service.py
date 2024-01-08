from dataclasses import dataclass

from entities.cafeteria_item import CafeteriaItem
from infrastructure.helpers.price_converter import PriceConverter


class CafeteriaItemService:
    def __init__(self):
        self.cafeteria_items = self.__populate_cafeteria_menu()
        self.price_converter = PriceConverter()

    def print_cafeteria_menu(self):
        """
        Prints the menu to the console.
        """
        for item in self.cafeteria_items:
            print(f"{item.Id}. {item.Name} - £{self.price_converter.format_price(item.Price)} | Stock - x{item.Stock}")

    def get_cafeteria_menu(self):
        """
        Returns the list of cafeteria menu items.
        """
        return self.cafeteria_items

    def subtract_from_stock(self, ordered_item: CafeteriaItem, menu_list: list[CafeteriaItem], ordered_amount: int):
        """
        Loops through the menu list and checks if the id of the item passed in the function matches the current item id
        in the loop, if it does it subtract the ordered amount from the current item stock and reassigns the menu to
        the newly updated one.
        """
        for cafeteria_item in menu_list:
            if ordered_item.Id == cafeteria_item.Id:
                cafeteria_item.Stock -= ordered_amount
        self.cafeteria_items = menu_list

    def add_to_stock(self, ordered_item: CafeteriaItem, menu_list: list[CafeteriaItem], ordered_amount: int):
        """
        Loops through the menu list and checks if the id of the item passed in the function matches the current item id
        in the loop, if it does it add the ordered amount to the current item stock and reassigns the menu to
        the newly updated one.
        """
        for cafeteria_item in menu_list:
            if ordered_item.Id == cafeteria_item.Id:
                cafeteria_item.Stock += ordered_amount
        self.cafeteria_items = menu_list

    def __populate_cafeteria_menu(self):
        """
        Populates the menu with initial values.
        """
        menu = [
            CafeteriaItem(1, "Woofin", 2.50, 10),
            CafeteriaItem(2, "Paw Cake", 3.20, 10),
            CafeteriaItem(3, "Cheeky Cheese Paws", 1.80, 10),
            CafeteriaItem(4, "Pup Cake", 2.00, 10)]
        return menu
