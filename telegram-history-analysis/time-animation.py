import io
import json
import json5

if __name__ == '__main__':
    """
    
    """
    file = "./result.json"
    start = '2021-06-25T12:01:01'
    end = '2021-11-02T14:01:01'

    with io.open(file, mode='r', encoding="utf-8") as f:
        content = f.read()
        obj = json.loads(content)

    with io.open('userid_to_name.json5', mode='r', encoding='utf-8') as f:
        userid_to_name = json5.loads(f.read())

    messages: list = obj['messages']
    messages = [m for m in messages if True
                # and start < m['date'] < end
                and m['type'] == 'message'
                # and m['from'] == 'Hykilpikonna'
                ]

    date_data = {}
    for m in messages:
        date = m['date'][:10]
        if date not in date_data:
            date_data[date] = {}
        user = m['from_id']
        if user not in userid_to_name:
            userid_to_name[user] = m['from']
        user = userid_to_name[user]
        if user not in date_data[date]:
            date_data[date][user] = 0
        date_data[date][user] += 1

    print(userid_to_name)

    user_totals = {}
    lines = ['id,date,value']
    for date in date_data:
        users = date_data[date]
        for u in users:
            if u not in user_totals:
                user_totals[u] = []
            user_totals[u].append(users[u])

        for u in user_totals:
            if u not in users:
                user_totals[u].append(0)
            total = sum(user_totals[u][-7:])
            if u in userid_to_name:
                u = userid_to_name[u]
            lines.append(f'{u},{date},{total}')

    with io.open('output.csv', mode='w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

