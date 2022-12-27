import gspread
import face_recognition
import numpy as np
import cv2
from PIL import Image, ImageDraw

sa = gspread.service_account(filename='service_account.json')
sh = sa.open("testing")
wks = sh.worksheet("Sheet1")


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


print(wks.get('b3'))
