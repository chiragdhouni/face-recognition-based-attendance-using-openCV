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

folderpath="Images"
pathlist=os.listdir(folderpath)
imglist=[]
studentids=[]

for path in pathlist:
    imglist.append(cv2.imread(os.path.join(folderpath,path)))
    studentids.append(os.path.splitext(path)[0])
    #filename = f"{folderpath}/{path}"
    #bucket=storage.bucket()
   # blob=bucket.blob(filename)
    #blob.upload_from_filename(filename)


print(len(imglist))

def findencoding(imagelist):
    encodelist=[]
    for img in imglist:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encodelist.append(face_recognition.face_encodings(img)[0])
    return encodelist
encodelistknown=findencoding(imglist)
encodelistknownwithids=[encodelistknown,studentids]


file=open("encoded_file.p","wb")
pickle.dump(encodelistknownwithids,file)
file.close()