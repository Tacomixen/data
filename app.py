import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from firebase_admin import credentials, firestore, initialize_app

import firebase_admin
from google.cloud import secretmanager
from google.oauth2 import service_account

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

from threading import Timer


class InfiniteTimer():
    """A Timer class that does not stop, unless you want it to."""

    def __init__(self, seconds, target):
        self._should_continue = False
        self.is_running = False
        self.seconds = seconds
        self.target = target
        self.thread = None

    def _handle_target(self):
        self.is_running = True
        self.target()
        self.is_running = False
        self._start_timer()

    def _start_timer(self):
        if self._should_continue: # Code could have been running when cancel was called.
            self.thread = Timer(self.seconds, self._handle_target)
            self.thread.start()

    def start(self):
        if not self._should_continue and not self.is_running:
            self._should_continue = True
            self._start_timer()
        else:
            print("Timer already started or running, please wait if you're restarting.")

    def cancel(self):
        if self.thread is not None:
            self._should_continue = False # Just in case thread is running and cancel fails.
            self.thread.cancel()
        else:
            print("Timer never started or failed to initialize.")


def tick():
    print('T E S T L O G G')

# Example Usage
t = InfiniteTimer(5, tick)
t.start()



if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))