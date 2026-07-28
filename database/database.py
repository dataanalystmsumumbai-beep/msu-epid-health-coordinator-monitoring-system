import gspread

from config.config import get_google_credentials

def connect_database():

    credentials = get_google_credentials()

    client = gspread.authorize(credentials)

    return client
