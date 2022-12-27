import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import Label
from PIL import ImageTk, Image
import shutil
import os
import gspread
import face_recognition
import numpy as np
import cv2
from PIL import Image, ImageDraw

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

        self.activate_button = tk.Button(self.root, text="Activate Webcam", command=self.activate)
        self.activate_button.pack()

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
                                                                                                "/img/known/{}.jpg".format(
            self.textbox.get()))

    def activate(self):
        sa = gspread.service_account(filename='service_account.json')
        sh = sa.open("testing")
        wks = sh.worksheet("Sheet1")

        all_student_names = []
        all_student_images = []
        all_student_encodings = []

        # Reference to webcam
        video_capture = cv2.VideoCapture(1)

        # Variables for webcam
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True

        # Return spreadsheet position of given name
        def findName(name):
            count = wks.row_count
            for i in range(count):
                val = i + 1
                if val > 1:
                    # print((wks.get('A{}'.format(val))[0])[0])
                    if (wks.get('A{}'.format(val))[0])[0] == name:
                        return val

        # Mark empty spaces with absent
        def markAbsent():
            count = wks.row_count
            for i in range(count):
                val = i + 1
                if val > 1:
                    if not wks.get('B{}'.format(val)):
                        wks.update('B{}'.format(val), "Absent")

        # Grab list of all student names from spreadsheet
        for record in wks.get_all_records():
            all_student_names.append(record["Name"])

        # List of student encodings
        for student in all_student_names:
            student_image = face_recognition.load_image_file('./img/known/{}.jpg'.format(student))
            all_student_encodings.append(face_recognition.face_encodings(student_image)[0])
            all_student_images.append('./img/known/{}.jpg'.format(student))

        found_names = []

        while True:
            # Grab a single frame of video
            ret, frame = video_capture.read()

            # Only process every other frame of video to save time
            if process_this_frame:
                # keep frame of video full size for accurate processing
                small_frame = cv2.resize(frame, (0, 0), fx=1.00, fy=1.00)

                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_small_frame = small_frame[:, :, ::-1]

                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(all_student_encodings, face_encoding)
                    name = "Unknown"

                    # # If a match was found in known_face_encodings, just use the first one.
                    # if True in matches:
                    #     first_match_index = matches.index(True)
                    #     name = known_face_names[first_match_index]

                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(all_student_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = all_student_names[best_match_index]
                        if name != "Unknown":
                            if name not in found_names:
                                # print(name)
                                found_names.append(name)

            process_this_frame = not process_this_frame

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, found_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 1
                right *= 1
                bottom *= 1
                left *= 1

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Display the resulting image
            cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()

        # Mark found names as present
        for student in found_names:
            index = findName(student)
            print(student)
            wks.update('B{}'.format(index), "Present")
        markAbsent()





mygui = MyGui()