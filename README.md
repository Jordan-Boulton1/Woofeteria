# [WOOFETERIA](https://woofeteria-1a0357d24185.herokuapp.com)

Woofeteria is a cafe built especially for your fluffy four-legged dog buddies. Woofeteria offers a wide selection of amazing and safe tasty treats for your fluffy buddies, made from our head chef Storm the Siberian Husky. Users of this application will be able to have a semi-realistic "conversation" with themselves. The user will also have the ability to order a selection of items from the menu which will be displayed in their cart. Along with the item being displayed in the users cart, they will also have the ability to see how many items they have ordered, the quantity of each item they have ordered, as well as the total price of their cart.

## Features

### Existing Features

### **User Flow**

- **Welcome Message**
    - Upon running the application the user is greeted with a welcome message, asking for the users name.
        
![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/features/userflow/welcome-message.png)

- **Menu**
    - A menu is presented to the user in the form of a table to clearly illustrate the item ID, Name, Price and the available stock.

![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/features/userflow/original-menu.png)

- **Order Instructions**
    - The user is displayed with a message with clear instructions on how to order something from the menu.
    - When the user has chosen to order an item from the menu they will be notified that the item has been added to their cart.

![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/features/userflow/order-instructions.png)

![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/features/userflow/add-to-cart-notify.png)

- **Finished Ordering?**
    - When the user has added an item/items to their cart, the user will be prompted with a message asking if they are finished ordering.
    - The user has two options to select from, (**Y**) and (**N**). If the user selects (**Y**) the user will be prompted with their cart and a message which asks them to pay the total in their cart.
    - If the user selects (**N**) they will be met with a further two options, (**Add**) and (**Remove**).

![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/features/userflow/is-user-finished.png)

![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/features/userflow/is-user-finished-yes.png)

- **Add or Remove**
    - If the user selects (**Add**), they will be taken through the process of adding an item from the menu again.
    - If the user selects (**Remove**), they will be prompted with a message, which gives the user clear instructions on how to remove an item(s). When the user removes an item, the will be notified which item has been removed from their cart, and the quantity that they chose to remove.

![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/features/userflow/is-user-finished-no.png)

![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/features/userflow/user-selection-add.png)

### Admin Functionality (Woofin Mode)

<details>
<summary> Spoiler </summary>

I've implemented a temporary solution in the application to handle the management of Woofeteria products and stock. However, it should be noted, that the data is not persistent across users or sessions and resets each time the app is launched. Ideally, this data should be linked to a real database for continuous updates between users and sessions.

To facilitate testing of this functionality, I've introduced a concealed Admin feature known as "Woofin Mode", which requires a password for access. You can use the following credentials:

```
Username: Storm
Password: barkies123
```

Upon entering the name "Storm" during the initial prompt, the app will prompt you for the secret password. If an incorrect password is entered 3 times, access will be denied and the user will be taken into the regular user flow of the app.

Upon successfully entering the correct password, the user will have full access to "Woofin Mode" with full product management and CRUD functionality.

- **Create**: user can add new products to the menu.
- **Retrieve**: user can retrieve/read products.
- **Update**: user can update existing products in the menu.
- **Delete**: user can delete products from the menu.

</details>