def calculate_average(numbers):
    """
    Calculates the average of a list of numbers.

    Args:
        numbers (list): A list of numeric values (int or float).

    Returns:
        float: The average of the list. Returns 0.0 if the list is empty.

    Raises:
        TypeError: If the input is not a list or contains non-numeric values.
        ValueError: If the list is empty but the function is not designed to return 0.0.
    """

    # Validate the input type to ensure it is a list
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list.")

    # Ensure all elements in the list are numeric
    for index, x in enumerate(numbers):
        if not isinstance(x, (int, float)):
            raise TypeError(f"Element at index {index} is not numeric: {x}")

    # Return 0.0 for an empty list to avoid division by zero
    if not numbers:  # More Pythonic way to check for an empty list
        return 0.0

    # Calculate and return the average by summing the list and dividing by its length
    average = sum(numbers) / len(numbers)
    return average