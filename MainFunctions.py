import re
import csv
import datetime
import pandas as pd
from HelpFunctions import Enterpassword
from HelpFunctions import SaveUserData
from HelpFunctions import start_date
from HelpFunctions import end_date
from HelpFunctions import SaveProjectData




# Menu function in the first screen to choose the action
def Menu():
    choose = input("choose : \n1 :Sign up\t2:Login in\n")
    if choose == "1":
        sign_up()
    elif choose == "2":
        e=log_in()
        Menu2(e)
    else:
        print("please ,enter a valid number\n")
        Menu()

def Menu2(e):
    options = input("choose :\n1 :create project\t2:View All\n3 :edit project\t4"
                    " :delete project\n5 :search by date\n")
    if options == '1':
        EnterProjct(e)
    elif options == '2':
        ViewAll(e)
    elif options == '3':
        editProject(e)
    elif options == '4':
        deleteproject(e)
    elif options == '5':
        Searchdate(e)


# sign up function which take data and save it in DB
def sign_up():
    # First  Name
    First_Name = input("please, Enter your First Name\n")
    while not re.fullmatch("^[A-Za-z]+$", First_Name):
        print("Make sure you only use letters in your name")
        First_Name = input("Please enter your first name again: \n")
    # second name
    Sec_Name = input("please, Enter your second Name\n")
    while not re.fullmatch("^[A-Za-z]+$", Sec_Name):
        print("Make sure you only use letters in your name")
        Sec_Name = input("Please enter your second name again:\n")
    # Email
    Email = input("please, Enter your Email\n")
    while not re.match(r"\b[A-Za-z0-9._%+-]+\@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", Email):
        print("Make sure you enter your Email in right format ")
        Email = input("Please enter your Email again: \n")
    csv_file = csv.reader(open('UsersInfo.csv', "r"), delimiter=",")
    for row in csv_file:
        if Email == row[2] :
            print("this email is already exist")
            Menu()
    # password
    password = Enterpassword()
    # PhoneNumber
    phone = str(input("please, Enter your phone number\n"))
    while not re.match(r"(\+02)* *01+[1,0,2,5][0-9]{8}$", phone):
        print("Make sure you enter your phonenumber in right format  ")
        phone = str(input("Please enter your phone number again: \n"))
    # calling the saving function
    data = [First_Name, Sec_Name, Email, password, phone]
    SaveUserData(data)
    print("welcome")
    Menu()



# ***********login function*********
def log_in():
    email = input("please enter your email\n")
    password = input("please input your password\n")
    csv_file = csv.reader(open('UsersInfo.csv', "r"), delimiter=",")
    for row in csv_file:
        # if current rows 2nd value is equal to input, print that row
        if email == row[2] and password == row[3]:
            print (row[3])
            print("Welcome")
            return email
    print("you enter wrong email or password ")
    log_in()


# **********Option functions***********
# Add project
def EnterProjct(email):
    # Title  Name
    title = input("please, Enter Title to the project\n").title()
    # Details
    details = input("please, Enter description of the project\n")
    # total target
    target = input("please, Enter the total target\n")
    while not re.match(r"[0-9]+$", target):
        print("Make sure you enter your target in number format ")
        target = input("Please enter your target again: \n")
    # start date
    startdate = start_date()
    enddate = end_date(startdate)
    data = [email, title, details, target, str(startdate)[0:10], str(enddate)[0:10]]
    SaveProjectData(data)
    print("project created")
    Menu2(email)





def ViewAll(email):
    with open('projects_data.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row[1:])
    Menu2(email)

def editProject(e):
    df = pd.read_csv("projects_data.csv")
    selected_project = input("please enter the title of the project you want to edit?")
    for idx, row in df.iterrows():
        if row['Email'] == e and row['title'] == selected_project:
            rowindex=idx
    # updating the column value/data
    edit_part=input("which info you want to change?\n1:title\n2:Description\n3:target\n4:Start time\n5:End time")
    if edit_part == '1':
        title = input("please, Enter Title to the project\n").title()
        df.iloc[rowindex, 1] = title
        # writing into the file
        df.to_csv("projects_data.csv", index=False)
    elif edit_part == '2':
        details = input("please, Enter description of the project\n")
        df.iloc[rowindex, 2] = details
        df.to_csv("projects_data.csv", index=False)
    elif edit_part == '3':
        target = input("please, Enter the total target\n")
        df.iloc[rowindex, 3] = target
        df.to_csv("projects_data.csv", index=False)
    elif edit_part == '4':
        startdate = start_date()
        df.iloc[rowindex, 4] = startdate
        df.to_csv("projects_data.csv", index=False)
    elif edit_part == '5':
        start = df.iloc[rowindex, 4]
        enddate = end_date(start)
        df.iloc[rowindex, 5] = enddate
        df.to_csv("projects_data.csv", index=False)
    Menu2(e)

def deleteproject(e):
    df = pd.read_csv("projects_data.csv")
    selected_project = input("please enter the title of the project you want to edit?").title()
    for idx, row in df.iterrows():
        if row['Email'] == e and row['title'] == selected_project:
            rowindex = idx
            df = df.drop(df.index[rowindex])
            print("successfully deleted")
            df.to_csv("projects_data.csv", index=False)
            Menu2(e)
    print("Not founded")
    Menu2(e)



def Searchdate(e):
    date = input("please, Enter the date time in format 'dd/mm/yyyy' :  \n")
    while not re.match(r"[0-9]{2}\/[0-9]{1,2}\/[0-9]{4}$", date):
        print("Make sure you enter date in right format format ")
        date = input("Please enter date again: \n")
    day, month, year = date.split('/')
    if not datetime.datetime(int(year), int(month), int(day)):
        print("input date is not valid,Make sure you enter time in right format format")
        Searchdate(e)
    isexist = 0
    search_date = datetime.datetime(int(year), int(month), int(day), int(00), int(00), int(00))
    csv_file = csv.reader(open('projects_data.csv', "r"), delimiter=",")
    found_list = []
    for row in csv_file:
        if row[0] == 'Email':
            continue
        date1 = datetime.datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S')
        date2 = datetime.datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S')
        if search_date > date1 and search_date < date2:
            found_list.append(row[1])

    if found_list==[]:
        print("there are not available campaign on that date")
    else:
        print("The available campaign(s) :")
        print(found_list)
    Menu2(e)