import re
import datetime
import csv
import os
# **********************helpful functions for Sign up function *************
# Enter password function
def Enterpassword():
    password = input("please Enter your password\n")
    while not CheckValidPass(password):
        password = input("please Enter your password again\n")
    password1 = input("please Enter again to confirm password\n")
    while not password1 == password:
        print("they are not the same, please try again ")
        Enterpassword()
    return password


# Check the strength of the password
def CheckValidPass(password):
    if len(password) < 8:
        print("Password length must be greater than 8")
        return False
    elif len(password) > 18:
        print("Password length must be less than 18")
        return False
    elif re.search('[0-9]', password) is None:
        print("Password must contain a number")
        return False
    elif re.search('[A-Z]', password) is None:
        print("Password must contain a capital letter")
        return False
    else:
        return True


# function to save data in a file
def SaveUserData(data):
    with open('UsersInfo.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)


# ************************** helpful functions for Enter project function ****************
def start_date():
    stime = input("please, Enter the start time in format 'dd/mm/yyyy' :  \n")
    while not re.match(r"[0-9]{2}\/[0-9]{1,2}\/[0-9]{4}$", stime):
        print("Make sure you enter time in right format format ")
        stime = input("Please enter start time again: \n")
    day, month, year = stime.split('/')
    if not datetime.datetime(int(year), int(month), int(day)):
        print("input date is not valid,Make sure you enter time in right format format")
        start_date()
    today = datetime.datetime.now()
    d1 = datetime.datetime(int(year), int(month), int(day))
    if d1 < today:
        print("it can't be before today")
        start_date()
    return d1


def end_date(d1):
    day1 = d1
    # end time
    etime = input("please, Enter the end time\n")
    while not re.match(r"[0-9]{2}\/[0-9]{1,2}\/[0-9]{4}$", etime):
        print("Make sure you enter time in right format format ")
        etime = input("Please enter end time again: \n")
    day2, month2, year2 = etime.split('/')
    if not datetime.datetime(int(year2), int(month2), int(day2)):
        print("input date is not valid,Make sure you enter time in right format format")
        end_date(day1)
    d2 = datetime.datetime(int(year2), int(month2), int(day2))
    today = datetime.datetime.now()
    if d2 < today:
        print("it can't be before today")
        end_date(day1)
    if d2 < day1:
        print("it can't be before start date")
        end_date(day1)
    if not datetime.datetime(int(year2), int(month2), int(day2)):
        print("input date is not valid,Make sure you enter time in right format format")
        end_date(day1)
    return d2


def SaveProjectData(data):
    with open('projects_data.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)


