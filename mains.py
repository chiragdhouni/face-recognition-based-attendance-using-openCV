import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime
cur_mode=0
frame=0
id=-1
bucket=storage.bucket()
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    "databaseURL":"https://faceattendance-2412f-default-rtdb.firebaseio.com/",
    "storageBucket":"faceattendance-2412f.appspot.com"
})

cam=cv2.VideoCapture(0)
cam.set(3,640)
cam.set(4,480)
background=cv2.imread("Resources/background.png")
Modes_path="Resources/Modes"
Modes_path_list=os.listdir(Modes_path)
Modes=[]
for path in Modes_path_list:
    Modes.append(cv2.imread(os.path.join(Modes_path,path)))

#loading the encoded_data
file=open("encoded_data.p","rb")
encoded_images_with_ids=pickle.load(file)
file.close()
encode_known_images,student_ids=encoded_images_with_ids
#print(studentids)


while True:
    success,img=cam.read()
    background[162:162 + 480, 55:55 + 640] = img
    background[44:44 + 633, 808:808 + 414] = Modes[cur_mode]
    cv2.imshow("background", background)
    cv2.waitKey(1)

    imgs = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)

    face_cur_frame=face_recognition.face_locations(imgs)
    encoded_current_frame=face_recognition.face_encodings(imgs,face_cur_frame)

    if face_cur_frame:
        for encode_face,face_frame in zip(encoded_current_frame,face_cur_frame):
            matches=face_recognition.compare_faces(encode_known_images,encode_face)
            distance=face_recognition.face_distance(encode_known_images,encode_face)
            print("matches",matches)
            print("facedis",distance)
            match_index=np.argmin(distance)
            if matches[match_index]:
                y1, x2, y2, x1 = face_frame
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                background = cvzone.cornerRect(background, bbox, rt=0)
                id =student_ids[match_index]
                print(id)
                cv2.imshow("face attendance", background)
                cv2.waitKey(1)

            if frame==0:
                cvzone.putTextRect(img,"Loading",(275,400))
                cv2.imshow("face attendance", background)
                cv2.waitKey(1)
                frame = 1
                modetype = 1
            if frame==1:
                #getting the data
                student_info=db.reference(f"Students/{id}").get()
                print(student_info)
                # get image from the storage
                # imgstudent=cv2.imdecode(array,cv2.COLOR_BGRS2BGR)
                # update data of attendance
                datetime_object=datetime.strptime(student_info["last_attendance_time"],
                "%Y-%m-%d %H:%M:%S")
                second_elapsed=(datetime.now()-datetime_object).total_seconds()
                print(second_elapsed)




    cv2.imshow("background", background)
    cv2.waitKey(1)