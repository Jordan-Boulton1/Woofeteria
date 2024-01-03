from dataclasses import dataclass

from models.cafeteria_item import CafeteriaItem
from models.cart import Cart


@dataclass
class CartService:
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


    def __calculate_total_quantity(self, selected_items: list[CafeteriaItem]):
        return sum(item.Quantity for item in selected_items)

    def __calculate_total_price(self, selected_items: list[CafeteriaItem]):
        return sum(item.Price for item in selected_items)






