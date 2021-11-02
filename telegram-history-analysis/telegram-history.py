import json
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

if __name__ == '__main__':
    # file = "~/Downloads/Telegram Desktop/ChatExport_2021-11-02 (1)/result.json"
    file = "./result-full.json"
    # start = datetime(2021, 11, 1, 12, 1, 1)
    # end = datetime(2021, 11, 2, 16, 1, 1)
    start = '2021-06-25T12:01:01'
    end = '2021-11-02T14:01:01'

    with open(file, 'r') as f:
        # lines = f.read().split('\n')
        # startFound = False
        # i = 0
        # while True:
        #     if not startFound:
        #         if lines[0][3:11] == '"date": ' and lines[0][12:31] >= start:
        #             startFound = True
        #         else:
        #             lines.pop(0)
        #     if startFound:
        #         if lines[i][3:11] == '"date": ' and lines[i][12:31] > end:
        #             lines = lines[0:i]
        #             break
        #         else:
        #             i += 1

        obj = json.load(f)

    messages: list = obj['messages']
    messages = [m for m in messages if start < m['date'] < end
                and m['type'] == 'message'
                # and m['from'] == 'Shu Lin'
                # and m['from'] == 'Hykilpikonna'
                ]

    timezone_delta = timedelta(hours=12)
    dates = [datetime.fromisoformat(m['date']) - timezone_delta for m in messages]

    # fig, ax = plt.subplots()
    # ax.hist('date', data=dates)
    #
    # ax.xaxis.set_major_locator(mdates.HourLocator(interval=3))
    # ax.xaxis.set_minor_locator(mdates.HourLocator())
    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %H'))

    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.hist(dates, bins=300, color='#ffcccc')
    plt.show()



