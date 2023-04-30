import sqlite3
import PySimpleGUI as sg
from datetime import datetime

# Create a connection to the database
conn = sqlite3.connect('project_manager.db')
c = conn.cursor()

# Create the projects table
c.execute('''CREATE TABLE IF NOT EXISTS projects
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT, start_date DATE, end_date DATE)''')

# Create the tasks table
c.execute('''CREATE TABLE IF NOT EXISTS tasks
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT, project_id INTEGER, due_date DATE,
             FOREIGN KEY(project_id) REFERENCES projects(id))''')

# Commit changes to the database
conn.commit()

project_column = [
    [sg.Text('Projects', font=('Helvetica', 16))],
    [sg.Listbox(values=[], size=(30, 10), key='-PROJECT_LIST-')],
    [sg.Button('Add Project'), sg.Button('Edit Project'), sg.Button('Delete Project')],
    [sg.Text('Name:'), sg.InputText(key='-PROJECT_NAME-')],
    [sg.Text('Description:'), sg.InputText(key='-PROJECT_DESC-')],
    [sg.Text('Start Date:'), sg.Input(key='-PROJECT_START-', enable_events=True)],
    [sg.Text('End Date:'), sg.Input(key='-PROJECT_END-', enable_events=True)],
    [sg.Button('Clear Project Form')]
]

task_column = [
    [sg.Text('Tasks', font=('Helvetica', 16), key='-TASK_COLUMN-', visible=False)],
    [sg.Listbox(values=[], size=(60, 10), key='-TASK_LIST-', select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)],
    [sg.Button('Add Task'), sg.Button('Edit Task'), sg.Button('Delete Task')],
    [sg.Text('Name:'), sg.InputText(key='-TASK_NAME-')],
    [sg.Text('Description:'), sg.InputText(key='-TASK_DESC-')],
    [sg.Text('Project ID:'), sg.Input(key='-TASK_PROJECT_ID-')],
    [sg.Text('Start Date:'), sg.Input(key='-TASK_START-', enable_events=True)],
    [sg.Text('End Date:'), sg.Input(key='-TASK_END-', enable_events=True)],
    [sg.Text('Status:'), sg.Input(key='-TASK_STATUS-')],
    [sg.Button('Clear Task Form'), sg.Button('View All Tasks')]
]

layout = [
    [sg.Column(project_column), sg.Column(task_column, key='-TASK_LIST_COLUMN-', visible=False)]
]

window = sg.Window('Project Management Tool', layout)





def add_project(values):
    """Add a new project to the database"""

    # Extract project information from the input values
    project_name = values['-PROJECT_NAME-']
    project_desc = values['-PROJECT_DESC-']
    project_start = values['-PROJECT_START-']
    project_end = values['-PROJECT_END-']

    # Insert the new project into the projects table
    c.execute('''INSERT INTO projects (name, description, start_date, end_date)
                 VALUES (?, ?, ?, ?)''', (project_name, project_desc, project_start, project_end))

    # Commit changes to the database
    conn.commit()

    # Update the project list
    update_project_list()


def edit_project(values):
    """Edit an existing project in the database"""

    # Get the selected project ID
    selected_project = values['-PROJECT_LIST-']
    if selected_project:
        project_id = selected_project[0][0]

        # Extract project information from the input values
        project_name = values['-PROJECT_NAME-']
        project_desc = values['-PROJECT_DESC-']
        project_start = values['-PROJECT_START-']
        project_end = values['-PROJECT_END-']

        # Update the project in the projects table
        c.execute('''UPDATE projects
                     SET name=?, description=?, start_date=?, end_date=?
                     WHERE id=?''', (project_name, project_desc, project_start, project_end, project_id))

        # Commit changes to the database
        conn.commit()

        # Update the project list and task list
        update_project_list()
        update_task_list(project_id)


