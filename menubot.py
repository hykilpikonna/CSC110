import base64
import os
import re
import traceback
from dataclasses import dataclass
from typing import Dict

import json5
import requests
import telegram
from bs4 import BeautifulSoup
from tabulate import tabulate
from telegram import Update
from telegram.ext import Updater, CallbackContext, Dispatcher, CommandHandler, MessageHandler, \
    Filters


def report(msg: str) -> None:
    print(msg)


def get_dining_halls() -> dict[str, dict[str, str]]:
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
    tg_token = os.environ['tg-token']
    updater = Updater(token=tg_token, use_context=True)
    dispatcher: Dispatcher = updater.dispatcher

    def r(u: Update, msg: str, md=True):
        updater.bot.sendMessage(chat_id=u.effective_chat.id, text=msg,
                                parse_mode='Markdown' if md else None)

    def start(u: Update, c: CallbackContext):
        r(u, 'Test')

    def error(u: Update, c: CallbackContext):
        traceback.print_exc()
        r(u, str(c.error), False)

    def dining_halls(u: Update, c: CallbackContext):
        halls = get_dining_halls()
        r(u, '*Available Dining Halls:* \n' + '\n'.join(halls.keys()) + '\n\nNext: /menus <hall>')

    def get_hall_with_name(hall: str):
        hall = hall.lower()
        halls = get_dining_halls()
        h = [halls[h] for h in halls if h.lower().startswith(hall)]
        if len(h) == 0:
            raise AssertionError(f'No dining hall {hall} found.')
        return h, h[0]

    def get_menu_with_name(hall: str, menu: str):
        menu = menu.lower()
        hall, h = get_hall_with_name(hall)
        m = [m for m in h if m.lower().startswith(menu)]
        if len(m) == 0:
            raise AssertionError(f'No menu {menu} found in {hall}.')
        return hall, m[0], get_menu(h[m[0]])[1]

    def get_menu_cats(hall: str, menu: str, cats: list[str]):
        hall, menu, m = get_menu_with_name(hall, menu)
        m = filter_menu(m)
        copy_cats = cats.copy()
        cats = [c.lower() for c in cats]
        cats = [([n for n in m if n.lower().startswith(c)] or [''])[0] for c in cats]
        cats = [c for c in cats if c != '']
        if len(cats) == 0:
            raise AssertionError(f'No categories in {copy_cats} are valid.')
        m = {c: m[c] for c in cats}
        return hall, menu, m

    def menus(u: Update, c: CallbackContext):
        if len(c.args) != 1:
            r(u, 'Usage: /menus <hall>')
            return
        hall = c.args[0]
        hall, h = get_hall_with_name(hall)
        r(u, '*Available Menus:* \n' + '\n'.join(h.keys()) + '\n\nNext: /cats <hall> <menu>')

    def categories(u: Update, c: CallbackContext):
        if len(c.args) < 2:
            r(u, 'Usage: /categories <hall> <menu>')
            return
        hall, menu = c.args
        hall, menu, m = get_menu_with_name(hall, menu)
        r(u, '*Available Menus:* \n' + '\n'.join(m.keys()) + '\n\nNext: /menu <hall> <menu> <cats>')

    def menu(u: Update, c: CallbackContext):
        if len(c.args) < 2:
            r(u, 'Usage: /menu <hall> <menu> <categories>')
            return
        hall, menu = c.args[:2]
        cats = c.args[2:]
        hall, menu, m = get_menu_cats(hall, menu, cats)
        r(u, f"*Today's Menu for {menu}:* \n" +
             '\n'.join(f"\n*{n}:* \n" + '\n'.join(
                 f"{i + 1}. {m[n][i].name} - ${m[n][i].price}" for i in range(len(m[n])))
                       for n in m))

    dispatcher.add_error_handler(error)
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('halls', dining_halls))
    dispatcher.add_handler(CommandHandler('menus', menus))
    dispatcher.add_handler(CommandHandler('categories', categories))
    dispatcher.add_handler(CommandHandler('cats', categories))
    dispatcher.add_handler(CommandHandler('menu', menu))
    dispatcher.add_handler(MessageHandler(Filters.update, start))
    updater.start_polling()
    #
    # menu = filter_menu(get_menu('f1343803-84f6-4b4f-bbfd-a374ed6bd00e')[1])
    # menu = {m: menu[m] for m in ['Soup', 'Lunch Entree', 'Pan Station']}
