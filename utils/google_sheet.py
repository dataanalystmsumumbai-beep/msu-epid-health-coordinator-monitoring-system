from database.database import Database
from config.config import SHEET_NAME

import streamlit as st
import time

# ======================================================
# Database Object
# ======================================================

database = Database()

# ======================================================
# Spreadsheet
# ======================================================

@st.cache_resource
def get_spreadsheet():

    return database.spreadsheet(SHEET_NAME)


# ======================================================
# Worksheet
# ======================================================

def get_worksheet(sheet_name):

    spreadsheet = get_spreadsheet()

    return spreadsheet.worksheet(sheet_name)


# ======================================================
# Read
# ======================================================

def read_all(sheet_name):

    worksheet = get_worksheet(sheet_name)

    return worksheet.get_all_records()


# ======================================================
# Insert
# ======================================================

def insert_row(sheet_name, row):

    worksheet = get_worksheet(sheet_name)

    worksheet.append_row(
        row,
        value_input_option="USER_ENTERED"
    )


# ======================================================
# Update Cell
# ======================================================

def update_value(
    sheet_name,
    row,
    column,
    value
):

    worksheet = get_worksheet(sheet_name)

    worksheet.update_cell(
        row,
        column,
        value
    )


# ======================================================
# Update Row
# ======================================================

def update_row(
    sheet_name,
    row,
    values
):

    worksheet = get_worksheet(sheet_name)

    start = f"A{row}"

    end = chr(64 + len(values))

    worksheet.update(
        f"{start}:{end}{row}",
        [values]
    )


# ======================================================
# Delete Row
# ======================================================

def delete_row(
    sheet_name,
    row
):

    worksheet = get_worksheet(sheet_name)

    worksheet.delete_rows(row)


# ======================================================
# Find
# ======================================================

def find(
    sheet_name,
    value
):

    worksheet = get_worksheet(sheet_name)

    return worksheet.find(value)


# ======================================================
# Row Count
# ======================================================

def row_count(sheet_name):

    worksheet = get_worksheet(sheet_name)

    return len(
        worksheet.get_all_records()
    )


# ======================================================
# Clear Sheet
# ======================================================

def clear_sheet(sheet_name):

    worksheet = get_worksheet(sheet_name)

    worksheet.clear()


# ======================================================
# Refresh Cache
# ======================================================

def refresh():

    st.cache_resource.clear()

    time.sleep(1)
