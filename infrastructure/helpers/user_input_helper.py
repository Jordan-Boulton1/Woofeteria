from dataclasses import dataclass


@dataclass
class UserInputHelper:
    def create_array_from_user_input(self, user_input: str):
        return [int(x) for x in user_input.split(',') if x.strip().isdigit()]