import colorama
from colorama import Style
from tabulate import tabulate
from dataclasses import dataclass

from entities.cafeteria_item import CafeteriaItem
from infrastructure.helpers.price_converter import PriceConverter
from infrastructure.validators.user_input_validator import UserInputValidator


class CafeteriaItemService:
    def __init__(self):
        self.cafeteria_items = self.__populate_cafeteria_menu()
        self.price_converter = PriceConverter()

    def print_cafeteria_menu(self, menu: list[CafeteriaItem]):
        headers = ["ID", "Name", "Price", "Stock"]
        table_items = []
        for item in menu:
            table_item = [item.Id, item.Name, f"£ {item.Price:.2f}", item.Stock]
            table_items.append(table_item)
        table1 = tabulate(table_items, headers=headers, tablefmt="pretty")
        print(table1)

    def get_cafeteria_menu(self):
        """
        Returns the list of cafeteria menu items.
        """
        return self.cafeteria_items

    def add_items_to_menu(self, amount_of_items: int):
        last_item = self.cafeteria_items[-1]
        input_text = "Please enter a name for the new cafeteria item: "
        for i in range(amount_of_items):
            item_id = last_item.Id + 1
            item_name = UserInputValidator.validate_user_input_is_correct_item_name(self.cafeteria_items,
                                                                                    input_text).title()
            validated_item_quantity = UserInputValidator.validate_user_input_is_correct_quantity(item_name)
            validated_item_price = UserInputValidator.validate_user_input_is_correct_price(item_name)
            item = CafeteriaItem(item_id, item_name, validated_item_price, validated_item_quantity)
            self.cafeteria_items.append(item)
        return self.cafeteria_items

    def update_items(self, item_ids: list[int]):
        for item in self.cafeteria_items:
            for item_id in item_ids:
                if item.Id == item_id:
                    input_text = f"Please enter a new name for {item.Name} or type '{Style.BRIGHT}Skip{Style.RESET_ALL}' not to change it."
                    item_name = UserInputValidator.validate_user_input_is_correct_item_name(
                        self.cafeteria_items,
                        input_text,
                        True).title()
                    item = self.__handle_update_value(item_name, item)
                    validated_item_quantity = UserInputValidator.validate_user_input_is_correct_quantity(item.Name,
                                                                                                         True)
                    item = self.__handle_update_value(validated_item_quantity, item)
                    validated_item_price = UserInputValidator.validate_user_input_is_correct_price(item.Name, True)
                    item = self.__handle_update_value(validated_item_price, item)
        return self.cafeteria_items

    def __handle_update_value(self, user_input, item: CafeteriaItem):
        if user_input != "Skip":
            if type(user_input) is str:
                item.Name = user_input
            if type(user_input) is int:
                item.Stock = user_input
            if type(user_input) is float:
                item.Price = user_input
        return item

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

    def recalculate_ids(self, menu_list: list[CafeteriaItem]):
        for index, item in enumerate(menu_list, start=1):
            item.Id = index
        return menu_list

    def __populate_cafeteria_menu(self):
        """
        Populates the menu with initial values.
        """
        menu = [
            CafeteriaItem(1, "Waggy Woofin", 2.50, 10),
            CafeteriaItem(2, "Paw Cake", 3.20, 10),
            CafeteriaItem(3, "Cheeky Cheese Paw", 1.80, 10),
            CafeteriaItem(4, "Barky Bacon Stick", 2.00, 10),
            CafeteriaItem(5, "Sonny's Soup", 1.40, 10),
            CafeteriaItem(6, "Alfie's Apple Tart", 2.50, 10),
            CafeteriaItem(7, "Barkie", 0.80, 10),
            CafeteriaItem(8, "Storm's Special Chicken Stew", 4.20, 10)]
        return menu