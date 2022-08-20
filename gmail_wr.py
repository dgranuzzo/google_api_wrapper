from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import datetime
import base64
from pprint import pprint
import os

class GmailAtitude:
	"""docstring for GmailAtitude"""
	def __init__(self, pathToToken, pathToCredentials):
		self.scopes = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/gmail.readonly']
		self.pathToToken = pathToToken
		self.pathToCredentials = pathToCredentials
		service = initialize_gmail(self.pathToToken, self.pathToCredentials, self.scopes)
		self.service = service

	def change_labels_from_email(self, msgId, labelsAdd, labelsDel):
		modificaLabel = {'addLabelIds':labelsAdd, 'removeLabelIds':labelsDel}
		self.service.users().messages().modify(userId = 'me', id = msgId, body = modificaLabel).execute()
		return

	def extract_body_from_email(self, email):
		try:
			body = email['payload']['parts'][0]
		except:
			body = email['payload']
		try:
			corpo = body['body']['data']
		except:
			try:
				corpo = body['parts'][0]['body']['data']
			except:
				corpo = body['parts'][0]['parts'][0]['body']['data']
		corpo = base64.urlsafe_b64decode(corpo.encode('ASCII'))
		corpo = corpo.decode('utf-8')
		corpo = str(corpo)
		#corpo = "(Remetente/Data) " + remetente + " " + data + "\n" + corpo
		corpo = corpo.replace("\\r", "\r")
		corpo = corpo.replace("\\n", "\n")

		return corpo

	def get_emails_ids_list(self):
		inbox = self.service.users().messages().list(userId='me', labelIds = ['INBOX']).execute()
		listEmails = inbox.get('messages', [])
		listIds = []
		for msgById in listEmails:
			listIds.append(msgById['id'])
		return listIds

	def get_email_by_id(self, msgId):
		email = self.service.users().messages().get(userId = 'me', id = msgId).execute()
		return email

	def get_headers(self, email):
		headers = email['payload']['headers']
		return headers

	def get_payload(self, email):
		payload = email['payload']
		return payload

	def get_labels(self, email):
		return email.get('labelIds', [])

	def save_attachments(self, payload, msgId, pathToSave):
		try:
			parts = payload['parts']
			for part in parts:
				filename = part.get("filename", "nofile")
				if filename == "nofile" or filename == "":
					pass
				else:
					attachment = self.service.users().messages().attachments().get(userId='me', messageId=msgId, id=part['body']['attachmentId']).execute()
					file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))
					caminho = os.path.join(pathToSave + "\\", part['filename'])
					f = open(caminho, 'wb')
					f.write(file_data)
					f.close()
			return "ok"
		except Exception as e:
			return e

def initialize_gmail(pathToToken, pathToCredentials, scopes):
	creds = None
	if os.path.exists(pathToToken):
		with open(pathToToken, 'rb') as token:
			creds = pickle.load(token)
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				pathToCredentials, scopes)
			creds = flow.run_local_server(port=0)
		with open(pathToToken, 'wb') as token:
			pickle.dump(creds, token)
	service = build('gmail', 'v1', credentials=creds, cache_discovery=False)
	return service
