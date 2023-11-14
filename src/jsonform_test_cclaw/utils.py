from datetime import datetime, timedelta

def offset_date(in_date_str, offset_days) -> str:
    """
    Returns a date that is a specified number of days before or after the given date.

    :param in_date_str: The input date as a string in 'YY-MM-DD' format.
    :param offset_days: The number of days to offset, can be negative or positive.
    :return: A string representing the new date in 'YY-MM-DD' format.
    """
    input_date = datetime.strptime(in_date_str, '%Y-%m-%d')
    offset_date = input_date + timedelta(days=offset_days)
    return offset_date.strftime('%Y-%m-%d')
