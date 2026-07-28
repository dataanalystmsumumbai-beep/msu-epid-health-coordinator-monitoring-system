import gspread

from config.config import get_google_credentials


class Database:

    def __init__(self):

        credentials = get_google_credentials()

        self.client = gspread.authorize(credentials)

    def spreadsheet(self, spreadsheet_name):

        return self.client.open(spreadsheet_name)
