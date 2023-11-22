from pathlib import Path
import os
from openpyxl import Workbook
from tkinter import filedialog

downloads_path = str(Path.home() / "Downloads")

test_paths = list({'internal/DataBase/james_cameron.jpg', 'internal/DataBase/arjun_chaudhary.jpg'})
students_found = []
all_students = []

for path in os.listdir("internal/DataBase"):
    fname = path[0: path.find("_")]
    lname = path[path.find("_") + 1: path.find('.')]
    all_students.append([fname, lname])

for i in test_paths:
    test_paths[test_paths.index(i)] = i.replace('internal/DataBase/', "")

for path in test_paths:
    fname = path[0: path.find("_")]
    lname = path[path.find("_") + 1: path.find('.')]
    students_found.append([fname, lname])

student_attendance = []

for student in all_students:
    if student in students_found:
        student_attendance.append([student, ["Present"]])
    else:
        student_attendance.append([student, ["Absent"]])


# mark attendance on xl sheet
workbook = Workbook()
sheet = workbook.active

sheet['A1'] = "First Name"
sheet['B1'] = "Last Name"
sheet['C1'] = "Attendance"

index = 2
for student in student_attendance:
    sheet['A{}'.format(index)] = student[0][0]
    sheet['B{}'.format(index)] = student[0][1]
    sheet['C{}'.format(index)] = student[1][0]

file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], initialfile="student_attendance_information")

# Check if the user selected a file
if file_path:
    # Save the workbook to the selected file path
    workbook.save(file_path)





