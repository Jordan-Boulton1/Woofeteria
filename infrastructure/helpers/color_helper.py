from colorama import Fore, Style


class ColorHelper:
    """
    This class includes static methods for generating colored text.
    """
    @staticmethod
    def color_yes_no_text():
        """
       Return colored text for 'Yes' and 'No' options.
       Returns:
           str: Colored text representing 'Yes' as (Y) in light green and 'No'
            as (N) in red.
       """
        return f'({Fore.LIGHTGREEN_EX}Y{Fore.RESET}/{Fore.RED}N{Fore.RESET})'

    @staticmethod
    def color_add_remove_text():
        """
       Return colored text for 'Add' and 'Remove' options.
       Returns:
           str: Colored text representing 'Add' in light green and 'Remove' in
            red.
       """
        return (f'({Fore.LIGHTGREEN_EX}Add{Fore.RESET}/{Fore.RED}Remove'
                f'{Fore.RESET})')

    @staticmethod
    def color_add_update_remove_exit_text():
        """
       Return colored text for 'Add', 'Update', 'Remove', and 'Exit' options.
       Returns:
           str: Colored text representing 'Add' in light green, 'Update' in
           light cyan, 'Remove' in red, and 'Exit' in bright style.
       """
        return (f'({Fore.LIGHTGREEN_EX}Add{Fore.RESET}/{Fore.LIGHTCYAN_EX}'
                f'Update{Fore.RESET}/{Fore.RED}Remove{Fore.RESET}'
                f'/{Style.BRIGHT}Exit{Style.RESET_ALL}) ')
