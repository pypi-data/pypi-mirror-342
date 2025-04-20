from dynamic_functioneer.dynamic_decorator import dynamic_function

class TaskManager:
    """
    A class to represent a task management system.
    """

    def __init__(self):
        """
        Initializes the task manager with an empty task dictionary.
        """
        self.tasks = {}

    @dynamic_function(
        model="meta-llama/llama-3.2-3b-instruct:free",
        extra_info="Adds a new task with a given priority. Updates priority if the task already exists.",
        error_model="meta-llama/llama-3.2-3b-instruct:free"
    )
    def add_task(self, task_name, priority):
        """
        Adds or updates a task in the task list.

        Args:
            task_name (str): The name of the task.
            priority (int): The priority level of the task.

        Returns:
            str: Confirmation message about the added or updated task.
        """
        pass

    @dynamic_function(
        model="meta-llama/llama-3.2-3b-instruct:free",
        extra_info="Retrieves the priority of a given task. Raises an error if the task does not exist.",
        error_model="meta-llama/llama-3.2-3b-instruct:free"
    )
    def get_task_priority(self, task_name):
        """
        Retrieves the priority of a specified task.

        Args:
            task_name (str): The name of the task.

        Returns:
            int: The priority level of the task.

        Raises:
            KeyError: If the task does not exist.
        """
        pass


# Example Usage
if __name__ == "__main__":
    manager = TaskManager()

    # Add tasks
    print(manager.add_task("Finish report", 1))
    print(manager.add_task("Buy groceries", 2))

    # Update an existing task
    print(manager.add_task("Finish report", 3))

    # Retrieve task priorities
    print(manager.get_task_priority("Finish report"))  # Output: 3
    print(manager.get_task_priority("Buy groceries"))  # Output: 2

