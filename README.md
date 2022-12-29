# AI_Attendance_Tracker
This program is meant to track attendance in a classroom using a webcam, images of students stored in an internal folder, and a google sheet provided with the names of all the students. The program will recognize students as they walk into the classroom on the webcam. When the user is finished, the program will update the google spreadsheet with all the students found and mark them as present. The ones that the program didn't find will be marked as absent

The facial recognition is a modified version of code from a public github repository: https://github.com/ageitgey/face_recognition

Spreadsheet: https://docs.google.com/spreadsheets/d/165smYMqEtrrebIX4v6ZuPbd3OBetcqCtQZ4XXdgQc4s/edit#gid=0
Make sure you have all the names of your students in the correct column and clear the present column before use for program to work correctly. It is best not to leave any extra rows and columns to avoid errors

