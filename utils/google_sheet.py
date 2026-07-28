import gspread
from database.database import connect_database


def get_spreadsheet(sheet_name: str):
    """
    Connect to Google Spreadsheet.
    Create Spreadsheet if it does not exist.
    """

    client = connect_database()

    try:
        spreadsheet = client.open(sheet_name)

    except gspread.SpreadsheetNotFound:
        spreadsheet = client.create(sheet_name)

    return spreadsheet


def get_or_create_worksheet(spreadsheet, worksheet_name, headers):

    try:
        worksheet = spreadsheet.worksheet(worksheet_name)

    except gspread.WorksheetNotFound:

        worksheet = spreadsheet.add_worksheet(
            title=worksheet_name,
            rows=1000,
            cols=max(len(headers), 20)
        )

        worksheet.append_row(headers)

    return worksheet
