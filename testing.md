# Testing

Return back to the [README.md](README.md) file.

## Code Validation

### Python

I have used the recommended [PEP8 CI Python Linter](https://pep8ci.herokuapp.com) to validate all of my Python files.

| File | CI URL | Screenshot | Notes |
| --- | --- | --- | --- |
| run.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Jordan-Boulton1/woofeteria/main/run.py) | ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/validation/py-validation-run.png) | Pass: No Errors |
| user_flow_service.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Jordan-Boulton1/woofeteria/main/services/user_flow_service.py) | ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/validation/py-validation-userflow.png) | Pass: No Errors |
| cart_service.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Jordan-Boulton1/woofeteria/main/services/cart_service.py) | ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/validation/py-validation-cart-service.png) | Pass: No Errors |
| cafeteria_item_service.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Jordan-Boulton1/woofeteria/main/services/cafeteria_item_service.py) | ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/validation/py-validation-item-service.png) | Pass: No Errors |
| admin_service.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Jordan-Boulton1/woofeteria/main/services/admin_service.py) | ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/validation/py-validation-admin-service.png) | Pass: No Errors |
| user_input_validator.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Jordan-Boulton1/woofeteria/main/infrastructure/validators/user_input_validator.py) | ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/validation/py-validation-user-input-validator.png) | Pass: No Errors |
| price_converter.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Jordan-Boulton1/woofeteria/main/infrastructure/helpers/price_converter.py) | ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/validation/py-validation-price-converter.png) | Pass: No Errors |
| json_file_helper.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Jordan-Boulton1/woofeteria/main/infrastructure/helpers/json_file_helper.py) | ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/validation/py-validation-json-file-helper.png) | Pass: No Errors |
| color_helper.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Jordan-Boulton1/woofeteria/main/infrastructure/helpers/color_helper.py) | ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/validation/py-validation-color-helper.png) | Pass: No Errors |
| enum_icon.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Jordan-Boulton1/woofeteria/main/infrastructure/enums/enum_icon.py) | ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/validation/py-validation-enum-icon.png) | Pass: No Errors |
| cart.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Jordan-Boulton1/woofeteria/main/entities/cart.py) | ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/validation/py-validation-cart.png) | Pass: No Errors |
| cafeteria_item.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/Jordan-Boulton1/woofeteria/main/entities/cafeteria_item.py) | ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/validation/py-validation-cafeteria-item.png) | Pass: No Errors |

## Browser Compatibility

I've tested my deployed project on multiple browsers to check for compatibility issues.

| Browser | User Flow | Admin Flow | Notes |
| --- | --- | --- | --- |
| Chrome | ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/compatibility/chrome-compatibility.png) | ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/compatibility/chrome-compatibility-admin.png) | Works as expected |
| Firefox | ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/compatibility/firefox-compatibility.png) | ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/compatibility/firefox-compatibility-admin.png) | Emoji's do not load properly |
| Edge | ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/compatibility/edge-compatibility.png) | ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/compatibility/edge-compatibility-admin.png) | Works as expected |

## Defensive Programming

Defensive programming was manually tested with the below user acceptance testing:

**Note - some images have been taken from the local terminal, this was due to the fact that I could fit more validation into one screenshot. However all validation has been tested in the Code Institute teminal.**

