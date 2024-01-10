import copy
import colorama
from dataclasses import dataclass
from colorama import Fore, Back, Style

from infrastructure.helpers.color_helper import ColorHelper

colorama.init()

from entities.cafeteria_item import CafeteriaItem
from entities.cart import Cart
from infrastructure.enums.enum_icon import Icon
from infrastructure.helpers.price_converter import PriceConverter
from infrastructure.validators.user_input_validator import UserInputValidator
from services.admin_service import AdminService
from services.cafeteria_item_service import CafeteriaItemService
from services.cart_service import CartService


@dataclass
class UserflowService:
    def __init__(self):
        self.cafeteria_item_service = CafeteriaItemService()
        self.admin_service = AdminService()
        self.cart_service = CartService()
        self.price_converter = PriceConverter()
        self.menu = self.cafeteria_item_service.get_cafeteria_menu()
        self.unique_set = set()
        self.cart_result = []

    def start_cafeteria_flow(self):
        """
        Starts the cafeteria and shows the user the menu, initialises the cart and adds the items to it.
        Also allows the user to either continue or finish their order.
        If the user provides unexpected inputs, the user will be prompted with a message stating that the input was not
        valid.
        """
        print(f"{Icon.DogIcon.value} Welcome to Storm's Woofeteria. {Icon.DogIcon.value}")
        user_input = UserInputValidator.validate_user_name()
        admin_name_provided = self.admin_service.validate_if_admin_name_provided(user_input)
        if not admin_name_provided[0]:
            if admin_name_provided[1] is not None:
                self.menu = admin_name_provided[1]
            print(f"Hello {user_input.title()}. Here is what Chef Storm has to offer.")
            self.__show_menu()
            cart_items = self.__handle_order(self.menu)
            cart = self.cart_service.add_to_cart(cart_items)
            while True:
                user_input = input(f"Are you finished with your order?"
                                   f"{ColorHelper.color_yes_no_text()} ")
                if user_input.capitalize() == "Y":
                    self.__complete_user_flow(cart)
                    break
                elif user_input.capitalize() == "N":
                    self.__continue_flow(user_input, cart)
                    break
                else:
                    print(f"The input entered is not valid. Please try using {ColorHelper.color_yes_no_text()} ")

    def __show_menu(self):
        """
        Shows the menu
        """
        print("Food")
        self.cafeteria_item_service.print_cafeteria_menu(self.menu)

    def __continue_flow(self, user_input: str, cart: Cart):
        """
        If the user provides the input value of "Y", the ordering flow will be completed.
        If the user provides the input value of "N", the ordering flow will provide two options to the user "Add" or
        "Remove". If "Add" is selected the user will be able to add more items to their cart. If "Remove" is selected
        the user will be able to remove items from their cart.
        If the user provides unexpected inputs, the user will be prompted with a message stating that the input was not
        valid.
        """
        is_flow_continued = True
        while True:
            if user_input.capitalize() == "Y":
                is_flow_continued = False
                self.__complete_user_flow(cart)
            elif user_input.capitalize() == "N":
                print("Your current order: ")
                self.cart_service.print_cart(cart)
                is_flow_continued = self.__show_options(cart)
            if is_flow_continued:
                continue
            else:
                self.__complete_user_flow(cart)
                break


    def __show_options(self, cart: Cart):
        result = False
        while True:
            user_input = input("Would you like to add or remove item(s) from your cart? (Add/Remove) ")
            if user_input.capitalize() == "Add":
                self.__add_to_cart(cart)
                result = self.__handle_continue_flow()
                break
            elif user_input.capitalize() == "Remove":
                self.__remove_from_cart(cart)
                result = self.__handle_continue_flow()
                break
            else:
                print("The input entered is not valid. Please try using (Add/Remove)")
        return result

    def __handle_continue_flow(self):
        """
        Handles the continuation of the ordering flow and ensures that the user can only provide a valid input, "Y" or
        "N".
        """
        result = True
        while True:
            user_input = input(f"Are you finished with your order? {ColorHelper.color_yes_no_text()} ")
            if user_input.capitalize() == "Y":
                result = False
                break
            elif user_input.capitalize() == "N":
                break
            else:
                print(f"The input entered is not valid. Please try using{ColorHelper.color_yes_no_text()} ")
        return result

    def __complete_user_flow(self, cart: Cart):
        """
        When completing the flow the user will be presented with the total price of their cart, which is formatted to
        two decimal places.
        The user will be asked to enter the exact amount of money they need to pay in order to complete their order.
        If the user enters a value that is not a decimal number, the user will be shown an error message stating that
        they have not entered a valid input.
        If the user enters a value that does not match the total price of the cart, the user will be shown an error
        message stating that the value they have entered does not match the total price of the cart.
        """
        formatted_price = self.price_converter.format_price(cart.TotalPrice)
        info_text = f"That's great, your total price is £{formatted_price}"
        while True:
            print(info_text)
            user_input = input("Please enter the amount on screen to complete your purchase. ")
            is_user_input_valid = UserInputValidator.validate_user_input_is_a_decimal(user_input)
            if not is_user_input_valid:
                print("Please enter a valid input")
                info_text = f"Your total price is £{formatted_price}"
            elif formatted_price != user_input:
                print("What you have entered does not match the total expected price. Please try again. ")
                info_text = f"Your total price is £{formatted_price}"
            else:
                print("Thank you, have a woofin day")
                break

    def __add_to_cart(self, cart: Cart):
        """
        Prints the menu and adds the ordered item to the cart.
        """
        self.__show_menu()
        cart_items = self.__handle_order(self.menu)
        cart.Items = cart_items
        self.cart_service.update_cart(cart, cart.Items)

    def __remove_from_cart(self, cart: Cart):
        """
        Validates that the user input contains integers and if there is more than one item they are separated by a
        comma.
        Then an array of integers is created from the user input and that array is used to locate the items in the cart
        after that the item is removed from the cart and added back to the cafeteria stock.
        """
        user_input = UserInputValidator.validate_input_before_parsing(cart.Items, True)
        item_ids = UserInputValidator.create_array_from_user_input(user_input)
        cart_items = [item for item in cart.Items if item.Id in item_ids]
        cart.Items = self.__add_stock(cart_items)
        self.cart_service.update_cart(cart, cart.Items)

    def __handle_order(self, items: list[CafeteriaItem]):
        """
        Orders the selected item from the user and removes it from the cafeteria stock.
        """
        ordered_items = self.__order_items(items)
        return self.__subtract_stock(ordered_items)

    def __subtract_stock(self, cart_items: list[CafeteriaItem]):
        """
        Creates a deepcopy of the cafeteria menu in order to preserve the original value of the menu, then we loop
        through the items inside the user cart and for each one of the items we find a specific one by matching the ids
        from the menu, and then we check if the item with the specified id is inside the unique global set if it is not
        we add the id to the unique set, and then we override the item stock with the user input and add it to a global
        array of cafeteria items.
        If the item id is already in the unique set, we simply add the user input to the stock of the existing item.
        Finally, we subtract the ordered item from the stock of the cafeteria.
        """
        menu_list_copy = copy.deepcopy(self.cafeteria_item_service.get_cafeteria_menu())
        for item in cart_items:
            menu_item = next((x for x in menu_list_copy if x.Id == item.Id), None)
            user_input = int(UserInputValidator.validate_input_for_items(menu_item))
            if item.Id not in self.unique_set:
                self.unique_set.add(item.Id)
                item.Stock = user_input
                self.cart_result.append(item)
            else:
                cart_item = next((x for x in self.cart_result if x.Id == item.Id), None)
                cart_item.Stock += user_input
            self.cafeteria_item_service.subtract_from_stock(item, menu_list_copy, user_input)
        self.menu = self.cafeteria_item_service.get_cafeteria_menu()
        return self.cart_result

    def __add_stock(self, cart_items: list[CafeteriaItem]):
        """
        Creates a deepcopy of the cafeteria menu in order to preserve the original value of the menu.
        We then create an empty array that will store the updated items for the user cart, then we loop through the
        items in the user cart, we validate the input, and then we check if the user is trying to remove an item from
        their cart that has a quantity of "1", we add it back to the cafeteria stock and continue the loop, otherwise
        we subtract from the quantity of the item in the user cart, we add it to the array that we created, and add the
        item back to the cafeteria stock.
        """
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
        self.menu = self.cafeteria_item_service.get_cafeteria_menu()
        return cart_items_updated

    def __order_items(self, menu_items: list[CafeteriaItem]):
        """
        Adds the ordered items to the cart, and validates that the user has entered integers and if more than one,
        they are separated by a comma then we create an array of integers from the user input and locate and return
        the items from the menu by their corresponding id.
        """
        user_input = UserInputValidator.validate_input_before_parsing(menu_items)
        item_ids = UserInputValidator.create_array_from_user_input(user_input)
        return [item for item in menu_items if item.Id in item_ids]
