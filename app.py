import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from firebase_admin import credentials, firestore, initialize_app

import firebase_admin
from google.cloud import secretmanager
from google.oauth2 import service_account

from threading import Timer,Thread,Event

GOOGLE_CLOUD_PROJECT_NUMBER = 544247596163
FIREBASE_SA_SECRET_NAME = 'firebase-key'
VERSION = 'latest'

# Create credentials object then initialize the firebase admin client
sec_client = secretmanager.SecretManagerServiceClient()
name = f"projects/{GOOGLE_CLOUD_PROJECT_NUMBER}/secrets/{FIREBASE_SA_SECRET_NAME}/versions/{VERSION}"
response = sec_client.access_secret_version(request={"name": name})
service_account_info = json.loads(response.payload.data.decode('utf-8'))

# build credentials with the service account dict
creds = firebase_admin.credentials.Certificate(service_account_info)

# initialize firebase admin
firebase_app = firebase_admin.initialize_app(creds)

# Initialize Firestore DB
db = firestore.client()
sensors_ref = db.collection('sensor_data')

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

class MyThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        while not self.stopped.wait(5):
            print("my thread")
            # call a function
            tick()


def tick():
    print('T E S T L O G G')



if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))

    stopFlag = Event()
    thread = MyThread(stopFlag)
    thread.start()
    # this will stop the timer
    #stopFlag.set()