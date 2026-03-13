import csv
import random
from tabulate import tabulate
from colorama import init, Fore, Style
import re
import os

#colour scheme for different output sections
init(autoreset=True)
section = Fore.CYAN + Style.BRIGHT
comment = Fore.MAGENTA + Style.BRIGHT
success = Fore.GREEN
error_word = Fore.RED
prompt = Fore.YELLOW
menu1 = Fore.MAGENTA
menu2 = Fore.BLUE


def main():
  # main heading and welcoming user
  print(section + "🌟 Routine Planner")
  name = input(comment + "Hey! What's your name? ")
  print(welcome(name))
  # main choices
  while True:
    print()
    print(menu1 + "let's plan your day!")
    print(menu2 + "1. Add task 📝 \n2. View tasks 👀\n3. Delete task 🗑️ \n4. Learning Journal 📚 \n5. Budget tracker 🪙\n6. Side quests 🗺️ \n7. Exit🚪")
    print()
    choice = input(prompt + "Enter your choice: ").strip()
    print()
    if choice not in ['1', '2', '3', '4', '5', '6','7']:
      print(error_word + "Please enter a valid choice!")
    elif choice == '1':
      add_task()
    elif choice == '2': 
      view_task_by_date()  
      
    elif choice == '3':
      # sub choices to delete specific dates or tasks
      while True:
        print(menu2 + "1. Delete specific date \n2. Delete specific task \n3. Go back ")
        choice = input(prompt + "Enter your choice: ").strip()
        print()
        if choice == "1":
          delete_date()
        elif choice == "2":
          delete_task_by_date()
        elif choice == "3":
          break
        else:
          print(error_word + "Please enter a valid choice!")
          
    elif choice == '4':
      print(section + "Welcome to your Learning Journal!")
      # sub choices for learning journal
      while True:
        print(menu2 + "1. Add study session 📘 \n2. View study sessions 📖 \n3. Add notes 📝 \n4. View notes 📄 \n5. Go back ")
        choice = input(prompt + "Enter your choice: ").strip()
        print()
        if choice == "1":
          add_study_session()
        elif choice == "2":
          view_study_sessions()
        elif choice == "3":
          add_notes()
        elif choice == "4":
          view_notes()
        elif choice == "5":
          break
        else:
          print(error_word + "Please enter a valid choice!")
          print()
          
    elif choice == '5':
      print(section + "Welcome to the Budget Tracker!")
      while True:
        print(menu2 + "1. Add income/expense \n2. View transactions \n3. View balance \n4. Go back")
        # sub choices for budget tracker
        choice = input(prompt + "Enter your choice: ")
        print()
        if choice == "1":
          add_budget_entry()
        elif choice == "2":
          view_transaction_history()
        elif choice == "3":
          view_balance()
        elif choice == "4":
          break
        else:
          print(error_word + "Please enter a valid choice!")

    elif choice == '6':
      print(menu1 + "let's create your To-Do list! ")
      print(menu2 + "1. Add task \n2. View list")
      # sub choices for to-do list
      while True:
        todo = input(prompt + "Enter your choice: ").strip()
        print()
        if todo == '1':
          add_task_todo()
          break
        elif todo == '2':
          if view_todo_list() == ("To-Do list is empty :("):
            print(success + "To-Do list is empty :(")
            break
          else:
            mark_completion()
            break
        else:
          print(error_word + "Please enter a valid choice!")

    else:
      print(success + "Thank you for visiting! :)")
      break

# order of functions: welcome, option 6, 1, 2, 5, 3, 4

#########################################################################################################################

# for welcoming the user by taking name as input
def welcome(x):
  return f"🌈 Hello {x}! Let's turn ideas into action it's time to conquer the day!"

########################################################################################################################

# part 6 side quest part 1
# takes task and priority level as input
def add_task_todo():
  task = input(prompt + "Enter task: ")
  while True:
    priority = input(prompt + "Enter priority level (High/Medium/Low): ")
    if priority.lower() in ["high", "medium", "low"]:
      break
  # opens/creates csv file To-Do.csv and writes the data    
  with open("To-Do.csv", "a+", newline="") as newfile:
    writer = csv.writer(newfile)
    writer.writerow([task, priority.title(), ""])
  print(success + "Task added to To-Do list!")
  print()


