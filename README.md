# Sync Assignments 📚

## Thank You for Visiting! &emsp; ![Visitor Count](https://visitor-badge.laobi.icu/badge?page_id=abhisaranand.SyncAssignments)

**Sync Assignments** is a tool designed for Purdue University students to seamlessly integrate their academic assignments from Brightspace into their personal Google Calendar and Google Tasks. This automation tool scans your Gmail for emails related to course assignments, extracts key information, and ensures your calendar and tasks are up-to-date with your academic deadlines.

## 🌟 Features

- **Brightspace Integration**: Specifically tuned for Purdue University students, focusing on assignment emails from Brightspace.
- **Email Parsing**: Automatically parses assignment details from Gmail, reducing manual entry.
- **Calendar Sync**: Creates Google Calendar events for each assignment with due dates and reminders.
- **Task Sync**: Adds assignments to Google Tasks with comprehensive details.
- **Todoist Integration**: Seamlessly integrates with Todoist, allowing for efficient task management alongside Google Tasks.
- **Duplication Avoidance**: Intelligent checks to prevent duplicate calendar events and tasks.
- **Log Management**: Maintains a detailed log of synced assignments, ensuring transparency and control.
- **Automated Cleanup**: Removes past-due assignments from logs to keep your list current.

## 🔧 Languages and Tools Used

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Google API](https://img.shields.io/badge/Google%20API-4285F4?style=for-the-badge&logo=google&logoColor=white)
![JSON](https://img.shields.io/badge/JSON-000000?style=for-the-badge&logo=json&logoColor=white)
![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)
![GoogleCalendar](https://img.shields.io/badge/Google%20Calendar-4285F4?style=for-the-badge&logo=google-calendar&logoColor=white%60)
![Todoist](https://img.shields.io/badge/Todoist-EF8E1F?style=for-the-badge&logo=todoist&logoColor=white%60)

## 🚀 Getting Started

### Prerequisites

- Python 3.6+
- Pip for Python package management
- Google Cloud Platform account for API access

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/AbhisarAnand/Sync-Assignments
    cd SyncAssignments
    ```

2. Install required Python packages:
    ```bash
    pip3 install -r requirements.txt
    ```

3. Follow [Google's guide](https://developers.google.com/workspace/guides/create-credentials) to set up `client_secret.json` for Gmail and Google Calendar API.

### Setup

1. Place your `client_secret.json` in the root directory.

### Usage

Run the Sync Assignments tool:
```bash
python3 Main.py
```
Authenticate with Google on first run and follow prompts to sync assignments.

## 🛠️ How It Works

- **GmailReader**: Scans Gmail for Brightspace assignment emails, extracting key information.
- **GCalendarTasks & TodoistTasks**: Syncs the extracted assignment information with Google Calendar, Google Tasks, and Todoist, ensuring your academic schedule is always up-to-date across your preferred task management platforms.
- **Main**: Orchestrates the flow from email parsing to calendar and task synchronization with both Google and Todoist services.

## 📄 License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## 📧 Contact

For queries or support, please email us at [abhisar.muz@gmail.com](mailto:abhisar.muz@gmail.com).

---

*Proudly created for Purdue University students by Abhisar Anand.*
