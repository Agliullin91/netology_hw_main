class Student:
    def __init__(self, name, surname, gender, *courses):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = courses
        self.grades = {}

    def rate_l(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            print('Ошибка')


class Mentor:
    def __init__(self, name, surname, *courses):
        self.name = name
        self.surname = surname
        self.courses_attached = courses


class Lecturer(Mentor):
    def __init__(self, name, surname, *courses):
        super().__init__(name, surname, *courses)
        self.grades = {}


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            print('Ошибка')


harry = Student('Harry', 'Potter', 'male', 'Python', 'C++')
katy = Student('Katy', 'Perry', 'female', 'html', 'Javascript')
gandalf = Lecturer('Gandalf', 'The Grey', 'Python', 'Javascript', 'html', 'C++')
rick = Lecturer('Rick', 'Sanchez', 'Python', 'C++', 'html')
tony = Reviewer('Tony', 'Stark', 'Python', 'html')

print()
harry.rate_l(gandalf, 'Python', 10)
print(f'Gandalf The Grey: {gandalf.grades}')
print(f'Rick Sanchez: {rick.grades}')
tony.rate_hw(katy, 'html', 8)
print(f'Katy Perry: {katy.grades}')
print(f'Harry Potter: {harry.grades}')
