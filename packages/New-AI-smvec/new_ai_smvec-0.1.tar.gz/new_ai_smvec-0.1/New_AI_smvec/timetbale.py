import random

# Step 1: Define classes
class Teacher:
    def __init__(self, name):
        self.name = name

class Subject:
    def __init__(self, name):
        self.name = name

# Step 3: Generate time table
def generate_time_table(teachers, subjects, classrooms_available):
    timetable = []
    slots = ["9AM-10AM", "10AM-11AM", "11AM-12PM", "1PM-2PM", "2PM-3PM"]

    for i in range(min(len(teachers), len(subjects), len(slots))):
        entry = {
            "Slot": slots[i],
            "Teacher": teachers[i].name,
            "Subject": subjects[i].name,
            "Classroom": classrooms_available[i % len(classrooms_available)]
        }
        timetable.append(entry)

    return timetable

# Step 4: Main function
def main():
    teachers = []
    subjects = []
    classrooms = []

    print("Enter number of entries:")
    n = int(input("How many teachers/subjects/classrooms? "))

    for i in range(n):
        t_name = input(f"Enter name of Teacher {i+1}: ")
        s_name = input(f"Enter Subject for {t_name}: ")
        c_room = input(f"Enter Classroom availability for {t_name}: ")

        teachers.append(Teacher(t_name))
        subjects.append(Subject(s_name))
        classrooms.append(c_room)

    timetable = generate_time_table(teachers, subjects, classrooms)

    print("\n📅 Generated Time Table:")
    for entry in timetable:
        print(f"{entry['Slot']} - {entry['Teacher']} teaches {entry['Subject']} in {entry['Classroom']}")

main()
