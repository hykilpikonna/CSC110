import json
from datetime import datetime, timedelta

import matplotlib.pyplot as plt

if __name__ == '__main__':
    file = "./result-full.json"
    start = '2021-06-25T12:01:01'
    end = '2021-11-02T14:01:01'

    with open(file, 'r') as f:
        obj = json.load(f)

    messages: list = obj['messages']
    messages = [m for m in messages if start < m['date'] < end
                and m['type'] == 'message'
                # and m['from'] == 'Hykilpikonna'
                ]

    timezone_delta = timedelta(hours=12)
    dates = [datetime.fromisoformat(m['date']) - timezone_delta for m in messages]

    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.hist(dates, bins=300, color='#ffcccc')
    plt.show()



