from dynamic_functioneer.dynamic_decorator import dynamic_function

@dynamic_function(
    model="gpt-4o-mini",
    prompt=None,
    extra_info="Calculates the median of a list of numbers.",
    fix_dynamically=True,
    error_trials=2
)
def calculate_median(numbers):
    """
    Calculates the median of a list of numbers.

    The median is the value separating the higher half from the lower half
    of a data sample. If the list length is odd, the middle element is returned.
    If the list length is even, the average of the two middle elements is returned.

    Args:
        numbers (list of float): A list of numerical values.

    Returns:
        float: The median value of the list.

    Raises:
        ValueError: If the input list is empty.
    """
    pass

# Example Usage
if __name__ == "__main__":
    data = [5, 1, 8, 3, 9]
    print(f"The median of {data} is {calculate_median(data)}")
