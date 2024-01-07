from dataclasses import dataclass
import re

from entities.cafeteria_item import CafeteriaItem


@dataclass
class UserInputValidator:
    @staticmethod
    def create_array_from_user_input(user_input: str):
        return [int(x) for x in user_input.split(',') if x.strip().isdigit()]

    @staticmethod
    def validate_user_input_is_comma_separated(user_input: str, array_length: int):
        if len(user_input) == 0:
            return False
        pattern = re.compile(r'^(?:[1-' + str(array_length) + '](?:, ?[1-' + str(array_length) + '])*)?$')
        return bool(re.match(pattern, user_input))

    @staticmethod
    def validate_user_input_is_a_number(user_input: str):
        if len(user_input) == 0:
            return False
        return bool(user_input.isdigit())

    @staticmethod
    def validate_user_input_is_a_decimal(user_input: str):
        if len(user_input) == 0:
            return False
        elif user_input.replace(".", "").isnumeric():
            return True
        else:
            return False

    @staticmethod
    def validate_input_before_parsing(cart, is_removing: bool = False):
        info_text = (
            "Please enter the relevant number from the menu, that corresponds to the item you wish to order.\n "
            "If you wish to order more than one item please separate each item number by comma.")
        if is_removing:
            info_text = ("Which item(s) would you like to remove?\n "
                         "If you wish to remove more than one item please separate each item number by comma.")
        while True:
            user_input = input(info_text)
            is_user_input_valid = UserInputValidator.validate_user_input_is_comma_separated(user_input,
                                                                                            len(cart.Items))
            if not is_user_input_valid:
                print("The value you entered is invalid, please try again.")
            else:
                break
        return user_input

    @staticmethod
    def validate_input_for_items(item: CafeteriaItem, is_removing: bool = False):
        info_text = "order"
        if is_removing:
            info_text = "remove"
        if item is None:
            print("Sorry, we could find an item with that Id")
        while True:
            user_input = input(f"How many {item.Name} would you like to {info_text}?")
            is_user_input_valid = UserInputValidator.validate_user_input_is_a_number(user_input)
            if not is_user_input_valid:
                print("You didn't enter a number. Please try again.")
            elif item.Stock < int(user_input):
                print("Sorry you have tried to order more than we have in stock.")
            else:
                break
        return user_input
