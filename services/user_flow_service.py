import copy
from dataclasses import dataclass

from entities.cafeteria_item import CafeteriaItem
from entities.cart import Cart
from infrastructure.enums.enum_icon import Icon
from infrastructure.helpers.user_input_helper import UserInputHelper
from services.cafeteria_item_service import CafeteriaItemService
from services.cart_service import CartService


@dataclass
class UserflowService:
    def __init__(self):
        self.cafeteria_item_service = CafeteriaItemService()
        self.cart_service = CartService()
        self.user_input_helper = UserInputHelper()
        self.menu = self.cafeteria_item_service.get_cafeteria_menu()

    def start_cafeteria_flow(self):
        print(f"{Icon.DogIcon.value} Welcome to Storm's Woofeteria. {Icon.DogIcon.value}\n "
              f"Here is what Chef Storm has to offer.")
        self.__show_menu()
        cart_items = self.__handle_order()
        cart = self.cart_service.add_to_cart(cart_items)
        user_input = input("Are you finished with your order? (Y/N)")
        self.__continue_flow(user_input, cart)

    def __show_menu(self):

        print("Food")
        self.cafeteria_item_service.print_cafeteria_menu()

    def __continue_flow(self, user_input: str, cart: Cart):
        while True:
            if user_input.capitalize() == "Y":
                break
            print("Your current order: ")
            self.cart_service.print_cart(cart)
            user_input = input("Would you like to add or remove item(s) from your cart? (Add/Remove)")
            self.__add_to_cart(user_input, cart)
            user_input = input("Are you finished with your order? (Y/N)")

    def __add_to_cart(self, user_input: str, cart: Cart):
        if user_input.capitalize() == "Add".capitalize():
            self.__show_menu()
            cart_items = self.__handle_order()
            cart.Items.extend(cart_items)
            cart = self.cart_service.update_cart(cart, cart.Items)
            self.cart_service.print_cart(cart)

    def __remove_from_cart(self, user_input: str, cart: Cart):
        self.cart_service.print_cart(cart)
        user_input = input("Which item(s) would you like to remove?\n "
                           "If you wish to remove more than one item please separate each item number by comma.")


    def __handle_order(self):
        ordered_items = self.__order_items(self.menu)
        return self.__subtract_stock(ordered_items)

    def __subtract_stock(self, cart_items: list[CafeteriaItem]):
        menu_list_copy = copy.deepcopy(self.menu)
        for item in cart_items:
            user_input = input(f"How many {item.Name} would you like to order?")
            user_input = int(user_input)
            item.Stock = user_input
            self.cafeteria_item_service.subtract_from_stock(item, menu_list_copy, user_input)
        return cart_items

    def __add_stock(self, cart_items: list[CafeteriaItem]):
        menu_list_copy = copy.deepcopy(self.menu)
        for item in cart_items:
            user_input = input(f"How many {item.Name} would you like to remove?")
            user_input = int(user_input)
            item.Stock = user_input
            self.cafeteria_item_service.add_to_stock(item, menu_list_copy, user_input)
        return cart_items

    def __order_items(self, menu_items: list[CafeteriaItem]):
        user_input = input(
            "Please enter the relevant number from the menu, that corresponds to the item you wish to order.\n "
            "If you wish to order more than one item please separate each item number by comma.")
        item_ids = self.user_input_helper.create_array_from_user_input(user_input)
        return [item for item in menu_items if item.Id in item_ids]
