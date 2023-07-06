import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    "databaseURL":"https://faceattendance-2412f-default-rtdb.firebaseio.com/",
    "storageBucket":"faceattendance-2412f.appspot.com"
})

ref =db.reference('Students')

data={
    "321654":
        {
            "name":"chirag singh",
            "major":"computer science",
            "starting_year":2020,
            "total_attendance":7,
            "standing":"G",
            "year":2,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "852741":
        {
            "name":"emily blunt",
            "major":"arts",
            "starting_year":2019,
            "total_attendance":5,
            "standing":"B",
            "year":1,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "963852":
        {
            "name":"elon musk",
            "major":"physics",
            "starting_year":2020,
            "total_attendance":9,
            "standing":"G",
            "year":3,
            "last_attendance_time": "2022-12-11 00:54:34"
        }

}
for key,value in data.items():
    ref.child(key).set(value)


#uploading images to storage

image_folder="Images"
images_path_list=os.listdir(image_folder)
for image_path in images_path_list:
    filename = f"{image_folder}/{image_path}"
    bucket = storage.bucket()
    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)



