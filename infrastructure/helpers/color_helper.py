from colorama import Fore


class ColorHelper:
    @staticmethod
    def color_yes_no_text():
        return f'{Fore.LIGHTGREEN_EX}Y{Fore.RESET}/{Fore.RED}N{Fore.RESET}'

    @staticmethod
    def color_text(color: Fore, text: str):
        return f'{color}{text}'
