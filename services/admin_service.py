from infrastructure.helpers.json_file_helper import JsonFileHelper
from services.cafeteria_item_service import CafeteriaItemService


class AdminService:
    def __init__(self):
        self.cafeteria_item_service = CafeteriaItemService()

    def validate_if_admin_name_provided(self, user_input: str):
        try:
            admin_info = JsonFileHelper.read_from_config_file()
            if admin_info["admin_user"] != user_input:
                return False
            else:
                user_input = input("Please enter the secret password: ")
                return self.__show_admin_flow(user_input, admin_info["admin_password"])
        except FileNotFoundError:
            print("Configuration file not found")
            return False

    def __show_admin_flow(self, user_input: str, expected_admin_password: str):
        if user_input == expected_admin_password:
            print("You have successfully authorized the secret woof mode.")
            self.cafeteria_item_service.print_cafeteria_menu()
            self.__show_available_options()
            return True
        else:
            return False

    @staticmethod
    def __show_available_options():
        while True:
            user_input = input("Would you like to edit the menu? (Add/Update/Remove)")
            if user_input.capitalize() == "Add":
                print("adding")
                break
            elif user_input.capitalize() == "Update":
                print("updating")
                break
            elif user_input.capitalize() == "Remove":
                print("removing")
                break
            else:
                print("The input entered is not valid. Please try using (Add/Update/Remove)")
    