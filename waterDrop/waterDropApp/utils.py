# coding:UTF-8


def get_slash_date(date):
    return '{}/{}/{}'.format(date.year, date.month, date.day)


def get_hyphen_date(date):
    return '{}-{}-{}'.format(date.year, date.month, date.day)


def convert_week(number):
    str_week = {0: '(月)',
                1: '(火)',
                2: '(水)',
                3: '(木)',
                4: '(金)',
                5: '(土)',
                6: '(日)',
                }
    return str_week[number]
