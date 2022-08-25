import numpy as np
import pandas as pd
import random as rnd
from random import randint
from datetime import datetime, timedelta
import time
import sys, os
import csv
import gspread
from pygsheets import *
from gspread_dataframe import set_with_dataframe, get_as_dataframe
from gspread_formatting import *
from oauth2client.service_account import ServiceAccountCredentials

# A function to return the full path of the files.
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

cred = {
  "type": "service_account",
  "project_id": "tidy-simplicity-354613",
  "private_key_id": "40f29104243f40ebf97cefa92096a3c5b6c1b60b",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCzvCRPq+ohmIT1\nGZIRqezcOz2rfvOKbVp5s/+wUKNJXGT6CcHu8JT67mc/hfnvpqzpJ6lQ1um59S8d\n2wYBGYGiQ/n1bwK2uaa0Tgp2LFrOagsSTQ8w5J9qg94lyfmleFLxtWTUhRGAvOrG\nvWFKxKtPOCrhuJ54lbtPaCgx27boippxoeZhDntu9HM95sgYrLPY+GGElV7YYzZR\nxX3KMcljCCUEuZD3zceDHqNZFDqDoxu24mHviILZJCCjgT0DPJVrUuzxkS9Ay+h7\nevdZdGPgB/LtwG33b/vKwFwMhTZKZw5/XrBVVkVDh3l22CvQXXqm8gEDLMuLxaG0\nBqrTfsjZAgMBAAECggEABz5do0VdMAHu19byO1qDFIQhsePxqkJKe22s8Bzr28TI\nwAf9JCVXh75sdFOwtT8dKF9kFEE5FbjDL5uYZBp0TkcZj5HsBNO6G3mqs8UJWtjM\nve3TnyeToi4S2aiIcmoFQ78JA4SiZjMW7jALOAFxmwV7OvIfFuKH9EURG6NMfZYo\n95yRdeEZPwtdqukKMha/RSt/0dKpKCAswdltfUkU0TPhTwswfq0HmFcTDa+lSjLT\nrhWFjl36CEmsVDMbjM3q0e3030Ikyi6ErYsxn+UllGKyoCJ3nDdOmWwGLVNVCEG1\nqq/s961JOCWS1CthMxcNsJDKSKr0AjO6Q0GMcU68lQKBgQD3tu8HnP65J7IESA7G\n9SuMUd3liMq2eHbDlOK2f5H6Kot1SsZ7fjh8kJdmIFJV7WSPdkR6xmc754kkW/ik\njri0S1Du7rB4OZQUoTes3KGUe36dAvXFBIkoNdJcruG5IBueyUUTSBkxxb1rSDK3\nid/pOxWUYvA2VzHotNlwnjNUlQKBgQC5vyEpmJwXp4SpChSrIW0a1rl278AxIXLF\njpAFbFjNhWzpNaYS/gDBR5xnME5D4MqpudMf8c67ZXU46uehHTbWTwNkgvYIlQ94\n7prkzk9iRxGoamIByTVN4J1+IeiPmKrdgwMi6vORyiMIqIH+JwOikLff2SHWyJS+\nZuETEJ2uNQKBgCWcyjiOtwKoK1iJFG1TRrR8rcOvfJAuRGI4FiB9yE2C7j/2BaM0\nrCEF12czWy0e6Zj67TTzMTOgWWuC54MdBKCjmvtclMD8hSaIwCpoKcSg572xeF3c\n7XKEkZdvGmkAnhEDIJDn7qNnEfbbNJA3yB7i0MkCKNUncjWSWD3IV6TtAoGAdZm6\nEFDr+tn31uJoBZUrM8PhNplCsJiBxuyk6JoZez3Pn7N0yy+AIN8K+hYOZ1FqXp0l\nO2NoRSNOXVP0hQAvGO57smZsCTD+080VymmIvytJ1bxNAt52XjEo5ZPoXwoEnCx3\njuL8hUBaf//YFaZz2bgQgqxBjW//JLGULPLnMkUCgYBY+WrPqsRtRzHjxq5N1+Ox\nGQu1XKzL75ETERuogXLiMdUsYlXsLQhKyNHUyaGiY3c8+RV2UFC8tokTvwCymrWX\nLyd1leiwEI0t08M0qNPAqCH+7/YahpugN9iHCoTuOZRBWkFzrWw0pf9eIO5oDAu1\nfcNCZF9WIZu80re2jbMk0g==\n-----END PRIVATE KEY-----\n",
  "client_email": "weekly-schedule-project-cbk-op@tidy-simplicity-354613.iam.gserviceaccount.com",
  "client_id": "103233759909625199450",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/weekly-schedule-project-cbk-op%40tidy-simplicity-354613.iam.gserviceaccount.com"
}

