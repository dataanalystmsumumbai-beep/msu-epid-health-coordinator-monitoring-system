from datetime import datetime


def generate_user_id():

    return "USR" + datetime.now().strftime("%Y%m%d%H%M%S")


def generate_task_id():

    return "TSK" + datetime.now().strftime("%Y%m%d%H%M%S")


def generate_review_id():

    return "REV" + datetime.now().strftime("%Y%m%d%H%M%S")
