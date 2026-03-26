class Course:
    GRADE_POINTS = {
        "A+": 4.3, "A": 4.0, "A-": 3.7,
        "B+": 3.3, "B": 3.0, "B-": 2.7,
        "C+": 2.3, "C": 2.0, "C-": 1.7,
        "D": 1.0, "F": 0.0
    }

    def __init__(self, prefix: str, number: str, credits: int):
        self.prefix = prefix
        self.number = number
        self.credits = credits

        # Not graded by default.
        # Alternatively, one can use default parameter.
        self.grade = None

    def set_grade(self, grade: str):
        if self.grade is not None:
            raise ValueError("Course already graded.")
        if grade not in Course.GRADE_POINTS:
            raise ValueError("Invalid grade.")
        self.grade = grade

    def get_grade_point(self):
        if self.grade is None:
            return None
        return Course.GRADE_POINTS[self.grade]
    
    def get_code(self):
        """Return the compact course code like COMP1023"""
        return f"{self.prefix}{self.number}"


class Student:
    def __init__(self, student_id: str, name: str):
        self.student_id = student_id
        self.name = name
        self.courses = []

    def enroll(self, course: Course):
        for c in self.courses:
            if c.get_code() == course.get_code():
                print(f"ERROR! {self.name} is already enrolled in {course.get_code()}.")
                return
        self.courses.append(course)

    def grade(self, prefix: str, number: str, grade: str):
        for c in self.courses:
            if c.prefix == prefix and c.number == number:
                if c.grade is not None:
                    print(f"Error! {self.name}'s {c.get_code()} is already graded.")
                    return
                # The try-except block is out of the course syllabus
                try:
                    c.set_grade(grade)
                except ValueError as e:
                    print(f"Error! {e}")
                return
        print(f"Error! {self.name} is not enrolled in {prefix}{number}.")

    def calculate_cga(self):
        total_points = 0
        total_credits = 0
        for c in self.courses:
            gp = c.get_grade_point()
            if gp is not None:
                total_points += gp * c.credits
                total_credits += c.credits
        if total_credits == 0:
            return None
        return total_points / total_credits