# Creating a service account in order to have access to the Google Sheets file.
sa = gspread.service_account_from_dict(cred)
key = '1HUQEUv-1SjHNL-xW7aN3EFGBuhLnt8fPBMkZKIDVihI' # SheetId
sheet = sa.open_by_key(key) # Entering into the sheet file.
wks = sheet.get_worksheet(-1) # First worksheet.

# Creating a dataframe to organize from the Google Sheets file.
df = get_as_dataframe(wks, evaluate_formulas=True)

# Using the google sheet file in order to fetch the name, email and tier of the analyst.
# in order to use them for later usage when arranging the shifts.
info_sa = gspread.service_account_from_dict(cred)
info_key = '1BeDEhxAYmopiDIKMu9grJFe7DxWzlPsmlfrKr9MVdJs' #analysts info sheetId
info_sheet = info_sa.open_by_key(info_key)
info_wks = info_sheet.get_worksheet(0)
emails_df = get_as_dataframe(info_wks, evaluate_formulas=True, usecols=[0,1,2]).dropna()

# Creating a service account in order to have access to the Google Sheets policy file.
policy_sa = gspread.service_account_from_dict(cred)
policy_key = '1LsHGTKCLi4ZV6cpEflUXqLPUNpi8HBxusW7-vLunrl4' # SheetId
policy_sheet = policy_sa.open_by_key(policy_key) # Entering into the sheet file.
policy_wks = policy_sheet.get_worksheet(-1) # First worksheet.
policy_val = policy_wks.acell('A2').value.lower()

#Giving columns names:
Days = ["Sunday", "Monday", "Tuesday","Wednesday","Thursday"]
Options = ["in","out","hours","place"]
columns = ["Name"]
for i in Days:
    for j in Options:
        temp = i + "_" + j
        columns.append(temp)
columns.append("Total")
columns.append("Notes")
df.columns = columns
df.reset_index(inplace=True)
df.drop([0], inplace=True)
df.reset_index(inplace=True)
df.drop(['index', 'level_0'], axis=1, inplace=True)


num_of_analysts = len(df['Name']) # Getting the analysts amount number.
spots_in_office = 14 # how many spots are in the office

df.fillna('', inplace=True)
received = df.copy()


# A function to return a list of the analyst who only asked to work from home.
def dudes_without_office(df):
    global bad_analysts 
    bad_analysts = []
    place_mat = df[["Sunday_place", "Monday_place","Tuesday_place","Wednesday_place","Thursday_place"]]
    place_mat = place_mat.replace("Office - Full Shift" , 1)
    place_mat = place_mat.replace("Home - Full Shift" , 0)
    place_mat = place_mat.replace("",0)

    sums = place_mat.sum(axis = 1, numeric_only=True)
    for i in range(len(sums) - 1):
        try:
            if (sums[i] == 0) and (float(df["Total"][i]) > 0):
                bad_analysts.append(df["Name"][i])
        except Exception as e:
            pass
        
    return bad_analysts

