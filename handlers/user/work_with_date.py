import datetime


def date_from_db_to_message(date):
    date_text = date.strftime('%d.%m.%Y')
    return date_text


def date_from_message_to_db(date):
    date_from_message = datetime.datetime.strptime(date, '%d.%m.%Y')
    return date_from_message
