import re


def extract_numbers(string):
    lst_numbers = re.findall(r'\d+', string)
    str_number = ''.join([str(elem) for elem in lst_numbers])
    int_number = int(str_number)

    return int_number
