from __future__ import annotations
import time
from pathlib import Path

import requests


def get_commits_for_branch(branch: str):
    commits: list = []

    # Get additional commits
    for page in range(1, 10000):
        url = f'https://api.github.com/repos/{repo}/commits?sha={branch}&per_page=100&page={page}'
        next_commits = requests.get(url).json()
        if len(next_commits) == 0:
            break
        commits += next_commits

    csv = ['Index,Date,Message']
    i = 0
    for commit in commits:
        message: str = commit['commit']['message']
        message = message.replace('\n', '\\n').replace('"', '""')
        date = commit['commit']['author']['date']
        csv.append(f'{i},{date},"{message}"')
        i += 1

    print(i)

    Path('output').mkdir(exist_ok=True)
    with open(f'output/{branch}.csv', 'w', encoding='utf-8') as f:
        f.write('\n'.join(csv))


if __name__ == '__main__':
    repo = 'tensorflow/model-card-toolkit'

    branches_raw = requests.get(f'https://api.github.com/repos/{repo}/branches').json()
    branches: list[str] = [b['name'] for b in branches_raw]

    for b in branches:
        get_commits_for_branch(b)

    time.sleep(1)
