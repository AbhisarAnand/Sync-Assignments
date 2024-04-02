import os
import datetime
import json
from todoist_api_python.api import TodoistAPI
from Constants import PROJECT_NAME, SECTION_NAME

class TodoistTasks:
    def __init__(self, tasks, log_file_path='todoist_tasks_log.json'):
        self.tasks = tasks
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.api_token = self.get_api_token()
        self.api = TodoistAPI(self.api_token)
        self.log_file_path = os.path.join(self.path, log_file_path)
        self.project_id = None
        self.section_id = None

    def get_api_token(self):
        try:
            with open(os.path.join(self.path, 'Token.json'), 'r') as file:
                data = json.load(file)
                return data['API_Token']
        except Exception as e:
            print(f"An error occurred while fetching API token: {e}")

    def get_project_id(self, project_name):
        try:
            projects = self.api.get_projects()
            for project in projects:
                if project.name == project_name:
                    return project.id
        except Exception as e:
            print(f"An error occurred while fetching projects: {e}")
        return None

    def get_section_id(self, project_id, section_name):
        try:
            sections = self.api.get_sections(project_id=project_id)
            for section in sections:
                if section.name == section_name:
                    return section.id
        except Exception as e:
            print(f"An error occurred while fetching sections: {e}")
        return None

    def read_task_log(self):
        if not os.path.exists(self.log_file_path):
            return []
        
        with open(self.log_file_path, 'r') as log_file:
            return json.load(log_file)

    def write_task_log(self, tasks_log):
        with open(self.log_file_path, 'w') as log_file:
            json.dump(tasks_log, log_file)

    def add_task(self, task_name, course_name, due_datetime):
        due_date = datetime.datetime.strptime(due_datetime, '%Y-%m-%dT%H:%M:%S')
        if due_date <= datetime.datetime.now():
            print(f"Skipping '{task_name}' as its due date is in the past.")
            return

        if self.project_id is None:
            self.project_id = self.get_project_id(PROJECT_NAME)
        if self.section_id is None:
            self.section_id = self.get_section_id(self.project_id, SECTION_NAME)

        tasks_log = self.read_task_log()
        task_log_names = [task['task_name'] for task in tasks_log]

        if task_name not in task_log_names:
            try:
                task = self.api.add_task(
                    content=task_name,
                    due_date=due_datetime,
                    labels=[course_name],
                    priority=2,
                    project_id=self.project_id,
                    section_id=self.section_id
                )
                print(f"Task added to Todoist in {PROJECT_NAME} project under {SECTION_NAME} section: {task.content}")

                tasks_log.append({
                    'task_name': task_name,
                    'course_name': course_name,
                    'created_at': datetime.datetime.now().isoformat(),
                    'due_date': due_datetime
                })
                self.write_task_log(tasks_log)
            except Exception as e:
                print(f"An error occurred while adding the task: {e}")
        else:
            print(f"Task '{task_name}' already exists in Todoist. No new task created.")

    def clean_task_log(self):
        tasks_log = self.read_task_log()
        current_time = datetime.datetime.now()
        filtered_log = [task for task in tasks_log if datetime.datetime.strptime(task['due_date'], '%Y-%m-%dT%H:%M:%S') > current_time]

        if len(filtered_log) != len(tasks_log):
            self.write_task_log(filtered_log)
            print("Cleaned up tasks from log file with due dates in the past.")

    def sync_tasks(self):
        self.clean_task_log()
        for task_name, (course_name, due_datetime) in self.tasks.items():
            due_date_string = due_datetime.strftime('%Y-%m-%dT%H:%M:%S')
            self.add_task(task_name, course_name, due_date_string)

if __name__ == '__main__':
    tasks = {
        'Homework Quiz #10': ('MA17500-02', datetime.datetime(2024, 4, 2, 13, 0)),
        'Quiz 21': ('MA16600-03', datetime.datetime(2024, 4, 2, 23, 59)),
        # Add other tasks as needed
    }

    # Initialize and authenticate Todoist
    todoist_tasks = TodoistTasks(tasks)
    todoist_tasks.sync_tasks()