| Feature | Expectation | Test | Result | Fix | Screenshot |
| --- | --- | --- | --- | --- | --- |
| Enter Name |
|  | Feature is expected to allow the user to input a name with the exception of some special characters, such as `-` and `'`. | Tested the feature by inputting an *integer*, a special character (outside of the ones mentioned), an empty string and a space.  | The feature behaved as expected, and it accepted a valid name. | Test concluded and passed | ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/defensive%20programming/dp-name-validation.png) |
| Menu |
|  | Feature is expected to allow the user to enter an integer that correlates to the item ID in the menu. | Tested the feature by entering invalid inputs such as: "Hello", "?", `empty` and `spacebar`. | The feature behaved as expected, and only allows the user to enter an integer. | Test concluded and passed | ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/defensive%20programming/dp-menu-validation.png) |
| Finished Ordering | 
| | Feature is expecting a user input of either (**Y**) or (**N**). | Tested the feature by entering invalid inputs such as: "hi", "!", 1, `empty` and `spacebar`. | The feature behaved as expected, and only allows the user to enter either (Y) or (N) | Test concluded and passed | ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/defensive%20programming/dp-finished-validation.png) |
|||||| ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/defensive%20programming/dp-finished-2-validation.png)
|  | In the event the user selects (Y), the feature is expected ask the user to pay the total amount of their cart. | Tested the feature by entering invalid inputs such as: "hello", "!", Invalid integers(incorrect total), `empty` and `spacebar`. | The feature behaved as expected, and only allows the user to enter the exact total of their cart. | Test concluded and passed | ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/defensive%20programming/dp-complete-uf-validation.png) | 
|||||| ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/defensive%20programming/dp-complete-uf-2-validation.png)
| | In the event the user selects (N), the feature will prompt the (Add)/(Remove) message. | Tested the feature by entering invalid inputs such as: "hello", "!", Invalid integers(incorrect total), `empty` and `spacebar`. | The feature behaved as expected, and prompts the user with the (Add)/(Remove) message. | Test concluded and passed | ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/defensive%20programming/dp-user-select-no.png) |
| Add/Remove |
|  | If the user selects (Add), the feature is expected to allow the user to add more items to their cart. | Tested the feature by entering invalid inputs such as: "hello", "!", integers, `empty` and `spacebar`.  | The feature behaved as expected, and allows the user to add more items to their cart. | Test concluded and passed | ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/defensive%20programming/dp-add-validation.png) |
| | If the user selects (Remove) the feature is expected to allow the user to remove items from their cart. | Tested the feature by entering invalid inputs such as: "hello", "!", integers, `empty` and `spacebar`. | The feature behaves as expected, and allows the user to remove items from their cart. | Test concluded and passed | ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/defensive%20programming/dp-remove-items-validation.png) |
### Admin
| Feature | Expectation | Test | Result | Fix | Screenshot |
| --- | --- | --- | --- | --- | --- |
| | Feature is expected to enter secret "Woofin" Mode when the correct credentials are entered. | Tested the feature by entering faulty passwords such as: special characters, `empty` and `spacebar`. | The feature behaves as expected and allows the user to enter the secret "Woofin" Mode if the correct credentials are entered. If the credentials are not correct it continues with the regular user flow. | Test concluded and passed | ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/defensive%20programming/dp-admin-login-validation.png) |
| Add/Update/Remove/Exit |
| | Feature is expected to take a user input of either Add, Update, Remove or Exit.| Tested the feature by entering invalid inputs such as: "hello", integers, special characters, `empty` and `spacebar`. | The feature behaves as expected and only accepts the valid inputs. | Test concluded and passed | ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/defensive%20programming/dp-successful-admin-login-validation.png) |
|||||| ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/defensive%20programming/dp-admin-validation-1.png)
|||||| ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/defensive%20programming/dp-admin-validation-2.png)
|||||| ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/defensive%20programming/dp-admin-validation-3.png)
|||||| ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/defensive%20programming/dp-admin-validation-4.png)
|||||| ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/defensive%20programming/dp-admin-validation-5.png)
|| If the admin selects (Add), the feature is expected to allow the admin to add more items to the menu by prompting the user to enter a *name*, a *stock* value and a *price* for the item. | Tested the feature by adding additional items to the menu and tested the validation by entering invalid inputs such as: characters, special characters, `empty` and `spacebar`. | The feature behaves as expected and only allows valid inputs to be entered in order to  add additional items to the menu. | Test concluded and passed | ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/defensive%20programming/dp-admin-add-validation.png) |
|||||| ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/defensive%20programming/dp-admin-add-validation-2.png)
|| If the admin selects (Update), the feature is expected to allow the admin to update the current menu items, allowing them to rename items, adjust stock and price values. The admin will also have the option to "Skip" if they wish to not update a certain value. | Tested the feature by updating a menu item and checking the validation by entering invalid inputs such as: characters, special characters, `empty` and `spacebar`. | The feature behaves as expected and only allows valid inputs in order to update menu items. | Test concluded and passed | ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/defensive%20programming/dp-admin-update-validation.png) |
|||||| ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/defensive%20programming/dp-admin-update-validation-2.png)
|||||| ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/defensive%20programming/dp-admin-update-validation-3.png)
|| If the admin selects (Remove), the feature is expected to allow the admin to remove items from the menu. | Tested the feature by removing an item from the menu. Tested the validation by entering invalid inputs such as: characters, special characters, `empty` and  `spacebar`. | The feature behaves as expected and only allows a valid input in order to remove items from the menu. | Test concluded and passed | ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/defensive%20programming/dp-admin-remove-validation.png) |
|||||| ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/defensive%20programming/dp-admin-remove-validation-2.png)
|| If the admin selects (Exit), the feature is expected to exit admin mode and return to the regular user flow. | Tested the feature by inputting exit and checking if it continued the regular user flow properly.| The feature behaves as expected and exits admin mode and continues the regular user flow. | Test concluded and passed | ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/defensive%20programming/dp-admin-exit-validation.png)

## Bugs

- Admin Flow - Not Recalculating Menu ID

    ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/bugs/admin-flow-bug.PNG)

    - To fix this, I made a function that recalculated the item ID's.

- Admin Flow - Validation
    
    ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/bugs/admin-flow-bug-2.png)
    
    - To fix this, I added an `else` check, that checks if what the user has entered is a valid input, if it isn't, it prints a message to the terminal.

- Cart Item Duplication

    ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/bugs/cart-bug.PNG)

    - To fix this, I added an `If` statement that checks if the same item is in the user cart the same item would not be added, instead the quantity would be increased.

- Stock Total

    ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/bugs/stock-bug.PNG)

    - To fix this, I removed a piece of code that was taking the user input and storing it as the Stock value.

## Unfixed Bugs

- When you run the terminal on the firefox web browser, only half of the emojis load.

    ![screenshot](https://github.com/Jordan-Boulton1/woofeteria/blob/main/documentation/testing/bugs/firefox-emoji-bug.png)

    - Attempted fix: As the terminal was not made by me, I was unsure how to fix this bug.

There are no remaining bugs that I am aware of.
