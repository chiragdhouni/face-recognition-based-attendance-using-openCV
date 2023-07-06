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




cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    "databaseURL":"https://faceattendance-2412f-default-rtdb.firebaseio.com/",
    "storageBucket":"faceattendance-2412f.appspot.com"
})

bucket=storage.bucket()

cap=cv2.VideoCapture(0)
background=cv2.imread("Resources/background.png")
cap.set(3,640)
cap.set(4,480)
foldermodepath="Resources/Modes"
modespathlist=os.listdir(foldermodepath)
imgmodelist=[]
for path in modespathlist:
    imgmodelist.append(cv2.imread(os.path.join(foldermodepath,path)))
#print(len(imgmodelist))

#loading the encoded file
file=open("encoded_file.p","rb")
encodelistknownwithids=pickle.load(file)
file.close()
encodelistknown,studentids=encodelistknownwithids
#print(studentids)

modetype=0
frame=0
id=-1
imgstudent=[]

while True:
    success,img=cap.read()

    imgs=cv2.resize(img,(0,0),None,0.25,0.25)
    imgs=cv2.cvtColor(imgs,cv2.COLOR_BGR2RGB)

    #cv2.imshow("webcam" ,img)
    facecurframe=face_recognition.face_locations(imgs)
    encodecurframe=face_recognition.face_encodings(imgs,facecurframe)

    background[162:162 + 480, 55:55 + 640] = img
    background[44:44 + 633, 808:808 + 414] = imgmodelist[modetype]

    if facecurframe:
        for encodeface ,faceloc in zip(encodecurframe,facecurframe):
            matches=face_recognition.compare_faces(encodelistknown,encodeface)
            facedis=face_recognition.face_distance(encodelistknown,encodeface)
            #print("matches",matches)
            #print("facedis",facedis)
            matchindex=np.argmin(facedis)
            print("match index",matchindex)
            if matches[matchindex]:
               # print("known face detected")
                y1,x2,y2,x1=faceloc
                y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
                bbox=55+x1,162+y1,x2-x1,y2-y1
                background=cvzone.cornerRect(background,bbox,rt=0)
                id=studentids[matchindex]
                if frame==0:
                    cvzone.putTextRect(background,"loading",(275,400))
                    cv2.imshow("face attendance",background)
                    cv2.waitKey(1)
                    frame=1
                    modetype=1
        if frame!=0:
            if frame==1:
                    #getting the data
                studentinfo=db.reference(f'Students/{id}').get()
                print(studentinfo)
                #get image from the storage
                #imgstudent=cv2.imdecode(array,cv2.COLOR_BGRS2BGR)
                #update data of attendance
                datetimeobject=datetime.strptime(studentinfo["last_attendance_time"],
                "%Y-%m-%d %H:%M:%S")
                secondeleapsed=(datetime.now()-datetimeobject).total_seconds()
                print(secondeleapsed)
                if secondeleapsed>30:
                    ref=db.reference(f"students/{id}")
                    studentinfo["total_attendance"]+=1
                    ref.child("total_attendance").set(studentinfo["total_attendance"])
                    ref.child("last_attendance_time").set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modetype=3
                    frame=0
                    background[44:44+633,808:808+414]=imgmodelist[modetype]

            if modetype!=3:
                if 10<frame<20:
                    modetype=2
                background[44:44+633,808:808+414]=imgmodelist[modetype]

                if frame<=10:
                    cv2.putText(background,str(studentinfo["total_attendance"]),(861,125),
                    cv2.FONT_HERSHEY_COMPLEX,1,(225,225,225),1)
                    cv2.putText(background, str(studentinfo["major"]), (1006,550),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (225, 225, 225), 1)
                    cv2.putText(background, str(id), (1006,493),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (225, 225, 225), 1)
                    cv2.putText(background, str(studentinfo["standing"]), (910,625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100,100,100), 1)
                    cv2.putText(background, str(studentinfo["year"]), (1025, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(background, str(studentinfo["starting_year"]),(1125, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    (w,h),_=cv2.getTextSize(studentinfo["name"],cv2.FONT_HERSHEY_COMPLEX,1,1)
                    offset=(414-w)//2
                    cv2.putText(background,str(studentinfo["name"]),(808+offset,445),
                    cv2.FONT_HERSHEY_COMPLEX,1,(50,50,50),1)
                    #background[175:175+216,909:909+216]=imgstudent
                frame+=1

                if frame>=20:
                    counter=0
                    modetype=0
                    studentinfo=[]
                    imgstudent=[]
                    background[44:44+633,808:808+414]=imgmodelist[modetype]
        else:
            modetype=0
            frame=0



        cv2.imshow("background image",background)
        cv2.waitKey(1)

