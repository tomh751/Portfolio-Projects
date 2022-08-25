import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import tkinter as tk
from tkinter import ttk
from tkinter import *
import calendar
import sys, os
from pathlib import Path
# import openpyxl
import gspread
from gspread_formatting import *
from gspread_dataframe import set_with_dataframe, get_as_dataframe
from gspread_formatting import *
from gspread_pandas import *
from pygsheets import *
from gspread import *
from oauth2client.service_account import ServiceAccountCredentials

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

def create_new_gsheet():
    info_sa = gspread.service_account_from_dict(cred)
    info_key = '1BeDEhxAYmopiDIKMu9grJFe7DxWzlPsmlfrKr9MVdJs' #analysts info sheetId
    info_sheet = info_sa.open_by_key(info_key)
    info_wks = info_sheet.get_worksheet(0)
    emails_df = get_as_dataframe(info_wks, evaluate_formulas=True, usecols=[0,1,2]).dropna()
#     emails_df = pd.read_excel(resource_path('analysts email and names.xlsx'))

    # Analysts names.
    analysts = [name.title() for name in emails_df['Name']]
    time_range = pd.date_range('08:00','20:00',freq='1h')
    time_lst = time_range.strftime('%H:%M:%S')
    time_lst # List that have time range between 8AM to 8PM.

    # Time range to use for entering the hour you start your shift.
    start_shift = time_lst.copy().tolist()

    # Time range to use for entering the hour you end your shift.
    end_shift = time_lst.copy().tolist()

    days = list(calendar.day_name)
    sunday = days[-1]
    rest_of_the_week = days[:-3]

    # An organized week list from Sunday-Thursday.
    week = [sunday] + rest_of_the_week

    # Option where you choose to work.
    workplace = ['Home','Office']

    # List of the subcolumn name.
    headers = ['In', 'Out', 'Hours', 'Workplace']

    # Creating the MultiIndex dataframe.
    mux = pd.MultiIndex.from_product([week, headers])
    full_week = pd.DataFrame(columns=mux)
    full_week.insert(0, 'Analyst', emails_df['Name'].str.title())
    full_week.insert(21, column='Total Hours',value=0)
    full_week.insert(22, column='Notes',value='')
    full_week = full_week.fillna('')

    scope =["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    wks_key = '1HUQEUv-1SjHNL-xW7aN3EFGBuhLnt8fPBMkZKIDVihI'

#     dir_path_credentials = os.path.join(dir_path, r'credentials.json')
#     creds = ServiceAccountCredentials.from_json_keyfile_name(dir_path_credentials, scope)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(cred, scope)
    client = gspread.authorize(creds)
    sh = client.open_by_key(wks_key)

    def create_date_to_sheet_name():
        sunday_date = datetime.today() - timedelta(days=datetime.today().isoweekday() % 7)
        date = sunday_date + timedelta(days=7)
        date = date.strftime('%m/%d/%y')
        return date

    analysts_num = len(full_week['Analyst'])+2
    wks = sh.add_worksheet(title=create_date_to_sheet_name(), rows=analysts_num, cols=23)
    sheetId = sh.get_worksheet(1)._properties['sheetId']

    # Merging the two cells in the first column of analysts names.
    requests1 = {
        "requests": [
            {
                "mergeCells": {
                    "mergeType": "MERGE_COLUMNS",
                    "range": {  
                        "sheetId": sheetId,
                        "startRowIndex": 0,
                        "endRowIndex": 2,
                        "startColumnIndex": 0,
                        "endColumnIndex": 1
                    }
                }
            }
        ]
    }
    res1= sh.batch_update(requests1)

    # Merging the two cells in the last two columns of total week hours and
    # notes.
    requests2 = {
        "requests": [
            {
                "mergeCells": {
                    "mergeType": "MERGE_COLUMNS",
                    "range": {  
                        "sheetId": sheetId,
                        "startRowIndex": 0,
                        "endRowIndex": 2,
                        "startColumnIndex": 21,
                        "endColumnIndex": 23
                    }
                }
            }
        ]
    }
    res2 = sh.batch_update(requests2)

    # Alligning the column names in the center.
    requests3 = {
      "requests": 
      [
        {
          "updateCells": 
          {
            "rows": 
            [
              {
                "values": 
                [
                  {
                    "userEnteredFormat": 
                    {
                      "horizontalAlignment": "CENTER"
                    }
                  }
                ]
              }
            ],
            "range": 
            {
              "sheetId": sheetId,
              "startRowIndex": 0,
              "endRowIndex": 1,
              "startColumnIndex": 0,
              "endColumnIndex": 22
            },
            "fields": "userEnteredFormat"
          }
        }
      ]
    }
    res3 = sh.batch_update(requests3)

    # Merging all the cells that contains Sunday in them.
    requests4 = {
        "requests": [
            {
                "mergeCells": {
                    "mergeType": "MERGE_ROWS",
                    "range": { 
                        "sheetId": sheetId,
                        "startRowIndex": 0,
                        "endRowIndex": 1,
                        "startColumnIndex": 1,
                        "endColumnIndex": 5
                    }
                }
            }
        ]
    }
    res4 = sh.batch_update(requests4)

    # Merging all the cells that contains Monday in them.
    requests5 = {
        "requests": [
            {
                "mergeCells": {
                    "mergeType": "MERGE_ROWS",
                    "range": { 
                        "sheetId": sheetId,
                        "startRowIndex": 0,
                        "endRowIndex": 1,
                        "startColumnIndex": 5,
                        "endColumnIndex": 9
                    }
                }
            }
        ]
    }
    res5 = sh.batch_update(requests5)

    # Merging all the cells that contains Tuesday in them.
    requests6 = {
        "requests": [
            {
                "mergeCells": {
                    "mergeType": "MERGE_ROWS",
                    "range": {  
                        "sheetId": sheetId,
                        "startRowIndex": 0,
                        "endRowIndex": 1,
                        "startColumnIndex": 9,
                        "endColumnIndex": 13
                    }
                }
            }
        ]
    }
    res6 = sh.batch_update(requests6)

    # Merging all the cells that contains Wednesday in them.
    requests7 = {
        "requests": [
            {
                "mergeCells": {
                    "mergeType": "MERGE_ROWS",
                    "range": { 
                        "sheetId": sheetId,
                        "startRowIndex": 0,
                        "endRowIndex": 1,
                        "startColumnIndex": 13,
                        "endColumnIndex": 17
                    }
                }
            }
        ]
    }
    res7 = sh.batch_update(requests7)

    # Merging all the cells that contains Thursday in them.
    requests8 = {
        "requests": [
            {
                "mergeCells": {
                    "mergeType": "MERGE_ROWS",
                    "range": {  
                        "sheetId": sheetId,
                        "startRowIndex": 0,
                        "endRowIndex": 1,
                        "startColumnIndex": 17,
                        "endColumnIndex": 21
                    }
                }
            }
        ]
    }
    res8 = sh.batch_update(requests8)

    # The number of analysts + 2 since we have the first two rows as headers.
    analysts_num = len(full_week['Analyst'])+2

    # Making the sheet sides borders more thicker.
    requests9 = {
      "requests": [
        {
          "updateBorders": {
            "range": {
              "sheetId": sheetId,
              "startRowIndex": 0,
              "endRowIndex": analysts_num,
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
    res9 = sh.batch_update(requests9)

    # Making the top and bottom more borders more thicker.
    requests10 = {
      "requests": [
        {
          "updateBorders": {
            "range": {
              "sheetId": sheetId,
              "startRowIndex": 0,
              "endRowIndex": analysts_num,
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
    res10 = sh.batch_update(requests10)

    # Making the column headers borders more thicker.
    requests11 = {
      "requests": [
        {
          "updateBorders": {
            "range": {
              "sheetId": sheetId,
              "startRowIndex": 0,
              "endRowIndex": 2,
              "startColumnIndex": 0,
              "endColumnIndex": 23
            },
            "innerHorizontal": {
              "style": "SOLID_THICK",
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
    res11 = sh.batch_update(requests11)

    # Using the 'credentials.json' file from the credentials section
    # in google cloud platform under the OAuth 2.0 Client IDs.
    # VERY IMPORTANT - after creating the service account, you need to add
    # that email in the share button in the google spreadsheet file!!!!

    sa = gspread.service_account_from_dict(cred)
    key = '1HUQEUv-1SjHNL-xW7aN3EFGBuhLnt8fPBMkZKIDVihI' #sheetId
    sheet = sa.open_by_key(key)
    wks = sheet.get_worksheet(-1) # First worksheet.


    # Creating a cell format with color, font and centralizning the headers.
    fmt = cellFormat(
        backgroundColor=color(0,128,128),
        textFormat=textFormat(fontFamily='calibri', fontSize=12,
                              bold=True, foregroundColor=color(0,0,0)),
                                horizontalAlignment='CENTER')

    # Creating a cell format for making the names in bold, font and size.
    fmt1 = cellFormat(textFormat=textFormat(fontFamily='calibri',
                                            fontSize=10,bold=True))

    format_cell_range(wks, 'A1:W2', fmt)
    format_cell_range(wks, 'A3:A', fmt1)

    # Freezing the first two rows and the analysts column.
    set_frozen(wks, rows=2, cols=1)

    def enter_data_to_sheet(wks, dataframe):
        return set_with_dataframe(wks, dataframe)

    enter_data_to_sheet(wks, full_week)
    wks.format(f'A1:W{analysts_num}', {"wrapStrategy": "WRAP"})
    
if __name__ == '__main__':
    create_new_gsheet()