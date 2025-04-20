from dynamic_functioneer.dynamic_decorator import dynamic_function

class BankAccount:
    """
    A class to represent a bank account system.
    """

    def __init__(self, account_number, account_holder, initial_balance=0.0):
        """
        Initializes a bank account.

        Args:
            account_number (str): The unique identifier for the account.
            account_holder (str): The name of the account holder.
            initial_balance (float): The initial amount in the account. Defaults to 0.0.
        """
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = initial_balance

    @dynamic_function(
        # model="google/gemini-exp-1206:free",
        extra_info="Handles deposits into the bank account. Returns confirmation message.",
        unit_test=False
    )
    def deposit(self, amount):
        """
        Deposits a specified amount into the account.

        Args:
            amount (float): The amount to deposit.

        Returns:
            str: A confirmation message including the new balance.

        Raises:
            ValueError: If the deposit amount is negative.

        Examples:
            >>> account = BankAccount("12345", "John Doe", 100.0)
            >>> account.deposit(50)
            'Deposit successful. New balance: 150.0'

            >>> account.deposit(-20)
            Traceback (most recent call last):
                ...
            ValueError: Deposit amount cannot be negative.
        """
        pass  # This will be dynamically implemented.

    @dynamic_function(
        # model="google/gemini-2.0-flash-exp:free",
        extra_info="Handles withdrawals from the bank account. Returns confirmation message.",
        unit_test=False
    )
    def withdraw(self, amount):
        """
        Withdraws a specified amount from the account.

        Args:
            amount (float): The amount to withdraw.

        Returns:
            str: A confirmation message including the new balance.

        Raises:
            ValueError: If the withdrawal amount exceeds the current balance.

        Examples:
            >>> account = BankAccount("12345", "John Doe", 100.0)
            >>> account.withdraw(50)
            'Withdrawal successful. New balance: 50.0'

            >>> account.withdraw(200)
            Traceback (most recent call last):
                ...
            ValueError: Insufficient funds. Current balance: 50.0
        """
        pass  # This will be dynamically implemented.

    @dynamic_function(
        # model="google/gemini-2.0-flash-exp:free",
        extra_info="Returns the current balance of the bank account.",
        unit_test=False
    )
    def get_balance(self):
        """
        Retrieves the current balance of the account.

        Returns:
            float: The current balance.

        Examples:
            >>> account = BankAccount("12345", "John Doe", 100.0)
            >>> account.get_balance()
            100.0
        """
        pass  # This will be dynamically implemented.

# Example Usage
if __name__ == "__main__":
    # Create a new bank account
    account = BankAccount("98765", "Alice Smith", 500.0)

    # Deposit funds
    print(account.deposit(200))

    # Withdraw funds
    print(account.withdraw(100))

    # Get current balance
    print(f"Current balance: {account.get_balance()}")

