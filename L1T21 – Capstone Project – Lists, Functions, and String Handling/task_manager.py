# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(
        task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(
        task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


import os  # Import os for file handling.

#====Login Section====
'''This code reads usernames and passwords from the user.txt file to 
    allow a user to login.
'''

# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().strip().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    try:
        username, password = user.split(';')
        username_password[username] = password
    except ValueError:
        print(f"Skipping invalid entry: {user}")

logged_in = False
while not logged_in:
    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password:
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


# Functions 
# Registering a user
def reg_user():
    '''Adds a new user to the user.txt file
    and checks if username already exists'''
    while True:
        # Check if username already exists.
        new_username = input("New Username: ")
        if new_username in username_password:
            print("Username already exists. Please try again!")
        else:
            new_password = input("New Password: ")
            confirm_password = input("Confirm Password: ")
            # Check if the new password and confirmed password are the same.
            if new_password == confirm_password:
                print("New user added")
                username_password[new_username] = new_password

                # Add user to "user.txt".
                with open("user.txt", "a") as out_file:
                    out_file.write(f"\n{new_username};{new_password}")
                break
            else:
                print("Passwords do not match")


# Adding a task.
def add_task():
    '''Allow a user to add a new task to task.txt file
        Prompt a user for the following: 
            - A username of the person whom the task is assigned to,
            - A title of a task,
            - A description of the task and 
            - the due date of the task.'''
    
    # Inputs.
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return  
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, 
                                              DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")


    # Then get the current date.
    curr_date = date.today()


    # Add the data to the file task.txt and
    # Include 'No' to indicate if the task is complete.
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")


# Viewing all tasks.
def view_all():
    '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling) 
    '''
    for t in task_list:
        disp_str = f"Task: {t['title']}\n"
        disp_str += f"Assigned to: {t['username']}\n"
        disp_str += (
            f"Date Assigned: "
            f"{t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n")
        disp_str += (f"Due Date: "
                f"{t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n")
        disp_str += f"Task Description: {t['description']}\n"
        print(disp_str)


# Viewing my task.
# First define function that will handle the functionality of updating
# details in tasks.txt.
def update_tasks(task_list):
    '''
    Takes details from "task_list" and updates "tasks.txt"
    '''
    with open("tasks.txt", "w") as file:
        for task in task_list:
            file.write(f"{task["username"]}; {task["title"]};" 
                    f"{task["description"]};" 
                    f"{task["due_date"].strftime(DATETIME_STRING_FORMAT)};"
                    f"{task["assigned_date"].strftime(DATETIME_STRING_FORMAT)};"
                    f"{"Yes" if task["completed"] else "No"}\n")


# Viewing all tasks.
def view_mine():
    '''Displays all tasks with a corresponding number, 
    allows user to select a specific task or "-1" to return to main menu,
    if the user selects a specific task, they should be able to either
    mark the task as complete or edit the task
    '''
    indx = 1
    indices = {}

    for i, t in enumerate(task_list):
        if t['username'] == curr_user:
            indices[indx] = i
            disp_str = f"{indx} Task: {t['title']}\n"
            disp_str += f"Assigned to: {t['username']}\n"
            disp_str += (
            f"Date Assigned: "
            f"{t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            )

            disp_str +=( f"Due Date: "
                        f"{t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            )
            disp_str += f"Task Complete? {'Yes' if t['completed'] else 'No'}\n"
            disp_str += f"Task Description: {t['description']}\n"
            print(disp_str)
            indx += 1
    
    while True:
        choice = input(f"\nSelect a task number, or press -1 to return to the"
             f"main menu: ")

        # Returns to main menu.
        if choice == "-1":
            return
        
        # Selects task and checks if completed.
        elif choice.isdigit():
            choice = int(choice)

            if choice in indices:
                selected_task_indx = indices[choice]
                selected_task = task_list[selected_task_indx]

                # If task is complete, prints relevant message.
                if selected_task["completed"]:
                    print("Task already complete.")
                
                # Allows user to mark task as complete, edit or return
                # to view_mine menu
                else: 
                    edit = input(
                "Enter 'y' to mark task as complete, 'e' to edit the task, "
                "or 'b' to go back: "
                ).lower()

                    if edit == "y":
                        selected_task["completed"] = True
                        update_tasks(task_list)
                        print("\nTask marked complete.")

                    # Allows username of who the task is assigned to,
                    # or the due date to be edited.
                    elif edit == "e":
                        edit_field = input(
                        "Enter 'username' to edit username, "
                        "'due date' to edit the due date, or 'b' to go back: "
                        ).lower()

                        if edit_field == "username":
                            new_username = input("Enter new username: ")
                            selected_task["username"] = new_username
                            update_tasks(task_list)
                            print("Username updated.")

                        elif edit_field == "due date":
                            while True:
                                try:
                                    new_due_date = input(
                                    f"Enter new due date (YYYY-MM-DD): "
                                    )

                                    selected_task["due_date"] = (
                                    datetime.strptime(
                                    new_due_date, DATETIME_STRING_FORMAT)
                                    )

                                    update_tasks(task_list)
                                    print("\nDue date updated!")
                                    break
                                except ValueError:
                                    print(f"Invalid date format,"
                                        f"follow specified format.")
                                    
                        elif edit_field == "b":
                            continue

                        else:
                            print("Invalid choice, try again.")

                    elif edit == "b":
                        continue

                    else:
                        print("Invalid choice, try again.")

            else:
                print("Invalid choice, try again.")

        else:
            print(f"Invalid choice. Enter a number from the list or"
                "'-1' to return to the main menu.")


def generate_reports():
    '''When selected, generates two txt files, called 1.task_overview.txt
    which tracks the total number of tasks, completed & uncompleted, 
    overdue, the percentage of tasks that are incomplete and those
    that are overdue. And 2.user_overview.txt, which tracks the total
    number of users registered and for each, total number of tasks
    assigned, the percentage. percentage of those completed, incomplete,
    and overdue.
    '''
    # Get the total amount of tasks, tasks completed & uncompleted.
    total_tasks = len(task_list)
    completed = sum(1 for task in task_list if task["completed"])
    uncompleted = total_tasks - completed

    # To check overdue tasks.
    today = datetime.today()
    overdue = sum(1 for task in task_list if not task["completed"] and
                  task["due_date"] < today)

    # Calculate percentages.
    percent_incomplete = ((uncompleted / total_tasks) 
                          * 100 if total_tasks != 0 else 0)
    percent_overdue = ((overdue / total_tasks) 
                       * 100 if total_tasks != 0 else 0)

    # Get the total amount of users.
    total_users = len(username_password)

    # Generate "task_overview.txt".
    with open("task_overview.txt", "w") as file:
        file.write("Tasks Overview: \n\n")
        file.write(f"Total number of tasks: {total_tasks}\n")
        file.write(f"Total number of completed tasks: {completed}\n")
        file.write(f"Total number of uncompleted tasks: {uncompleted}\n")
        file.write(f"Total number of overdue tasks: {overdue}\n")
        file.write(f"Percentage of incomplete tasks: {percent_incomplete}\n")
        file.write(f"Percentage of overdue tasks: {percent_overdue}\n")

    # Generate "user_overview.txt".
    with open("user_overview.txt", "w") as file:
        file.write("Users Overview:\n\n")
        file.write(f"Total number of users: {total_users}\n")
        file.write(f"Total number of tasks: {total_tasks}\n\n")

        for username, password in username_password.items():
            user_tasks = sum(1 for task in task_list if task["username"]
                              == username)
            user_completed = sum(1 for task in task_list if task["username"] 
                                 == username and task["completed"])
            user_percent_tasks = ((user_tasks / total_tasks) 
                                  * 100 if total_tasks != 0 else 0)
            user_percent_completed = ((user_completed / user_tasks) 
                                      * 100 if user_tasks != 0 else 0)
            user_percent_remaining = 100 - user_percent_completed
            user_overdue = sum(1 for task in task_list if task["username"] 
                               == username and not task["completed"]
                                 and task["due_date"] < today)
            user_percent_overdue = ((user_overdue / user_tasks) 
                                    * 100 if user_tasks != 0 else 0)

            file.write(f"Username: {username}\n")
            file.write(f"Password: {password}\n")
            file.write(f"Total number of tasks assigned: {user_tasks}\n")
            file.write(f"Percentage of total tasks assigned:" 
                       f"{user_percent_tasks}%\n")
            file.write(f"Percentage of completed tasks:"
                        f"{user_percent_completed}%\n")
            file.write(f"Percentage of tasks remaining:" 
                       f"{user_percent_remaining}%\n")
            file.write(f"Percentage of tasks overdue:" 
                       f"{user_percent_overdue}%\n")



# Displaying statistics.
def display_statistics():
    '''Reads and displays overview reports from "task_overview.txt" and
    "user_overview.txt", and generates them if they don't exist
    '''
    if not (os.path.exists("task_overview.txt") or 
            os.path.exists("user_overview.txt")):
        generate_reports()
    
    with open("task_overview.txt", "r") as file:
        task_overview = file.read()
        print(f"\n{task_overview}")

    print("*" * 78)

    with open("user_overview.txt", "r") as file:
        user_overview = file.read()
        print(f"\n{user_overview}")



# Menu function
def print_menu():
    '''Displays a menu with options:
    r - register user
    a - add task
    va - view all tasks
    vm - view my tasks
    gr - generate reports # Only for admin
    ds - display statistics # Only for admin
    e - exit
    '''
    while True:
        print()
        menu = input('''Select one of the following Options below:
        r - Registering a user
        a - Adding a task
        va - View all tasks
        vm - View my task
        gr - generate reports
        ds - Display statistics
        e - Exit
        : ''').lower()

        if menu == 'r':
            if curr_user == "admin":
                reg_user()
            else:
                print("Only the admin can register a new user.")

        elif menu == 'a':
            add_task()

        elif menu == 'va':
            view_all()

        elif menu == 'vm':
            view_mine()
        
        # Only for admin.
        elif menu == 'gr' and curr_user == "admin":
            generate_reports()

        # Only for admin.
        elif menu == 'ds' and curr_user == "admin":
            display_statistics()

        elif menu == 'e':
            print('Goodbye!!!')
            exit()

        else:
            print("You have made a wrong choice, Please Try again")


# Call the menu
if __name__ == "__main__":
    print_menu()