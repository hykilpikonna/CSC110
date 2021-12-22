import io
import os

import json5
import requests

if __name__ == '__main__':
    """
    This method doesn't work
    """
    token = os.environ.get('tg-bot-token')

    with io.open('userid_to_name.json5', mode='r', encoding='utf-8') as f:
        userid_to_name = json5.loads(f.read())

    for user_id in userid_to_name:
        user = userid_to_name[user_id]

        # Get photo
        r = requests.get(f'https://api.telegram.org/bot{token}/getUserProfilePhotos',
                         params={'user_id': user_id[4:]})

        o = r.json()
        if 'result' not in o:
            print(f'Result not in o for {user}')
            print(o)
            continue

        o = o['result']
        if o['total_count'] == 0:
            print(f'Total count is 0 for user {user}')
            continue

        photo = max(o['photos'][0], key=lambda x: x['height'])

        # Get file
        r = requests.get(f'https://api.telegram.org/bot{token}/getFile',
                         params={'file_id': photo['file_id']})
        o = r.json()['result']

        # Download file
        r = requests.get(f'https://api.telegram.org/file/bot{token}/{o["file_path"]}',
                         params={'file_id': photo['file_id']})

        # Write file
        with io.open(f'avatars/{userid_to_name[user_id]}.jpg', 'wb') as f:
            f.write(r.content)
