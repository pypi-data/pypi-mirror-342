"""
A customisable text driven menu system.
"""
# TODO - Move doco to readthedocs - https://docs.readthedocs.com/platform/stable/tutorial/
import textwrap


class MDMenu():
    """
    Object for the creation and configuration of a text driven menu system. Public functions are
    provided to add and remove items from the menu.

    Several instance attributes control various aspects of menu:

        footer_content (default: None)
            A text body to be displayed in the footer of the menu, after the main body of the menu.
        footer (default: True)
            Enabled by default, this boolean attribute indicates if the menu will be displayed with
            footer.
        key_trailing_gap (default: 3)
            The number of white space to be added after the menu item key and before the items name
            when displaying the menu.
                eg.     5:<key_trailing_gap>Hello World
        key_width (default: 7)
            The number of characters to pad the menu item key to when displayed.
                eg.<key_width>:     Hello World
        menu_character (default: "#")
            The character used to create borders of 'self.menu_width' for the menu
        menu_hold_last (default: True)
            When true, the last item in the 'self.menu_items" dict is maintained as the item with
            the highest/last key value. As the default and most likely first item added is the exit,
            this provides a easy mechanism to keep it as the last last menu item even when key
            values are automatically assigned.
        menu_items (default: {1: ("Exit", exit)})
            The dict of menu items in the system. Each item has a int key and a tuple with the items
            title and associated function.
        menu_name (default: "Menu")
            The name of the menu as a string. The name is displayed when the attribute 'title' is
            true.
        menu_width (default: 80)
            The width of the menu system
        title_border (default: True)
            Enabled by default, this boolean attribute indicates if the menus title should be
            surrounded by a border of 'self.menu_character'.
        title_padding (default: " ")
            The character to use to pad the left and right of 'self.menu_name' when displayed in the
            menu title.
        title_preface (default: None)
            A text body to be displayed between the menu title and the main body of the menu.
        title (default: True)
            Enabled by default, this boolean attribute indicates if the menus title should be
            displayed.
    """


