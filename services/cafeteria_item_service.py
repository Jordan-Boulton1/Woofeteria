from dataclasses import dataclass

from entities.cafeteria_item import CafeteriaItem


class CafeteriaItemService:

    def print_cafeteria_menu(self):
        menu = self.__populate_cafeteria_menu()
        for item in menu:
            format_price = "{0:.2f}".format(item.Price)
            print(f"{item.Id}. {item.Name} - £{format_price}")

    def __populate_cafeteria_menu(self):
        menu = [
            CafeteriaItem(1, "Woofin", 2.50, 10),
            CafeteriaItem(2, "Paw Cake", 3.20, 10),
            CafeteriaItem(3, "Cheeky Cheese Paws", 1.80, 10),
            CafeteriaItem(4, "Pup Cake", 2, 10)]
        return menu
