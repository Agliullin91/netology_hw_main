from typing import Any, Union


class Human:
    def __init__(self, name, surname, gender=None, age=None):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.age = age

    def _avr_grade(self, person):
        grades_list = []
        for item in person.grades.values():
            for element in item:
                grades_list.append(element)
        if len(grades_list) == 0:
            return 0
        else:
            avr = sum(grades_list) / len(grades_list)
        return avr


class Student(Human):
    student_list = []

    def __init__(self, name, surname, gender, *courses):
        super().__init__(name, surname, gender)
        self.finished_courses = []
        self.courses_in_progress = courses
        self.grades = {}
        self.student_list += [self]

    def rate_l(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            print('Ошибка')

    def __str__(self):
        result = f'Имя: {self.name}\nФамилия: {self.surname}\n' \
                 f'Средняя оценка за ДЗ: {round(super()._avr_grade(self), 2)}\n' \
                 f'Курсы в процессе изучения: {self.courses_in_progress}\nЗавершенные курсы: {self.finished_courses}'
        return result

    def __lt__(self, other):
        if not isinstance(other, Student):
            return 'Ошибка'
        else:
            return super()._avr_grade(self) < super()._avr_grade(other)

    def avr_course_grade(course):
        course_grade_list = []
        for item in Student.student_list:
            if course in item.grades.keys():
                course_grade_list += item.grades.get(course)
            else:
                pass
        if len(course_grade_list) == 0:
            return f'{course}: Nobody has any rating on this course.'
        else:
            avr = sum(course_grade_list) / len(course_grade_list)
            return f'{course}: {round(avr, 2)}'

    def kak(self):
        print(f'hui eto {self.surname}')

    def vottak(self):
        self.kak()

    def avottak(self):
        Student.kak()

class Mentor(Human):
    def __init__(self, name, surname, *courses):
        super().__init__(name, surname)
        self.courses_attached = courses


class Lecturer(Mentor):
    lecturers_list = []

    def __init__(self, name, surname, *courses):
        super().__init__(name, surname, *courses)
        self.grades = {}
        self.lecturers_list += [self]

    def __str__(self):
        result = f'Имя: {self.name}\nФамилия: {self.surname}\n' \
                 f'Средняя оценка за лекции: {round(super()._avr_grade(self), 2)}'
        return result

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return 'Ошибка'
        else:
            return super()._avr_grade(self) < super()._avr_grade(other)

    def avr_course_grade(course):
        course_grade_list = []
        for item in Lecturer.lecturers_list:
            if course in item.grades.keys():
                course_grade_list += item.grades.get(course)
            else:
                pass
        if len(course_grade_list) == 0:
            return f'{course}: Nobody has any rating on this course.'
        else:
            avr = sum(course_grade_list) / len(course_grade_list)
            return f'{course}: {round(avr, 2)}'


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            print('Ошибка')

    def __str__(self):
        result = f'Имя: {self.name}\nФамилия: {self.surname}'
        return result


# Блок создания объектов
harry = Student('Harry', 'Potter', 'male', 'Python', 'C++')
katy = Student('Katy', 'Perry', 'female', 'html', 'Javascript')
gandalf = Lecturer('Gandalf', 'The Grey', 'Python', 'Javascript', 'html', 'C++')
rick = Lecturer('Rick', 'Sanchez', 'Python', 'C++', 'html')
tony = Reviewer('Tony', 'Stark', 'Python', 'html')
bruce = Reviewer('Bruce', 'Wayne', 'html', 'C++')
# Блок проверки: Задачи №1 и №2
print()
harry.rate_l(gandalf, 'Python', 10)
harry.rate_l(gandalf, 'C++', 7)
harry.rate_l(gandalf, 'C++', 9)
print(f'Gandalf The Grey: {gandalf.grades}')
print(f'Rick Sanchez: {rick.grades}')
tony.rate_hw(katy, 'html', 8)
tony.rate_hw(katy, 'html', 10)
tony.rate_hw(katy, 'html', 7)
print(f'Katy Perry: {katy.grades}')
print(f'Harry Potter: {harry.grades}')
# Блок проверки: Задача №3
print()
print(tony)
print()
print(gandalf)
print()
katy.finished_courses = 'Введение в программирование'
print(katy)
print()
print(harry)
print()
print(f'Katy Perry > Harry Potter: {katy > harry}')
print(f'Katy Perry < Harry Potter: {katy < harry}')
print()
print(f'Gandalf The Grey > Rick Sanchez: {gandalf > rick}')
print(f'Rick Sanchez < Gandalf The Grey: {rick < gandalf}')
# Блок проверки: Задача №4
print()
print(Student.avr_course_grade('html'))
print(Student.avr_course_grade('Python'))
print(Student.avr_course_grade('Javascript'))
print()
print(Lecturer.avr_course_grade('html'))
print(Lecturer.avr_course_grade('Python'))
print(Lecturer.avr_course_grade('C++'))
print()
katy.vottak()
harry.avottak()