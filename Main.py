from Google.GmailReader import GmailReader
from Google.GCalendarTasks import GCalendarTasks
from Todoist.TodoistTasks import TodoistTasks
from Constants import EMAIL, GCAL_SYNC, TODOIST_SYNC



if __name__ == '__main__':
    reader = GmailReader()
    reader.authenticate()

    reader.filter_messages(EMAIL)
    reader.break_down_email()

    # print("Tasks: ", reader.tasks)

    if GCAL_SYNC:
        calendar_tasks = GCalendarTasks(reader.tasks)
        calendar_tasks.authenticate()
        calendar_tasks.sync_tasks()
        print("Tasks synced to Google Calendar!")

    if TODOIST_SYNC:
        todoist_tasks = TodoistTasks(reader.tasks)
        todoist_tasks.sync_tasks()
        print("Tasks synced to Todoist!")
