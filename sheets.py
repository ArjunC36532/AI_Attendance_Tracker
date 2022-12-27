import gspread
import face_recognition
from PIL import Image, ImageDraw

sa = gspread.service_account(filename='service_account.json')
sh = sa.open("testing")
wks = sh.worksheet("Sheet1")

# print("Rows:", wks.row_count)
# print("Cols", wks.col_count)
# print(wks.acell('A5').value)
# print(wks.get('A2:B5'))
# print(wks.update('B5', 'No'))

records = wks.get_all_records()

# # print(wks.get('A3')[0])
#
# count = wks.row_count
# for i in range(count):
#     val = i+1
#     if val>1:
#         # print((wks.get('A{}'.format(val))[0])[0])
#         if (wks.get('A{}'.format(val))[0])[0] == 'Steve Jobs':
#             print(val)

for record in wks.get_all_records():
    print(record["Name"])



