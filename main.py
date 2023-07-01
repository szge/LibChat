import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import csv

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

SAMPLE_SPREADSHEET_ID = '1JFyivbZzcRjRE-ImCZBT-D9IILZ7JEL9aUyII8GE5q4'
SAMPLE_RANGE_NAME = "Books"


def save_to_csv():
    creds = Credentials.from_authorized_user_file('token.json', SCOPES) if os.path.exists("token.json") else None
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        values = service.spreadsheets().values().get(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range=SAMPLE_RANGE_NAME
        ).execute().get('values', [])

        if not values:
            print('No data found.')
            return

        # save to csv file
        with open('books.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(values)

        # there might be multiple comma separated authors in a cell.

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    save_to_csv()
