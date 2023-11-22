import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import PIL.Image
import os
from tktimepicker import AnalogPicker, AnalogThemes
from tkinter.messagebox import askyesno
from tkinter import *
from webcam import *
from pathlib import Path
from openpyxl import Workbook
from tkinter import messagebox

# create main home screen
root = tk.Tk()
root.title("Attendance Tracker")
root.geometry('500x500')


class AddStudent:
    def __init__(self):
        self.window = tk.Toplevel(root)

        # center window
        self.window.geometry('300x400')

        self.window.title('Add Student')
        self.student_first_name = None
        self.student_last_name = None

        self.student_first_name_box = tk.Entry(self.window, )
        self.student_last_name_box = tk.Entry(self.window)

        self.fname_label = tk.Label(self.window, text="First Name")
        self.lname_label = tk.Label(self.window, text="Last Name")

        self.upload_button = tk.Button(self.window, text="upload student portrait", command=self.open_image)
        self.picture_show_label = tk.Label(self.window)

        self.add_student_button = tk.Button(self.window, text="Add Student to Database", command=self.add_student)

        # put elements onto screen
        self.fname_label.pack()
        self.student_first_name_box.pack(pady=10)
        self.lname_label.pack()
        self.student_last_name_box.pack(pady=10)
        self.upload_button.pack(pady=10)
        self.picture_show_label.pack(pady=10)
        self.add_student_button.pack(pady=10)

    def get_text(self):
        self.student_first_name = self.student_first_name_box.get()
        self.student_last_name = self.student_last_name_box.get()

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if file_path:
            image = PIL.Image.open(file_path)
            image.thumbnail((100, 100))  # Resize the image to a small portrait
            self.photo = ImageTk.PhotoImage(image)
            self.picture_show_label.config(image=self.photo)

            self.student_image = image

        self.student_image = image

    def add_student(self):
        try:
            # save student img into database as student_name
            self.get_text()
            self.student_image.save(
                "internal/DataBase/{}_{}.jpg".format(self.student_first_name.lower(), self.student_last_name.lower()),
                "JPEG")
            # self.student_image.save("internal/DataBase/{}_{}".format(self.student_first_name, self.student_last_name))
            self.window.destroy()
        except:
            pass


class MyStudents:
    def __init__(self):
        self.window = tk.Toplevel(root)
        self.student_names = []
        self.get_student_names()
        self.names_grid = ttk.Treeview(self.window, columns=('First Name', 'Last Name'), show='headings')
        self.setup_grid()
        self.window.geometry('500x300')
        self.names_grid.pack()

    def get_student_names(self):
        # extract student names from database files
        for path in os.listdir("internal/DataBase"):
            fname = path[0: path.find("_")]
            lname = path[path.find("_") + 1: path.find('.')]
            self.student_names.append([fname, lname])

    def setup_grid(self):
        self.names_grid.heading('First Name', text='First Name')
        self.names_grid.heading('Last Name', text='Last Name')
        for student in self.student_names:
            self.names_grid.insert('', 'end', values=(student[0], student[1]))


class RemoveStudents:
    def __init__(self):
        self.window = tk.Toplevel(root)
        self.student_names = []
        self.get_student_names()
        self.window.geometry('300x300')

        self.student_first_name_box = tk.Entry(self.window)
        self.student_last_name_box = tk.Entry(self.window)

        self.fname_label = tk.Label(self.window, text="First Name")
        self.lname_label = tk.Label(self.window, text="Last Name")

        self.student_first_name, self.student_last_name = None, None

        self.remove_button = tk.Button(self.window, text="Remove Student", command=self.remove_student)

        # put elements onto screen
        self.fname_label.pack()
        self.student_first_name_box.pack(pady=10)
        self.lname_label.pack()
        self.student_last_name_box.pack(pady=10)
        self.remove_button.pack(pady=10)

    def get_student_names(self):
        # extract student names from database files
        for path in os.listdir("internal/DataBase"):
            fname = path[0: path.find("_")]
            lname = path[path.find("_") + 1: path.find('.')]
            self.student_names.append([fname, lname])

    def get_text(self):
        # get student names from input boxes
        self.student_first_name = self.student_first_name_box.get()
        self.student_last_name = self.student_last_name_box.get()

    def remove_student(self):
        # get entered name
        self.get_text()
        # remove student from database, check for invalid name
        try:
            os.remove(
                "internal/DataBase/{}_{}.jpg".format(self.student_first_name.lower(), self.student_last_name.lower()))
            self.window.destroy()
        except:
            # change later
            print('invalid name')


class Start:
    def __init__(self):
        self.cam = None
        self.run = True

        self.window = tk.Toplevel(root)
        self.window.geometry('300x100')

        self.label = Label(self.window, text="Time Duration (Minutes) ")

        self.duration_scale = Scale(self.window, from_=1, to=10, orient=HORIZONTAL)
        self.start_button = tk.Button(self.window, text="Start Attendance-Tracking", command=self.confirm_webcam)

        self.label.pack()
        self.duration_scale.pack()
        self.start_button.pack()

        self.face_AI = FaceRecog()

    def confirm_webcam(self):
        confirmation = askyesno(title="Webcam",
                                message="Would you like to use an external webcam if connected to your laptop?")
        try:
            if confirmation:
                self.face_AI.start_process(True, self.duration_scale.get())
            else:
                self.face_AI.start_process(False, self.duration_scale.get())
        except:
            messagebox.showerror("Error", "Webcam Error")

        # get paths of student faces detected, remove duplicates
        all_students_found_paths = self.face_AI.find_matches()
        paths_cleaned = list(set(all_students_found_paths))
        students_found = []

        # create list of student names detected from camera
        # add to spreadsheet
        for i in paths_cleaned:
            paths_cleaned[paths_cleaned.index(i)] = i.replace('internal/DataBase/', "")

        for path in paths_cleaned:
            fname = path[0: path.find("_")]
            lname = path[path.find("_") + 1: path.find('.')]
            students_found.append([fname, lname])

        self.generate_spreadsheet(students_found)

    def generate_spreadsheet(self, students_found):
        # get list of all students in database
        all_students = []
        for path in os.listdir("internal/DataBase"):
            fname = path[0: path.find("_")]
            lname = path[path.find("_") + 1: path.find('.')]
            all_students.append([fname, lname])

        # list of student attendance
        student_attendance = []
        for student in all_students:
            if student in students_found:
                student_attendance.append([student, ["Present"]])
            else:
                student_attendance.append([student, ["Absent"]])

        # generate spreadsheet and save
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

            index += 1

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")],
                                                 initialfile="student_attendance_information")

        # Check if the user selected a file
        if file_path:
            # Save the workbook to the selected file path
            workbook.save(file_path)


def create_add_student_window():
    addStudent = AddStudent()


def create_my_students_window():
    myStudents = MyStudents()


def create_remove_students_window():
    removeStudents = RemoveStudents()


def create_start_window():
    start = Start()


add_student_button = tk.Button(root, text="Add Student", width=500, command=create_add_student_window)
my_students_button = tk.Button(root, text="My Students", width=500, command=create_my_students_window)
remove_student_button = tk.Button(root, text="Remove Student", width=500, command=create_remove_students_window)
start_button = tk.Button(root, text="Start", width=500, command=create_start_window)
attendance_button = tk.Button(root, text="Attendance", width=500)

my_students_button.pack(pady=50)
add_student_button.pack(pady=50)
remove_student_button.pack(pady=50)
start_button.pack(pady=50)

root.mainloop()
