from datetime import datetime


def current_date():

    return datetime.now().strftime("%d-%m-%Y")


def current_time():

    return datetime.now().strftime("%I:%M %p")


def current_datetime():

    return datetime.now().strftime("%d-%m-%Y %I:%M %p")