# part 6 side quest part 2
# opens To-Do.csv in read mode and reads all the information and prints it in a tabular form
def view_todo_list():
  l = []
  try:
    with open("To-Do.csv", "r") as myfile:
      reader = csv.reader(myfile)
      for row in reader:
        l.append(row)
      for i in range(0, len(l)):
        l[i].insert(0, i + 1)  
      l.insert(0, ["No.", "Task", "Priority", "Completion Status"])  # for adding heading to the table of date
      print(tabulate(l, headers="firstrow", tablefmt="grid"))
      print()
  except:
    return ("To-Do list is empty :(")


# part 6 side quest part 3
# for taking serial number from displayed table as input and placing tick mark emoji to mark complete    
def mark_completion():
  while True:
    ans = input(prompt + "Do you want to mark any task as completed? (Yes/No) ").lower().strip()
    if ans == "yes":
      while True:
        try:
          num = int(input(prompt + "Enter the serial number of the task: "))
          break
        except ValueError:
          print(error_word + "Please enter a valid number!")

      m = []
      with open("To-Do.csv", "r") as myfile:
        reader = csv.reader(myfile)
        for row in reader:
          m.append(row)

      if 1 <= num <= len(m):
        m[num - 1][2] = "Done" 
        with open("To-Do.csv", "w", newline="") as newfile:
          writer = csv.writer(newfile)
          for row in m:
            writer.writerow(row)
        print(success + "Task marked as completed!")
        print()
      else:
        print(error_word + "Invalid serial number")
      break
    elif ans == "no":
      break
    else:
      print(error_word + "Please enter a valid choice!")


################################################################################################


# option 1
def add_task():
# takes date, time, task as input from user
  while True:
    date = input(prompt + "Enter a date (DD-MM-YYYY): ")
    if matches := re.search(r"^(0?[1-9]|[1-2][0-9]|3[0-1])-(0?[1-9]|1[0-2])-([1-9][0-9][0-9][0-9])$", date):
      break
    else:
      print(error_word + "Please enter a valid date :(")

  while True:
    time_input = input(prompt + "Enter a time slot in meridiem time (__ am/pm to __ am/pm): ")
    time = convert(time_input)
    if time:
      task = input(prompt + "Enter task: ")
      break
    else:
      print(error_word + "Please enter a valid time :(")

  # creates a csv file for that date and writes the data
  with open(f"{date}.csv", "a+", newline="") as newfile:
    writer = csv.writer(newfile)
    writer.writerow([time, task])

  #to keep track of the list of dates the user added tasks to
  try:
    with open("date_list.csv", "r") as myfile:
      reader = csv.reader(myfile)
      track_of_dates_list = list(reader)
      # to check if the date is already there in the csv file
      if [date] not in track_of_dates_list:
        with open("date_list.csv", "a") as myfile:                  
          myfile.write(date + "\n")
  # creates the csv file if the date_list.csv does not exist already
  except FileNotFoundError:     
    with open("date_list.csv", "a") as myfile:                   
      myfile.write(date + "\n")
  
  print(success + "Task added successfully!")
  print()


# changes user input time from meridiam time to 24 hour clock time
def convert(s):
  s = s.lower()
  if matches := re.search(r"^(([1-9]|1[0-2])(:[0-5][0-9])?) (am|pm) to (([1-9]|1[0-2])(:[0-5][0-9])?) (am|pm)$", s):
    new_list = s.split("to")
    new_list[0] = new_list[0].strip()
    new_list[1] = new_list[1].strip()

    output = []
    for time in new_list:

      if "am" in time:
        if ":" in time:
          time_list = time.split(" ")
          hour, min = time_list[0].split(":")
          hour = int(hour)
          if hour < 10:
            output.append(f"0{hour}:{min}")
          elif 9 < hour < 12:
            output.append(f"{hour}:{min}")
          else:
            output.append(f"00:{min}")

        else:
          time_list = time.split(" ")
          hour = int(time_list[0])
          if hour < 10:
            output.append(f"0{hour}:00")
          elif 9 < hour < 12:
            output.append(f"{hour}:00")
          else:
            output.append("00:00")

      if "pm" in time:
        if ":" in time:
          time_list = time.split(" ")
          hour, min = time_list[0].split(":")
          hour = int(hour)
          if hour < 12:
            hour = hour + 12
            output.append(f"{hour}:{min}")
          else:
            output.append(f"12:{min}")

        else:
          time_list = time.split(" ")
          hour = int(time_list[0])
          if hour < 10:
            hour = hour + 12
            output.append(f"{hour}:00")
          else:
            output.append("12:00")

    return f"{output[0]} to {output[1]}"
  else:
    return None