place_header = ["Sunday_place","Monday_place","Tuesday_place","Wednesday_place","Thursday_place"]
random_lst = [x for x in range(0,num_of_analysts)]
rnd.shuffle(random_lst)

# a function to count how many available spots are in the office each day.
def counter():
    count = 0
    ind = 0
    count_array = [0,0,0,0,0]
    for i in place_header:
        for j in range(0,num_of_analysts):
            if "Office" in received.loc[j,i]:
                count += 1
        count_array[ind] = spots_in_office - count
        ind += 1
        count = 0
    return count_array

dudes_without_office(df)

# Creating a dictionary to get the working analysts and their index number in the dataframe.
def dic(df):
    d = {x:i for i,x in enumerate(df["Name"]) if df["Name"][i] not in bad_analysts and df['Total'][i] != 0}
    return d

# A function to create the analyst names in different order.
def rotated_list(lst):
    return lst[int(len(lst)/2):] + lst[:int(len(lst)/2)]

# Creating different combinations to run the system fairly.
d = dic(df)
fair1 = [x for x in d.values()]
fair2 = fair1[::-1]
fair3 = rotated_list(fair1)
fair4 = fair3[::-1]

fairs = [fair1, fair2, fair3, fair4]
fair = rnd.choice(fairs)

# Creating the fairness system in the dataframe.
def fairness(lst):
    screwed = []
    d = {}
    count_office = 0
    actual_working_analysts = len(df['Name'].loc[df["Total"] > 0]) - len(bad_analysts)
    names_that_got_office = []
    for i in place_header:
        for j in fair:
            if "Office" in df.loc[j, i] and lst[fair.index(j)] == min(lst) and count_office < spots_in_office:
                received.loc[j, i] = df.loc[j, i]
                lst[fair.index(j)] += 1
                names_that_got_office.append(df["Name"].iloc[j])
                count_office += 1
            elif "Office" in df.loc[j, i] and lst[fair.index(j)] != min(lst) and count_office < spots_in_office:
                received.loc[j, i] = "Home - Full Shift"
                screwed.append(j)
            elif "Office" in df.loc[j, i] and count_office == spots_in_office:
                received.loc[j, i] = "Home - Full Shift"
            elif "Home" in df.loc[j, i]:
                received.loc[j, i] = "Home - Full Shift"
            
        for j in screwed:
            if "Office" in df.loc[j, i] and count_office < spots_in_office and "Home" in received.loc[j, i]:
                received.loc[j, i] = df.loc[j, i]
                lst[fair.index(j)] += 1
                count_office += 1
            if count_office == spots_in_office:
                continue
        count_office = 0
        if actual_working_analysts == len(names_that_got_office):
            names_that_got_office = []
    return lst
 

lst = [0 for x in range(len(fair))]
print(fairness(lst))
print(counter())

# Sending the dataframe into the Google Sheets.
def create_date_to_sheet_name():
    sunday_date = datetime.today() - timedelta(days=datetime.today().isoweekday() % 7)
    date = sunday_date + timedelta(days=7)
    date = date.strftime('%m/%d/%y')
    return date

wks.add_rows(num_of_analysts+3)
wks = sheet.get_worksheet(-1)
sheetId = sheet.get_worksheet(-1)._properties['sheetId']

# Making the sheet sides borders more thicker.
requests9 = {
  "requests": [
    {
      "updateBorders": {
        "range": {
          "sheetId": sheetId,
          "startRowIndex": num_of_analysts+5,
#           "endRowIndex": num_of_analysts*2+6,
          "startColumnIndex": 0,
          "endColumnIndex": 23
        },
        "left": {
          "style": "SOLID_THICK",
          "color": {
            "blue": 0.0
          },
        },
        "right": {
          "style": "SOLID_THICK",
          "color": {
            "blue": 0.0
          },
        },
        "innerVertical": {
          "style": "SOLID_THICK",
          "width": 0,
          "color": {
            "blue": 0.0
          },
        },
      }
    }
  ]
}
res9 = sheet.batch_update(requests9)

