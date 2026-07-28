import gspread

from database.database import connect_database
from config.config import SHEET_NAME


def get_database():

    client = connect_database()

    spreadsheet = client.open(SHEET_NAME)

    return spreadsheet


def get_sheet(sheet_name):

    spreadsheet = get_database()

    return spreadsheet.worksheet(sheet_name)


def read_data(sheet_name):

    sheet = get_sheet(sheet_name)

    return sheet.get_all_records()


def append_row(sheet_name, row):

    sheet = get_sheet(sheet_name)

    sheet.append_row(row)


def update_cell(sheet_name, row, column, value):

    sheet = get_sheet(sheet_name)

    sheet.update_cell(row, column, value)
