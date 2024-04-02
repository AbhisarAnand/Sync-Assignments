from Google.GmailReader import GmailReader
from Google.GCalendarTasks import GCalendarTasks



if __name__ == '__main__':
    reader = GmailReader()
    reader.authenticate()

    # reader.filter_messages('d2lsupport@purdue.brightspace.com')
    reader.filter_messages('anana06@pfw.edu')
    reader.break_down_email()

    print("Tasks: ", reader.tasks)

    calendar_tasks = GCalendarTasks(reader.tasks)
    calendar_tasks.authenticate()
    calendar_tasks.sync_tasks()

    print("Tasks synced to Google Calendar!")
