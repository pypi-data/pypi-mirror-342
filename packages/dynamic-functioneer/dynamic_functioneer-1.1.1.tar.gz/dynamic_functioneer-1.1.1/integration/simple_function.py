# import sys
# print("Interactive shell sys.path:")
# for p in sys.path:
#     print(p)



# import sys
# print(sys.executable)


from dynamic_functioneer.dynamic_decorator import dynamic_function

@dynamic_function(
        # model="meta-llama/llama-3.3-70b-instruct:free",
        # model='claude-3-7-sonnet-latest',
        # model = 'crewai-sequential2-gemini-2.0-flash',
        model = 'crewai-sequential2-google/gemini-2.0-flash',
        # model = 'crewai-sequential2-claude-3-7-sonnet-latest',
        # error_model="mistralai/mistral-small-24b-instruct-2501:free",
        # model = 'crewai-sequential2-meta-llama/llama-3.3-70b-instruct:free',
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
