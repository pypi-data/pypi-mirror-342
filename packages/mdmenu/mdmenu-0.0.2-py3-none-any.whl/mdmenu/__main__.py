"""
A customisable text driven menu system.
Entry point when module is run directly.
"""
from .mdmenu import MDMenu
from .mdmenu import invalid


def mdmenu_hello():
    """
    Test function
    """
    print("Hello world")


print("Running MDMenu")
my_menu = MDMenu()
my_menu.add_menu_item(item=("Hello", mdmenu_hello))

for i in range(1, 3):
    print(my_menu)
    print(f"Make A Choice: {i}")
    item_name, function_called = my_menu.menu_items.get(int(i), [None, invalid])
    function_called()
