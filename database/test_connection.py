from utils.google_sheet import get_spreadsheet


def test_connection():

    try:

        spreadsheet = get_spreadsheet()

        print(spreadsheet.title)

        return True

    except Exception as e:

        print(e)

        return False
