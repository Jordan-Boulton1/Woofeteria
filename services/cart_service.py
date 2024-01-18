from dataclasses import dataclass

from entities.cafeteria_item import CafeteriaItem
from entities.cart import Cart
from infrastructure.helpers.price_converter import PriceConverter


@dataclass
class CartService:
    """
        Service class for managing the shopping cart.
        Attributes:
        price_converter (PriceConverter): An instance of the PriceConverter
        class for handling price formatting.
    """
    def __init__(self):
        self.price_converter = PriceConverter()

    def add_to_cart(self, selected_items: list[CafeteriaItem]):
        """
        Create a new Cart object with the provided list of CafeteriaItems.
        Args:
            selected_items (list[CafeteriaItem]): A list of CafeteriaItems to
             be added to the cart.
        Returns:
            Cart: A new Cart object initialized with the provided
            selected_items, total quantity, and total price calculated from
            the selected_items.
        """
        cart = Cart(selected_items,
                    self.__calculate_total_quantity(selected_items),
                    self.__calculate_total_price(selected_items))
        return cart

    def update_cart(self, cart: Cart, selected_items: list[CafeteriaItem]):
        """
       Update the provided Cart object with information from a list of selected
       CafeteriaItems.
       Args:
           cart (Cart): The Cart object to be updated.
           selected_items (list[CafeteriaItem]): A list of CafeteriaItems
            to be added to the cart.
       Returns:
           Cart: The updated Cart object containing the total price,
           total quantity, and a sorted list of selected CafeteriaItems
           based on their IDs.
       """
        cart.TotalPrice = self.__calculate_total_price(selected_items)
        cart.TotalQuantity = self.__calculate_total_quantity(selected_items)
        cart.Items = selected_items
        cart.Items = sorted(cart.Items, key=lambda o: o.Id)
        return cart

    def remove_from_cart(self, cart: Cart, item_id: int):
        """
        Remove a CafeteriaItem with the specified item ID from the given Cart.
        Args:
            cart (Cart): The Cart object from which the item will be removed.
            item_id (int): The ID of the CafeteriaItem to be removed from the
             cart.
        Returns:
            Cart: The updated Cart object after removing the specified
            CafeteriaItem.
        """
        cart.Items = [item for item in cart.Items if item.Id != item_id]
        return self.update_cart(cart, cart.Items)

    def print_cart(self, cart: Cart):
        """
        Print the contents of a Cart including total quantity, total price,
        and item details.
        Args:
            cart (Cart): The Cart object to be printed.
        Prints:
            The total quantity and total price of items in the cart, along
            with details of each CafeteriaItem including its ID, name, price
            and stock quantity.
        """
        print(f"Total Quantity: {cart.TotalQuantity}")
        print(f"Total Price: £"
              f"{self.price_converter.format_price(cart.TotalPrice)}")
        for item in cart.Items:
            print(f"{item.Id}. {item.Name} - £"
                  f"{self.price_converter.format_price(item.Price)} - "
                  f"x{item.Stock}")

    def __calculate_total_quantity(self, selected_items: list[CafeteriaItem]):
        """
        Calculate the total quantity of a list of CafeteriaItems based on
        their stock quantities.
        Args:
           selected_items (list[CafeteriaItem]): A list of CafeteriaItems for
            which to calculate the total quantity.
       Returns:
           int: The total quantity calculated by summing the individual stock
           quantities of each item in the selected_items list.
        """
        return sum(item.Stock for item in selected_items)

    def __calculate_total_price(self, selected_items: list[CafeteriaItem]):
        """
       Calculate the total price of a list of CafeteriaItems based on their
       prices and quantities.
       Args:
           selected_items (list[CafeteriaItem]): A list of CafeteriaItems for
            which to calculate the total price.
       Returns:
           float: The total price calculated by summing the individual total
           prices of each item (price multiplied by quantity) in the
           selected_items list.
       """
        total_price_per_item_array = []
        for selected_item in selected_items:
            total_price_per_item = selected_item.Price * selected_item.Stock
            total_price_per_item_array.append(total_price_per_item)
        return sum(item for item in total_price_per_item_array)
