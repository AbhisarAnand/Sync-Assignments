import os.path
import base64
import datetime
import re
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

class GmailReader:
    def __init__(self, credentials_path='client_secret.json', token_path='GmailToken.json'):
        path = os.path.dirname(os.path.abspath(__file__))
        self.credentials_path = os.path.join(path, credentials_path)
        self.token_path = os.path.join(path, token_path)
        self.service = None
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        self.filteredEmails = []
        self.tasks = {}

    def authenticate(self):
        creds = None
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
        self.service = build('gmail', 'v1', credentials=creds)

    def filter_messages(self, sender_email):
        if not self.service:
            print("You must authenticate before filtering messages.")
            return

        today = datetime.datetime.now().strftime('%Y/%m/%d')
        query = f'from:{sender_email} after:{today}'

        results = self.service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])

        if not messages:
            print("No messages found.")
            return

        for message in messages:
            msg = self.service.users().messages().get(userId='me', id=message['id']).execute()
            email_details = {'id': message['id'], 'snippet': msg['snippet']}
            self.filteredEmails.append(email_details)

    def get_message_body(self, message_id):
        if not self.service:
            print("You must authenticate before getting a message body.")
            return

        message = self.service.users().messages().get(userId='me', id=message_id, format='full').execute()

        if 'parts' in message['payload']:
            for part in message['payload']['parts']:
                if part['mimeType'] == 'text/plain' or part['mimeType'] == 'text/html':
                    data = part['body']['data']
                    text = base64.urlsafe_b64decode(data.encode('ASCII')).decode('utf-8')
                    return text
        else:
            # For simple email bodies (non-multipart)
            data = message['payload']['body']['data']
            text = base64.urlsafe_b64decode(data.encode('ASCII')).decode('utf-8')
            return text

        return "No readable message body found."
    
    def break_down_email(self):
        for email in self.filteredEmails:
            email_id = email['id']
            email_body = self.get_message_body(email_id)
            courseName = ""
            taskName = ""
            dueDate = ""
            task_name_pattern = re.compile(r"^(.*?)<")

            lines = email_body.split("\n")
            for i in range(len(lines)):
                lines[i] = lines[i].replace("FW: ", "")
                parts = lines[i].split(' ')
                if courseName == "" and "Activity summary for" in lines[i]:
                    parts = parts[5:]
                    courseName = "".join(parts[1:3])
                elif "- Due date is in" in lines[i] and courseName != "":
                    taskName = task_name_pattern.search(lines[i]).group(1).strip()
                    clean_time_string = lines[i + 1].lstrip(": ").strip().replace("Due date: ", "")  # Strip whitespace from both ends
                    try:
                        dueDate = datetime.datetime.strptime(clean_time_string[:-4].strip(), "%A, %B %d, %Y %I:%M %p")
                    except ValueError as e:
                        print("Error parsing date:", e, "from string:", repr(clean_time_string))
                    self.tasks[taskName] = (courseName, dueDate)


# Usage example:
if __name__ == '__main__':
    reader = GmailReader('client_secret.json')
    reader.authenticate()

    # reader.filter_messages('d2lsupport@purdue.brightspace.com')
    reader.filter_messages('anana06@pfw.edu')

    # Access the filtered emails
    # for email in reader.filteredEmails:
    #     print("Email: ", email)
    #     print("Message body: ", reader.get_message_body(email['id']))
    reader.break_down_email()
    print("Tasks: ", reader.tasks)

