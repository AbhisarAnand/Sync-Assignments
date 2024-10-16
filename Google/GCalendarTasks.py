import os
import datetime
import json
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError

class GCalendarTasks:
    def __init__(self, tasks, credentials_path='client_secret.json', token_path='TasksToken.json'):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.tasks = tasks
        self.credentials_path = os.path.join(self.path, credentials_path)
        self.token_path = os.path.join(self.path, token_path)
        self.service = None
        self.SCOPES = ['https://www.googleapis.com/auth/tasks']

    def authenticate(self):
        creds = None
        if os.path.exists(self.token_path):
            try:
                creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
            except Exception as e:
                print("Error loading credentials:", e)
                creds = None

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except RefreshError:
                    print("Token expired or revoked. Re-authenticating...")
                    creds = None  # Set creds to None to trigger re-authentication
            if not creds:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, self.SCOPES)
                creds = flow.run_local_server(port=0)
                with open(self.token_path, 'w') as token:
                    token.write(creds.to_json())
        self.service = build('gmail', 'v1', credentials=creds)

    def read_task_log(self):
        log_file_path = os.path.join(self.path, 'gTasks_log.json')
        if not os.path.exists(log_file_path):
            return []
        
        with open(log_file_path, 'r') as log_file:
            return [json.loads(line) for line in log_file]

    def write_task_log(self, tasks):
        log_file_path = os.path.join(self.path, 'gTasks_log.json')
        with open(log_file_path, 'w') as log_file:
            for task in tasks:
                json.dump(task, log_file)
                log_file.write('\n')

    def create_google_task(self, task_name, due_date):
        current_time = datetime.datetime.utcnow()
        due_date_utc = due_date.replace(tzinfo=None)

        if due_date_utc <= current_time:
            print(f"Skipping '{task_name}' as its due date is in the past.")
            return

        tasks_log = self.read_task_log()
        task_log_names = [task['task_name'] for task in tasks_log]

        if task_name not in task_log_names:
            due_rfc3339 = due_date_utc.isoformat() + 'Z'
            task = {
                'title': task_name,
                'due': due_rfc3339
            }
            result = self.service.tasks().insert(tasklist='@default', body=task).execute()
            print(f"Task created: {result['title']} with due date {result['due']}")

            tasks_log.append({
                'task_name': task_name,
                'created_at': current_time.isoformat() + 'Z',
                'due_date': due_rfc3339
            })
            self.write_task_log(tasks_log)
        else:
            print(f"Task '{task_name}' already exists. No new task created.")



    def sync_tasks(self):
        tasks_log = self.read_task_log()
        tasks_log = [task for task in tasks_log if datetime.datetime.strptime(task['due_date'], '%Y-%m-%dT%H:%M:%SZ') >= datetime.datetime.utcnow()]
        self.write_task_log(tasks_log)
        
        for task_name, (course_name, due_datetime) in self.tasks.items():
            full_task_name = f"{task_name} - {course_name}"
            self.create_google_task(full_task_name, due_datetime) 


if __name__ == '__main__':
    tasks = {
        'Homework Quiz #10': ('MA17500-02', datetime.datetime(2024, 4, 2, 13, 0)),
        'Quiz 21': ('MA16600-03', datetime.datetime(2024, 4, 2, 23, 59)),
        # Add other tasks as needed
    }

    calendar_tasks = GCalendarTasks(tasks)
    calendar_tasks.authenticate()
    calendar_tasks.sync_tasks()
