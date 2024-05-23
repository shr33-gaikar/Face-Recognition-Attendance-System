import cv2
import pickle
import os
import time
from datetime import datetime
from sklearn.neighbors import KNeighborsClassifier
import csv
from win32com.client import Dispatch

def speak(str1):
    speak = Dispatch(("SAPI.SpVoice"))
    speak.Speak(str1)

# Video capture
video = cv2.VideoCapture(0)

# Load face detection classifier and trained data
facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

# Load trained data
with open('data/names.pkl', 'rb') as w:
    LABELS = pickle.load(w)
with open('data/faces_data.pkl', 'rb') as f:
    FACES = pickle.load(f)

print('Shape of Faces matrix --> ', FACES.shape)

# Train KNN classifier
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

# Load background image
imgBackground = cv2.imread("bg.png")

# Define column names for CSV file
COL_NAMES = ['NAME', 'TIME']

while True:
    ret, frame = video.read()
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w, :]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
        output = knn.predict(resized_img)

        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")
        attendance_file = "Attendance/Attendance_" + date + ".csv"

        # Check if the directory exists, if not, create it
        attendance_dir = "Attendance"
        if not os.path.exists(attendance_dir):
            os.makedirs(attendance_dir)

        exist = os.path.isfile(attendance_file)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 2)
        cv2.rectangle(frame, (x, y-40), (x+w, y), (50, 50, 255), -1)
        cv2.putText(frame, str(output[0]), (x, y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
        attendance = [str(output[0]), str(timestamp)]

    # Update the background image
    imgBackground[162:162 + 480, 55:55 + 640] = frame
    cv2.imshow("Frame", imgBackground)
    k = cv2.waitKey(1)

    # Take attendance on pressing 'o' key
    if k == ord('o'):
        speak("Attendance Taken..")
        time.sleep(3)
        with open(attendance_file, "+a") as csvfile:
            writer = csv.writer(csvfile)
            if exist:
                writer.writerow(attendance)
            else:
                writer.writerow(COL_NAMES)
                writer.writerow(attendance)

    # Exit loop on pressing 'q' key
    if k == ord('q'):
        break

# Release video capture and close all windows
video.release()
cv2.destroyAllWindows()
