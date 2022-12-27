import gspread
import face_recognition
from PIL import Image, ImageDraw

sa = gspread.service_account(filename='service_account.json')
sh = sa.open("testing")
wks = sh.worksheet("Sheet1")

all_student_names = []
all_student_photos = []
all_student_encodings = []

class_image = face_recognition.load_image_file('./img/groups/bill-steve.jpg')
class_image_encoding = face_recognition.face_encodings(class_image)

class_image_face_locations = face_recognition.face_locations(class_image)
class_image_face_encodings = face_recognition.face_encodings(class_image, class_image_face_locations)


def findName(name):
    count = wks.row_count
    for i in range(count):
        val = i + 1
        if val > 1:
            # print((wks.get('A{}'.format(val))[0])[0])
            if (wks.get('A{}'.format(val))[0])[0] == name:
                return val


def markAbsent():
    count = wks.row_count
    for i in range(count):
        val = i + 1
        if val > 1:
            if not wks.get('B{}'.format(val)):
                wks.update('B{}'.format(val), "Absent")


# track attendance with given sheet
# use list of names to identify names instead of file-names

# Grab list of all student names from spreadsheet
for record in wks.get_all_records():
    all_student_names.append(record["Name"])

# List of student encodings
for student in all_student_names:
    student_image = face_recognition.load_image_file('./img/known/{}.jpg'.format(student))
    all_student_encodings.append(face_recognition.face_encodings(student_image)[0])
    all_student_photos.append('./img/known/{}.jpg'.format(student))

# Check attendance photo and create list of all found photo


for student in all_student_names:
    encoding = all_student_encodings[all_student_names.index(student)]
    compare = face_recognition.compare_faces(encoding, class_image_face_encodings)
    if True in compare:
        index = findName(student)
        wks.update('B{}'.format(index), "Present")

markAbsent()
