from database.database import Database
from config.config import SHEET_NAME


database = Database()


def get_spreadsheet():

    return database.spreadsheet(SHEET_NAME)


def get_worksheet(sheet_name):

    spreadsheet = get_spreadsheet()

    return spreadsheet.worksheet(sheet_name)


def read_all(sheet_name):

    worksheet = get_worksheet(sheet_name)

    return worksheet.get_all_records()


def insert_row(sheet_name, row):

    worksheet = get_worksheet(sheet_name)

    worksheet.append_row(row)


def update_value(sheet_name, row, col, value):

    worksheet = get_worksheet(sheet_name)

    worksheet.update_cell(row, col, value)


def clear_sheet(sheet_name):

    worksheet = get_worksheet(sheet_name)

    worksheet.clear()
