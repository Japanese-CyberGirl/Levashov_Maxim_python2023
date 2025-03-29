from collections import namedtuple

def custom_sort(students_list):
    return sorted(students_list, key=lambda student: -(len(student.name) + len(student.surname)))

# Создаем namedtuple для хранения данных о студентах
Student = namedtuple('Student', ['name', 'surname'])

# Создаем список студентов
students = [
    Student(name='ghhjgyu', surname='guyybjug'),
    Student(name='hgy', surname='hgg'),
    Student(name='alex', surname='smith'),
    Student(name='anna', surname='johnson')
]

# Сортируем и выводим результат
sorted_students = custom_sort(students)
for student in sorted_students:
    print(f"Name: {student.name}, Surname: {student.surname}")