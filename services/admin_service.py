from infrastructure.helpers.json_file_helper import JsonFileHelper
from infrastructure.validators.user_input_validator import UserInputValidator
from services.cafeteria_item_service import CafeteriaItemService
import copy


class AdminService:
    def __init__(self):
        self.cafeteria_item_service = CafeteriaItemService()
        self.menu = self.cafeteria_item_service.get_cafeteria_menu()

    def validate_if_admin_name_provided(self, user_input: str):
        try:
            admin_info = JsonFileHelper.read_from_config_file()
            if admin_info["admin_user"] != user_input:
                return False, None
            else:
                user_input = input("Please enter the secret password: ")
                result = self.__show_admin_flow(user_input, admin_info["admin_password"])
                return result
        except FileNotFoundError:
            print("Configuration file not found")
            return False, None

    def __show_admin_flow(self, user_input: str, expected_admin_password: str):
        if user_input == expected_admin_password:
            print("You have successfully authorized the secret woof mode.")
            result = self.__show_available_options()
            return result
        else:
            return False

    def __show_available_options(self):
        result = False, None
        is_flow_continued = False
        while True:
            self.cafeteria_item_service.print_cafeteria_menu(self.cafeteria_item_service.get_cafeteria_menu())
            user_input = input("How would you like to edit the menu? (Add/Update/Remove)")
            if user_input.capitalize() == "Add":
                result = False, self.__handle_add()
                is_flow_continued = self.__continue_or_complete_flow()
            elif user_input.capitalize() == "Update":
                result = False, self.__handle_update()
                is_flow_continued = self.__continue_or_complete_flow()
            elif user_input.capitalize() == "Remove":
                result = False, self.__handle_remove()
                is_flow_continued = self.__continue_or_complete_flow()
            else:
                print("The input entered is not valid. Please try using (Add/Update/Remove)")
                is_flow_continued = True
            if is_flow_continued:
                continue
            else:
                break
        return result

    def __handle_update(self):
        user_input = UserInputValidator.validate_input_before_parsing(self.menu, False, True)
        item_ids = UserInputValidator.create_array_from_user_input(user_input)
        updated_menu = self.cafeteria_item_service.update_items(item_ids)
        self.menu = updated_menu
        return self.menu

    def __handle_remove(self):
        self.cafeteria_item_service.print_cafeteria_menu(self.menu)
        user_input = UserInputValidator.validate_input_before_parsing(self.menu, True)
        item_ids = UserInputValidator.create_array_from_user_input(user_input)
        updated_menu = [item for item in self.menu if item.Id not in item_ids]
        self.menu = updated_menu
        return self.menu

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
                self.menu = updated_menu
                break
        return self.menu

    @staticmethod
    def __continue_or_complete_flow():
        result = False
        while True:
            user_input = input("Do you want to continue editing the menu? (Y/N)")
            if user_input.capitalize() == "Y":
                result = True
                break
            elif user_input.capitalize() == "N":
                print("Exiting secret Woofin mode")
                break
        return result