############################################################################################################


# option 2
def view_task_by_date():
  # opens date_list.csv to display all the user input dates in the system
  try:
    with open("date_list.csv", "r") as myfile:
      dates = myfile.readlines()
    print(section + "Your saved dates 📚")
    for i in range(len(dates)):
      print(f"{i+1}.{dates[i].strip()}")
    print()
    # takes date as input from user (one out of the dates exsisting in the displayed list)
    while True:
      date = input(prompt + "Enter a date (DD-MM-YYYY): ")
      if matches := re.search(r"^(0?[1-9]|[1-2][0-9]|3[0-1])-(0?[1-9]|1[0-2])-([1-9][0-9][0-9][0-9])$", date):
        break
      else:
        print(error_word + "Please enter a valid date :(")
    # opens the csv file for that specific date and displays the list of task in tabular format
    l = []
    try:
      with open(f"{date}.csv", "r") as myfile:
        reader = csv.reader(myfile)
        for row in reader:
          l.append(row)
        for i in range(0, len(l)):
          l[i].insert(0, i + 1)
        l.insert(0, ["No.", "Time", "Task"])
        print(tabulate(l, headers="firstrow", tablefmt="grid"))
        print()
    except:
      print(success + "No record found!")
      print()
  # incase no tasks have been added to any dates
  except FileNotFoundError:
    print(success + "No tasks are added to any date yet!")
    print()


###############################################################################################################

# functions for budget tracker


