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

import sys
import random
import json
from optparse import OptionParser


def generate_student_data(first_name, last_name, birth_date):
    return {
        'personal_info': {'first_name': first_name, 'last_name': last_name, 'birth_data': birth_date},
        'classes': {}
    }


def assign_student_to_class(data_dict, student_number, class_name):
    if student_number in data_dict:
        data_dict[student_number]['classes'][class_name] = {
            'grades': [],
            'attendance': {}
        }


def generate_student_number(data_dict):
    return str(int(max(data_dict, key=int))+1) if len(data_dict) > 0 else '1'


def save_data_to_json(data, path):
    with open(path, 'w') as f:
        json.dump(data, f)


def read_data_from_json(path):
    with open(path, 'r') as f:
        return json.load(f)


def add_grade_to_student(data_dict, student_number, class_name, grade):
    data_dict[student_number]['classes'][class_name]['grades'].append(grade)


def add_presence_to_student(data_dict, student_number, class_name, date, present):
    data_dict[student_number]['classes'][class_name]['attendance'][date] = present


def calculate_average_score_in_class(data_dict, student_number, class_name):
    grades = data_dict[student_number]['classes'][class_name]['grades']
    return float(sum(grades)) / len(grades) if len(grades) > 0 else 0.0


def calculate_average_score(data_dict, student_number):
    avg_scores = []
    for class_name in data_dict[student_number]['classes']:
        avg_scores.append(calculate_average_score_in_class(data_dict, student_number, class_name))
    return float(sum(avg_scores)) / len(avg_scores)


def count_total_attendance(data_dict, student_number):
    result = {'presences': 0, 'absences': 0}
    for class_name, class_data in data_dict[student_number]['classes'].iteritems():
        for date, present in class_data['attendance'].iteritems():
            key_to_increment = 'presences' if present else 'absences'
            result[key_to_increment] += 1
    return result


if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option('-s', '--simulation', dest='run_simulation', default=False, action="store_true", help='Specifies whether to run simulation or not')
    parser.add_option('-i', '--input', dest='input_path', type="string", help='Path to file from which data should be loaded. Used only if simulation is disabled')
    parser.add_option('-o', '--output', dest='output_path', type="string", help='Path to which results of the simulation will be saved. Used only if simulation is enabled')

    (options, args) = parser.parse_args()

    if options.run_simulation:

        print('\nSimulation:\n')

        students = dict()

        first_student_number = generate_student_number(students)
        students[first_student_number] = generate_student_data('Jan', 'Nowak', '19.02.2000')

        second_student_number = generate_student_number(students)
        students[second_student_number] = generate_student_data('Andrzej', 'Kowalski', '05.04.2000')

        first_class_name = 'First class'
        second_class_name = 'Second class'

        assign_student_to_class(students, first_student_number, first_class_name)
        assign_student_to_class(students, first_student_number, second_class_name)
        assign_student_to_class(students, second_student_number, first_class_name)
        assign_student_to_class(students, second_student_number, second_class_name)

        add_grade_to_student(students, first_student_number, first_class_name, random.randint(1, 5))
        add_grade_to_student(students, first_student_number, first_class_name, random.randint(1, 5))

        add_grade_to_student(students, first_student_number, second_class_name, random.randint(1, 5))
        add_grade_to_student(students, first_student_number, second_class_name, random.randint(1, 5))

        add_grade_to_student(students, second_student_number, first_class_name, random.randint(1, 5))
        add_grade_to_student(students, second_student_number, first_class_name, random.randint(1, 5))

        add_grade_to_student(students, second_student_number, second_class_name, random.randint(1, 5))
        add_grade_to_student(students, second_student_number, second_class_name, random.randint(1, 5))

        date = '12.11.2017'
        add_presence_to_student(students, first_student_number, first_class_name, date, random.choice([True, False]))
        add_presence_to_student(students, first_student_number, second_class_name, date, random.choice([True, False]))
        add_presence_to_student(students, second_student_number, first_class_name, date, random.choice([True, False]))
        add_presence_to_student(students, second_student_number, second_class_name, date, random.choice([True, False]))

        date = '21.11.2017'
        add_presence_to_student(students, first_student_number, first_class_name, date, random.choice([True, False]))
        add_presence_to_student(students, first_student_number, second_class_name, date, random.choice([True, False]))
        add_presence_to_student(students, second_student_number, first_class_name, date, random.choice([True, False]))
        add_presence_to_student(students, second_student_number, second_class_name, date, random.choice([True, False]))

        if options.output_path:
            save_data_to_json(students, options.output_path)
            print('Simulation data saved in: {}'.format(options.output_path))

    elif options.input_path:
        students = read_data_from_json(options.input_path)
        print('\nData from file {}\n'.format(options.input_path))

    else:
        print('Neither simulation nor input option provided')
        sys.exit()

    for student_number, data in students.iteritems():
        personal_info = data['personal_info']
        total_avg_score = calculate_average_score(students, student_number)
        student_classes = data['classes'].keys()
        class_name = student_classes[0] if len(student_classes) > 0 else None
        if class_name:
            avg_score_in_class = calculate_average_score_in_class(students, student_number, class_name)
        attendance = count_total_attendance(students, student_number)

        print('Student {}: {} {}'.format(student_number, personal_info['first_name'], personal_info['last_name']))
        print('Average score across classes: {}'.format(total_avg_score))
        if class_name:
            print('Average score in class "{}": {}'.format(class_name, avg_score_in_class))
        print('Total attendance: {}'.format(attendance))
        print('\n')
