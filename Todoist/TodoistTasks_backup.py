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

    def list_all_projects(self):
        """Debug method to list all available projects"""
        try:
            projects = self.api.get_projects()
            print("Available projects:")
            if isinstance(projects, list):
                for project in projects:
                    if hasattr(project, 'name'):
                        print(f"  - Name: '{project.name}', ID: {project.id}")
                    elif isinstance(project, dict):
                        print(f"  - Name: '{project.get('name')}', ID: {project.get('id')}")
            return projects
        except Exception as e:
            print(f"Error fetching projects: {e}")
            return []

    def list_all_sections(self, project_id):
        """Debug method to list all sections in a project"""
        try:
            sections = self.api.get_sections(project_id=project_id)
            print(f"Available sections in project ID {project_id}:")
            if isinstance(sections, list):
                for section in sections:
                    if hasattr(section, 'name'):
                        print(f"  - Name: '{section.name}', ID: {section.id}")
                    elif isinstance(section, dict):
                        print(f"  - Name: '{section.get('name')}', ID: {section.get('id')}")
            return sections
        except Exception as e:
            print(f"Error fetching sections: {e}")
            return []

    def get_project_id(self, project_name):
        try:
            projects = self.api.get_projects()
            # Handle both list and object responses
            if isinstance(projects, list):
                for project in projects:
                    if hasattr(project, 'name') and project.name == project_name:
                        return project.id
                    elif isinstance(project, dict) and project.get('name') == project_name:
                        return project.get('id')
            else:
                # If projects is a single object
                if hasattr(projects, 'name') and projects.name == project_name:
                    return projects.id
        except Exception as e:
            print(f"An error occurred while fetching projects: {e}")
        return None

    def get_section_id(self, project_id, section_name):
        try:
            sections = self.api.get_sections(project_id=project_id)
            # Handle both list and object responses
            if isinstance(sections, list):
                for section in sections:
                    if hasattr(section, 'name') and section.name == section_name:
                        return section.id
                    elif isinstance(section, dict) and section.get('name') == section_name:
                        return section.get('id')
            else:
                # If sections is a single object
                if hasattr(sections, 'name') and sections.name == section_name:
                    return sections.id
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

    def debug_sync_setup(self):
        """Debug method to check project and section setup"""
        print("=== DEBUGGING TODOIST SETUP ===")
        
        # List all projects
        projects = self.list_all_projects()
        
        # Try to find our target project
        self.project_id = self.get_project_id(PROJECT_NAME)
        print(f"\nLooking for project: '{PROJECT_NAME}'")
        print(f"Found project ID: {self.project_id}")
        
        if self.project_id:
            # List sections in our project
            self.list_all_sections(self.project_id)
            
            # Try to find our target section
            self.section_id = self.get_section_id(self.project_id, SECTION_NAME)
            print(f"\nLooking for section: '{SECTION_NAME}'")
            print(f"Found section ID: {self.section_id}")
        else:
            print(f"ERROR: Project '{PROJECT_NAME}' not found!")
        
        print("=== END DEBUG ===\n")

    def add_task(self, task_name, course_name, due_datetime):
        # Handle both string and datetime objects
        if isinstance(due_datetime, str):
            due_date = datetime.datetime.strptime(due_datetime, '%Y-%m-%dT%H:%M:%S')
            due_date_string = due_datetime
        else:
            due_date = due_datetime
            due_date_string = due_datetime.strftime('%Y-%m-%dT%H:%M:%S')
        
        if due_date <= datetime.datetime.now():
            print(f"Skipping '{task_name}' as its due date is in the past.")
            return

        if self.project_id is None:
            self.project_id = self.get_project_id(PROJECT_NAME)
            print(f"Debug: Found project ID for '{PROJECT_NAME}': {self.project_id}")
        if self.section_id is None:
            self.section_id = self.get_section_id(self.project_id, SECTION_NAME)
            print(f"Debug: Found section ID for '{SECTION_NAME}': {self.section_id}")

        tasks_log = self.read_task_log()
        task_log_names = [task['task_name'] for task in tasks_log]

        if task_name not in task_log_names:
            try:
                task = self.api.add_task(
                    content=task_name,
                    due_date=due_date,  # Pass datetime object, not string
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
                    'due_date': due_date_string
                })
                self.write_task_log(tasks_log)
            except Exception as e:
                print(f"An error occurred while adding the task: {e}")
                import traceback
                traceback.print_exc()
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
        # First run debug to see what's available
        self.debug_sync_setup()
        
        self.clean_task_log()
        for task_name, (course_name, due_datetime) in self.tasks.items():
            # Handle both string and datetime objects
            if isinstance(due_datetime, datetime.datetime):
                due_date_string = due_datetime.strftime('%Y-%m-%dT%H:%M:%S')
            else:
                due_date_string = due_datetime
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
