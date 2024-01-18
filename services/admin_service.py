from infrastructure.helpers.color_helper import ColorHelper
from infrastructure.helpers.json_file_helper import JsonFileHelper
from infrastructure.validators.user_input_validator import UserInputValidator
from services.cafeteria_item_service import CafeteriaItemService


class AdminService:
    """
    Service class for administrative tasks related to cafeteria management
    including adding, removing and updating the items in the menu
    Attributes:
        cafeteria_item_service (CafeteriaItemService): An instance of
         CafeteriaItemService for managing cafeteria items.
        menu (list[CafeteriaItem]): The current cafeteria menu.
    """
    def __init__(self):
        self.cafeteria_item_service = CafeteriaItemService()
        self.menu = self.cafeteria_item_service.get_cafeteria_menu()

    def validate_if_admin_name_provided(self, user_input: str):
        """
        Validate if the provided user input matches the admin username.
        Args:
            user_input (str): The user input to be validated.
        Returns:
            tuple[bool, Union[None, menu (list[CafeteriaItem])]]: A tuple
            indicating whether the validation is successful (True or False)
            and, if successful, an updated version of the menu.
            The second value of the tuple is a  union which can return
            either None or menu (list[CafeteriaItem]).
        This method reads the admin information from the configuration file
        and compares the provided user input with the admin username.
        If they match, the method returns a tuple with True and a menu
        instance. If they do not match or the configuration file is not found,
        the method returns a tuple with False and None.
        """
        try:
            admin_info = JsonFileHelper.read_from_config_file()
            if admin_info["admin_user"] != user_input:
                return False, None
            else:
                result = self.__show_admin_flow(admin_info["admin_password"])
                return result
        except FileNotFoundError:
            print("Configuration file not found")
            return False, None

    def __show_admin_flow(self,  expected_admin_password: str):
        """
        Show the admin flow to authorize access to the secret admin mode.
        Args:
            expected_admin_password (str): The expected password for admin
             authorization.
        Returns:
            tuple[bool, Union[None, menu (list[CafeteriaItem])]]: A tuple
            indicating whether the admin authorization is successful
            (True or False) and, if successful, a menu instance.
        This private method prompts the user to enter the secret password
        for admin authorization. It allows up to three attempts to enter the
        correct password. If the correct password is entered, it prints a
        success message and returns a tuple with True and a menu instance.
        If the password is incorrect after three attempts, it returns a tuple
        with False and None.
        """
        retry_counter = 3
        result = False, None
        for attempted_try in range(retry_counter):
            user_input = input("Please enter the secret password:\n")
            if user_input == expected_admin_password:
                print("You have successfully authorized the secret woof mode.")
                result = self.__show_available_options()
                break
            else:
                attempted_try += 1
                attemps_left = retry_counter - attempted_try
                attempts_left_info = ""
                if attemps_left > 0:
                    attempts_left_info = (f"You have {attemps_left}"
                                          f" attempts left")
                print(f"Password incorrect. Woofin mode access denied. "
                      f"{attempts_left_info}")
                continue
        return result

    def __show_available_options(self):
        """
        Show the available options for editing the cafeteria menu in admin
        mode.
        Returns:
            tuple[bool, Union[None, menu (list[CafeteriaItem])]]: A tuple
            indicating whether the admin flow should be continued
            (True or False) and, if applicable, a menu instance.
        This private method displays the available options for editing the
        cafeteria menu in admin mode. It prompts the user to choose between
        adding, updating, removing items from the menu, or exiting the
        admin mode. Depending on the user's choice, it calls the respective
        private methods (__handle_add, __handle_update, __handle_remove) and
        continues or completes the admin flow accordingly. It returns a tuple
        with a boolean value indicating whether the admin flow should be
        continued (True) or not (False), and if applicable, a menu instance.
        """
        result = False, None
        is_flow_continued = False
        while True:
            self.cafeteria_item_service.print_cafeteria_menu(self.menu)
            user_input = input(f"How would you like to edit the menu?"
                               f"{ColorHelper.color_add_update_remove_exit_text()}\n")  # noqa
            if user_input.capitalize() == "Add":
                result = False, self.__handle_add()
                is_flow_continued = self.__continue_or_complete_flow()
            elif user_input.capitalize() == "Update":
                result = False, self.__handle_update()
                is_flow_continued = self.__continue_or_complete_flow()
            elif user_input.capitalize() == "Remove":
                result = False, self.__handle_remove()
                is_flow_continued = self.__continue_or_complete_flow()
            elif user_input.capitalize() == "Exit":
                result = False, self.menu
                is_flow_continued = False
            else:
                print(f"The input entered is not valid. Please try using"
                      f"{ColorHelper.color_add_update_remove_exit_text()}")
                is_flow_continued = True
            if is_flow_continued:
                continue
            else:
                break
        return result

    def __handle_update(self):
        """
        Handle the updating of cafeteria items in the menu.
        Returns:
            list[CafeteriaItem]: The updated menu after applying the specified
            updates.
        This private method handles the process of updating cafeteria items in
        the menu. It prompts the user to input the item IDs they wish to update
        and calls the update_items method from the CafeteriaItemService to
        perform the updates. The updated menu is then stored, and the method
        returns the updated menu list.
        """
        user_input = (UserInputValidator.validate_input_before_parsing
                      (self.menu, False, True))
        item_ids = UserInputValidator.create_array_from_user_input(user_input)
        self.menu = (self.cafeteria_item_service.update_items
                     (item_ids, self.menu, True))
        return self.menu

    def __handle_remove(self):
        """
        Handle the removal of cafeteria items from the menu.
        Returns:
            list[CafeteriaItem]: The updated menu after removing specified
            items.
        This private method handles the process of removing cafeteria items
        from the menu. It prompts the user to input the item IDs they wish to
        remove and calls the recalculate_ids method from the
        CafeteriaItemService to perform the removal. The updated menu, with the
        specified items removed, is then stored, and the method returns the
        updated menu list.
        """
        user_input = (UserInputValidator.validate_input_before_parsing
                      (self.menu, True))
        item_ids = UserInputValidator.create_array_from_user_input(user_input)
        updated_menu = [item for item in self.menu if item.Id not in item_ids]
        item_removed = [item for item in self.menu if item.Id in item_ids]
        removed_item_names = [x.Name for x in item_removed]
        print(f"The following item(s) have been removed: "
              f"{', '.join(removed_item_names)}")
        self.menu = self.cafeteria_item_service.recalculate_ids(updated_menu)
        return self.menu

    def __handle_add(self):
        """
        Handle the addition of new cafeteria items to the menu.
        Returns:
            list[CafeteriaItem]: The updated menu after adding new items.
        This private method handles the process of adding new cafeteria items
        to the menu. It prompts the user to input the number of items they
        want to add, validates the input, and then calls the add_items_to_menu
        method from the CafeteriaItemService to perform the addition.
        The updated menu, with the newly added items, is then stored,
        and the method returns the updated menu list.
        """
        while True:
            user_input = input("How many items would you like to add?\n")
            validate_user_input = (UserInputValidator
                                   .validate_user_input_is_a_number(user_input)
                                   )
            if not validate_user_input:
                print("Please enter a valid input")
            elif validate_user_input and int(user_input) == 0:
                print(f"You cannot add {user_input} items")
            else:
                self.menu = (self.cafeteria_item_service.add_items_to_menu
                             (int(user_input), self.menu))
                break
        return self.menu

    @staticmethod
    def __continue_or_complete_flow():
        """
        Determine whether to continue editing the menu or exit secret Woofin
        mode.
        Returns:
           bool: True if the user wants to continue editing the menu, False if
           they want to exit.
        This private method prompts the user to decide whether to continue
        editing the cafeteria menu or to exit the secret Woofin mode.
        The user input is validated, and the method returns a boolean value
        indicating whether the editing flow should continue (True) or if the
        secret Woofin mode should be exited (False).
        """
        result = False
        while True:
            user_input = input(f"Do you want to continue editing the menu? "
                               f"{ColorHelper.color_yes_no_text()}\n")
            if user_input.capitalize() == "Y":
                result = True
                break
            elif user_input.capitalize() == "N":
                print("Exiting secret Woofin mode")
                break
        return result
