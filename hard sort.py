from collections import namedtuple

def custom_sort(students_list):
    return sorted(students_list, key=lambda student: -(len(student.name) + len(student.surname)))


Student = namedtuple('Student', ['name', 'surname'])


students = [
    Student(name='ghhjgyu', surname='guyybjug'),
    Student(name='hgy', surname='hgg'),
    Student(name='alex', surname='smith'),
    Student(name='anna', surname='johnson')
]

sorted_students = custom_sort(students)
for student in sorted_students:
    print(f"Name: {student.name}, Surname: {student.surname}")