from infrastructure.helpers.json_file_helper import JsonFileHelper
from infrastructure.validators.user_input_validator import UserInputValidator
from services.cafeteria_item_service import CafeteriaItemService


class AdminService:
    def __init__(self):
        self.cafeteria_item_service = CafeteriaItemService()

    def validate_if_admin_name_provided(self, user_input: str):
        try:
            admin_info = JsonFileHelper.read_from_config_file()
            if admin_info["admin_user"] != user_input:
                return False, None
            else:
                user_input = input("Please enter the secret password: ")
                return self.__show_admin_flow(user_input, admin_info["admin_password"])
        except FileNotFoundError:
            print("Configuration file not found")
            return False, None

    def __show_admin_flow(self, user_input: str, expected_admin_password: str):
        if user_input == expected_admin_password:
            print("You have successfully authorized the secret woof mode.")
            self.cafeteria_item_service.print_cafeteria_menu(self.cafeteria_item_service.get_cafeteria_menu())
            return self.__show_available_options()
        else:
            return False

    def __show_available_options(self):
        while True:
            user_input = input("Would you like to edit the menu? (Add/Update/Remove)")
            if user_input.capitalize() == "Add":
                return self.__handle_add()
            elif user_input.capitalize() == "Update":
                print("updating")
                break
            elif user_input.capitalize() == "Remove":
                print("removing")
                break
            else:
                print("The input entered is not valid. Please try using (Add/Update/Remove)")

    def __handle_add(self):
        while True:
            user_input = input("How many items would you like to add? ")
            validate_user_input = UserInputValidator.validate_user_input_is_a_number(user_input)
            if not validate_user_input:
                print("Please enter a valid input")
            elif validate_user_input and int(user_input) == 0:
                print(f"You cannot add {user_input} items")
            else:
                updated_menu = self.cafeteria_item_service.add_items_to_menu(int(user_input))
                return self.__continue_or_complete_flow(), updated_menu

    def __continue_or_complete_flow(self):
        while True:
            user_input = input("Do you want to continue editing the menu? (Y/N)")
            if user_input.capitalize() == "Y":
                self.__show_available_options()
                return True
            elif user_input.capitalize() == "N":
                print("Exiting secret Woofin mode")
                return False
            else:
                print("The input entered is not valid. Please try using (Y/N)")
