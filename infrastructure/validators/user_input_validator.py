import re
from dataclasses import dataclass

from colorama import Style

from entities.cafeteria_item import CafeteriaItem


@dataclass
class UserInputValidator:
    """
    A utility class for validating user inputs in a cafeteria application.

    This class provides static methods for validating various types of user
    inputs, including integers, decimals, item IDs, and names.
    It also handles input parsing and user prompts related to the
    cafeteria application.
    """
    @staticmethod
    def create_array_from_user_input(user_input: str):
        """
        Create an array of integers from a comma-separated user input string.
        Args:
            user_input (str): A comma-separated string containing integer
             values.
        Returns:
            list: A list of integers extracted from the user input string.
        """
        return [int(x) for x in user_input.split(',') if x.strip().isdigit()]

    @staticmethod
    def validate_item_ids(items: list[CafeteriaItem],
                          is_removing: bool = False):
        """
        Validate user input for selecting CafeteriaItems by their IDs.
        Args:
            items (list[CafeteriaItem]): The list of CafeteriaItems to validate
             against.
            is_removing (bool): A flag indicating whether the operation is for
             removal.
        Returns:
           list[CafeteriaItem]: A list of CafeteriaItems corresponding to the
           validated item IDs. This function prompts the user to input item
           IDs, validates the input against the provided list of CafeteriaItems
           and returns a list of found CafeteriaItems. If removal is intended,
           the input is additionally validated to ensure the IDs exist in the
           provided list of items.
        """
        while True:
            user_input = (UserInputValidator.validate_input_before_parsing
                          (items, is_removing))
            item_ids = (UserInputValidator.create_array_from_user_input
                        (user_input))
            menu_ids = [x.Id for x in items]
            is_input_valid_ids = all(ele in menu_ids for ele in item_ids)
            if not is_input_valid_ids:
                print("The value you entered is invalid, please try again.")
            else:
                found_items = [item for item in items if item.Id in item_ids]
                break
        return found_items

    @staticmethod
    def validate_user_input_is_comma_separated(user_input: str, start: int,
                                               end: int):
        """
        Validate that user input is a comma-separated list of integers within
        a specified range.
        Args:
            user_input (str): The user-provided input to be validated.
            start (int): The lower bound of the allowed range.
            end (int): The upper bound of the allowed range.
        Returns:
            bool: True if the input is a valid comma-separated list of integers
             within the specified range, False otherwise. This function checks
             whether the user input is a non-empty string consisting of
             integers separated by commas. The integers are expected to be
             within the specified range [start, end].
        """
        if len(user_input) == 0:
            return False
        pattern = re.compile(
            r'^(?:[' + str(start) + '-' + str(end) + '](?:, ?[' + str(start) +
            '-' + str(end) + '])*)?$')
        return bool(re.match(pattern, user_input))

    @staticmethod
    def validate_user_input_is_a_number(user_input: str):
        """
        Validate that user input is a non-zero positive integer.
        Args:
            user_input (str): The user-provided input to be validated.
        Returns:
            bool: True if the input is a non-zero positive integer, False
            otherwise.
        This function checks whether the user input is a non-empty string
        representing a non-zero positive integer.
        """
        if len(user_input) == 0:
            return False
        elif user_input == "0":
            return False
        return bool(user_input.isdigit())

    @staticmethod
    def validate_user_input_is_a_decimal(user_input: str):
        """
        Validate that user input is a positive decimal number with exactly two
        decimal places.
        Args:
            user_input (str): The user-provided input to be validated.
        Returns:
            bool: True if the input is a positive decimal number with exactly
            two decimal places, False otherwise.
        """
        try:
            integral, fractional = user_input.split('.')
            number = float(user_input)
            if len(fractional) != 2:
                return False
            elif number <= 0:
                return False
            else:
                return True
        except ValueError:
            return False

    @staticmethod
    def validate_input_before_parsing(cafeteria_items: list[CafeteriaItem],
                                      is_removing: bool = False,
                                      is_updating: bool = False):
        """
        Validate user input before parsing for ordering, updating, or
        removing items.
        Args:
            cafeteria_items (list[CafeteriaItem]): The list of CafeteriaItems
             to validate against.
            is_removing (bool): A flag indicating whether the operation is for
             removing.
            is_updating (bool): A flag indicating whether the operation is for
             updating.
        Returns:
            str: The validated user input containing item numbers separated
            by commas.
        This function prompts the user to input item numbers, validates the
        input against the provided list of CafeteriaItems, and returns the
        validated user input. It provides context-specific information based
        on the operation (order, update, or remove).
        """
        action = "order"
        if is_updating:
            action = "update"
        info_text = (
            f"Please enter the relevant number from the menu, that "
            f"corresponds to the item you wish to {action}.\n"
            f"If you wish to {action} more than one item please separate "
            f"each item number by comma.\n")
        if is_removing:
            info_text = ("Which item(s) would you like to remove?\n"
                         "If you wish to remove more than one item please "
                         "separate each item number by comma.\n")
        while True:
            user_input = input(info_text)
            first_item = cafeteria_items[0]
            last_item = cafeteria_items[-1]
            is_user_input_valid = (UserInputValidator.
                                   validate_user_input_is_comma_separated
                                   (user_input, first_item.Id, last_item.Id))
            if not is_user_input_valid:
                print("The value you entered is invalid, please try again.")
            else:
                break
        return user_input

    @staticmethod
    def validate_input_for_items(item: CafeteriaItem,
                                 is_removing: bool = False):
        """
        Validate user input for the quantity of a CafeteriaItem to order or
        remove.
        Args:
            item (CafeteriaItem): The CafeteriaItem for which the quantity is
             being validated.
            is_removing (bool): A flag indicating whether the operation is for
             removing.
        Returns:
            str: The validated user input representing the quantity.
        This function prompts the user to input the quantity of a specific
        CafeteriaItem for ordering or removing, validates the input as a
        non-zero positive integer, and returns the validated user input.
        """
        info_text = "order"
        if is_removing:
            info_text = "remove"
        if item is None:
            print("Sorry, we could find an item with that Id")
        while True:
            user_input = input(f"How many {item.Name} would you like to "
                               f"{info_text}?\n")
            is_user_input_valid = (UserInputValidator
                                   .validate_user_input_is_a_number(user_input)
                                   )
            if not is_user_input_valid:
                print("You didn't enter a valid input. Please try again.")
            else:
                break
        return user_input

    @staticmethod
    def validate_user_name():
        """
        Validate user input as a valid name.
        Returns:
            str: The validated user input representing the user's name.
        This function prompts the user to input their name and validates the
        input as a valid name using the "__validate_user_input_is_name"
        private method. If the input is not a valid name, the user is
        prompted to try again.
        """
        while True:
            user_input = input("What is your name?\n")
            if not UserInputValidator.__validate_user_input_is_name(
                    user_input):  # noqa
                print(f"Hmm {user_input.title()} didn't quite hit the bark. "
                      f"Try again.")
            else:
                break
        return user_input

    @staticmethod
    def validate_user_input_is_correct_quantity(item_name: str,
                                                is_updating: bool = False,
                                                is_admin: bool = False):
        """
        Validate user input for the quantity of a CafeteriaItem during addition
        or update.
        Args:
            item_name (str): The name of the CafeteriaItem for which the
             quantity is being validated.
            is_updating (bool): A flag indicating whether the operation is for
             updating.
            is_admin (bool): A flag indicating whether the user is an
             administrator.
        Returns:
            Union[int, str]: The validated user input representing the quantity
             or "Skip" if skipped.
        This function prompts the user to input the quantity of a CafeteriaItem
        during addition or update. If updating and the user enters "Skip,"
        the function returns "Skip". If the input is not "Skip," the function
        validates the input as a positive integer. If the input is valid,
        it returns the quantity as an integer; otherwise, the user is prompted
        to try again. For administrators, the option to skip is available.
        """
        result = ""
        info_text = (f"Please enter the amount of {item_name} you would like "
                     f"to add to the menu:\n")
        if is_admin:
            info_text = (f"Please enter the amount of {item_name} you would "
                         f"like to add to the menu, or enter "
                         f"{Style.BRIGHT}'Skip'{Style.RESET_ALL}:\n")
        while True:
            item_quantity = input(info_text)
            if is_updating and item_quantity.capitalize() == "Skip":
                result = "Skip"
                break
            validate_item_quantity = (UserInputValidator.
                                      validate_user_input_is_a_number
                                      (item_quantity))
            if not validate_item_quantity:
                print("Please enter a valid input")
            else:
                result = int(item_quantity)
                break
        return result

    @staticmethod
    def validate_user_input_is_correct_price(item_name: str,
                                             is_updating: bool = False,
                                             is_admin: bool = False):
        """
        Validate user input for the price of a CafeteriaItem during addition or
        update.
        Args:
            item_name (str): The name of the CafeteriaItem for which the price
             is being validated.
            is_updating (bool): A flag indicating whether the operation is for
             updating.
            is_admin (bool): A flag indicating whether the user is an
             administrator.
        Returns:
            Union[float, str]: The validated user input representing the price
             or "Skip" if skipped.
        This function prompts the user to input the price for a CafeteriaItem
        during addition or update. If updating and the user enters "Skip,"
        the function returns "Skip". If the input is not "Skip," the function
        validates the input as a positive decimal number. If the input is
        valid, it returns the price as a float; otherwise, the user is prompted
        to try again. For administrators, the option to skip is available.
        """
        result = ""
        info_text = f"Please enter the price for one {item_name}:\n"
        if is_admin:
            info_text = (
                f"Please enter the price for one {item_name} or enter "
                f"{Style.BRIGHT}'Skip'{Style.RESET_ALL}:\n")
        while True:
            item_price = input(info_text)
            if is_updating and item_price.capitalize() == "Skip":
                result = "Skip"
                break
            validate_item_price = (UserInputValidator.
                                   validate_user_input_is_a_decimal(item_price)
                                   )
            if not validate_item_price:
                print("Please enter a valid input")
            else:
                result = float(item_price)
                break
        return result

    @staticmethod
    def validate_user_input_is_correct_item_name(menu: list[CafeteriaItem],
                                                 info_text: str,
                                                 is_updating: bool = False):
        """
        Validate user input for the name of a CafeteriaItem during addition or
        update.
        Args:
            menu (list[CafeteriaItem]): The list of CafeteriaItems in the menu.
            info_text (str): The informational text prompting the user for
             input.
            is_updating (bool): A flag indicating whether the operation is for
             updating.
        Returns:
            str: The validated user input representing the item name.
        This function prompts the user to input the name for a CafeteriaItem
        during addition or update. It validates the input as a non-empty
        string, a valid name, and checks if the name already exists
        in the menu. If updating and the user enters "Skip," the function
        breaks out of the loop. If the input is not valid, the user is prompted
        to try again; otherwise, the function returns the validated item name.
        """
        while True:
            item_name = input(info_text)
            if len(item_name) == 0:
                print("Please enter a valid input")
            elif not UserInputValidator.__validate_user_input_is_name(
                    item_name):
                print("Please enter a valid input")
            elif next((x for x in menu if x.Name.capitalize() == item_name
                      .capitalize()), None) is not None:
                print(f"An item with the name {item_name.title()} "
                      f"already exists in the menu")
            elif is_updating and item_name.capitalize() == "Skip":
                break
            else:
                break
        return item_name

    @staticmethod
    def __validate_user_input_is_name(user_input: str):
        """
        Validate user input as a valid name.
        Args:
            user_input (str): The user input to be validated.
        Returns:
            bool: True if the input is a valid name, False otherwise.
        This private method checks if the given user input is a valid name.
        It returns True if the input is a non-empty string containing only
        alphabetic characters, optionally separated by spaces, apostrophes
        or hyphens.
        """
        if user_input.isspace():
            return False
        pattern = (re.compile(r"^[A-Za-z]+(?:['-][A-Za-z]+)?(?: [A-Za-z]+(?:['-][A-Za-z]+)?)?$"))  # noqa
        return bool(re.match(pattern, user_input))
