from dynamic_functioneer.dynamic_decorator import dynamic_function

@dynamic_function(
        unit_test=True,
    # model="meta-llama/llama-3.2-3b-instruct:free",
    # prompt="custom_prompt.txt",
    # hs_condition="len(numbers) > 1000",
    # execution_context={"frequent_inputs": [[], [1, 2, 3]]},
    # keep_ok_version=True
)
def calculate_average(numbers):
    """
    Calculates the average of a list of numbers.

    Args:
        numbers (list of float): A list of numeric values.

    Returns:
        float: The average of the list.
    """
    pass


print(calculate_average([1, 3, 7]))

# print(calculate_average([3.3]*2000))
