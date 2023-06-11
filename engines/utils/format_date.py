from datetime import datetime
import re


def convert_with_pattern(text, date_pattern, regex, target_pattern):
    date_pattern_py = date_pattern.replace('yyyy', '%Y').replace('MM', '%m').replace('dd', '%d')
    target_pattern_py = target_pattern.replace('yyyy', '%Y').replace('MM', '%m').replace('dd', '%d')

    for match in re.finditer(regex, text):
        date_str = match.group(0)
        try:
            date = datetime.strptime(date_str, date_pattern_py)
            new_date_str = date.strftime(target_pattern_py)
            text = text.replace(date_str, new_date_str)
        except ValueError:
            # If the date format does not match, we will ignore this exception,
            # because we are trying to match multiple date formats.
            pass

    return text


def convert_dates_accurate_to_the_day(text):
    patterns = [
        ("yyyy.MM.dd", r"\d{4}\.\d{2}\.\d{2}", "yyyy年MM月dd日"),
        ("yyyy-MM-dd", r"\d{4}-\d{2}-\d{2}", "yyyy年MM月dd日"),
        ("yyyy/MM/dd", r"\d{4}/\d{2}/\d{2}", "yyyy年MM月dd日"),
        ("dd.MM.yyyy", r"\d{2}\.\d{2}\.\d{4}", "yyyy年MM月dd日"),
        ("dd-MM-yyyy", r"\d{2}-\d{2}-\d{4}", "yyyy年MM月dd日"),
        ("dd/MM/yyyy", r"\d{2}/\d{2}/\d{4}", "yyyy年MM月dd日"),
        ("yyyy.MM", r"\d{4}\.\d{2}", "yyyy年MM月"),
        ("yyyy-MM", r"\d{4}-\d{2}", "yyyy年MM月"),
        ("yyyy/MM", r"\d{4}/\d{2}", "yyyy年MM月"),
        ("MM.yyyy", r"\d{2}\.\d{4}", "yyyy年MM月"),
        ("MM-yyyy", r"\d{2}-\d{4}", "yyyy年MM月"),
        ("MM/yyyy", r"\d{2}/\d{4}", "yyyy年MM月"),
    ]

    text = text.replace("—", "-")
    for pattern in patterns:
        text = convert_with_pattern(text, *pattern)

    return text


# text = """
# I was born on 1990-05-25, and my sister was born on 1992/04/21.
# We moved to a new city in 2000.02.
# I graduated from university on 2013/06/15, and my sister graduated on 2015.07.20.
# """
#
# # Convert the dates in the text to the target format, accurate to the day
# converted_text = convert_dates_accurate_to_the_day(text)
#
# print(converted_text)
