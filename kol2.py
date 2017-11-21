# Class diary  
#
# Create program for handling lesson scores.
# Use python to handle student (highscool) class scores, and attendance.
# Make it possible to:
# - Get students total average score (average across classes)
# - get students average score in class
# - hold students name and surname
# - Count total attendance of student
# The default interface for interaction should be python interpreter.
# Please, use your imagination and create more functionalities. 
# Your project should be able to handle entire school.
# If you have enough courage and time, try storing (reading/writing) 
# data in text files (YAML, JSON).
# If you have even more courage, try implementing user interface.

import random


class Student(object):
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


class ClassMember(Student):
    def __init__(self, student, number):
        super(ClassMember, self).__init__(student.first_name, student.last_name)
        self.number = number
        self.attendance = {}
        self.scores = []

    def __str__(self):
        return '{0}: {1} {2}'.format(self.number, self.first_name, self.last_name)

    def save_presence(self, date, presence):
        self.attendance[date] = presence

    def add_score(self, score):
        self.scores.append(score)

    def get_average_score(self):
        return float(sum(self.scores)) / len(self.scores)

    def get_scores(self):
        return self.scores

    def count_attendance(self):
        result = {
            'presences': 0,
            'absences': 0
        }
        for date_key, presence in self.attendance.iteritems():
            if presence:
                result['presences'] += 1
            else:
                result['absences'] += 1
        return result


class Class(object):
    def __init__(self, name):
        self.name = name
        self.students = []

    def add_student(self, student):
        class_member = ClassMember(student, self.generate_student_number())
        self.students.append(class_member)

    def generate_student_number(self):
        numbers = map(lambda s: s.number, self.students)
        return max(numbers) + 1 if len(numbers) > 0 else 1

    def save_presence(self, date, presence_dict):
        for student in self.students:
            student_presence = presence_dict[student.number] if student.number in presence_dict else False
            student.save_presence(date, student_presence)

    def get_students_average_score(self):
        average_scores = map(lambda st: st.get_average_score(), self.students)
        return float(sum(average_scores)) / len(average_scores)

    def get_students(self):
        return self.students

    def get_name(self):
        return self.name


def get_all_students_average_score(classes):
    all_students = []
    for class_object in classes:
        all_students = all_students + class_object.students
    average_scores = map(lambda s: s.get_average_score(), all_students)
    return float(sum(average_scores)) / len(average_scores)


def generate_random_presence_dict(students):
    presence_dict = {}
    for student in students:
        presence_dict[student.number] = random.choice([True, False])
    return presence_dict


if __name__ == '__main__':

    test_class = Class('test class')

    first_student = Student('Jan', 'Nowak')
    second_student = Student('Andrzej', 'Kowalski')
    third_student = Student('Jan', 'Kowalski')

    test_class.add_student(first_student)
    test_class.add_student(second_student)
    test_class.add_student(third_student)

    date = '2017-11-20'
    test_class.save_presence(date, generate_random_presence_dict(test_class.get_students()))

    date = '2017-11-21'
    test_class.save_presence(date, generate_random_presence_dict(test_class.get_students()))

    date = '2017-11-22'
    test_class.save_presence(date, generate_random_presence_dict(test_class.get_students()))

    for st in test_class.get_students():
        st.add_score(random.randint(1, 5))
        st.add_score(random.randint(1, 5))
        st.add_score(random.randint(1, 5))

    print('\nClass name: {}\n'.format(test_class.get_name()))

    for st in test_class.get_students():
        print(st)
        print('Attendance: {}'.format(st.count_attendance()))
        print('Scores: {}'.format(st.get_scores()))
        print('Average score: {}'.format(st.get_average_score()))
        print('\n')

    print('Class average score: {}'.format(test_class.get_students_average_score()))

