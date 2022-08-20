import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import storage
import time
import json
import sys

class FirebaseAtitude:
    """docstring for FirebaseAtitude"""
    def __init__(self, cert, dataBaseUrl, name, bucketName):
        self.cert = cert
        self.cred = credentials.Certificate(cert)
        self.fbAdmin = firebase_admin.initialize_app(self.cred,{'databaseURL':dataBaseUrl}, name=name)
        self.fc = firestore.client()
        self.bucketName = bucketName

    def upload_to_storage(self, pathToFile, fileName, urlStorage):
        storageClient = storage.Client.from_service_account_json(self.cert)
        bucket = storageClient.get_bucket(urlStorage, self.fbAdmin)
        blob = bucket.blob(pathToFile)
        blob.upload_from_filename(fileName)
        return blob.public_url

    def download_file(self, pathToFile, fileName, urlStorage):
        try:
            storageClient = storage.Client.from_service_account_json(self.cert)
            bucket = storageClient.get_bucket(urlStorage, self.fbAdmin)
            blob = bucket.blob(pathToFile)
            blob.download_to_filename(fileName)
            return "ok"
        except Exception as e:
            err = "firebaseConnection.py - download_file | " + str(e)
            return err

    def download_save_all(self, storageRef, downloadLocalPath):
        try:
            client = storage.Client.from_service_account_json(self.cert)
            for blob in client.list_blobs(self.bucketName, prefix = storageRef):
                print(blob.name)
                nameFile = blob.name
                nameFile = nameFile.split("/")[-1]
                blob.download_to_filename(downloadLocalPath + "/" + nameFile)
            return 'ok'
        except Exception as e:
            err = "firebaseConnection.py - download_save_all() | " + str(e)
            return err

    def set_info_db_realtime(self, ref, data):
        try:
            keys = list(data.keys())
            values = list(data.values())
            db.reference(ref, self.fbAdmin).set(data)
            # map keys values
            return [keys, values]
        except Exception as e:
            err = "firebaseConnection.py - set_info_db_realtime | " + str(e)
            return err

    def get_info_db_realtime(self, ref):
        refresp = db.reference(ref, self.fbAdmin).get()
        return refresp

    def del_info_db_realtime(self, ref):
        try:
            db.reference(ref, self.fbAdmin).delete()
            return 'ok'
        except Exception as e:
            err = "firebaseConnection.py - del_info_db_realtime | " + str(e)
            return err