# TODO - Consider using this for input validation for instance attributes - Link below
# https://stackoverflow.com/questions/2825452/correct-approach-to-validate-attributes-of-an-instance-of-class
    def __init__(self,
                 footer_content=None,
                 footer=True,
                 key_trailing_gap=3,
                 key_width=7,
                 menu_character="#",
                 menu_hold_last=True,
                 menu_items=None,
                 menu_name="Menu",
                 menu_width=80,
                 title_border=True,
                 title_padding=" ",
                 title_preface=None,
                 title=True
                 ) -> None:
        # TODO - Why not set a default like the rest
        if menu_items is None:
            self.menu_items = {1: ("Exit", exit)}
        else:
            self.menu_items = menu_items

        self.menu_name = menu_name
        self.menu_character = menu_character
        self.menu_width = menu_width
        self.menu_hold_last = menu_hold_last
        self.title = title
        self.title_border = title_border
        self.title_padding = title_padding
        self.title_preface = title_preface
        self.footer = footer
        self.footer_content = footer_content
        self.key_width = key_width
        self.key_trailing_gap = key_trailing_gap

    def __str__(self) -> str:
        """
        Creates a representation of the menu to be displayed to the console.

        Returns:
            str: Formatted menu test of the menu
        """
        output: str = ""

        if self.title:
            output += self._create_title()

        for key in sorted(self.menu_items.keys()):
            space = " "
            key_str = str(key) + ":"
            item_str = self._format_menu_item(self.menu_items[key][0])
            output += f"{key_str:{space}>{self.key_width}}{space * self.key_trailing_gap}{item_str}\n"

        if self.footer:
            output += self._create_footer()

        return output

    def _create_footer(self) -> str:
        """
        Creates a string for the footer of the menu. If footer_content is defined, its formatted and included in the
        footer.

        Returns:
            str: Formatted menu footer text
        """
        if self.footer_content is None:
            return self._create_border()

        return self._create_border() + self._format_content(self.footer_content) + self._create_border()

    def _format_content(self, content: str) -> str:
        """
        Creates string formatted to the length specified by of self.menu_width long.

        Args:
            content (str): A string to be formatted to the width of the menu.

        Returns:
            str: Formatted text
        """
        lines = textwrap.wrap(content, width=self.menu_width)
        # Backslashes are not allowed in the {} portion of f-strings
        newline = "\n"
        return f"{newline.join(lines)}\n"

    def _format_menu_item(self, content: str) -> str:
        """
        Creates string formatted to the length available after menu item padding and gap to display the menu item.
            eg. self.menu_width - self.key_width - self.key_trailing_gap = remaining space
                ################################################################################
                         1:                   Hello 2nd
                         2:                   Hello 3nd
                <key_width>:<key_trailing_gap><--- remaining space ---------------------------->

        Args:
            content (str): A string to be formatted to the intended width.

        Returns:
            str: Formatted text
        """
        remaining_space = self.menu_width - self.key_width - self.key_trailing_gap
        taken_space = self.key_width + self.key_trailing_gap

        if len(content) <= remaining_space:
            return content

        lines = textwrap.wrap(content, width=remaining_space)

        # Remove the first line so indentation in not applied
        first_line = lines.pop(0)

        # Add the indentations to all lines except the first line and then join back to one list of lines
        space = " " * taken_space
        lines = [first_line] + [f"{space}{line}" for line in lines]

        # Backslashes are not allowed in the {} portion of f-strings
        newline = "\n"
        return f"{newline.join(lines)}"

    def _create_title(self) -> str:
        """
        Creates title string of self.menu_name. When self.title_border is true the title sting is wrapped in a border
        string of self.menu_character that is self.menu_width characters long.

        Returns:
            str: Formatted menu title text
        """
        output: str = ""
        if self.title_border:
            output += self._create_border()

        output += f"{self.menu_name:{self.title_padding}^{self.menu_width}}\n"

        if self.title_border:
            output += self._create_border()

        if self.title_preface is not None:
            output += self._format_content(self.title_preface) + self._create_border()

        return output

    def _create_border(self) -> str:
        """
        Creates a border string of self.menu_character that is self.menu_width characters long.

        Returns:
            str: A border string self.menu_width characters long
        """
        return f"{self.menu_width * self.menu_character}\n"

    def add_menu_item(self, item: tuple, key: int = None,) -> None:
        """
        Add a new menu item to the menu. If no key is given for the menu item the next available key is allocated. When
        self.menu_hold_last is True, the last item, typically an exit option, is renumbered to remain as the last item
        in the menu.

        Args:
            item (tuple): A tuple of the Menu item. (item_name, item_function)
            key (int, optional): The key to add the menu item with. Defaults to None.

        Raises:
            ValueError: A ValueError is raised when a key which already exist is added.
        """

        highest_index = max(list(self.menu_items.keys()))

        if key is None:
            # When no key is specified get the next lowest key that is not already being used
            key = next(
                (i for i in range(1, highest_index) if i not in self.menu_items.keys()), highest_index)
            # When auto allocating a key and not holding last we need to avoid a collision
            if key == highest_index and not self.menu_hold_last:
                key += 1

        if key >= highest_index and self.menu_hold_last:
            # Move the current highest item up by one to maintain its position
            last_item = self.menu_items.pop(highest_index)
            self.menu_items[key + 1] = last_item

        if key in self.menu_items:
            raise ValueError(f"Key {key} already exists in the menu.")

        self.menu_items[key] = item

    def remove_menu_item(self, key: int) -> tuple:
        """
        Removes a menu item from the menu with the specified key.

        Args:
            key (int): The key of the menu item to remove.

        Returns:
            tuple: The key and value removed from the menu

        Raises:
            KeyError: A keyError is raised when a key which does not exist is removed from the menu
        """
        # TODO: log a message if this throws an error
        return self.menu_items.pop(key)


def invalid() -> None:
    """
    Default function called when an invalid menu option is selected.
    """
    print("INVALID CHOICE!")


if __name__ == "__main__":  # pragma: no cover
    print("Running")

    def hello():
        """
        Test function
        """
        print("Hello world")

    my_menu = MDMenu()
    my_menu.add_menu_item(item=("Hello", hello))

    while True:
        print(my_menu)
        ans = input("Make A Choice: ")

        try:
            item_name, function_called = my_menu.menu_items.get(int(ans), [None, invalid])
            function_called()
        except ValueError:
            print(("Input must be a valise int."))
