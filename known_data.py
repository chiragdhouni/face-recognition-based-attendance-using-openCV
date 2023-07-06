import os

import cv2
import face_recognition
import pickle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    "databaseURL":"https://faceattendance-2412f-default-rtdb.firebaseio.com/",
    "storageBucket":"faceattendance-2412f.appspot.com"
})

image_folder="Images"
images_path_list=os.listdir(image_folder)
images=[]
student_ids=[]
for path in images_path_list:
    images.append(cv2.imread(os.path.join(image_folder,path)))
    student_ids.append(os.path.splitext(path)[0])

def encoding(images):
    encoded_images=[]
    for img in images:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encoded_images.append(face_recognition.face_encodings(img)[0])
    return encoded_images

encoded_images=encoding(images)
encoded_images_with_ids=[encoded_images,student_ids]

file=open("encoded_data.p","wb")
pickle.dump(encoded_images_with_ids,file)
file.close()