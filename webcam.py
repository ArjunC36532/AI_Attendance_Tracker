import cv2
import sys
import time
import numpy
from face_recog import *
import threading

from datetime import datetime, time
import time


class Webcam:
    def __init__(self):
        self.video_capture = None
        self.count_down = 5
        self.coordinates = (580, 80)
        self.font = cv2.FONT_HERSHEY_COMPLEX
        self.BLACK = (0, 0, 0)
        self.scale = 3
        self.thickness = 2
        self.last_time = time.time()
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.face_recognition = FaceRecog()
        self.face_recognition.clear_capture_directory()
        self.time_elapsed = 0

        self.duration = None

    def take_snapshot(self, frame):
        flash = numpy.ones_like(frame) * 255
        cv2.imshow('Video', flash)
        cv2.waitKey(200)
        cv2.imwrite("internal/Frame/frame.jpg", frame)
        self.face_recognition.seperate_faces()

    def run(self, webcam_used=False):
        if webcam_used:
            self.video_capture = cv2.VideoCapture(1)
        else:
            self.video_capture = cv2.VideoCapture(0)

        run = True
        while run:
            ret, frame = self.video_capture.read()
            frame_with_text = cv2.putText(frame, str(self.count_down), self.coordinates, self.font, self.scale,
                                          self.BLACK, self.thickness, cv2.LINE_AA)

            gray_scale_frame = cv2.cvtColor(frame_with_text, cv2.COLOR_BGR2GRAY)

            faces_detected = self.face_cascade.detectMultiScale(gray_scale_frame, 1.1, 4)

            for (x, y, w, h) in faces_detected:
                cv2.rectangle(frame_with_text, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.imshow('Video', frame_with_text)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                run = False

            if time.time() - self.last_time >= 1:
                self.count_down -= 1
                self.last_time = time.time()

            if self.count_down < 1:
                print('take a photo')
                self.take_snapshot(frame_with_text)
                self.count_down = 5
                self.time_elapsed += 5

            if self.time_elapsed >= self.duration:
                run = False

        self.video_capture.release()
        cv2.destroyAllWindows()
