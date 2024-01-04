from dataclasses import dataclass

from entities.cafeteria_item import CafeteriaItem
from entities.cart import Cart
from infrastructure.helpers.price_converter import PriceConverter


@dataclass
class CartService:
    def __init__(self):
        self.price_converter = PriceConverter()
    def add_to_cart(self, selected_items: list[CafeteriaItem]):
        cart = Cart(selected_items,
                    self.__calculate_total_quantity(selected_items),
                    self.__calculate_total_price(selected_items))
        return cart

    def update_cart(self, cart: Cart, selected_items:list[CafeteriaItem]):
        cart.TotalPrice = self.__calculate_total_price(selected_items)
        cart.TotalQuantity = self.__calculate_total_quantity(selected_items)
        cart.Items = selected_items
        return cart

    def remove_from_cart(self, cart: Cart, item_id: int):
        cart.Items = [item for item in cart.Items if item.Id != item_id]
        return self.update_cart(cart, cart.Items)

    def print_cart(self, cart: Cart):
        print(f"Total Quantity: {cart.TotalQuantity}")
        print(f"Total Price: £{self.price_converter.format_price(cart.TotalPrice)}")
        for item in cart.Items:
            print(f"{item.Id}. {item.Name} - £{self.price_converter.format_price(item.Price)}")


    def __calculate_total_quantity(self, selected_items: list[CafeteriaItem]):
        return sum(item.Stock for item in selected_items)

    def __calculate_total_price(self, selected_items: list[CafeteriaItem]):
        total_price_per_item_array = []
        for selected_item in selected_items:
            total_price_per_item = selected_item.Price * selected_item.Stock
            total_price_per_item_array.append(total_price_per_item)
        return sum(item for item in total_price_per_item_array)