# part 5 option 1
def add_budget_entry():
  # takes date, income/expense, description and amount as input from user
  while True:
    date = input(prompt + "Enter a date (DD-MM-YYYY): ")
    if matches := re.search(r"^(0?[1-9]|[1-2][0-9]|3[0-1])-(0?[1-9]|1[0-2])-([1-9][0-9][0-9][0-9])$", date):
      break
    else:
      print(error_word + "Please enter a valid date :(")
  while True:
    entry_type = input(prompt + "Enter type (income/expense): ").strip().lower()
    if entry_type not in ['income', 'expense']:
      print(error_word + "Invalid type! Must be 'income' or 'expense'!")
    else:
      break
  desc = input(prompt + "Enter description: ")
  while True:
    try:
      amount = float(input(prompt + "Enter amount: "))
      break
    except:
      print(error_word + "Invalid type!")

  # checking balance
  last_balance = 0
  try:
    with open('budget.csv', 'r') as file:
      reader = csv.reader(file)
      rows = list(reader)
      if rows:
        last_row = rows[-1]
        if len(last_row) >= 5:
          last_balance = float(last_row[-1])
  except FileNotFoundError:
    pass

  # updating balance amount
  if entry_type == "income":
    balance = last_balance + amount
  else:
    balance = last_balance - amount
  # opens budget.csv and writes all the data in file
  with open('budget.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([date, entry_type, desc, amount, balance])
  print(success + "Transaction added.")
  print()


# part 5 option 2
def view_transaction_history():
  # opens csv file in read mode and prints the data in tabular format
  l = []
  try:
    with open("budget.csv", "r") as myfile:
      reader = csv.reader(myfile)
      for row in reader:
        l.append(row)
      for i in range(0, len(l)):
        l[i].insert(0, i + 1)
      l.insert(0, ["No.", "Date", "Type", "Description", "Amount", "Balance"])
      print(tabulate(l, headers="firstrow", tablefmt="grid"))
      print()    
  except FileNotFoundError:
    print(success + "No transactions found :(")  # if file does not exist
    print()


# part 5 option 3
# opens budget.csv and reads the balance column to display the remaining balance
def view_balance():
  try:
    with open('budget.csv', 'r') as file:
      reader = csv.reader(file)
      rows = list(reader)
      if rows:
        last_row = rows[-1]
        if len(last_row) == 5:
          balance = float(last_row[-1])
          print(success + f"Current Balance: {balance}")
          print()
      else:
        print(success + "No transactions to show balance")
        print()
  except FileNotFoundError:
    print(success + "No budget file found :(")
    print()


##############################################################################################################

# option 3 part 1 
# for deleting all the tasks of a specific date
def delete_date():
  while True:
    # takes date as input from user to delete
    date = input(prompt + "Enter a date (DD-MM-YYYY): ")
    if re.search(r"^(0?[1-9]|[1-2][0-9]|3[0-1])-(0?[1-9]|1[0-2])-([1-9][0-9][0-9][0-9])$", date):
      break
    else:
      print(error_word + "Please enter a valid date :(")
      
  date_to_delete = f'{date}.csv'
  try:
    os.remove(date_to_delete)      # deletes the csv file of that specific date
    print(success + f"Successfully deleted all tasks of {date}")
    print()
  except:
    print(error_word + "No record found!")
    print()

  # updates date_list.csv by removing the entry of that date
  new_list = []
  with open("date_list.csv", "r") as myfile:
    reader = csv.reader(myfile)
    dates_on_list = list(reader)
    for i in dates_on_list:
      if i[0] != f"{date}":
        new_list.append(i)
  
  with open("date_list.csv", "w", newline='') as myfile:
    writer = csv.writer(myfile)
    writer.writerows(new_list)
    

# option 3 part 2
# for deleting a specific task from the list of tasks of a specific date
def delete_task_by_date():
  # takes date as user input
  while True:
    date = input(prompt + "Enter a date (DD-MM-YYYY): ")
    if re.search(r"^(0?[1-9]|[1-2][0-9]|3[0-1])-(0?[1-9]|1[0-2])-([1-9][0-9][0-9][0-9])$", date):
      break
    else:
      print(error_word + "Please enter a valid date :(")
  # opens the csv file of the date given by user and displays the list of task in tabular format
  try:
    with open(f"{date}.csv", "r") as file:
      reader = csv.reader(file)
      tasks = list(reader)
    if not tasks:
      print(success + "No tasks found for this date :(")
    display = []
    for i in range(len(tasks)):
      row = [i + 1]
      row.extend(tasks[i])
      display.append(row)
    display.insert(0, ["No.", "Time", "Task"])
    print(tabulate(display, headers="firstrow", tablefmt="grid"))
    print()

    # taking serial number as input to delete the specific task
    while True:
      try:
        to_delete = int(input(prompt + "Enter the serial number of the task you want to delete: "))
        if 1 <= to_delete <= len(tasks):
          break
        else:
          print(error_word + "Please enter a number from the list")
      except ValueError:
        print(error_word + "Enter a valid number!")
    deleted_task = tasks.pop(to_delete - 1)

    # after deleting task rewrites the updated list on the csv file of that specific date
    with open(f"{date}.csv", "w", newline='') as myfile:
      writer = csv.writer(myfile)
      writer.writerows(tasks)
    print(success + "Task deleted successfully :)")
    print()
  except FileNotFoundError:
    print(success + "No tasks found for this date :(")
    print()


##############################################################################################################

# functions for study planner

# for motivating user according to the amount of time they spend over each subject!
def feedback(minutes):

  if minutes <= 60:
    messages = [
        "Good start! Every minute counts. Keep going! 💪",
        "Awesome! Even short sessions build up over time. 📈",
        "One step at a time. You're doing great! 🌱",
        "You showed up, and that's what matters most today. 🌟",
        "Solid focus! Consistency is key. 🔐"]
    print(comment + random.choice(messages))
    return "Good start!"

  elif minutes <= 120:
    messages = [
        "You're in the zone! Keep that momentum going. 🚀",
        "Nice! That's a focused block of study. 🧠",
        "Great commitment! You're getting ahead. 🎯",
        "You've built a solid foundation for today! 🧱",
        "Amazing effort! Two hours of deep work. 🏆"]
    print(comment + random.choice(messages))
    return "You're in the zone!"

  elif minutes <= 300:
    messages = [
        "Wow! Your focus is top-notch today. Keep it up! 🔥",
        "Impressive! This is how goals get crushed. 💼",
        "You're building serious discipline. Keep going! 💯",
        "Incredible stamina! Don't forget to hydrate. 💧",
        "You're doing awesome! Be sure to stretch a bit! 🤸"]
    print(comment + random.choice(messages))
    return "Impressive!"

  elif minutes <= 360:
    messages = [
        "Amazing focus! Maybe take a small break? 🧘",
        "Incredible dedication — but don't forget rest matters too! 😌",
        "You've earned a breather. Great work! ☕",
        "Five hours?! You're a machine! Just make sure to rest. ⚙️",
        "That's some serious commitment! Respect! 🫡"]
    print(comment + random.choice(messages))
    return "Incredible dedication"

  elif minutes <= 480:
    messages = [
        "Whoa! That's a long stretch. Break it up next time for better retention. 🔄",
        "You're going strong — maybe *too* strong. Avoid burnout! 🛑",
        "Consider smaller study chunks with breaks. It improves learning. 📚",
        "Don't overdo it — your brain needs rest too! 🧠💤",
        "Great work ethic, but don't forget to breathe. 🌬️"]
    print(comment + random.choice(messages))
    return "Don't overdo it"

  else:
    messages = [
        "8+ hours is marathon mode. Try spacing sessions across the day. ⏳",
        "Overstudying can hurt more than help. Quality > Quantity. ⚖️",
        "Take care of your health. No success without well-being. ❤️",
        "Break this into chunks — over 8 hours is not sustainable. 💀",
        "Rest is productivity. Don't drain yourself. ⚠️💤"]
    print(comment + random.choice(messages))
    return "Don't drain yourself"


# option 4 part 1
def add_study_session():
  # takes date,subject and topic as input from user
  while True:
    date = input(prompt + "Enter date (DD-MM-YYYY): ")
    if re.search(r"^(0?[1-9]|[1-2][0-9]|3[0-1])-(0?[1-9]|1[0-2])-([1-9][0-9]{3})$", date):
      break
    else:
      print(error_word + "Invalid date format!")
  subject = input(prompt + "Enter subject: ")
  topic = input(prompt + "Enter topic: ")
  # takes input of how much time they'll spend on a topic in minutes
  while True:
    try:
      minutes = int(input(prompt + "Enter time spent (in minutes): "))
      if minutes <= 0:
        print("Enter a positive number!")
      else:
        feedback(minutes)
        break
    except ValueError:
      print(error_word + "Enter a valid number!")
      continue
  # changes just minutes to hours and minutes format
  hours = minutes // 60
  mins = minutes % 60
  time = f"{hours}h {mins}m"

  # writes the data in a csv file
  with open("study_sessions.csv", "a", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([date, subject, topic, time])
  print(success + "Study session added!")
  print()


# option 4 part 2
# opens study_sessions.csv and displays all the data(study plans) in a tabular format  
def view_study_sessions():
  l = []
  try:
    with open("study_sessions.csv", "r") as file:
      reader = csv.reader(file)
      for row in reader:
        l.append(row)
      for i in range(len(l)):
        l[i].insert(0, i + 1)
      if l:
        l.insert(0, ["No.", "Date", "Subject", "Topic", "Time Spent"])
        print(tabulate(l, headers="firstrow", tablefmt="grid"))
        print()
      else:
        print(success + "No study sessions found!")
        print()
  except FileNotFoundError:
    print(success + "No study sessions recorded yet")
    print()


# option 4 part 3
def add_notes():
  # takes title and content from user  
  print(section + "let's write a new note! ")
  title = input(prompt + "note title: ").strip()
  content = input(prompt + "Write your note :")
  # writes the content on a csv file with title as the name of file
  with open(f"{title}.txt", "w") as myfile:
    myfile.write(content)
  # logging the note title into another csv file
  with open("notes_list.csv", "a") as myfile:
    myfile.write(title + "\n")
  print(success + "Note saved successfully!")
  print()


# option 4 part 4
def view_notes():
  # displays the list of all note titles logged into the system
  print(section + "Your saved notes 📚")
  try:
    with open("notes_list.csv", "r") as myfile:
      titles = myfile.readlines()
    if not titles:
      print(success + "No notes added yet!")
    for i in range(len(titles)):
      print(f"{i+1}.{titles[i].strip()}")
    print()
    # takes serial number of the note user wants to open as input
    while True:
      try:
        choice = int(input(prompt + "Enter the serial number of the note you want to open: "))
        if 1 <= choice <= len(titles):
          break
        else:
          print(error_word + "Please enter a number from the list")
      except:
        print(error_word + "Enter a valid number!")
    note_title = titles[choice - 1].strip()
    # opens the csv file in read mode and displays the title and content 
    print(f"--- {note_title} ---")
    with open(f"{note_title}.txt", "r") as myfile:
      print(myfile.read())
    print()
  except FileNotFoundError:
    print(success + "No notes added yet!")
    print()


if __name__ == "__main__":
  main()
