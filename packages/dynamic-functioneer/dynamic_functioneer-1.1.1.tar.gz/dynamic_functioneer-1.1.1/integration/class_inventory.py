from dynamic_functioneer.dynamic_decorator import dynamic_function

class Inventory:
    """
    A class to represent an inventory system.
    """

    def __init__(self):
        """
        Initializes the inventory with an empty stock dictionary.
        """
        self.stock = {}

    @dynamic_function(
        # model="meta-llama/llama-3.2-3b-instruct:free"
        model = 'crewai-sequential2-gemini-2.0-flash',
    )
    def update_stock(self, item, quantity):
        """
        Updates the stock for a given item. If the item is not found in the inventory
        and the quantity is positive, the item will be created and added to the inventory.
        Negative quantities require the item to exist and have sufficient stock.

        Args:
            item (str): The name of the item.
            quantity (int): The quantity to add (positive) or remove (negative).

        Returns:
            str: Confirmation message about the stock update.

        Raises:
            ValueError: If the quantity is negative and results in stock below zero.
            ValueError: If the item does not exist in the inventory and the quantity is negative.

        Examples:
            >>> inventory = Inventory()
            >>> inventory.update_stock("apple", 50)
            'Stock updated: apple -> 50 units'

            >>> inventory.update_stock("banana", 30)
            'Stock updated: banana -> 30 units'

            >>> inventory.update_stock("apple", -20)
            'Stock updated: apple -> 30 units'

            >>> inventory.update_stock("banana", -50)
            Traceback (most recent call last):
                ...
            ValueError: Insufficient stock for item 'banana'.

            >>> inventory.update_stock("orange", -10)
            Traceback (most recent call last):
                ...
            ValueError: Item 'orange' not found in inventory.

            >>> inventory.update_stock("orange", 10)
            'Stock updated: orange -> 10 units'
        """
        pass  # This will be dynamically implemented.

    @dynamic_function(
        # model="google/gemini-2.0-flash-exp:free"
        model = 'crewai-sequential2-gemini-2.0-flash',
    )
    def get_stock(self, item):
        """
        Retrieves the current stock for a given item.

        Args:
            item (str): The name of the item.

        Returns:
            int: The quantity of the item in stock.

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
    # Initialize the inventory
    inventory = Inventory()

    # Add items to the inventory
    print(inventory.update_stock("apple", 50))
    print(inventory.update_stock("banana", 30))

    # # Remove items from the inventory
    print(inventory.update_stock("apple", -20))

    # Check stock
    print(f"Stock of apples: {inventory.get_stock('apple')}")
    print(f"Stock of bananas: {inventory.get_stock('banana')}")

    # # Attempt to remove more items than available
    # try:
    #     inventory.update_stock("apple", -40)
    # except ValueError as e:
    #     print(f"Error: {e}")

