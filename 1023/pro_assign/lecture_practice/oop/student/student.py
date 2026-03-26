'''
Create a student management system, involving:

A class Student.

Instance variables:
their student ID,
their name,
their courses (empty by default).

Methods:
Calculate the CGA of the student.
Enroll the student in a course.
Grade the student in a course.


A class Course.

Instance variables:
the course prefix (e.g., "COMP"),
the course number (e.g., "1023"),
the credits of the course (e.g., 3),
the grade of the student (e.g., A+, A), or None if not yet graded.
Your classes should support the following code snippet:
'''

'''
# Grade to Grade Points:
# A+ = 4.3, A = 4.0, A- = 3.7
# B+ = 3.3, B = 3.0, B- = 2.7
# C+ = 2.3, C = 2.0, C- = 1.7
# D = 1.0, F = 0.0
'''

to_score={'A':4.0,'B':3.0,'C':2.0}

class course:
    def __init__(self,course_name,number,credits,):
        self._course_name=course_name
        self._number=number
        self._credits=credits

class student:
    def __init__(self,stu_id,name):
        self._stu_id=stu_id
        self._name=name
        self._courses=[]
        #course will be a list of dictionarys,for each dictionary
        #key is course name, and value is a list containing score and credit
        #example like [{'math:[3.5,3]} , {'lang':[4.0,3]}]
    def __str__(self):
        return f'{self._name}'
    
    def calculate_cga(self):
        if not self._courses:
            print('no course yet')
            return
        total_score=0
        total_credits=0
        for course in self._courses:
            for val in course.values():
                score,credit=val
                if score and credit:
                    total_score+=score*credit
                    total_credits+=credit
        cga=total_score/total_credits
        print(cga)
        return cga if cga else None

    def grade(self,course_name,course_number,grade):
        complete=course_name+course_number
        #convert grade like a+ to point like 4.0
        point=to_score[grade]

        for course in self._courses:
            for key in course:
                if key==course_name:
                    score,_=course[key]
                    if score==None:
                        #update the dictionary
                        course[key][0]=point
                    else:
                        print(f'{course_name} is already graded')
                        return
        print(f"grade {self._name}'s {complete} to {grade}")

    def enroll(self,cor:course):
        for course in self._courses:
            if cor._course_name in course:
                print(f'{cor._course_name} course already exisits')
                return
        #score of a course is none initally
        #it will be changed once gradedd

        temp={}
        temp[cor._course_name]=[None,cor._credits]
        self._courses.append(temp)

        

s=student('wewe','1212')
print(s)