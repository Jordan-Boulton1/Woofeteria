from dataclasses import dataclass
import re

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
    def validate_user_input_is_comma_separated(user_input: str, array_length: int):
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
        pattern = re.compile(r'^(?:[1-' + str(array_length) + '](?:, ?[1-' + str(array_length) + '])*)?$')
        return bool(re.match(pattern, user_input))

    @staticmethod
    def validate_user_input_is_a_number(user_input: str):
        """
        If the user is an empty string or whitespace, returns false.
        Returns a boolean value based on the evaluation if the user input is a digit.
        """
        if len(user_input) == 0:
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
    def validate_input_before_parsing(cart, is_removing: bool = False):
        """
        Replaces the displayed text in the console depending on if the user is removing or adding an item then creates a
        while loop which validates if the provided input contains integers and if more than one they are separated by
        comma.
        If the validation fails the user will be prompted with a message stating the input is invalid.
        Otherwise, the loop will break and return the user input.
        """
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
            user_input = input(f"How many {item.Name} would you like to {info_text}?")
            is_user_input_valid = UserInputValidator.validate_user_input_is_a_number(user_input)
            if not is_user_input_valid:
                print("You didn't enter a number. Please try again.")
            elif item.Stock < int(user_input):
                print("Sorry you have tried to order more than we have in stock.")
            else:
                break
        return user_input

    @staticmethod
    def validate_user_name():
        while True:
            user_input = input("What is your name? ")
            if not user_input.isalpha():
                print("Hmm, that didn't quite hit the bark. Try again.")
            else:
                break
        return user_input

    @staticmethod
    def validate_user_input_is_correct_quantity(item_name: str):
        while True:
            item_quantity = input(f"Please enter the amount of {item_name} you would ike to add to the menu: ")
            validate_item_quantity = UserInputValidator.validate_user_input_is_a_number(item_quantity)
            if not validate_item_quantity:
                print("Please enter a valid input")
            else:
                break
        return int(item_quantity)

    @staticmethod
    def validate_user_input_is_correct_price(item_name):
        while True:
            item_price = input(f"Please enter the price for one {item_name}: ")
            validate_item_price = UserInputValidator.validate_user_input_is_a_decimal(item_price)
            if not validate_item_price:
                print("Please enter a valid input")
            else:
                break
        return float(validate_item_price)

    @staticmethod
    def validate_user_input_is_correct_item_name():
        while True:
            item_name = input("Please enter a name for the new cafeteria item: ")
            if len(item_name) == 0:
                print("Please enter a valid input")
            elif not item_name.isalpha():
                print("Please enter a valid input")
            else:
                break
        return item_name
