from dynamic_functioneer.dynamic_decorator import dynamic_function


class Inventory:
    """
    A class to manage an inventory of items with stock levels.
    """

    def __init__(self):
        """
        Initializes the inventory with an empty stock dictionary.
        """
        self.stock = {}

    @dynamic_function(
        model="gpt-4o",
        extra_info="If the item does not exist and quantity is positive, create the item in the inventory.",
        unit_test=False,
        error_trials=3,
        error_model="gpt-4o"
    )
    def update_stock(self, item, quantity):
        """
        Updates the stock for a given item.

        Args:
            item (str): The name of the item.
            quantity (int): The quantity to add (positive) or remove (negative).

        Returns:
            str: Confirmation message about the stock update.

        Raises:
            ValueError: If the quantity is negative and results in stock below zero.

        Examples:
            >>> inventory = Inventory()
            >>> inventory.update_stock("apple", 50)
            'Stock updated: apple -> 50 units'

            >>> inventory.update_stock("apple", -10)
            'Stock updated: apple -> 40 units'

            >>> inventory.update_stock("orange", -5)
            Traceback (most recent call last):
                ...
            ValueError: Cannot remove stock from 'orange': Item does not exist.

            >>> inventory.update_stock("apple", -50)
            Traceback (most recent call last):
                ...
            ValueError: Insufficient stock for 'apple'.
        """
        pass  # This will be dynamically implemented.

    @dynamic_function(
        model="meta-llama/llama-3.2-3b-instruct:free",
        extra_info="Fetch the stock level of an item from the inventory.",
        unit_test=False,
        error_trials=2,
        error_model="meta-llama/llama-3.2-3b-instruct:free"
    )
    def get_stock(self, item):
        """
        Retrieves the stock level for a given item.

        Args:
            item (str): The name of the item.

        Returns:
            int: The current stock level.

        Raises:
            ValueError: If the item does not exist in the inventory.

        Examples:
            >>> inventory = Inventory()
            >>> inventory.update_stock("apple", 50)
            'Stock updated: apple -> 50 units'

            >>> inventory.get_stock("apple")
            50

            >>> inventory.get_stock("orange")
            Traceback (most recent call last):
                ...
            ValueError: Item 'orange' not found in inventory.
        """
        pass  # This will be dynamically implemented.


# Example Usage
if __name__ == "__main__":
    inventory = Inventory()

    # Add items to inventory
    print(inventory.update_stock("apple", 30))  # Stock updated: apple -> 30 units
    print(inventory.update_stock("banana", 20))  # Stock updated: banana -> 20 units

    # Check stock levels
    print(f"Apple stock: {inventory.get_stock('apple')}")  # Apple stock: 30
    print(f"Banana stock: {inventory.get_stock('banana')}")  # Banana stock: 20

    # Remove stock
    print(inventory.update_stock("apple", -10))  # Stock updated: apple -> 20 units

    