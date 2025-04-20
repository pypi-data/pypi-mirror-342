from dynamic_functioneer.dynamic_decorator import dynamic_function

class StudentGrades:
    """
    A class to manage student grades in a course.
    """

    def __init__(self):
        """
        Initializes the StudentGrades class with an empty dictionary for student records.
        """
        self.grades = {}

    @dynamic_function(
        # model="meta-llama/llama-3.2-1b-instruct:free",
        # model='claude-3-7-sonnet-latest',
        model='gemini-2.0-flash',
        extra_info="Adds or updates a student's grade for a specific course.",
        # error_model="chatgpt-4o-latest"
    )

    def add_grade(self, student_name, course_name, grade):
        """
        Adds or updates a student's grade for a specific course.

        Args:
            student_name (str): The name of the student.
            course_name (str): The name of the course.
            grade (float): The grade to assign to the student for the course.

        Returns:
            str: Confirmation message about the added or updated grade.

        Examples:
            >>> grades = StudentGrades()
            >>> grades.add_grade("Alice", "Math", 95.0)
            'Added grade for Alice in Math with grade 95.0'

            >>> grades.add_grade("Alice", "Math", 98.0)
            'Updated grade for Alice in Math to 98.0'

            >>> grades.grades
            {'Alice': {'Math': 98.0}}
        """

        pass


    @dynamic_function(
        model="gpt-4o-mini",
        extra_info="Retrieves the grade for a student in a specific course. Raises an error if the student or course is not found.",
        error_model="chatgpt-4o-latest"
    )

    def get_grade(self, student_name, course_name):
        """
        Retrieves the grade for a specific course.

        Args:
            student_name (str): The name of the student.
            course_name (str): The name of the course.

        Returns:
            float: The grade for the course.

        Raises:
            KeyError: If the student or course does not exist.

        Examples:
            >>> grades = StudentGrades()
            >>> grades.add_grade("Alice", "Math", 95.0)
            >>> grades.get_grade("Alice", "Math")
            95.0

            >>> grades.get_grade("Bob", "Math")
            Traceback (most recent call last):
                ...
            KeyError: "Student 'Bob' not found."

            >>> grades.get_grade("Alice", "Science")
            Traceback (most recent call last):
                ...
            KeyError: "Course 'Science' not found for student 'Alice'."
        """

        pass


# Example Usage
if __name__ == "__main__":
    grades = StudentGrades()

    # Add grades
    print(grades.add_grade("Alice", "Math", 95.0))
    print(grades.add_grade("Bob", "Math", 88.5))
    print(grades.add_grade("Alice", "Science", 89.0))

    # # Update a grade
    print(grades.add_grade("Alice", "Math", 98.0))  # Should update the Math grade for Alice

    # # Retrieve grades
    print(f"Alice's Math grade: {grades.get_grade('Alice', 'Math')}")  # Output: 98.0
    print(f"Bob's Math grade: {grades.get_grade('Bob', 'Math')}")      # Output: 88.5
    print(f"Alice's Science grade: {grades.get_grade('Alice', 'Science')}")  # Output: 89.0