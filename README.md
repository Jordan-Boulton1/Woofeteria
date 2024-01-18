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

### Future Features

- Description of menu items
    - I would like add a future feature, so that the user can see a description of what the menu item is.
- Global Stock
    - I would like to implement a stock feature that is hooked up to [googlesheets](https://docs.google.com/spreadsheets/u/0/), where the stock is global and menu items can be sold out.
- Global Stock Refresh Timer
    - I would like to implement a timer that refreshes the global stock every 30 minutes with random stock values.

## Tools & Technologies Used

- [Python](https://www.python.org) used as the back-end programming language.
- [Git](https://git-scm.com) used for version control. (`git add`, `git commit`, `git push`)
- [GitHub](https://github.com) used for secure online code storage.
- [PyCharm](https://www.jetbrains.com/pycharm/) used as a cloud-based IDE for development.
- [Heroku](https://www.heroku.com) used for hosting the deployed back-end site.
- [Regex101](https://regex101.com/) used to build regex expressions

### Classes & Functions

In addition to the layers that came with the template from Code Institute **Controllers** and **Views**, there were 3 additional layers that were added to achieve a clean and structured code -
**Entities**, **Services** and **Infrastructure**

- **Entities**: A layer that represents the business objects in the problem domain. In our case, the problem domain is the **Woofeteria** and the **Entities** layer is constructed by the following classes: 

```python
class Cart:
    """
    Represents a shopping cart in a cafeteria application.

    Attributes:
    - Items (List[CafeteriaItem]): A list of CafeteriaItem objects representing items in the cart.
    - TotalQuantity (int): The total quantity of items in the cart.
    - TotalPrice (float): The total price of all items in the cart.
   """
    Items: list[CafeteriaItem]
    TotalQuantity: int
    TotalPrice: float
```

```python
class CafeteriaItem:
    """
    Represents a cafeteria item with unique identifier, name, price, and stock.

    Attributes:
    - Id (int): A unique identifier for the cafeteria item.
    - Name (str): The name of the cafeteria item.
    - Price (float): The price of the cafeteria item.
    - Stock (int): The available stock or quantity of the cafeteria item.
   """
    Id: int
    Name: str
    Price: float
    Stock: int
```

- **Services**: A layer that represents the business logic in the problem domain. In our case, the problem domain is the **Woofeteria** and the **Services** layer is constructed by the following classes:
```python
class UserflowService:
    """
    Service class managing user interactions for the cafeteria application.
    This class orchestrates the user interactions within the cafeteria application,
    including menu navigation, order handling, and secret Woofin mode for administrators.
    Attributes:
        cafeteria_item_service (CafeteriaItemService): The service for cafeteria item operations.
        admin_service (AdminService): The service for administrator-related operations.
        cart_service (CartService): The service for shopping cart operations.
        price_converter (PriceConverter): The service for price formatting operations.
        menu (list[CafeteriaItem]): The current cafeteria menu.
        unique_set (set): A set to keep track of unique item IDs in the shopping cart.
        cart_result (list[CafeteriaItem]): A list to store items in the shopping cart.
    """
    def __init__(self):
        self.cafeteria_item_service = CafeteriaItemService()
        self.admin_service = AdminService()
        self.cart_service = CartService()
        self.price_converter = PriceConverter()
        self.menu = self.cafeteria_item_service.get_cafeteria_menu()
        self.unique_set = set()
        self.cart_result = []
```

```python
class CartService:
    """
    Service class for managing the shopping cart.
    Attributes:
        price_converter (PriceConverter): An instance of the PriceConverter class for handling price formatting.
    """
    def __init__(self):
        self.price_converter = PriceConverter()
```

```python
class CafeteriaItemService:
    """
    Service class for managing cafeteria items and related functionalities.

    Attributes:
       cafeteria_items (list[CafeteriaItem]): A list containing cafeteria items.
       price_converter (PriceConverter): An instance of PriceConverter for handling price-related operations.
    """
    def __init__(self):
        self.cafeteria_items = self.__populate_cafeteria_menu()
        self.price_converter = PriceConverter()
```

```python
class AdminService:
    """
    Service class for administrative tasks related to cafeteria management
    including adding, removing and updating the items in the menu
    Attributes:
       cafeteria_item_service (CafeteriaItemService): An instance of CafeteriaItemService for managing cafeteria items.
       menu (list[CafeteriaItem]): The current cafeteria menu.
    """
    def __init__(self):
        self.cafeteria_item_service = CafeteriaItemService()
        self.menu = self.cafeteria_item_service.get_cafeteria_menu()
```

- **Infrastructure**: A layer that is constructed of generic helpers and domain types that support the business layer (**Services**). The **Infrastructure** layer is constructed by 3 additional layers that clearly segragate the helpers and domain types by the resopnsibilities they provide - **Helpers**, **Validators** and **Enums**:
    - **Helpers**:
        ```python
       class ColorHelper:
           """
           This class includes static methods for generating colored text.
           """
        ```
         ```python
        class JsonFileHelper:
             """
             Helper class for reading from a JSON file.
             """
        ```
        ```python
          class JsonFileHelper:
            """
            A utility class for formatting prices.
            This class provides methods to format prices to a specific decimal precision.
            """
        ```
    - **Validators**
         ```python
           class UserInputValidator:
            """
            A utility class for validating user inputs in a cafeteria application.
    
            This class provides static methods for validating various types of user inputs,
            including integers, decimals, item IDs, and names. It also handles input parsing
            and user prompts related to the cafeteria application.
            """
        ```
    - **Enums**
         ```python
          class Icon(Enum):
            """
            Enumerates different icons representing elements in the system.
        
            Attributes:
            - DogIcon (str): Unicode character for a dog icon.
            - PawIcon (str): Unicode character for a paw icon.
            """
            
            DogIcon = '\U0001F436'
            PawIcon = '\U0001F43E'
         ```

The primary functions used on this application are: 

- `start_cafeteria_flow()`
    - Begins the cafeteria flow, welcoming the user, displaying the menu, and handling user orders.
- `add_to_cart()`
    - Creates a new Cart object with the provided list of CafeteriaItems.
- `update_cart()`
    - Updates the provided Cart object with information from a list of selected CafeteriaItems.
- `remove_from_cart()`
    - Removes a CafeteriaItem with the specified item ID from the given Cart.
- `print_cart()`
    - Prints the contents of a Cart including total quantity, total price, and item details.
- `print_cafeteria_menu()`
    - Prints the Cafeteria menu in a formatted table.
- `get_cafeteria_menu()`
    - Retrieves the current state of the Cafeteria menu.
- `add_items_to_menu()`
    - Adds new cafeteria items to the menu.
- `update_items()`
    - Updates cafeteria items in the menu.
- `update_items()`
    - Updates cafeteria items in the menu.
- `subtract_from_stock()`
    - Subtracts the specified quantity from the stock of a cafeteria item.
- `add_to_stock()`
    - Adds stock to the specified cafeteria item in the menu.
- `recalculate_ids()`
    - Recalculates the IDs for cafeteria items in the provided menu list.
- `validate_if_admin_name_provided()`
    - Validates if the provided user input matches the admin username.
- `create_array_from_user_input()`
    - Creates an array of integers from a comma-separated user input string.
- `validate_item_ids()`
    - Validates the user input for selecting CafeteriaItems by their IDs.
- `validate_user_input_is_comma_separated()`
    - Validates that user input is a comma-separated list of integers within a specified range.
- `validate_user_input_is_comma_separated()`
    - Validates that user input is a non-zero positive integer.
- `validate_user_input_is_a_decimal()`
    - Validates that user input is a positive decimal number with exactly two decimal places.
- `validate_input_before_parsing()`
    - Validates user input before parsing for ordering, updating, or removing items.
- `validate_input_for_items()`
    - Validates user input for the quantity of a CafeteriaItem to order or remove.
- `validate_user_name()`
    - Validates user input as a valid name.
- `validate_user_input_is_correct_quantity()`
    - Validates user input for the quantity of a CafeteriaItem during addition or update.
- `validate_user_input_is_correct_price()`
    - Validates user input for the price of a CafeteriaItem during addition or update.
- `validate_user_input_is_correct_item_name()`
    - Validates user input for the name of a CafeteriaItem during addition or update.
- `format_price()`
    - Formats the given price to two decimal places.
- `read_from_config_file()`
    - Reads data from a configuration file.
- `color_yes_no_text()`
    -  Returns colored text for 'Yes' and 'No' options.
- `color_add_remove_text()`
    - Returns colored text for 'Add' and 'Remove' options.
- `color_add_update_remove_exit_text()`
    -  Returns colored text for 'Add', 'Update', 'Remove', and 'Exit' options.
### Imports

I've used the following Python packages and/or external imported packages.
- `copy`: used to create a deep
- `colorama`: used for including color in the terminal
- `tabulate`: used for building tables in the terminal
- `re`: used for evaluating regex expression

## Testing

For all testing, please refer to the [TESTING.md](TESTING.md) file.

## Deployment

Code Institute has provided a [template](https://github.com/Code-Institute-Org/python-essentials-template) to display the terminal view of this backend application in a modern web browser.
This is to improve the accessibility of the project to others.

The live deployed application can be found deployed on [Heroku](https://woofeteria-1a0357d24185.herokuapp.com).

### Heroku Deployment

This project uses [Heroku](https://www.heroku.com), a platform as a service (PaaS) that enables developers to build, run, and operate applications entirely in the cloud.

Deployment steps are as follows, after account setup:

- Select **New** in the top-right corner of your Heroku Dashboard, and select **Create new app** from the dropdown menu.
- Your app name must be unique, and then choose a region closest to you (EU or USA), and finally, select **Create App**.
- From the new app **Settings**, click **Reveal Config Vars**, and set the value of KEY to `PORT`, and the value to `8000` then select *add*.
- If using any confidential credentials, such as CREDS.JSON, then these should be pasted in the Config Variables as well.
- Further down, to support dependencies, select **Add Buildpack**.
- The order of the buildpacks is important, select `Python` first, then `Node.js` second. (if they are not in this order, you can drag them to rearrange them)

Heroku needs two additional files in order to deploy properly.

- requirements.txt
- Procfile

You can install this project's **requirements** (where applicable) using:

- `pip3 install -r requirements.txt`

If you have your own packages that have been installed, then the requirements file needs updated using:

- `pip3 freeze --local > requirements.txt`

The **Procfile** can be created with the following command:

- `echo web: node index.js > Procfile`

For Heroku deployment, follow these steps to connect your own GitHub repository to the newly created app:

Either:

- Select **Automatic Deployment** from the Heroku app.

Or:

- In the Terminal/CLI, connect to Heroku using this command: `heroku login -i`
- Set the remote for Heroku: `heroku git:remote -a app_name` (replace *app_name* with your app name)
- After performing the standard Git `add`, `commit`, and `push` to GitHub, you can now type:
	- `git push heroku main`

The frontend terminal should now be connected and deployed to Heroku!

### Local Deployment

This project can be cloned or forked in order to make a local copy on your own system.

For either method, you will need to install any applicable packages found within the *requirements.txt* file.

- `pip3 install -r requirements.txt`.

If using any confidential credentials, such as `CREDS.json` or `env.py` data, these will need to be manually added to your own newly created project as well.

#### Cloning

You can clone the repository by following these steps:

1. Go to the [GitHub repository](https://github.com/Jordan-Boulton1/woofeteria) 
2. Locate the Code button above the list of files and click it 
3. Select if you prefer to clone using HTTPS, SSH, or GitHub CLI and click the copy button to copy the URL to your clipboard
4. Open Git Bash or Terminal
5. Change the current working directory to the one where you want the cloned directory
6. In your IDE Terminal, type the following command to clone my repository:
	- `git clone https://github.com/Jordan-Boulton1/woofeteria.git`
7. Press Enter to create your local clone.

Alternatively, if using Gitpod, you can click below to create your own workspace using this repository.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/Jordan-Boulton1/woofeteria)

Please note that in order to directly open the project in Gitpod, you need to have the browser extension installed.
A tutorial on how to do that can be found [here](https://www.gitpod.io/docs/configure/user-settings/browser-extension).

#### Forking

By forking the GitHub Repository, we make a copy of the original repository on our GitHub account to view and/or make changes without affecting the original owner's repository.
You can fork this repository by using the following steps:

1. Log in to GitHub and locate the [GitHub Repository](https://github.com/Jordan-Boulton1/woofeteria)
2. At the top of the Repository (not top of page) just above the "Settings" Button on the menu, locate the "Fork" Button.
3. Once clicked, you should now have a copy of the original repository in your own GitHub account!
