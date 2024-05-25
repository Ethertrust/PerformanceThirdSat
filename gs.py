# from __future__ import print_function

import os.path
import performance

import pandas as pd
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1Neha8OoG_OORL8sd-1yleBIJB2XjTWj_PqsGSjN2CsY'
SAMPLE_RANGE_NAME = 'b Performance'
sa_file = "C:\\Users\\HYPER\\PycharmProjects\\Classes B\\Saturday\\8\\client_sa.json"

def read(SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME):
    credentials = service_account.Credentials.from_service_account_file(filename=sa_file)
    try:
        service = build('sheets', 'v4', credentials=credentials)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return
        columns = values[1]
        data = values[2:]
        df = pd.DataFrame(data, columns=columns)
        return df
    except HttpError as err:
        print(err)

def write(data, SAMPLE_SPREADSHEET_ID, sheetname):
    credentials = service_account.Credentials.from_service_account_file(filename=sa_file)
    try:
        service = build('sheets', 'v4', credentials=credentials)

        # Call the Sheets API
        sheet = service.spreadsheets()
        vr_data = {
            'majorDimension': 'ROWS',
            'values': data
        }
        sheet.values().update(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            valueInputOption='USER_ENTERED',
            range=sheetname + '!A3', #"b performance!A3"
            body=vr_data
        ).execute()
        # print(er)
    except HttpError as err:
        print(err)

def test():
    print(__name__)

if __name__ == '__main__':
    # print(__name__)
    # performance.test()
    for val in read('1Neha8OoG_OORL8sd-1yleBIJB2XjTWj_PqsGSjN2CsY', 'b Performance').values:
        print(val[0])
    # listsandsheets = {'a': {'SAMPLE_SPREADSHEET_ID': '1kGblujShU2h1GQ13mXHZQnE3f4vmeaG-fy4PZFQ5kmU',
    #                         'SAMPLE_RANGE_NAME': 'Performance2023'},
    #                   'b': {'SAMPLE_SPREADSHEET_ID': '1-XdadVGTx6L2bVC_B16vJUhjpNQIKht1Ve709n0e6lc',
    #                         'SAMPLE_RANGE_NAME': 'b Performance'}}
    # for key in ['a', 'b']:
    #    print(read(listsandsheets[key]['SAMPLE_SPREADSHEET_ID'], listsandsheets[key]['SAMPLE_RANGE_NAME']))