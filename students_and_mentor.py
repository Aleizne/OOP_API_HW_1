class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress\
                and course in lecturer.courses_attached:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def avr_grades(self, course=None):
        if course is None:
            res = sum(self.grades.values(), [])
            res = sum(res) / len(res)
        elif isinstance(course, str) and course in self.courses_in_progress:
            res = sum(self.grades[course]) / len(self.grades[course])
        else:
            res = "Ошибка"
        return round(res, 2)

    def __str__(self):
        res = f'Имя: {self.name} \nФамилия: {self.surname}\nСредняя оценка за домашние задания: {self.avr_grades()}' \
              f'\nКурсы в процессе изучения: {", ".join(self.courses_in_progress)}' \
              f'\nЗавершенные курсы: {", ".join(self.finished_courses)}'
        return res

    def __lt__(self, other, course=None):

        return self.avr_grades(course) < other.avr_grades(course)


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        res = f'Имя: {self.name} \nФамилия: {self.surname}'
        return res


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def avr_grades(self, course=None):
        if course is None:
            res = sum(self.grades.values(), [])
            res = sum(res) / len(res)
        elif isinstance(course, str) and course in self.courses_attached:
            res = sum(self.grades[course]) / len(self.grades[course])
        else:
            res = "Ошибка"
        return round(res, 2)

    def __str__(self):
        res = f'Имя: {self.name} \nФамилия: {self.surname}\nСредняя оценка за лекции: {self.avr_grades()}'
        return res

    def __lt__(self, other, course=None):
        return self.avr_grades(course) < other.avr_grades(course)


# Создаем студентов

best_student = Student('Ruoy', 'Eman', 'your_gender')
best_student.courses_in_progress += ['Python']
best_student.courses_in_progress += ['GIT']
best_student.finished_courses += ['Введение в программирование']

bestest_student = Student('Xio', 'Volkof', 'AI')
bestest_student.courses_in_progress = ['Python', 'GIT']
bestest_student.finished_courses += ['Человеческая коммуникация для элементарных']

# Создаем "Проверяющего"
mega_reviewer = Reviewer('Pyton', 'Buddy')
mega_reviewer.courses_attached += ['Python']
mega_reviewer.courses_attached += ['GIT']

# Cоздаем лектора
guru_lectorer = Lecturer('Just', 'Guru')
guru_lectorer.courses_attached = ['Python', 'GIT', 'HumanMind для инфузорий-винтиков']

# Выставляем оценки
mega_reviewer.rate_hw(best_student, 'Python', 10)
mega_reviewer.rate_hw(best_student, 'Python', 9)
mega_reviewer.rate_hw(best_student, 'Python', 10)
mega_reviewer.rate_hw(best_student, 'GIT', 10)
mega_reviewer.rate_hw(best_student, 'GIT', 9)

mega_reviewer.rate_hw(bestest_student, 'Python', 8)
mega_reviewer.rate_hw(bestest_student, 'Python', 9)
mega_reviewer.rate_hw(bestest_student, 'GIT', 10)
mega_reviewer.rate_hw(bestest_student, 'GIT', 10)

best_student.rate_lecture(guru_lectorer, 'Python', 10)
best_student.rate_lecture(guru_lectorer, 'Python', 8)
best_student.rate_lecture(guru_lectorer, 'Python', 10)
bestest_student.rate_lecture(guru_lectorer, 'Python', 9)
bestest_student.rate_lecture(guru_lectorer, 'Python', 10)

best_student.rate_lecture(guru_lectorer, 'GIT', 8)
best_student.rate_lecture(guru_lectorer, 'GIT', 10)
bestest_student.rate_lecture(guru_lectorer, 'GIT', 10)
bestest_student.rate_lecture(guru_lectorer, 'GIT', 10)

# пробуем
print(best_student)
print(bestest_student)
print(guru_lectorer)
print(mega_reviewer)

# тут можно протестировать protected метод:
# print(guru_lectorer.avr_grades())
# print(f'А теперь по Python: {guru_lectorer.avr_grades("Python")}')

print("---Сравнения---")
print(f'Ryan учится лучше чем Xio? {best_student < bestest_student}')
print(f'А оценки Хio и Just Guru как в сравнении (по Python)? {bestest_student.__lt__(guru_lectorer, "Python")}')

# Можно проверить:
# print(f'Xio по Python: {bestest_student.avr_grades("Python")}')
# print(f'Guru по Python: {guru_lectorer.avr_grades("Python")}')


print("---Функции, списки и среднее---")

studets_list = [bestest_student, best_student]
lectorer_list = [guru_lectorer]

# Здесь я НАМЕРЕННО пересчитываю среднию по оценкам.
# Если взять за основу метод из классов - будет "средняя средних" (что нельзя), т.к. кол-во отметок может отличаться


def averege_calc(target_list, course=None):
    res = 0
    marks_counter = 0
    if course is None:
        for single_target in target_list:
            for values in single_target.grades.values():
                res += sum(values)
                marks_counter += len(values)
        return round(res / marks_counter, 2)
    elif isinstance(course, str):
        for element in target_list:
            if course not in element.grades.keys():
                continue
            res += sum(element.grades[course])
            marks_counter += len(element.grades[course])
        if marks_counter == 0:
            print("Нет необходимых элементов в списке")
            return
        res = round(res / marks_counter, 2)
        return round(res, 2)
    else:
        print("Ошибка!")
        return


print(f'Средняя по Python для студентов: {averege_calc(studets_list, "Python")}')
print(f'Средняя для студентов: {averege_calc(studets_list)}')

print(f'Средняя по Python для преподавателей: {averege_calc(lectorer_list, "Python")}')
print(f'Средняя для преподавателей: {averege_calc(lectorer_list)}')