# Making the top and bottom more borders more thicker.
requests10 = {
  "requests": [
    {
      "updateBorders": {
        "range": {
          "sheetId": sheetId,
          "startRowIndex": num_of_analysts+5,
#           "endRowIndex": num_of_analysts*2+6,
          "startColumnIndex": 0,
          "endColumnIndex": 23
        },
        "innerHorizontal": {
          "style": "SOLID",
          "width": 0,
          "color": {
            "blue": 0.0
          },
        },
          "top": {
          "style": "SOLID_THICK",
          "color": {
            "blue": 0.0
          },
        },
          "bottom": {
          "style": "SOLID_THICK",
          "color": {
            "blue": 0.0
          },
        },
      }
    }
  ]
}
res10 = sheet.batch_update(requests10)

set_with_dataframe(wks, received, row=num_of_analysts+6, include_column_header=False)

# Getting the analysts who only took home shifts.
vacation = []
if len(dudes_without_office(df)) > 0:
    home_analysts_names = ', '.join(dudes_without_office(df))
else:
    home_analysts_names = 'None'

# Creating a long string with all the available spots in the office for each day.
spots = counter()
days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']

spots_lst = []
for day, spot in zip(days, spots):
    spots_lst.append(f"{day}'s available spots: {spot}.")
    
if len(spots_lst) > 0:
    empty_spots = '\n'.join(spots_lst)
else:
    empty_spots = 'None'

if len(vacation) > 0:
    vac = ', '.join(vacation)
else:
    vac = 'None'
    
# Getting all the analysts that have worked more than the hours they need.
if policy_val == 'min':
    my_message = (
    f'The analysts who only took home shifts are: {home_analysts_names}. \n\n'
    f'{empty_spots} \n\n'
    f'The analysts who are not working this week are: {vac}.'
    )
elif policy_val == 'max':
    workoholics = []
    vacation = []
    for i,h in enumerate(received["Total"]):
        if emails_df['Status'].iloc[i] == 'Tier 1' and h > 15:
            workoholics.append(received['Name'].iloc[i])
        elif emails_df['Status'].iloc[i] == 'Tier 2' and h > 20:
            workoholics.append(received['Name'].iloc[i])
        elif h == 0:
            vacation.append(received['Name'].iloc[i])

    if len(workoholics) > 0:
        more_than_expected = '\n'.join(workoholics)
    else:
        more_than_expected = 'None'
    my_message = (
    f'The analysts who only took home shifts are: {home_analysts_names}. \n\n'
    f'The analysts who worked more hours than they should are: {more_than_expected}. \n\n'
    f'{empty_spots} \n\n'
    f'The analysts who are not working this week are: {vac}.'
    )

# Getting Sunday's date for each week to add to the email subject.
def sunday_date_week():
    sunday_date = datetime.today() - timedelta(days=datetime.today().isoweekday() % 7)
    date = sunday_date + timedelta(days=7)
    date = date.strftime('%m/%d/%y')
    return date

print(my_message)

#To generate a passowrd - go to cbk ops gmail settings -> security -> Signing in to Google -> app passwords. 
#Then, choose windows computer on device and mail on app type. Afterwards click generate and copy the password.
import smtplib

def send_email(author_email, receiver_email):
    password = 'uirlpcuqhbtivzak' #password for my work email
    subject = f'Weekly Schedule Info for Week {sunday_date_week()}'

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (author_email, receiver_email, subject, my_message)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(author_email, password)
        server.sendmail(author_email, receiver_email, message.encode("utf8"))
        server.close()
        print(f'Successfully sent the mail to {receiver_email}')
    except:
        print("Failed to send mail")
    
# send_email('tom@justt.ai', ['dan.b@justt.ai', 'ayala@justt.ai'])
# send_email('tom@justt.ai', 'roy@justt.ai')
send_email('tom@justt.ai', 'tom@justt.ai')