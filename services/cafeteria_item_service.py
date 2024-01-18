from colorama import Style
from tabulate import tabulate

from entities.cafeteria_item import CafeteriaItem
from infrastructure.helpers.price_converter import PriceConverter
from infrastructure.validators.user_input_validator import UserInputValidator


class CafeteriaItemService:
    """
    Service class for managing cafeteria items and related functionalities.

    Attributes:
        cafeteria_items (list[CafeteriaItem]): A list containing cafeteria
         items.
        price_converter (PriceConverter): An instance of PriceConverter for
         handling price-related operations.
    """
    def __init__(self):
        self.cafeteria_items = self.__populate_cafeteria_menu()
        self.price_converter = PriceConverter()

    def print_cafeteria_menu(self, menu: list[CafeteriaItem]):
        """
        Print the Cafeteria menu in a formatted table.
        Args:
            menu (list[CafeteriaItem]): The list of CafeteriaItems to be
             displayed.
        This method generates a formatted table to display the Cafeteria menu.
        Each row of the table includes the item ID, name, price
        (formatted with two decimal places), and stock quantity of the
        CafeteriaItem. The table is printed to the console using the 'pretty'
        table format from tabulate.
        """
        headers = ["ID", "Name", "Price", "Stock"]
        table_items = []
        for item in menu:
            table_item = [item.Id, item.Name, f"£ {item.Price:.2f}",
                          item.Stock]
            table_items.append(table_item)
        table1 = tabulate(table_items, headers=headers, tablefmt="pretty")
        print(table1)

    def get_cafeteria_menu(self):
        """
        Retrieve the current state of the Cafeteria menu.
        Returns:
            list[CafeteriaItem]: The list of CafeteriaItems representing the
            current menu.
        This method returns the current state of the Cafeteria menu, which is a
        list of CafeteriaItem objects representing the items available in the
        menu.
        """
        return self.cafeteria_items

    def add_items_to_menu(self, amount_of_items: int,
                          menu: list[CafeteriaItem]):
        """
        Add new cafeteria items to the menu.
        Args:
            amount_of_items (int): The number of new cafeteria items to add.
            menu (list[CafeteriaItem]): The existing list of CafeteriaItems
             representing the menu.
        Returns:
            list[CafeteriaItem]: The updated menu after adding the new items.
        This method allows the addition of a specified number of new cafeteria
        items to the menu. It prompts the user to enter names, quantities,
        and prices for each new item. The item details are then used to create
        new `CafeteriaItem` objects, which are added to the menu. The method
        prints a confirmation message for each added item, including its
        quantity, name, and price. Finally, it recalculates the IDs of the menu
        items to ensure they are consecutive.
        """
        last_item = self.cafeteria_items[-1]
        input_text = "Please enter a name for the new cafeteria item:\n"
        for i in range(amount_of_items):
            item_id = last_item.Id + 1
            item_name = (UserInputValidator
                         .validate_user_input_is_correct_item_name
                         (self.cafeteria_items, input_text).title())
            validated_item_quantity = (UserInputValidator
                                       .validate_user_input_is_correct_quantity
                                       (item_name, False))
            validated_item_price = (UserInputValidator
                                    .validate_user_input_is_correct_price
                                    (item_name))
            item = CafeteriaItem(item_id, item_name, validated_item_price,
                                 validated_item_quantity)
            menu.append(item)
            print(f"{validated_item_quantity}x {item_name} has been added to "
                  f"the menu at a price of £{validated_item_price:.2f}")
        self.recalculate_ids(menu)
        return menu

    def update_items(self, item_ids: list[int], menu: list[CafeteriaItem],
                     is_admin: bool = False):
        """
        Update cafeteria items in the menu.
        Args:
            item_ids (list[int]): The list of item IDs to update.
            menu (list[CafeteriaItem]): The list of CafeteriaItems representing
             the menu.
            is_admin (bool, optional): A flag indicating whether the update is
             performed by an admin.
        Returns:
            list[CafeteriaItem]: The updated menu after applying the specified
            updates. This method updates the specified cafeteria items in the
            menu based on their IDs. For each item in the menu, it checks if
            its ID is in the provided item_ids list. If a match is found,
            the item's name, quantity, and price are updated using private
            helper methods. The updated menu is then returned.
        """
        for item in menu:
            for item_id in item_ids:
                if item.Id == item_id:
                    item = self.__update_item_name(item, menu)
                    item = self.__update_item_quantity(is_admin, item)
                    item = self.__update_item_price(is_admin, item)
        return menu

    def __update_item_price(self, is_admin, item):
        """
        Update the price of a cafeteria item.
        Args:
            is_admin (bool): A flag indicating whether the update is performed
             by an admin.
            item (CafeteriaItem): The cafeteria item to update.
        Returns:
            CafeteriaItem: The updated cafeteria item.
        This private method prompts the user for a new price for the specified
        cafeteria item. It validates the input using the UserInputValidator and
        ensures that the new price is different from the current price.
        If a valid and different price is provided, it updates the item's price
        and prints a message indicating the change. If "Skip" is entered,
        the method ends. The updated cafeteria item is returned.
        """
        while True:
            validated_item_price = (UserInputValidator
                                    .validate_user_input_is_correct_price
                                    (item.Name, True, is_admin))
            if validated_item_price != "Skip":
                if item.Price != validated_item_price:

                    print(
                        f"The price of {item.Name} has been changed from "
                        f"£{PriceConverter.format_price(item.Price)} to "
                        f"£{PriceConverter.format_price(validated_item_price)}"
                    )
                    item = self.__handle_update_value(validated_item_price,
                                                      item)
                else:
                    print(
                        f"The price of {item.Name} is already "
                        f"{PriceConverter.format_price(item.Price)}. "
                        f"Please, try again.")
                    continue
            else:
                break
            return item

    def __update_item_quantity(self, is_admin, item):
        """
        Update the stock quantity of a cafeteria item.
        Args:
            is_admin (bool): A flag indicating whether the update is performed
             by an admin.
            item (CafeteriaItem): The cafeteria item to update.
        Returns:
            CafeteriaItem: The updated cafeteria item.
        This private method prompts the user for a new stock quantity for the
        specified cafeteria item. It validates the input using the
        UserInputValidator and ensures that the new quantity is different from
        the current quantity. If a valid and different quantity is provided,
        it updates the item's quantity and prints a message indicating
        the change. If "Skip" is entered, the method ends. The updated
        cafeteria item is returned.
        """
        while True:
            validated_item_quantity = (UserInputValidator
                                       .validate_user_input_is_correct_quantity
                                       (item.Name, True, is_admin))
            if validated_item_quantity != "Skip":
                if item.Stock != validated_item_quantity:
                    print(
                        f"The stock value of {item.Name} "
                        f"has been changed from {item.Stock} "
                        f"to {validated_item_quantity}")
                    item = self.__handle_update_value(validated_item_quantity,
                                                      item)
                    break
                else:
                    print(
                        f"The stock value of {item.Name} is already "
                        f"{item.Stock}. Please, try again.")
                    continue
            else:
                break
        return item

    def __update_item_name(self, item, menu):
        """
        Update the name of a cafeteria item.
        Args:
            item (CafeteriaItem): The cafeteria item to update.
            menu (list[CafeteriaItem]): The list of CafeteriaItems representing
             the menu.
        Returns:
            CafeteriaItem: The updated cafeteria item.
        This method prompts the user for a new name for the specified cafeteria
        item. It uses the UserInputValidator to ensure the entered name
        is valid. If a valid name is provided (not equal to "Skip"),
        it prints a message indicating the change. If the new name is different
        from the current name, it updates the item's name. The updated
        cafeteria item is then returned.
        """
        input_text = (f"Please enter a new name for {item.Name} "
                      f"or type "
                      f"'{Style.BRIGHT}Skip{Style.RESET_ALL}' "
                      f"not to change it.\n")
        item_name = (UserInputValidator
                     .validate_user_input_is_correct_item_name
                     (menu, input_text, True).title())
        if item_name != "Skip":
            print(f"{item.Name} has been changed to {item_name}")
        if item.Name != item_name:
            item = self.__handle_update_value(item_name, item)
        return item

    def __handle_update_value(self, user_input, item: CafeteriaItem):
        """
        Handle updating the value of a cafeteria item.
        Args:
            user_input (str, int, float): The new value to set for the
             cafeteria item.
            item (CafeteriaItem): The cafeteria item to update.
        Returns:
            CafeteriaItem: The updated cafeteria item.
        This private method handles updating the value of a cafeteria item
        based on the provided user_input. It checks the type of user_input and
        updates the corresponding attribute of the cafeteria item
        (Name, Stock, or Price). If user_input is "Skip," no updates are
        performed. The updated cafeteria item is then returned.
        """
        if user_input != "Skip":
            if type(user_input) is str:
                item.Name = user_input
            if type(user_input) is int:
                item.Stock = user_input
            if type(user_input) is float:
                item.Price = user_input
        return item

    def subtract_from_stock(self, ordered_item: CafeteriaItem,
                            menu_list: list[CafeteriaItem],
                            ordered_amount: int):
        """
        Subtract the specified quantity from the stock of a cafeteria item.
        Args:
            ordered_item (CafeteriaItem): The cafeteria item to update.
            menu_list (list[CafeteriaItem]): The list of cafeteria items
             representing the menu.
            ordered_amount (int): The quantity to subtract from the item's
             stock.
        This method updates the stock of a cafeteria item based on the ordered
        quantity.
        """
        for cafeteria_item in menu_list:
            if ordered_item.Id == cafeteria_item.Id:
                cafeteria_item.Stock -= ordered_amount
        self.cafeteria_items = menu_list

    def add_to_stock(self, ordered_item: CafeteriaItem,
                     menu_list: list[CafeteriaItem], ordered_amount: int):
        """
        Add stock to the specified cafeteria item in the menu.

        Args:
            ordered_item (CafeteriaItem): The cafeteria item for which stock is
             to be added.
            menu_list (list[CafeteriaItem]): The list representing the
             cafeteria menu.
            ordered_amount (int): The quantity of stock to be added to the
             ordered item.

        This method iterates through the menu list to find the cafeteria item
        with the specified ID (ordered_item.Id) and then increases its stock by
        the ordered_amount. The updated menu list is then assigned to
        self.cafeteria_items.
        """
        for cafeteria_item in menu_list:
            if ordered_item.Id == cafeteria_item.Id:
                cafeteria_item.Stock += ordered_amount
        self.cafeteria_items = menu_list

    def recalculate_ids(self, menu_list: list[CafeteriaItem]):
        """
        Recalculate the IDs for cafeteria items in the provided menu list.
        Args:
            menu_list (list[CafeteriaItem]): The list of cafeteria items
             representing the menu.
        This method iterates through the provided menu_list and recalculates
        the IDs for each cafeteria item, starting from 1.
        The modified menu_list with updated IDs is then returned.
        """
        for index, item in enumerate(menu_list, start=1):
            item.Id = index
        return menu_list

    def __populate_cafeteria_menu(self):
        """
        Populate the initial cafeteria menu with predefined items.
        Returns:
            list[CafeteriaItem]: The list of predefined cafeteria items.
        This private method initializes and returns a list of CafeteriaItem
        objects representing the initial cafeteria menu.
        Each item has a unique ID, a name, a price, and an initial stock
        quantity.
        """
        menu = [
            CafeteriaItem(1, "Waggy Woofin", 2.50, 10),
            CafeteriaItem(2, "Paw Cake", 3.20, 10),
            CafeteriaItem(3, "Cheeky Cheese Paw", 1.80, 10),
            CafeteriaItem(4, "Barky Bacon Stick", 2.00, 10),
            CafeteriaItem(5, "Sonny's Soup", 1.40, 10),
            CafeteriaItem(6, "Alfie's Apple Tart", 2.50, 10),
            CafeteriaItem(7, "Barkie", 0.80, 10),
            CafeteriaItem(8, "Storm's Special Chicken Stew", 4.20, 10)]
        return menu
