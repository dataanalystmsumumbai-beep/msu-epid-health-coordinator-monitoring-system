from utils.google_sheet import (
    get_spreadsheet,
    get_or_create_worksheet
)

from config.config import SHEET_NAME


def initialize_database():

    spreadsheet = get_spreadsheet(SHEET_NAME)

    worksheets = {

        "01_User_Master": [
            "User_ID",
            "Name",
            "Username",
            "Password",
            "Role",
            "Ward",
            "Mobile",
            "Status",
            "Created_On",
            "Created_By"
        ],

        "02_Task_Master": [
            "Task_ID",
            "Task_Name",
            "Assigned_To",
            "Priority",
            "Start_Date",
            "Due_Date",
            "Status",
            "Remarks"
        ],

        "03_Daily_Review": [
            "Review_ID",
            "Date",
            "Coordinator",
            "Ward",
            "Task",
            "Status",
            "Remarks",
            "Updated_On"
        ],

        "04_Login_Log": [
            "Login_Time",
            "Username",
            "Role",
            "IP_Address",
            "Browser"
        ],

        "05_Audit_Log": [
            "Date_Time",
            "User",
            "Role",
            "Action",
            "Details"
        ],

        "06_System_Settings": [
            "Setting",
            "Value"
        ],

        "07_Notifications": [
            "Date",
            "Title",
            "Message",
            "Status"
        ],

        "08_Backup": [
            "Backup_Date",
            "Backup_By",
            "Remarks"
        ]
    }

    for sheet_name, headers in worksheets.items():
        get_or_create_worksheet(
            spreadsheet,
            sheet_name,
            headers
        )

    return spreadsheet
