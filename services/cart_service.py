from dataclasses import dataclass

from entities.cafeteria_item import CafeteriaItem
from entities.cart import Cart
from infrastructure.helpers.price_converter import PriceConverter


@dataclass
class CartService:
    def __init__(self):
        self.price_converter = PriceConverter()

    def add_to_cart(self, selected_items: list[CafeteriaItem]):
        """
        Creates a new cart object with the ordered items from the user and
        calculated quantity and price.
        """
        cart = Cart(selected_items,
                    self.__calculate_total_quantity(selected_items),
                    self.__calculate_total_price(selected_items))
        return cart

    def update_cart(self, cart: Cart, selected_items: list[CafeteriaItem]):
        """
        Recalculates the total quantity and price of the cart from the newly
        selected items.
        """
        cart.TotalPrice = self.__calculate_total_price(selected_items)
        cart.TotalQuantity = self.__calculate_total_quantity(selected_items)
        cart.Items = selected_items
        cart.Items = sorted(cart.Items, key=lambda o: o.Id)
        return cart

    def remove_from_cart(self, cart: Cart, item_id: int):
        """
        Filters out the item from the cart that is to be removed and updates
        the cart.
        """
        cart.Items = [item for item in cart.Items if item.Id != item_id]
        return self.update_cart(cart, cart.Items)

    def print_cart(self, cart: Cart):
        """
        Prints the details of the cart to the console.
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
        Calculates the total quantity of the cart by using the items inside it.
        """
        return sum(item.Stock for item in selected_items)

    def __calculate_total_price(self, selected_items: list[CafeteriaItem]):
        """
        Creates an empty array that will store the total price * order
        quantity per item in the cart, and loops through the list of ordered
        items, calculates the price per item and adds it to the array.
        Finally sums up the total price per item.
        """
        total_price_per_item_array = []
        for selected_item in selected_items:
            total_price_per_item = selected_item.Price * selected_item.Stock
            total_price_per_item_array.append(total_price_per_item)
        return sum(item for item in total_price_per_item_array)
