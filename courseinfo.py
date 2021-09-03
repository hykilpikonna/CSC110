import re

import requests


def get_course_info(id: str):
    link = f'https://artsci.calendar.utoronto.ca/course/{id}'
    html = requests.get(link).text
    name: str = re.findall(r'(?<=<h1 class="title page-title">).*(?=<)', html)[0]
    hours: str = re.findall(r'(?<=<div class="field__item"><p>).*(?=<)', html)[0]
    hours = '/'.join([str(int(it[:-1]) / 12) + it[-1] for it in hours.split('/')])
    return {'id': id, 'name': name, 'link': link, 'hours': hours,
            'full': f'`{id}` - [{hours}] {name} ({link})'}


if __name__ == '__main__':
    sep = input('Please enter the separator (Eg. a comma): ')
    l = input(f'Please enter course codes separated by "{sep}": ')
    [print(get_course_info(it.strip())['full']) for it in l.split(sep)]
