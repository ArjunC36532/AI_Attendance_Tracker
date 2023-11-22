from deepface import DeepFace as DF
import cv2
import os
import shutil
import numpy
import time


class FaceRecog:
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

        self.time_elapsed = 0

        self.duration = None

        self.count = 0

    def clear_capture_directory(self):
        # Clear webcam captures folder
        for file in os.listdir("internal/Webcam_Captures"):
            os.remove(os.path.join("internal/Webcam_Captures", file))

    def take_snapshot(self, frame):
        flash = numpy.ones_like(frame) * 255
        cv2.imshow('Video', flash)
        cv2.waitKey(200)
        cv2.imwrite("internal/Frame/frame.jpg", frame)
        self.seperate_faces()

    def find_matches(self):
        # dfs = DeepFace.find(img_path="img1.jpg",
        #                     db_path="C:/workspace/my_db",
        #                     distance_metric=metrics[2]
        path_to_files_found = []
        for capture in os.listdir("internal/Webcam_Captures"):
            results = DF.find(img_path="internal/Webcam_Captures/{}".format(capture), db_path="internal/DataBase",
                              enforce_detection=False)
            paths = results[0]['identity'].tolist()
            for i in paths:
                path_to_files_found.append(i)
        try:
            os.remove("internal/DataBase/representations_vgg_face.pkl")
        except:
            pass

        return path_to_files_found

    def start_process(self, webcam_used, duration):
        self.duration = duration * 60
        self.clear_capture_directory()

        if webcam_used:
            self.video_capture = cv2.VideoCapture(1)
        else:
            self.video_capture = cv2.VideoCapture(0)

        run = True
        while run:
            ret, frame = self.video_capture.read()
            frame_with_text = cv2.putText(frame, str(self.count_down), self.coordinates, self.font, self.scale,
                                          self.BLACK, self.thickness, cv2.LINE_AA)
            frame_with_text_2 = cv2.putText(frame_with_text, "press q to quit", (10, 30), self.font, 0.5,
                                          (255, 0, 0), 1, cv2.LINE_AA)

            gray_scale_frame = cv2.cvtColor(frame_with_text_2, cv2.COLOR_BGR2GRAY)

            faces_detected = self.face_cascade.detectMultiScale(gray_scale_frame, 1.1, 4)

            for (x, y, w, h) in faces_detected:
                cv2.rectangle(frame_with_text_2, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.imshow('Video', frame_with_text_2)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                run = False

            if time.time() - self.last_time >= 1:
                self.count_down -= 1
                self.last_time = time.time()

            if self.count_down < 1:
                print('take a photo')
                self.take_snapshot(frame_with_text_2)
                self.count_down = 5
                self.time_elapsed += 5

            if self.time_elapsed >= self.duration:
                run = False

        self.video_capture.release()
        cv2.destroyAllWindows()

    def seperate_faces(self):
        # load frame
        frame = cv2.imread("internal/Frame/frame.jpg")

        # convert to grayscale
        gray_scale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect faces
        faces_detected = self.face_cascade.detectMultiScale(gray_scale_frame, 1.1, 4)

        for (x, y, w, h) in faces_detected:
            face = frame[y:y + h, x:x + w]  # slice the face from the image
            cv2.imwrite("internal/Webcam_Captures/{}.jpg".format(self.count), face)  # save the image
            self.count += 1