def delete_project(values):
    """Delete an existing project from the database"""

    # Get the selected project ID
    selected_project = values['-PROJECT_LIST-']
    if selected_project:
        project_id = selected_project[0][0]

        # Delete the project and its associated tasks from the database
        c.execute('DELETE FROM projects WHERE id=?', (project_id,))
        c.execute('DELETE FROM tasks WHERE project_id=?', (project_id,))

        # Commit changes to the database
        conn.commit()

        # Update the project list and task list
        update_project_list()
        update_task_list(None)


def add_task(values):
    """Add a new task to the database"""

    # Get the selected project ID
    selected_project = values['-PROJECT_LIST-']
    if selected_project:
        project_id = selected_project[0][0]

        # Extract task information from the input values
        task_name = values['-TASK_NAME-']
        task_desc = values['-TASK_DESC-']
        task_due = values['-TASK_DUE-']

        # Insert the new task into the tasks table
        c.execute('''INSERT INTO tasks (name, description, project_id, due_date)
                     VALUES (?, ?, ?, ?)''', (task_name, task_desc,    project_id, task_due))

    # Commit changes to the database
    conn.commit()

    # Update the task list
    update_task_list(project_id)

def edit_task(values):
    """Edit an existing task in the database"""
    # Get the selected task ID
    selected_task = values['-TASK_LIST-']
    if selected_task:
        task_id = selected_task[0][0]

        # Extract task information from the input values
        task_name = values['-TASK_NAME-']
        task_desc = values['-TASK_DESC-']
        task_due = values['-TASK_DUE-']

        # Update the task in the tasks table
        c.execute('''UPDATE tasks
                     SET name=?, description=?, due_date=?
                     WHERE id=?''', (task_name, task_desc, task_due, task_id))

        # Commit changes to the database
        conn.commit()

        # Update the task list
        update_task_list(None)

def delete_task(values):
    """Delete an existing task from the database"""
    # Get the selected task ID
    selected_task = values['-TASK_LIST-']
    if selected_task:
        task_id = selected_task[0][0]

        # Delete the task from the tasks table
        c.execute('DELETE FROM tasks WHERE id=?', (task_id,))

        # Commit changes to the database
        conn.commit()

        # Update the task list
        update_task_list(None)

def update_project_list():
    """Update the project list in the GUI"""
    # Get the list of projects from the database
    c.execute('SELECT id, name FROM projects')
    projects = c.fetchall()
    # Update the project list element in the GUI
    window['-PROJECT_LIST-'].update(values=projects)

def update_task_list(project_id):
    """Update the task list in the GUI"""
    # Get the list of tasks from the database
    if project_id:
        c.execute('SELECT id, name FROM tasks WHERE project_id=?', (project_id,))
        tasks = c.fetchall()
    else:
        tasks = []

    # Update the task list element in the GUI
    window['-TASK_LIST-'].update(values=tasks)


#update_project_list()
update_task_list(None)



while True:
    event, values = window.read()
    # Exit the program when the window is closed
    if event == sg.WIN_CLOSED:
        break

    # Project events
    elif event == '-PROJECT_LIST-':
        project_id = values['-PROJECT_LIST-'][0][0]
        update_task_list(project_id)

    elif event == 'Add Project':
        add_project(values)

    elif event == 'Edit Project':
        edit_project(values)

    elif event == 'Delete Project':
        delete_project(values)

    # Task events
    elif event == '-TASK_LIST-':
        task_id = values['-TASK_LIST-'][0][0]
        c.execute('SELECT name, description, due_date FROM tasks WHERE id=?', (task_id,))
        task_data = c.fetchone()
        window['-TASK_NAME-'].update(value=task_data[0])
        window['-TASK_DESC-'].update(value=task_data[1])
        window['-TASK_DUE-'].update(value=task_data[2])

    elif event == 'Add Task':
        add_task(values)

    elif event == 'Edit Task':
        edit_task(values)

    elif event == 'Delete Task':
        delete_task(values)

    # Date picker events
    elif event == '-PROJECT_START-' or event == '-PROJECT_END-' or event == '-TASK_DUE-':
        date_string = values[event].strftime('%Y-%m-%d')
        window[event].update(value=date_string)

window.close()
conn.close()


