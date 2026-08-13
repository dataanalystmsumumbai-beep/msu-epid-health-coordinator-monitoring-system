import streamlit as st
import gspread
from google.oauth2.service_account import Credentials


# ==========================================================
# CONFIG
# ==========================================================

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


# ==========================================================
# GOOGLE CONNECTION
# ==========================================================

@st.cache_resource
def get_client():

    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )

    return gspread.authorize(
        credentials
    )


@st.cache_resource
def get_spreadsheet():

    client = get_client()

    sheet_name = st.secrets.get(
        "google_sheet_name",
        "MSU-EPID Health Coordinator Monitoring System Database"
    )

    return client.open(
        sheet_name
    )


# ==========================================================
# GET WORKSHEET
# ==========================================================

def get_worksheet(
    worksheet_name
):

    spreadsheet = get_spreadsheet()

    return spreadsheet.worksheet(
        worksheet_name
    )


# ==========================================================
# READ ALL
# ==========================================================

def read_all(
    worksheet_name
):

    worksheet = get_worksheet(
        worksheet_name
    )

    records = worksheet.get_all_records()

    return records or []


# ==========================================================
# READ VALUES
# ==========================================================

def read_values(
    worksheet_name
):

    worksheet = get_worksheet(
        worksheet_name
    )

    return worksheet.get_all_values()


# ==========================================================
# INSERT ROW
# ==========================================================

def insert_row(
    worksheet_name,
    row
):

    worksheet = get_worksheet(
        worksheet_name
    )

    worksheet.append_row(
        list(row),
        value_input_option="USER_ENTERED"
    )

    return True


# ==========================================================
# UPDATE VALUE
# ==========================================================

def update_value(
    worksheet_name,
    row_no,
    column_no,
    value
):

    worksheet = get_worksheet(
        worksheet_name
    )

    worksheet.update_cell(
        int(row_no),
        int(column_no),
        value
    )

    return True


# ==========================================================
# DELETE ROW
# ==========================================================

def delete_row(
    worksheet_name,
    row_no
):

    worksheet = get_worksheet(
        worksheet_name
    )

    worksheet.delete_rows(
        int(row_no)
    )

    return True


# ==========================================================
# FIND ROW
# ==========================================================

def find_row(
    worksheet_name,
    column_name,
    value
):

    records = read_all(
        worksheet_name
    )

    value = str(
        value or ""
    ).strip().lower()


    for index, record in enumerate(
        records,
        start=2
    ):

        record_value = str(
            record.get(
                column_name,
                ""
            )
        ).strip().lower()


        if record_value == value:

            return index, record


    return None, None


# ==========================================================
# UPDATE ROW
# ==========================================================

def update_row(
    worksheet_name,
    row_no,
    values
):

    worksheet = get_worksheet(
        worksheet_name
    )

    end_column = len(
        values
    )

    cell_range = (
        f"A{row_no}:"
        f"{_column_letter(end_column)}{row_no}"
    )


    worksheet.update(
        cell_range,
        [list(values)],
        value_input_option="USER_ENTERED"
    )

    return True


# ==========================================================
# COLUMN LETTER
# ==========================================================

def _column_letter(
    column_number
):

    result = ""

    while column_number:

        column_number, remainder = divmod(
            column_number - 1,
            26
        )

        result = (
            chr(
                65 + remainder
            )
            + result
        )

    return result
