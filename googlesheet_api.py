import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request
import os
import pickle

#Tutorial from https://medium.com/analytics-vidhya/how-to-read-and-write-data-to-google-spreadsheet-using-python-ebf54d51a72c

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


##### Read #####

def read_google(sheet_id, sheet_range):
    """This function pulls data from google spreadsheet, given spreadsheet_id and range"""

    global values_input, service
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES) # here enter the name of your downloaded JSON file
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result_input = sheet.values().get(spreadsheetId=sheet_id,
                                range=sheet_range).execute()
    values_input = result_input.get('values', [])

    if not values_input and not values_expansion:
        print('No data found.')
        
    return pd.DataFrame(values_input[1:], columns=values_input[0])


##### write ######

def Create_Service(client_secret_file, api_service_name, api_version, *scopes):
    """Function to set up google service API"""

    global service
    SCOPES = [scope for scope in scopes[0]]
    #print(SCOPES)
    
    cred = None

    if os.path.exists('token_write.pickle'):
        with open('token_write.pickle', 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
            cred = flow.run_local_server()

        with open('token_write.pickle', 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(api_service_name, api_version, credentials=cred)
        print(api_service_name, 'service created successfully')
        #return service
    except Exception as e:
        print(e)
        #return None

def Export_Data_To_Sheets(df, gsheet_id, gsheet_range):
    """Function to export data to google sheets"""

    Create_Service('credentials.json', 'sheets', 'v4',['https://www.googleapis.com/auth/spreadsheets'])
    
    gsheetId = gsheet_id
    range_name = gsheet_range
    
    response_date = service.spreadsheets().values().update(
        spreadsheetId=gsheetId,
        valueInputOption='RAW',
        range=range_name,
        body=dict(
            majorDimension='ROWS',
            values=df.values.tolist())
    ).execute()
    print('Sheet successfully Updated')
