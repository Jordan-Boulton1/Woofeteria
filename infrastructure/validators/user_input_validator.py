import re
from colorama import Style
from dataclasses import dataclass
from entities.cafeteria_item import CafeteriaItem


@dataclass
class UserInputValidator:
    @staticmethod
    def create_array_from_user_input(user_input: str):
        """
        Splits each character, if it is an integer, in the user input string into an array of integers.
        """
        return [int(x) for x in user_input.split(',') if x.strip().isdigit()]

    @staticmethod
    def validate_user_input_is_comma_separated(user_input: str, start: int, end: int):
        """
        If the user is an empty string or whitespace, returns false.
        Otherwise, creates a regex pattern that will accept only integers from 1 until the array length provided.
        If the user input contains more than one integer from 1 until the array length provided the pattern expects the
        integers to be separated by comma with optional space inbetween.
        After that it matches the user input against the regex pattern and returns a boolean value depending on the
        matching evaluation.
        """
        if len(user_input) == 0:
            return False
        pattern = re.compile(r'^(?:[' + str(start) + '-' + str(end) + '](?:, ?[' + str(start) + '-' + str(end) + '])*)?$')
        return bool(re.match(pattern, user_input))

    @staticmethod
    def validate_user_input_is_a_number(user_input: str):
        """
        If the user is an empty string or whitespace, returns false.
        Returns a boolean value based on the evaluation if the user input is a digit.
        """
        if len(user_input) == 0:
            return False
        elif user_input == "0":
            return False
        return bool(user_input.isdigit())

    @staticmethod
    def validate_user_input_is_a_decimal(user_input: str):
        """
        If the user is an empty string or whitespace, returns false.
        Replaces the "." in the user input string with an empty string and checks if the result of that is numeric.
        If it is numeric it returns true otherwise, it returns false.
        """
        if len(user_input) == 0:
            return False
        elif user_input.replace(".", "").isnumeric():
            return True
        else:
            return False

    @staticmethod
    def validate_input_before_parsing(cafeteria_items: list[CafeteriaItem], is_removing: bool = False, is_updating: bool = False):
        """
        Replaces the displayed text in the console depending on if the user is removing or adding an item then creates a
        while loop which validates if the provided input contains integers and if more than one they are separated by
        comma.
        If the validation fails the user will be prompted with a message stating the input is invalid.
        Otherwise, the loop will break and return the user input.
        """
        action = "order"
        if is_updating:
            action = "update"
        info_text = (
            f"Please enter the relevant number from the menu, that corresponds to the item you wish to {action}.\n"
            f"If you wish to {action} more than one item please separate each item number by comma.\n")
        if is_removing:
            info_text = ("Which item(s) would you like to remove?\n "
                         "If you wish to remove more than one item please separate each item number by comma.\n")
        while True:
            user_input = input(info_text)
            first_item = cafeteria_items[0]
            last_item = cafeteria_items[-1]
            is_user_input_valid = UserInputValidator.validate_user_input_is_comma_separated(user_input,
                                                                                            first_item.Id, last_item.Id)
            if not is_user_input_valid:
                print("The value you entered is invalid, please try again.")
            else:
                break
        return user_input

    @staticmethod
    def validate_input_for_items(item: CafeteriaItem, is_removing: bool = False):
        """
               Replaces the displayed text in the console depending on if the user is removing or adding an item then creates
               a while loop that prompts the user how much of the selected item they wish to order or remove and validates if
               the provided input contains integers and if more than one they are separated by comma.
               If the validation fails the user will be prompted with a message stating the input is invalid.
               Otherwise, the loop will break and return the user input.
               """
        info_text = "order"
        if is_removing:
            info_text = "remove"
        if item is None:
            print("Sorry, we could find an item with that Id")
        while True:
            user_input = input(f"How many {item.Name} would you like to {info_text}?\n")
            is_user_input_valid = UserInputValidator.validate_user_input_is_a_number(user_input)
            if not is_user_input_valid:
                print("You didn't enter a valid input. Please try again.")
            else:
                break
        return user_input

    @staticmethod
    def validate_user_name():
        while True:
            user_input = input("What is your name?\n")
            if not UserInputValidator.__validate_user_input_is_name(user_input):
                print("Hmm, that didn't quite hit the bark. Try again.")
            else:
                break
        return user_input

    @staticmethod
    def validate_user_input_is_correct_quantity(item_name: str, is_updating: bool = False, is_admin: bool = False):
        result = ""
        info_text = f"Please enter the amount of {item_name} you would like to add to the menu:\n"
        if is_admin:
            info_text = f"Please enter the amount of {item_name} you would like to add to the menu, or enter {Style.BRIGHT}'Skip'{Style.RESET_ALL}:\n"
        while True:
            item_quantity = input(info_text)
            if is_updating and item_quantity.capitalize() == "Skip":
                result = "Skip"
                break
            validate_item_quantity = UserInputValidator.validate_user_input_is_a_number(item_quantity)
            if not validate_item_quantity:
                print("Please enter a valid input")
            else:
                result = int(item_quantity)
                break
        return result

    @staticmethod
    def validate_user_input_is_correct_price(item_name: str, is_updating: bool = False, is_admin: bool = False):
        result = ""
        info_text = f"Please enter the price for one {item_name}:\n"
        if is_admin:
            info_text = f"Please enter the price for one {item_name} or enter {Style.BRIGHT}'Skip'{Style.RESET_ALL}:\n"
        while True:
            item_price = input(info_text)
            if is_updating and item_price.capitalize() == "Skip":
                result = "Skip"
                break
            validate_item_price = UserInputValidator.validate_user_input_is_a_decimal(item_price)
            if not validate_item_price:
                print("Please enter a valid input")
            else:
                result = float(item_price)
                break
        return result

    @staticmethod
    def validate_user_input_is_correct_item_name(menu: list[CafeteriaItem], info_text: str, is_updating: bool = False):
        while True:
            item_name = input(info_text)
            if len(item_name) == 0:
                print("Please enter a valid input")
            elif not UserInputValidator.__validate_user_input_is_name(item_name):
                print("Please enter a valid input")
            elif next((x for x in menu if x.Name.capitalize() == item_name.capitalize()), None) is not None:
                print(f"An item with the name {item_name.title()} already exists in the menu")
            elif is_updating and item_name.capitalize() == "Skip":
                break
            else:
                break
        return item_name


    @staticmethod
    def __validate_user_input_is_name(user_input: str):
        if len(user_input) == 0:
            return False
        pattern = "^(?=.{2,100}$)[^\W\d_]+(?:[-' ][^\W\d_]+)*[.?!]?$"
        return bool(re.match(pattern, user_input))

