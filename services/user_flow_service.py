import copy
from dataclasses import dataclass
from tabulate import tabulate

from infrastructure.helpers.color_helper import ColorHelper

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
    """
    Service class managing user interactions for the cafeteria application.

    This class orchestrates the user interactions within the cafeteria
    application, including menu navigation, order handling, and secret Woofin
    mode for administrators.

    Attributes:
        cafeteria_item_service (CafeteriaItemService): The service for
         cafeteria item operations.
        admin_service (AdminService): The service for administrator-related
         operations.
        cart_service (CartService): The service for shopping cart operations.
        price_converter (PriceConverter): The service for price formatting
         operations.
        menu (list[CafeteriaItem]): The current cafeteria menu.
        unique_set (set): A set to keep track of unique item IDs in the
         shopping cart.
        cart_result (list[CafeteriaItem]): A list to store items in the
         shopping cart.
    """
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
        Begin the cafeteria flow, welcoming the user, displaying the menu
        and handling user orders.

        Prints a welcome message and prompts the user for their name.
        If an admin name is provided, sets the menu to the provided admin menu.
        Otherwise, displays Chef Storm's menu and handles user orders by
        showing the menu, handling the order, and creating a cart. Continues to
        prompt the user to review and complete their order until the user
        indicates they are finished or wish to continue. Once the order is
        completed, proceeds to the next steps of the cafeteria flow.
        """
        print(
            f"{Icon.DogIcon.value}  Welcome to Storm's Woofeteria.  "
            f"{Icon.DogIcon.value}")
        user_input = UserInputValidator.validate_user_name()
        admin_name_provided = (self.admin_service.
                               validate_if_admin_name_provided(user_input))
        if not admin_name_provided[0]:
            if admin_name_provided[1] is not None:
                self.menu = admin_name_provided[1]
            print(f"Hello {user_input.title()}. "
                  f"Here is what Chef Storm has to offer.")
            self.__show_menu()
            cart_items = self.__handle_order(self.menu)
            cart = self.cart_service.add_to_cart(cart_items)
            while True:
                self.print_user_cart(cart)
                user_input = input(f"Are you finished with your order?"
                                   f" {ColorHelper.color_yes_no_text()}\n")
                if user_input.capitalize() == "Y":
                    self.__complete_user_flow(cart)
                    break
                elif user_input.capitalize() == "N":
                    self.__continue_flow(user_input, cart)
                    break
                else:
                    print(
                        f"The input entered is not valid. Please try using "
                        f"{ColorHelper.color_yes_no_text()} ")

    def __show_menu(self):
        """
        Display the current cafeteria menu.

        Calls the "print_cafeteria_menu" method of the "CafeteriaItemService"
        to print a formatted table of the current items in the menu.
        """
        self.cafeteria_item_service.print_cafeteria_menu(self.menu)

    def __continue_flow(self, user_input: str, cart: Cart):
        """
        Continue or complete the cafeteria flow based on user input.
        Args:
            user_input (str): The user's input indicating whether
             they want to continue ('Y') or not ('N').
            cart (Cart): The Cart object representing the user's current
             selections.
        The method continues prompting the user based on their input, either
        continuing the flow or showing options and updating the cart.
        If the flow is to be continued, the loop continues; otherwise,
        it breaks and proceeds to completing the user flow.
        """
        is_flow_continued = True
        while True:
            if user_input.capitalize() == "Y":
                is_flow_continued = False
                self.__complete_user_flow(cart)
            elif user_input.capitalize() == "N":
                is_flow_continued = self.__show_options(cart)
            if is_flow_continued:
                continue
            else:
                self.__complete_user_flow(cart)
                break

    def __show_options(self, cart: Cart):
        """
        Display options for adding or removing items from the user's cart.
        Args:
            cart (Cart): The Cart object representing the user's current
             selections.
        Returns:
            bool: True if the user chooses to continue the flow,
             otherwise - False.
        The method prompts the user to add or remove items from their cart and
        handles the corresponding actions. It returns True if the user chooses
        to continue the flow, otherwise - False.
        If the input is invalid, it prints a message stating that the input is
        invalid and prompts the user to try again.
        """
        result = False
        while True:
            self.print_user_cart(cart)
            user_input = input(
                f"Would you like to add or remove item(s) from your cart? "
                f"{ColorHelper.color_add_remove_text()}\n")
            if user_input.capitalize() == "Add":
                updated_cart = self.__add_to_cart(cart)
                result = self.__handle_continue_flow(updated_cart)
                break
            elif user_input.capitalize() == "Remove":
                updated_cart = self.__remove_from_cart(cart)
                result = self.__handle_continue_flow(updated_cart)
                break
            else:
                print(
                    f"The input entered is not valid. Please try using "
                    f"{ColorHelper.color_add_remove_text()}")
        return result

    def __handle_continue_flow(self, cart: Cart):
        """
        Handle user input to continue or complete the cafeteria flow.
        Args:
            cart (Cart): The Cart object representing the user's current
             selections.
        Returns:
            bool: True if the user chooses to continue the flow,
             otherwise - False.
        The method prompts the user to indicate whether they are finished with
        their order or want to continue. It returns True if the user chooses to
        continue the flow, otherwise - False. If the input is invalid, it
        prints a message stating that the input is invalid and prompts the user
        to try again.
        """
        result = True
        while True:
            self.print_user_cart(cart)
            user_input = input(
                f"Are you finished with your order? "
                f"{ColorHelper.color_yes_no_text()}\n")
            if user_input.capitalize() == "Y":
                result = False
                break
            elif user_input.capitalize() == "N":
                print("Your current order: ")
                self.cart_service.print_cart(cart)
                break
            else:
                print(
                    f"The input entered is not valid. Please try using"
                    f"{ColorHelper.color_yes_no_text()} ")
        return result

    def __complete_user_flow(self, cart: Cart):
        """
        Complete the user's cafeteria flow by finalizing the purchase.
        Args:
            cart (Cart): The Cart object representing the user's final
             selections.
        The method prompts the user to enter the cart total displayed on
        the screen to complete the purchase. It validates the user input and
        finalizes the purchase if the input is valid and matches the expected
        total price. If the input is valid, it prints a thank-you message and
        concludes the cafeteria flow. Otherwise, it prints a message stating
        that the input is invalid and prompts the user to try again.
        """
        while True:
            formatted_price = (self.price_converter.
                               format_price(cart.TotalPrice))
            self.print_user_cart(cart)
            if len(cart.Items) == 0:
                print(
                    f"{Icon.PawIcon.value}Thanks for visiting Woofeteria, "
                    f"have a pawesome day!{Icon.PawIcon.value}")
                break
            user_input = input(
                "Please enter the cart total on screen (minus the pound sign) "
                "to complete your purchase.\n")
            is_user_input_valid = (UserInputValidator.
                                   validate_user_input_is_a_decimal(user_input)
                                   )
            if not is_user_input_valid:
                print("Please enter a valid input")
            elif formatted_price != user_input:
                print(
                    "What you have entered does not match the total expected "
                    "price. Please try again. ")
            else:
                print(
                    f"{Icon.PawIcon.value}  Thank you, have a pawesome day  "
                    f"{Icon.PawIcon.value}")
                break

    def print_user_cart(self, cart: Cart):
        """
        Print the contents of the user's shopping cart.
        Args:
            cart (Cart): The Cart object representing the user's current
             selections.
        Prints:
            A formatted table displaying the ID, Name, Price, and Quantity
            of each item in the user's shopping cart. Additionally, prints the
            total price of the cart.
        """
        formatted_price = self.price_converter.format_price(cart.TotalPrice)
        headers = ["ID", "Name", "Price", "Quantity"]
        table_items = []
        for cart_item in cart.Items:
            table_item = [cart_item.Id, cart_item.Name,
                          f"£ {cart_item.Price:.2f}", cart_item.Stock]
            table_items.append(table_item)
        cart_table = tabulate(table_items, headers=headers, tablefmt="pretty")
        print(cart_table)
        cart_total = print(f"Your cart total is: £{formatted_price}")
        return cart_total

    def __add_to_cart(self, cart: Cart):
        """
        Add items to the user's shopping cart.
        Args:
            cart (Cart): The Cart object representing the user's current
             selections.
        Returns:
            Cart: The updated Cart object after adding items based on
            the user's order. The method displays the current menu, handles the
            user's order to select items, updates the items in the user's cart
            and returns the updated Cart object.
        """
        self.__show_menu()
        cart_items = self.__handle_order(self.menu)
        cart.Items = cart_items
        return self.cart_service.update_cart(cart, cart.Items)

    def __remove_from_cart(self, cart: Cart):
        """
        Remove items from the user's shopping cart.
        Args:
            cart (Cart): The Cart object representing the user's current
             selections.
        Returns:
            Cart: The updated Cart object after removing items based on the
            user's selection. The method prompts the user to select items
            to be removed from the cart, validates the input, pdates the stock
            of the selected items, handles the removal from the cart
            and returns the updated Cart object.
        """
        cart_items = UserInputValidator.validate_item_ids(cart.Items, True)
        updated_items = self.__add_stock(cart_items)
        self.handle_remove_from_cart(cart, cart_items, updated_items)
        return self.cart_service.update_cart(cart, cart.Items)

    def handle_remove_from_cart(self, cart, cart_items, updated_items):
        """
        Handle the removal of items from the user's shopping cart.

        Args:
            cart (Cart): The Cart object representing the user's current
             selections.
            cart_items (list[CafeteriaItem]): The list of CafeteriaItems to be
             removed from the cart.
            updated_items (list[CafeteriaItem]): The list of updated
             CafeteriaItems after removal.
        The method updates the user's cart based on the removal of
        selected items. If the stock of an item becomes zero, it is removed
        from the cart, otherwise, the item is updated in the cart with
        the new stock.
        """
        if len(updated_items) == 0:
            self.unique_set.clear()
            cart.Items = updated_items
        else:
            for cart_item in cart_items:
                for updated_item in updated_items:
                    if cart_item.Id == updated_item.Id:
                        if updated_item.Stock == 0:
                            self.unique_set.remove(cart_item.Id)
                            self.cart_result.remove(cart_item)
                            if [item for item in cart.Items if
                                item.Id == cart_item.Id]:  # noqa
                                cart.Items.remove(cart_item)
                        else:
                            cart.Items.remove(cart_item)
                            cart.Items.append(updated_item)
                            if [item for item in self.cart_result if
                                item.Id == cart_item.Id]:  # noqa
                                self.cart_result.remove(cart_item)
                                self.cart_result.append(updated_item)

    def __handle_order(self, items: list[CafeteriaItem]):
        """
        Handle the user's order by validating and subtracting stock from
        selected items.
        Args:
            items (list[CafeteriaItem]): The list of CafeteriaItems available
             for the user's order.
        Returns:
            list[CafeteriaItem]: The list of CafeteriaItems representing the
            user's ordered items. The method prompts the user to select items
            for their order, validates the input, and subtracts stock from
            the selected items. The resulting list represents the user's
            ordered items.
        """
        ordered_items = UserInputValidator.validate_item_ids(items)
        return self.__subtract_stock(ordered_items)

    def __subtract_stock(self, cart_items: list[CafeteriaItem]):
        """
        Subtract stock from selected items in the menu and update the user's
        cart.
        Args:
            cart_items (list[CafeteriaItem]): The list of CafeteriaItems
             representing the user's ordered items.
        Returns:
           list[CafeteriaItem]: The list of updated CafeteriaItems in the
           user's cart. The method deep copies the menu, subtracts stock from
           selected items based on user input, updates the user's cart
           and returns the updated list of CafeteriaItems in the user's cart.
        """
        menu_list_copy = copy.deepcopy(self.menu)
        for item in cart_items:
            menu_item = next((x for x in menu_list_copy if x.Id == item.Id),
                             None)
            if item.Stock == 0:
                print(f"Sorry {item.Name} is out of stock.")
                continue
            user_input = int(
                UserInputValidator.validate_input_for_items(menu_item))
            if item.Id not in self.unique_set:
                self.unique_set.add(item.Id)
                item.Stock = user_input
                self.cart_result.append(item)
            else:
                cart_item = next(
                    (x for x in self.cart_result if x.Id == item.Id), None)
                if menu_item.Stock == 0:
                    continue
                else:
                    cart_item.Stock += user_input
            self.cafeteria_item_service.subtract_from_stock(item,
                                                            menu_list_copy,
                                                            user_input)
            print(f"You have added x{user_input} {item.Name} to your cart")
        self.menu = self.cafeteria_item_service.get_cafeteria_menu()
        return self.cart_result

    def __add_stock(self, cart_items: list[CafeteriaItem]):
        """
        Add stock back to selected items in the menu and update the user's
        cart.
        Args:
            cart_items (list[CafeteriaItem]): The list of CafeteriaItems to be
             updated with added stock.
        Returns:
           list[CafeteriaItem]: The list of updated CafeteriaItems in the
           user's cart after adding stock. The method deep copies the menu,
           adds stock back to selected items based on user input, updates the
           user's cart, and returns the updated list of CafeteriaItems in the asdsa
           user's cart.
        """
        menu_list_copy = copy.deepcopy(self.menu)
        cart_items_updated = []
        for item in cart_items:
            user_input = int(
                UserInputValidator.validate_input_for_items(item, True))
            item.Stock -= user_input
            print(f"You have removed: x{user_input} {item.Name}")
            cart_items_updated.append(item)
            self.cafeteria_item_service.add_to_stock(item, menu_list_copy,
                                                     user_input)
        self.menu = self.cafeteria_item_service.get_cafeteria_menu()
        return cart_items_updated
