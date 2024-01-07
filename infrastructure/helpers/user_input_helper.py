from dataclasses import dataclass
import re


@dataclass
class UserInputHelper:
    def create_array_from_user_input(self, user_input: str):
        return [int(x) for x in user_input.split(',') if x.strip().isdigit()]

    def validate_user_input_is_comma_separated(self, user_input: str, array_length: int):
        if len(user_input) == 0:
            return False
        pattern = re.compile(r'^(?:[1-' + str(array_length) + '](?:, ?[1-' + str(array_length) + '])*)?$')
        return bool(re.match(pattern, user_input))

    def validate_user_input_is_a_number(self, user_input: str):
        if len(user_input) == 0:
            return False
        return bool(user_input.isdigit())

    def validate_user_input_is_a_decimal(self, user_input: str):
        if len(user_input) == 0:
            return False
        elif user_input.replace(".", "").isnumeric():
            return True
        else:
            return False
