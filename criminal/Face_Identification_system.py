import os
import cv2
import face_recognition
from tkinter import Tk, Label, Button, filedialog, simpledialog
import mysql.connector
known_criminals_folder = "images"
known_encodings = []
known_names = []
flag = 0
# Required imports
from collections import deque
from datetime import time
import time
import numpy as np
import cv2
t=0
l=[]
name=''
class Parameters:
    def __init__(self):
        self.CLASSES = open("model/action_recognition_kinetics.txt"
                            ).read().strip().split("\n")
        self.ACTION_RESNET = 'model/resnet-34_kinetics.onnx'
#         self.VIDEO_PATH = None
        self.VIDEO_PATH = "test/example1.mp4"
        # SAMPLE_DURATION is maximum deque size
        self.SAMPLE_DURATION = 16
        self.SAMPLE_SIZE = 112


def load_known_criminals():
    for file_name in os.listdir(known_criminals_folder):
        image_path = os.path.join(known_criminals_folder, file_name)
        name = os.path.splitext(file_name)[0]
        image = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(image)[0]
        known_encodings.append(encoding)
        known_names.append(name)

def match_criminal():

    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            name = "Unknown"
            flag = 1
            if True in matches:
                matched_indices = [index for index, match in enumerate(matches) if match]
                first_match_index = matched_indices[0]
                name = known_names[first_match_index]
                flag = 0
            top, right, bottom, left = face_locations[0]
            cv2.rectangle(frame, (left, top), (right, bottom), (237, 255, 32), 2)
            if flag == 0:
                cv2.putText(frame, "Matched Criminal: "+name, (left-40, top - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (158, 49, 255), 2)
            else:
                cv2.putText(frame, "Not Matched", (left, top - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 37), 2)
            match_label.config(text="Matched Criminal: " + name)
        cv2.imshow('TechVidvan', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Initialise instance of Class Parameter
    param = Parameters()

    # A Double ended queue to store our frames captured and with time
    # old frames will pop
    # out of the deque
    captures = deque(maxlen=param.SAMPLE_DURATION)

    # load the human activity recognition model
    print("[INFO] loading human activity recognition model...")
    net = cv2.dnn.readNet(model=param.ACTION_RESNET)

    print("[INFO] accessing video stream...")
    # Take video file as input if given else turn on web-cam
    # So, the input should be mp4 file or live web-cam video
    vs = cv2.VideoCapture(0)
    t=0

    while True:
        # Loop over and read capture from the given video input
        (grabbed, capture) = vs.read()

        # break when no frame is grabbed (or end if the video)
        if not grabbed:
            print("[INFO] no capture read from stream - exiting")
            break

        # resize frame and append it to our deque
        capture = cv2.resize(capture, dsize=(550, 400))
        captures.append(capture)

        # Process further only when the deque is filled
        if len(captures) < param.SAMPLE_DURATION:
            continue

        # now that our captures array is filled we can
        # construct our image blob
        # We will use SAMPLE_SIZE as height and width for
        # modifying the captured frame
        imageBlob = cv2.dnn.blobFromImages(captures, 1.0,
                                           (param.SAMPLE_SIZE,
                                            param.SAMPLE_SIZE),
                                           (114.7748, 107.7354, 99.4750),
                                           swapRB=True, crop=True)

        # Manipulate the image blob to make it fit as as input
        # for the pre-trained OpenCV's
        # Human Action Recognition Model
        imageBlob = np.transpose(imageBlob, (1, 0, 2, 3))
        imageBlob = np.expand_dims(imageBlob, axis=0)

        # Forward pass through model to make prediction
        net.setInput(imageBlob)
        outputs = net.forward()
        # Index the maximum probability
        label = param.CLASSES[np.argmax(outputs)]

        # time.sleep(0.1)
        # Show the predicted activity
        cv2.rectangle(capture, (0, 0), (300, 40), (255, 255, 255), -1)
        cv2.putText(capture, label, (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0, 0, 0), 2)

        # Display it on the screen
        l.append(label)

        if label == 'sharpening knives':
            t += 1
            print(t)
            if t >=1:
                conn = mysql.connector.connect(user='root', password='', host='localhost', database='criminaldb')
                cursor = conn.cursor()
                cursor.execute("update criminalstatus set address='trichy',details='"+label+"'")
                conn.commit()
                conn.close()
        if label == 'beatboxing':
            t += 1
            print(t)
            if t >=1:
                conn = mysql.connector.connect(user='root', password='', host='localhost', database='criminaldb')
                cursor = conn.cursor()
                cursor.execute("update criminalstatus set address='trichy',details='"+label+"'")
                conn.commit()
                conn.close()
        if label == 'Fight':
            t += 1
            print(t)
            if t >= 1:
                conn = mysql.connector.connect(user='root', password='', host='localhost', database='criminaldb')
                cursor = conn.cursor()
                cursor.execute("update criminalstatus set address='trichy',details='"+label+"'")
                conn.commit()
                conn.close()
        if label == 'Fight':
            t += 1
            print(t)
            if t >= 1:
                conn = mysql.connector.connect(user='root', password='', host='localhost', database='criminaldb')
                cursor = conn.cursor()
                cursor.execute("update criminalstatus set address='trichy',details='"+label+"'")
                conn.commit()
                conn.close()
        if label == 'person with knife':
            t += 1
            print(t)
            if t >=1:
                conn = mysql.connector.connect(user='root', password='', host='localhost', database='criminaldb')
                cursor = conn.cursor()
                cursor.execute("update criminalstatus set address='trichy',details='"+label+"'")
                conn.commit()
                conn.close()


        cv2.imshow("Human Activity Recognition", capture)

        key = cv2.waitKey(1) & 0xFF
        # Press key 'q' to break the loop
        if key == ord("q"):
            break
    vs.release()
    cv2.destroyAllWindows()



def add_criminal():
    file_path = filedialog.askopenfilename(initialdir="/", title="Select Image",
                                           filetypes=(("Image Files", "*.jpg;*.jpeg;*.png"), ("All Files", "*.*")))
    if file_path:
        image = cv2.imread(file_path)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encoding = face_recognition.face_encodings(rgb_image)[0]
        name = simpledialog.askstring("Add Criminal", "Enter the name of the criminal:")
        if name:
            known_encodings.append(encoding)
            known_names.append(name)
            file_name = name + ".jpg"
            save_path = os.path.join(known_criminals_folder, file_name)
            cv2.imwrite(save_path, image)
            print("Criminal added successfully.")

load_known_criminals()

root = Tk()
root.title("Criminal Identification System")
root.geometry("500x300")

label = Label(root, text="Welcome to the Criminal Identification System")
label.pack()

match_button = Button(root, text="Match Criminal", command=match_criminal)
match_button.pack()

match_label = Label(root, text="Matched Criminal: ")
match_label.pack()

root.mainloop()
