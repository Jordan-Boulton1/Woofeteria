from colorama import Fore, Style


class ColorHelper:
    @staticmethod
    def color_yes_no_text():
        return f'({Fore.LIGHTGREEN_EX}Y{Fore.RESET}/{Fore.RED}N{Fore.RESET})'

    @staticmethod
    def color_add_remove_text():
        return f'({Fore.LIGHTGREEN_EX}Add{Fore.RESET}/{Fore.RED}Remove{Fore.RESET})'

    @staticmethod
    def color_add_update_remove_exit_text():
        return f'({Fore.LIGHTGREEN_EX}Add{Fore.RESET}/{Fore.LIGHTCYAN_EX}Update{Fore.RESET}/{Fore.RED}Remove{Fore.RESET}/{Style.BRIGHT}Exit{Style.RESET_ALL}) '

    @staticmethod
    def color_text(color: Fore, text: str):
        return f'{color}{text}'
