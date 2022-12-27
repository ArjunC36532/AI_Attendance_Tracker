import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import Label
from PIL import ImageTk, Image
import shutil
import os


class MyGui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('600x600')

        self.label = tk.Label(self.root, text='Add Student', font=('Arial', 14))
        # self.label.grid(row=0, column=1, padx=300)
        self.label.pack()

        self.textbox = tk.Entry(self.root, width=200, font=('Arial', 12))
        self.textbox.insert(END, 'Enter students full name, this should be the same name on the spreadsheet')
        # self.textbox.grid(row=1, column=1, columnspan=2)
        self.textbox.pack()

        self.image_button = tk.Button(self.root, text="Student Image", command=self.file_viewer)
        # self.image_button.grid(row=1, column=2)
        self.image_button.pack()

        self.root.mainloop()

    def file_viewer(self):
        self.root.file_name = filedialog.askopenfilename(initialdir='Downloads', title="Selected Student Image")
        student_image = ImageTk.PhotoImage(Image.open(self.root.file_name))
        student_image_label = Label(image=student_image)
        student_image_label.pack()
        print(os.path.split(self.root.file_name))
        breakup = os.path.split(self.root.file_name)
        name = breakup[1]
        shutil.copy(self.root.file_name, r"C:/Users/s00rm/Desktop/Python/Attendance_Tracker/img/known")
        os.rename("C:/Users/s00rm/Desktop/Python/Attendance_Tracker/img/known/{}".format(name), "C:/Users/s00rm/Desktop"
                                                                                                "/Python/Attendance_Tracker"
                                                                                                "/img/known/{}.jpeg".format(
            self.textbox.get()))


mygui = MyGui()
