import base64
import re
from dataclasses import dataclass
from typing import Dict

import json5
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate


def report(msg: str) -> None:
    print(msg)


def get_dinning_halls() -> dict[str, dict[str, str]]:
    r: str = requests.get('https://fso.ueat.utoronto.ca/FSO/ServiceMenuReport/Today').text
    m: list[str] = re.findall(r"ASPx\.createControl\(MVCxClientMenu,'mnuUnits','',.*", r)

    if len(m) == 0:
        raise AssertionError('Failed to get menu units. Maybe API changed?')

    data = m[0]
    data = data.replace("ASPx.createControl(MVCxClientMenu,'mnuUnits','',", '')[:-2]
    data = re.sub(r"{'ItemClick':function.*?;}},", '', data)

    b64 = re.findall(r"(?<={'itemsInfo':')[A-Za-z0-9=]*(?='})", data)[0]
    b64 = base64.b64decode(b64).decode('utf-8')
    items_json = re.findall(r"(?<={'items':).*(?=})", data)[0]
    items = json5.loads(items_json)[0]['items']

    dining_halls: dict[str, dict[str, str]] = {}

    # Get dining hall names
    for i in items:
        first_id = i['items'][0]['name']
        name = re.findall(f"(?<=.)[A-Za-z0-9() ]+(?=.*\\${first_id})", b64)[-1]
        dining_halls[name] = {}

        # Get menu names
        for menu in i['items']:
            mn = re.findall(f"(?<=\\${menu['name']}).*?[A-Za-z0-9() ]+(?=.)", b64)[0]
            mn = re.findall(r"[A-Za-z0-9() ]+", mn)[0]
            dining_halls[name][mn] = menu['name']

    return dining_halls


@dataclass
class MenuItem:
    name: str
    serving_size: str
    price: float
    calories: int


def get_menu(id: str) -> tuple[list[list[str]], dict[str, list[MenuItem]]]:
    r = requests.post(f" https://fso.ueat.utoronto.ca/FSO/ServiceMenuReport/GetReport/{id}").text
    s = BeautifulSoup(r, 'html.parser')

    # Parse table
    t = s.find('table')
    d = [[i.text.strip() for i in r.find_all('td')] for r in t.find_all('tr')]

    data = {}
    current: list[MenuItem] = []
    for i in d[1:]:
        # Title
        if len(i) == 1:
            current = []
            data[i[0]] = current
        # Item
        else:
            current.append(MenuItem(i[0], i[1], float(i[2] or '-1'), int(i[3] or '-1')))

    return d, data


def filter_menu(menu: dict[str, list[MenuItem]]) -> dict[str, list[MenuItem]]:
    menu: dict[str, list[MenuItem]] = \
        {m: [i for i in menu[m] if i.price != -1] for m in menu}

    for m in menu:
        for i in menu[m]:
            i.name = i.name.replace(' - Small', '').replace(' - Large', '')

        names = {n.name for n in menu[m]}
        menu[m] = [[i for i in menu[m] if i.name == n][0] for n in names]

    return menu


if __name__ == '__main__':
    menu = filter_menu(get_menu('f1343803-84f6-4b4f-bbfd-a374ed6bd00e')[1])
    menu = {m: menu[m] for m in ['Soup', 'Lunch Entree', 'Pan Station']}
    print(menu)
