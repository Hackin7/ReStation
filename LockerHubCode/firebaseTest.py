import firebase
from google.cloud import storage
from google.cloud.storage import client
import cv2

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
##https://stackoverflow.com/questions/52883534/firebase-storage-upload-file-python

cred = credentials.Certificate('./restation-8e253-526f5f260257.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'restation-8e253.appspot.com'
})

bucket = storage.bucket()

path = "output.jpeg"
imageBlob = bucket.blob(path) #Local Path
imageBlob.upload_from_filename('/tmp/output.jpeg')
