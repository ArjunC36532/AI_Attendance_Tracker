import gspread
import face_recognition
from PIL import Image, ImageDraw


# use internal files to track for attendance with given spreadsheet

sa = gspread.service_account(filename='service_account.json')
sh = sa.open("testing")
wks = sh.worksheet("Sheet1")
# print("Rows:", wks.row_count)
# print("Cols", wks.col_count)
# print(wks.acell('A5').value)
# print(wks.get('A2:B5'))
# print(wks.update('B5', 'No'))

image_of_bill = face_recognition.load_image_file('./img/known/Bill Gates.jpg')
bill_face_encoding = face_recognition.face_encodings(image_of_bill)[0]

image_of_steve = face_recognition.load_image_file('./img/known/Steve Jobs.jpg')
steve_face_encoding = face_recognition.face_encodings(image_of_steve)[0]

image_of_elon = face_recognition.load_image_file('./img/known/elon musk.jpg')
elon_face_encoding = face_recognition.face_encodings(image_of_elon)[0]

# Create array of encodings and names
known_face_encodings = [
    bill_face_encoding,
    steve_face_encoding,
    elon_face_encoding
]

known_face_names = [
    "Bill Gates",
    "Steve Jobs",
    "Elon Musk"
]


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


# Load class image
class_image = face_recognition.load_image_file('./img/groups/bill-steve-elon.jpg')

# Convert to PIL format
pil_image = Image.fromarray(class_image)

# Find faces in test image
face_locations = face_recognition.face_locations(class_image)
face_encodings = face_recognition.face_encodings(class_image, face_locations)

# Loop through faces
for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
    draw = ImageDraw.Draw(pil_image)
    name = "Unknown"
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

    if True in matches:
        first_match_index = matches.index(True)
        name = known_face_names[first_match_index]
        index = findName(name)
        wks.update('B{}'.format(index), "Present")

    draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 0))

    text_width, text_height = draw.textsize(name)
    draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 0), outline=(0, 0, 0))
    draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))

    del draw

markAbsent()
pil_image.show()
