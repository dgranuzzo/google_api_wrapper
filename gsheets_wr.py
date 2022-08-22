from googleapiclient.discovery import build
#from google_auth_oauthlib.flow import InstalledAppFlow
#from google.auth.transport.requests import Request

import pickle
import os.path

from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials

#PATH_CRED_JSON = r'D:\attadmin-gsheet-1.json'
#SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
#creds = ServiceAccountCredentials.from_json_keyfile_name(PATH_CRED_JSON, SCOPES)
#service = build('sheets', 'v4', http=creds.authorize(Http()))

class Gsheets:
    """
    class encapsulating gsheets api
    how to generate token: https://developers.google.com/sheets/api/quickstart/python
    """
    def __init__(self, tokenPath, sheetId):
        with open(tokenPath, 'rb') as token:
            creds = pickle.load(token)
        service = build('sheets', 'v4', credentials=creds)
        self.sheet = service.spreadsheets()
        self.sheetId = sheetId

    def get_data(self, rangeName):
        result = self.sheet.values().get(spreadsheetId=self.sheetId,range=rangeName).execute()
        values = result.get('values', [])
        return values


if __name__=='__main__':
    TOKEN = 'gsheetstoken.pickle'
    LIMP_PORTAL_GSHEET_ID = 'sheet_id_here'
    gsheet1 = Gsheets(TOKEN,LIMP_PORTAL_GSHEET_ID)
    rangeName = 'Sheet1!A2:D100'
    resp = gsheet1.get_data(rangeName)
    print(resp)