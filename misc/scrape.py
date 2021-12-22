"""
Since the final test is open-notes, I've made this script to combine all course notes into one html
file, so I can ctrl+F without needing to find which chapter some definition is from.
"""
import binascii
import os
import re
import secrets
from pathlib import Path

import requests


def write(file: str, text: str) -> None:
    """
    Write text to a file

    :param file: File path
    :param text: Text
    :return: None
    """
    if '/' in file:
        Path(file).parent.mkdir(parents=True, exist_ok=True)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(text)


def read(file: str) -> str:
    """
    Read file content

    :param file: File path (will be converted to lowercase)
    :return: None
    """
    with open(file, 'r', encoding='utf-8') as f:
        return f.read()


def get(url: str) -> str:
    req = requests.get(url)
    req.encoding = req.apparent_encoding
    return req.text


if __name__ == '__main__':
    host = 'https://www.teach.cs.toronto.edu'
    baseurl = f'{host}/~csc110y/fall/notes/'
    basedir = 'notes'

    r = get(baseurl)

    # Replace references
    g: set[str] = set(re.findall('(?<=href=").*?(?=")', r))
    for href in g:
        url = href
        filename = href.replace('~', '-')
        if not (url.startswith('//') or url.startswith('http')):
            if url.startswith('/'):
                url = host + url
            else:
                url = baseurl + url
        else:
            filename = filename.split("//")[1]

        if filename.endswith('/'):
            filename += 'index.html'

        r = r.replace(href, filename)
        path = os.path.join(basedir, filename)
        if os.path.isfile(path):
            continue

        content = get(url)
        write(path, content)

    write(os.path.join(basedir, 'index.html'), r)

    # Create full file
    r = re.sub('<[/]*(section|p).*?>', '', r)
    r = r.replace('<a href="www.teach.cs.toronto.edu/-csc110y/fall/notes/index.html">CSC110 Course Notes Home</a>',
                  '{INJECT_HERE}')

    links: list[str] = re.findall('<a.*?>.*?</a>', r)
    for link in links:
        uid = secrets.token_hex(5)
        href: str = re.findall('(?<=href=").*?(?=")', link)[0]
        anchor = '-'.join([i[:2] for i in href.split('/')])
        html = read(os.path.join(basedir, href))
        html = re.sub('<(!DOCTYPE|html|/html|body|/body).*?>', '', html)
        html = re.sub('<(head|div style="display:none"|footer)>.*?</(head|div|footer)>', '', html,
                      flags=re.DOTALL)
        # Replace IDs
        ids = set(re.findall('(?<=id=").*?(?=")', html))
        for id in ids:
            html = html.replace(f'"{id}"', f'"{id}-{uid}"')
            html = html.replace(f'"#{id}"', f'"#{id}-{uid}"')

        if '<section>' in html and '</section>' not in html:
            html += '</section>'

        # Download images
        g: set[str] = set(re.findall('(?<=src=").*?(?=")', html))
        for src in g:
            if src.startswith('//') or src.startswith('http'):
                continue
            path = os.path.join(basedir, src)
            # if os.path.isfile(path):
            #     continue

            if src.startswith('/'):
                url = host + src
            else:
                url = baseurl + f'{href.split("/")[-2]}/' + src

            print(url)
            img_data = requests.get(url).content
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'wb') as f:
                f.write(img_data)

        r = r.replace(link, f'<a id="anchor-{anchor}"></a>' + html)
        # print(link.replace(href, f'#anchor-{anchor}'))

    r = r.replace('{INJECT_HERE}', read('scrape-addon.html'))
    write(os.path.join(basedir, 'full.html'), r)



