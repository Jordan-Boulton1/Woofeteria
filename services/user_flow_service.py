import copy
from dataclasses import dataclass

from entities.cafeteria_item import CafeteriaItem
from entities.cart import Cart
from infrastructure.enums.enum_icon import Icon
from infrastructure.helpers.price_converter import PriceConverter
from infrastructure.validators.user_input_validator import UserInputValidator
from services.cafeteria_item_service import CafeteriaItemService
from services.cart_service import CartService


@dataclass
class UserflowService:
    def __init__(self):
        self.cafeteria_item_service = CafeteriaItemService()
        self.cart_service = CartService()
        self.price_converter = PriceConverter()
        self.menu = self.cafeteria_item_service.get_cafeteria_menu()
        self.unique_set = set()
        self.cart_result = []

    def start_cafeteria_flow(self):
        print(f"{Icon.DogIcon.value} Welcome to Storm's Woofeteria. {Icon.DogIcon.value}\n "
              f"Here is what Chef Storm has to offer.")
        self.__show_menu()
        cart_items = self.__handle_order()
        cart = self.cart_service.add_to_cart(cart_items)
        while True:
            user_input = input("Are you finished with your order? (Y/N)")
            if user_input.capitalize() == "Y":
                self.__complete_user_flow(cart)
                break
            elif user_input.capitalize() == "N":
                self.__continue_flow(user_input, cart)
                break
            else:
                print("The input entered is not valid. Please try using (Y/N)")

    def __show_menu(self):
        print("Food")
        self.cafeteria_item_service.print_cafeteria_menu()

    def __continue_flow(self, user_input: str, cart: Cart):
        while True:
            if user_input.capitalize() == "Y":
                self.__complete_user_flow(cart)
                break
            elif user_input.capitalize() == "N":
                print("Your current order: ")
                self.cart_service.print_cart(cart)

                while True:
                    user_input = input("Would you like to add or remove item(s) from your cart? (Add/Remove)")
                    if user_input.capitalize() == "Add".capitalize():
                        self.__add_to_cart(cart)
                        self.__handle_continue_flow(cart)
                    elif user_input.capitalize() == "Remove".capitalize():
                        self.__remove_from_cart(cart)
                        self.__handle_continue_flow(cart)
                    else:
                        print("The input entered is not valid. Please try using (Add/Remove)")
            else:
                print("The input entered is not valid. Please try using (Y/N)")

    def __handle_continue_flow(self, cart: Cart):
        while True:
            user_input = input("Are you finished with your order? (Y/N)")
            if user_input.capitalize() == "Y":
                self.__complete_user_flow(cart)
                break
            elif user_input.capitalize() == "N":
                self.__continue_flow(user_input, cart)
                break
            else:
                print("The input entered is not valid. Please try using (Y/N)")

    def __complete_user_flow(self, cart: Cart):
        while True:
            formatted_price = self.price_converter.format_price(cart.TotalPrice)
            print("That's great, your total price is £", formatted_price)
            user_input = input("Please enter the amount on screen to complete your purchase.")
            is_user_input_valid = UserInputValidator.validate_user_input_is_a_decimal(user_input)
            if not is_user_input_valid:
                print("Please enter the expected price")
            elif formatted_price != user_input:
                print("What you have entered does not match the total expected price. Please try again.")
            else:
                print("Thank you, have a woofin day")
                break

    def __add_to_cart(self, cart: Cart):
        self.__show_menu()
        cart_items = self.__handle_order()
        cart.Items = cart_items
        self.cart_service.update_cart(cart, cart.Items)

    def __remove_from_cart(self, cart: Cart):
        user_input = UserInputValidator.validate_input_before_parsing(cart, True)
        item_ids = UserInputValidator.create_array_from_user_input(user_input)
        cart_items = [item for item in cart.Items if item.Id in item_ids]
        cart.Items = self.__add_stock(cart_items)
        self.cart_service.update_cart(cart, cart.Items)

    def __handle_order(self):
        ordered_items = self.__order_items(self.menu)
        return self.__subtract_stock(ordered_items)

    def __subtract_stock(self, cart_items: list[CafeteriaItem]):
        menu_list_copy = copy.deepcopy(self.cafeteria_item_service.get_cafeteria_menu())
        for item in cart_items:
            menu_item = next((x for x in menu_list_copy if x.Id == item.Id), None)
            user_input = int(UserInputValidator.validate_input_for_items(menu_item))
            if item.Id not in self.unique_set:
                self.unique_set.add(item.Id)
                item.Stock = user_input
                self.cart_result.append(item)
            else:
                item.Stock += user_input
            self.cafeteria_item_service.subtract_from_stock(item, menu_list_copy, user_input)
        return self.cart_result

    def __add_stock(self, cart_items: list[CafeteriaItem]):
        menu_list_copy = copy.deepcopy(self.cafeteria_item_service.get_cafeteria_menu())
        cart_items_updated = []
        for item in cart_items:
            user_input = int(UserInputValidator.validate_input_for_items(item, True))
            if item.Stock == 1:
                self.cafeteria_item_service.add_to_stock(item, menu_list_copy, user_input)
                continue
            else:
                item.Stock -= user_input
                cart_items_updated.append(item)
            self.cafeteria_item_service.add_to_stock(item, menu_list_copy, user_input)
        return cart_items_updated

    def __order_items(self, menu_items: list[CafeteriaItem]):
        cart = self.cart_service.add_to_cart(menu_items)
        user_input = UserInputValidator.validate_input_before_parsing(cart)
        item_ids = UserInputValidator.create_array_from_user_input(user_input)
        return [item for item in menu_items if item.Id in item_ids]
